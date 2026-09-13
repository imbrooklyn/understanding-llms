# SPDX-License-Identifier: Apache-2.0
"""Independent fractions and perturbations test observable mechanisms, not generated goldens."""
import copy
import importlib.util
import json
import math
from pathlib import Path
import unittest
from mechanisms import (distribution, draw_index, rotate_quarter, rmsnorm, swiglu, kv_bytes,
                        latency, quantize, weighted_gradient, speculative_correction, linear_prefix,
                        rescue, two_step_beam, confusion)
ROOT=Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('part_v_run', ROOT / 'code/part-v/run.py')
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)
run, pipeline = RUNNER.run, RUNNER.pipeline


class MechanismTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=run()
        cls.expected=json.loads((ROOT/'data/part-v/expected.json').read_text())
        cls.inputs=json.loads((ROOT/'data/part-v/mechanisms.json').read_text())

    def test_budget_and_storage_integer_products(self):
        r,e=self.result,self.expected
        self.assertEqual(r['budget_flops'],e['budget_flops'])
        self.assertEqual(r['lifecycle_flops'],e['lifecycle_flops'])
        self.assertEqual(r['training']['state_bytes'],16_000_000)
        self.assertEqual(r['training']['activation_bytes'],32_768*40)
        self.assertEqual(r['training']['total_bytes'],17_310_720)
        self.assertEqual(r['training']['with_headroom_bytes'],21_638_400)
        self.assertEqual(4_000_000+12_000_000//4,e['optimizer_shard_state_bytes'])

    def test_rotation_preserves_length_and_relative_displacement(self):
        self.assertEqual(self.result['rotation_dots'],[1,0,0,-1])
        self.assertEqual(rotate_quarter([3,4],1),[-4,3])
        self.assertEqual(sum(x*x for x in rotate_quarter([3,4],-3)),25)
        self.assertEqual(rotate_quarter([3,4],4),[3,4])

    def test_rms_scale_not_offset_and_zero_boundary(self):
        y=rmsnorm([3,4],0)
        self.assertAlmostEqual(sum(v*v for v in y)/2,1)
        self.assertEqual(y,rmsnorm([6,8],0))
        self.assertNotEqual(y,rmsnorm([4,5],0))
        self.assertEqual(rmsnorm([0,0]),[0,0])
        with self.assertRaises(ValueError):rmsnorm([0,0],0)
        with self.assertRaises(ValueError):rmsnorm([1],float('nan'))

    def test_gate_sign_and_symbolic_output(self):
        r=self.result['swiglu']
        self.assertEqual(r['gate'],[1,-1]);self.assertEqual(r['up'],[2,3])
        self.assertLess(r['product'][1],0)
        self.assertAlmostEqual(r['output'][0],(2*math.e-3)/(1+math.e))
        self.assertAlmostEqual(r['output'][1],-3/(1+math.e))

    def test_architecture_counts_and_loss_of_order(self):
        r=self.result['architecture']
        self.assertEqual((r['total_parameters'],r['active_parameters']),(60_000_000,40_000_000))
        self.assertEqual([x['output'] for x in r['linear']],[4,2,2.25])
        self.assertEqual(linear_prefix([1,2,1],[3,1,4])[-1],r['linear'][-1])
        self.assertIsNone(linear_prefix([0],[4])[0]['output'])
        self.assertEqual(linear_prefix([1,2,1,2],[4,1,3,6])[-1]['output'],3.5)

    def test_accumulation_weights_valid_events(self):
        self.assertEqual(weighted_gradient([1,3],[2,6]),2.5)
        self.assertEqual(weighted_gradient([2,-2],[3,1]),1)
        self.assertNotEqual(weighted_gradient([1,3],[2,6]),sum([1,3])/2)
        with self.assertRaises(ValueError):weighted_gradient([2],[0])

    def test_patch_controls_and_undefined_recovery(self):
        self.assertEqual([r['margin'] for r in self.result['intervention']],[4,-4,4,-4,-4,4])
        self.assertEqual(self.result['rescue'],[1,0])
        self.assertEqual(rescue(6,2,5),.75)
        self.assertIsNone(rescue(2,2,5))
        self.assertGreater(rescue(4,-4,8),1)
        self.assertLess(rescue(4,-4,-8),0)

    def test_sampling_weights_shift_ties_and_boundaries(self):
        z=[math.log(4),math.log(2),0,0]
        self.assertEqual(distribution(z),[.5,.25,.125,.125])
        for a,b in zip(distribution(z),distribution([x+100 for x in z])):self.assertAlmostEqual(a,b)
        self.assertEqual(distribution([1,1,0],temperature=0),[1,0,0])
        self.assertEqual(distribution([0,0,0],top_k=2),[.5,.5,0])
        self.assertEqual([draw_index(distribution(z),u) for u in [.49,.5,.75,.99]],[0,1,2,3])
        with self.assertRaises(ValueError):draw_index([1],1)
        with self.assertRaises(ValueError):distribution(z,temperature=-1)
        with self.assertRaises(ValueError):distribution(z,top_p=0)
        with self.assertRaises(ValueError):distribution(z,top_k=5)

    def test_top_p_minimal_mass_and_renormalization(self):
        z=[math.log(4),math.log(2),0,0]
        for p,count in zip([.5,.6,.75,.8],[1,2,2,3]):
            y=distribution(z,top_p=p)
            self.assertEqual(sum(v>0 for v in y),count);self.assertAlmostEqual(sum(y),1)
        self.assertEqual(distribution(z,top_p=.75),[2/3,1/3,0,0])
        for a,b in zip(distribution(z,top_p=.8),[4/7,2/7,1/7,0]):self.assertAlmostEqual(a,b)
        self.assertEqual(distribution(z,top_k=2,top_p=.6),[1,0,0,0])
        for a,b in zip(distribution(z,temperature=.5),[8/11,2/11,1/22,1/22]):self.assertAlmostEqual(a,b)

    def test_beam_uses_joint_probability_not_first_step(self):
        b=self.inputs['sampling']['beam'];after={'A':b['after_A'],'B':b['after_B']}
        self.assertEqual(two_step_beam(b['first'],after,1)[0]['tokens'],['A','EOS'])
        best=two_step_beam(b['first'],after,2)[0]
        self.assertEqual(best['tokens'],['B','EOS']);self.assertAlmostEqual(best['probability'],.36)
        self.assertEqual(two_step_beam({'A':.8,'B':.2},after,2)[0]['tokens'],['A','EOS'])

    def test_kv_dimensions_and_linear_growth(self):
        self.assertEqual(self.result['kv_bytes_per_layer'],[2_097_152,524_288,262_144])
        self.assertEqual(self.result['small_cache_bytes'],[512,576,640])
        self.assertEqual(self.result['large_cache_bytes'],384*1024**2)
        self.assertEqual(kv_bytes(24,4096,4,128,2,sequences=4),768*1024**2)
        self.assertEqual(kv_bytes(2,0,2,4,2),0)
        with self.assertRaises(ValueError):kv_bytes(2,8,0,4,2)

    def test_latency_denominator_and_missing_interval(self):
        r=latency(10,[110,160,220])
        self.assertEqual(r,dict(ttft_ms=100,gaps_ms=[50,60],tpot_ms=55,end_to_end_ms=210))
        self.assertIsNone(latency(0,[100])['tpot_ms'])
        with self.assertRaises(ValueError):latency(0,[])
        with self.assertRaises(ValueError):latency(10,[9])
        with self.assertRaises(ValueError):latency(0,[20,10])

    def test_quantization_rounding_clipping_and_argmax_change(self):
        q=quantize([-1.2,-.2,.7,1.8],.5)
        self.assertEqual(q['integers'],[-2,0,1,4]);self.assertEqual(q['decoded'],[-1,0,.5,2])
        self.assertEqual(quantize([.75,-.75],.5)['integers'],[2,-2])
        self.assertEqual(quantize([8],.5)['errors'],[-4.5])
        self.assertEqual(distribution([.6,.7],temperature=0),[0,1])
        self.assertEqual(distribution(quantize([.6,.7],.5)['decoded'],temperature=0),[1,0])
        with self.assertRaises(ValueError):quantize([1],0)

    def test_serving_window_and_single_request_tradeoff(self):
        r=self.result['serving'];a=r['serial'];b=r['continuous']
        self.assertEqual([x['ttft_ms'] for x in a['requests']],[100,240,320])
        self.assertEqual([x['ttft_ms'] for x in b['requests']],[100,130,140])
        self.assertEqual(a['requests'][0]['tpot_ms'],40);self.assertEqual(b['requests'][0]['tpot_ms'],50)
        self.assertAlmostEqual(a['throughput_tokens_per_second'],50/3)
        self.assertEqual(b['throughput_tokens_per_second'],30)
        self.assertEqual(a['output_tokens']/.4,b['output_tokens']/.4)
        self.assertAlmostEqual(a['assumed_dollars'],.0002)

    def test_speculation_recovers_distribution_including_zero_proposal(self):
        for p,q in [([.6,.4],[.8,.2]),([.3,.7],[.6,.4]),([.25,.75],[1,0]),([.5,.5],[.5,.5])]:
            r=speculative_correction(p,q)
            accepted=[v*a for v,a in zip(q,r['accept'])];rejected=1-sum(accepted)
            actual=[a+rejected*s for a,s in zip(accepted,r['residual'] or [0]*len(p))]
            for a,b in zip(actual,p):self.assertAlmostEqual(a,b)
        self.assertIsNone(speculative_correction([.5,.5],[.5,.5])['residual'])
        self.assertNotAlmostEqual(.6+.2*.6,.6)

    def test_pipeline_records_mistaken_filter_and_all_stage_counts(self):
        source=json.loads((ROOT/'data/part-v/pipeline-input.json').read_text())
        result=pipeline(source)
        self.assertEqual(result['stage_counts'],[8,7,6,6,5])
        self.assertEqual({r['id'] for r in result['retained']},{'new','old','contact','red','zh'})
        self.assertNotIn('analyst@example.invalid',str(result['retained']))
        self.assertEqual(next(r for r in result['ledger'] if r['id']=='copy')['duplicate_of'],'new')
        self.assertEqual(next(r for r in result['ledger'] if r['id']=='canary')['revised_result'],'evaluation_overlap')
        extended=copy.deepcopy(source);extended['records'].append(dict(id='extra',locale='en',html='<p>Another original sentence.</p>'))
        self.assertEqual(pipeline(extended)['stage_counts'],[9,8,7,7,6])

    def test_evaluator_confusion_uses_actual_and_predicted_denominators(self):
        r=self.result['calibration']
        self.assertEqual(r['substring'],dict(tp=3,fp=2,tn=1,fn=0))
        self.assertEqual(r['strict'],dict(tp=1,fp=0,tn=3,fn=2))
        self.assertEqual(r['substring']['tp']+r['substring']['tn'],r['strict']['tp']+r['strict']['tn'])
        self.assertEqual(confusion([False],[True]),dict(tp=0,fp=0,tn=0,fn=1))

    def test_monthly_cost_boundary(self):
        api=lambda n:n*(1000*2/1e6+200*10/1e6)
        local=lambda n:20+.001*n
        self.assertLess(api(6666),local(6666));self.assertGreater(api(6667),local(6667))
        self.assertEqual((api(5000),local(5000)),(20,25))


if __name__=='__main__':unittest.main()
