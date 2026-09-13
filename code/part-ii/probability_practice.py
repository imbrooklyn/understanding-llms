# SPDX-License-Identifier: Apache-2.0
"""Chapter 6 outputs, checked against fractions before rounding."""
import json
import math
from numerical import softmax, target_loss, kl


def run():
    logits = [math.log(2), 0, 0]
    probabilities = softmax(logits)
    losses = [target_loss(logits, target) for target in [0, 1]]
    mean = sum(losses) / 2
    for actual, expected in zip(probabilities, [1 / 2, 1 / 4, 1 / 4]):
        assert math.isclose(actual, expected, abs_tol=1e-12)
    assert math.isclose(mean, math.log(8) / 2, abs_tol=1e-12)
    assert math.isclose(math.exp(mean), math.sqrt(8), abs_tol=1e-12)
    shifted = softmax([x + 1000 for x in logits])
    assert all(math.isclose(a, b, abs_tol=1e-12) for a, b in zip(shifted, probabilities))
    assert target_loss([0, -1000], 1) == 1000
    q, p = [0.75, 0.25], [0.5, 0.5]
    output = {"probabilities": probabilities, "target_losses_nats": losses,
              "mean_loss_nats": mean, "perplexity": math.exp(mean),
              "shifted_probabilities": shifted, "kl_q_p_nats": kl(q, p),
              "kl_p_q_nats": kl(p, q), "zero_support_kl": "infinite",
              "underflow_safe_loss": target_loss([0, -1000], 1)}
    assert math.isinf(kl([1, 0], [0, 1]))
    assert kl([1, 0], [1, 0]) == 0
    print(json.dumps(output, indent=2))
    return output


if __name__ == "__main__":
    run()
