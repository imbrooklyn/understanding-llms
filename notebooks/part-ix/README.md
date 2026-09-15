# Part IX executed notebooks

Run both notebooks from a fresh CPU kernel using the environment and commands in [the practice README](../../code/part-ix/README.md). `pnpm notebooks:part-ix` executes every cell in order and fails on errors. Its input map includes the saved release record read by Notebook 2, and rejects stale or mid-run changed inputs.

1. `01-service.ipynb` makes actual loopback requests, checks current/historical/missing evidence and ownership, and stops a running worker without a late result.
2. `02-operations.ipynb` evaluates candidate gates and independent policy arithmetic, then explicitly inspects the recorded rollback. Reading that saved file is not a new deployment, write or model call.

The books contain all key calculations, outcomes and reference answers statically; executing these notebooks is the optional practice path. Original prose and printed original observations are CC BY-SA 4.0; code cells are Apache-2.0. All accounts and policies are fictional. No weights, GPU, model account or paid API is required.
