# Cortex Phoenix

Cortex Phoenix is the frozen experimental bounded-memory runtime milestone
derived from Cortex Stream Forge. It is kept separate from the native Cortex
development path.

## Scope

The source and documentation cover:

- bounded GGUF/pread tensor streaming;
- selected-expert-only MoE loading;
- recurrent and hybrid state serialization/restoration;
- execution-scoped tensor capture and canonical hashing;
- M-RoPE position handling;
- sequential layer execution with context/model release;
- transaction commit/rollback and final-head experiments.

## Build

Use the runtime source under:

`runtime-flashnext-layer-exp/`

The primary native transaction target is:

`llama-flashnext-owned-layer`

Build with the same CMake command documented in the source handoff and run
only under an explicitly verified 4 GiB RAM / 4 GiB swap scope.

## Frozen milestone

Protected tag:

`cortex-phoenix-v1`

Commit:

`dc270bb27dc992cc91a2f1ccea5a688f8f415b85`

Reported milestone evidence includes a 48-layer first-token path, predicted
token ID `180671`, logits hash `4744d0f41ebcc108`, and approximately 3.9 GiB
peak RSS with zero swap. These are historical milestone records and were not
rerun during packaging.

## Finish next

Do not merge Phoenix wholesale into Cortex. First isolate reusable pieces,
then validate them against an independent oracle:

1. Reproduce the frozen milestone from this repository.
2. Separate proven source-level mechanisms from historical measurements.
3. Validate state restoration and recreated-context continuation independently.
4. Resolve remaining graph/state ownership and mathematical correctness
   questions before transferring code into Cortex.

The Phoenix tag is frozen and should not be moved or rewritten.
