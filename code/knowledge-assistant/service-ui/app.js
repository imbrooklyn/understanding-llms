// SPDX-License-Identifier: Apache-2.0
// Localized user text is loaded exclusively from the shared content resource.
const $=id=>document.getElementById(id);
const locale=new URLSearchParams(location.search).get('lang')==='zh-hans'?'zh-hans':'en';
let text, active=null, current=null, previous=null, epoch=0;
const headers={'Authorization':'Bearer demo-north','Content-Type':'application/json'};
async function api(path,body){
 const response=await fetch(path,{method:body===undefined?'GET':'POST',headers,body:body===undefined?undefined:JSON.stringify(body)});
 const result=await response.json();
 if(!response.ok)throw Object.assign(new Error(result.error),{result,status:response.status});
 return result;
}
function setStatus(key){$('status').textContent=text[key]??text.error;}
function render(value){
 $('answer').replaceChildren();$('citations').replaceChildren();
 if(!value)return;
 const result=value.result;
 if(value.state==='answered' && result?.kind==='order'){
  $('answer').textContent=`${result.order.order_id}: ${text[result.order.status]??result.order.status}. ${text.order_as_of}`;
 }else if(value.state==='answered'){
  $('answer').textContent=result.answer.answer;
  for(const cite of result.answer.citations){
   const label=document.createElement('p'),quote=document.createElement('blockquote');
   label.textContent=`${text.source}: ${cite.source_id}, ${text.lines} ${cite.line_start}–${cite.line_end}`;
   quote.textContent=cite.quote;$('citations').append(label,quote);
  }
 }else{$('answer').textContent=text[value.state]??text.error;}
}
function busy(value){$('submit').disabled=value;$('order').disabled=value;$('cancel').disabled=!value||!active;$('clear').disabled=value;$('undo').disabled=value||!previous;$('feedback').disabled=value||!current;}
async function follow(id,token){
 const response=await fetch(`/api/requests/${id}/events`,{headers});
 if(!response.ok)throw new Error('stream_failed');
 const reader=response.body.getReader(),decoder=new TextDecoder();let buffer='';
 while(true){
  const {value,done}=await reader.read();if(done)break;
  buffer+=decoder.decode(value,{stream:true});let end;
  while((end=buffer.indexOf('\n\n'))!==-1){
   const frame=buffer.slice(0,end);buffer=buffer.slice(end+2);
   const line=frame.split('\n').find(s=>s.startsWith('data: '));
   if(line&&token===epoch){const event=JSON.parse(line.slice(6));if(text[event.stage])setStatus(event.stage);}
  }
 }
 // A final GET is safe and bounded; a new POST is never silently substituted.
 let value;
 for(let attempt=0;attempt<2;attempt++){
  try{value=await api(`/api/requests/${id}`);break;}catch(error){if(attempt===1)throw error;await new Promise(r=>setTimeout(r,100));}
 }
 if(token===epoch){current=value;render(value);setStatus(value.state);}
}
async function submit(topic){
 if(active||!$('ask').reportValidity())return;
 const token=++epoch;current=null;busy(true);setStatus('accepted');$('answer').replaceChildren();$('citations').replaceChildren();
 try{
  const value=await api('/api/requests',{question:topic==='order'?'A-104':$('question').value,on_date:$('on-date').value,topic,locale});
  active=value.request_id;busy(true);await follow(active,token);
 }catch(error){setStatus(error.status===429?'rate_limited':error.status===503?'overloaded':'connection_unknown');}
 finally{active=null;busy(false);}
}
async function initialize(){
 text=(await(await fetch('/content.json')).json())[locale];
 $('ask').addEventListener('submit',e=>{e.preventDefault();submit('travel');});
 $('order').onclick=()=>submit('order');
 $('cancel').onclick=async()=>{if(!active)return;const id=active,token=epoch;try{await api(`/api/requests/${id}/cancel`,{});if(active===id&&epoch===token)setStatus('cancelling');}catch(error){if(epoch===token)setStatus(error.status===409?'already_finished':'connection_unknown');}};
 $('clear').onclick=()=>{previous={current,question:$('question').value};current=null;$('question').value='';render(null);$('handoff-note').textContent='';setStatus('cleared');busy(false);$('question').focus();};
 $('undo').onclick=()=>{if(!previous)return;current=previous.current;$('question').value=previous.question;previous=null;render(current);setStatus('restored');busy(false);};
 $('handoff').onclick=()=>{$('handoff-note').textContent=`${text.handoff_text}\n${$('question').value}\n${$('on-date').value}`;};
 for(const button of document.querySelectorAll('[data-category]'))button.onclick=async()=>{if(!current)return;try{await api(`/api/requests/${current.request_id}/feedback`,{category:button.dataset.category});setStatus('feedback_saved');}catch{setStatus('error');}};
}
initialize().catch(()=>{$('status').textContent=$('status').getAttribute('data-error');});
