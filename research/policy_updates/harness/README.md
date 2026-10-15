# policy-updates

This is the code for the study **Policy Updates Mid-Conversation** (workshop version).

- **Design (authoritative):** `policy_updates_workshop_design.md` (committee's shared docs)
- **Implementation guide:** `implementation_handbook.md` (committee's shared docs)
- **Sibling module:** `../policy_checker/` is Task 4's rule checker and labeling tools.

If this README and the design disagree, the design wins.

This repository currently contains **Task 3: the conversation builder, runner and environment** (handbook §6). The other tasks plug in through the interfaces described below.

## Quick start

```bash
uv sync                    # dev environment (any OS); no GPU needed
uv run pytest              # all tests use a mock backend; no model is run
uv run pu --help
uv run pu estimate         # token-count-based GPU-hour estimate
```

On the GPU box (Linux + CUDA), see `docs/ENVIRONMENT.md`:

```bash
uv sync --extra gpu        # vllm==0.31.0, transformers==5.17.0 (pinned in uv.lock)
# or: docker build -f docker/Dockerfile -t policy-updates .
```

## Pipeline

```
Task 1 items  ──►  pu histories  ──►  pu build  ──►  pu render  ──►  pu run  ──►  responses  ──►  Task 4 checker
  (JSONL)          (R-hist/P-hist)    (neutral        (Task 2         (vLLM or
                                       conversations   renderer)       mock)
                                       + blinded keys)
```

| Step | Command | Input | Output |
|---|---|---|---|
| Histories | `pu histories --model m1 --backend vllm --items ... --history-items ... --out data/histories/turns.jsonl --renderer <task2>` | probe + history items | one JSONL record per history turn |
| Build | `pu build --split confirm --items ... --history-items ... --histories ... --models m1,m2,m3,m4` | items + histories | `data/conversations/<split>/<model>.conversations.jsonl`, `recog_meta.jsonl`, `build_manifest.json`; **`keys/<split>.condition_key.jsonl` (blinded analyst only)** |
| Render | `pu render --model m1 --conversations ... --out data/requests/m1.jsonl --renderer <task2>` | neutral conversations | exact prompt strings, with sampling settings and seeds |
| Run | `pu run --model m1 --backend vllm --requests ... --responses data/responses/m1.jsonl` | rendered requests | responses + `*.manifest.json` |

## What is real and what is a placeholder

| Piece | Status | Owner |
|---|---|---|
| Shared data formats (`src/pu/schemas.py`) | Real; frozen at the day-1 meeting | Task 3; review by all |
| Cell catalog, conversation assembly, C4 clock, R3 remedy, recognition branch | Real | Task 3 |
| Opaque IDs and condition keys | Real | Task 3 writes them; Task 5 holds the keys |
| History generation, runner, retries, resume, manifests | Real (tested on a mock backend) | Task 3 |
| `VLLMBackend` | Real, but **not yet run on a GPU**; wiring tested against a fake `vllm` module | Task 3 |
| `configs/texts/v0.yaml` | **DRAFT** texts copied from the handbook | **Task 2** finalizes them |
| `PlainRenderer` | **Test-only.** Real runs need Task 2's chat-template renderer | **Task 2** |
| Disclosure check for retries | Placeholder `retry_all_truncated` (retries every truncated response) | **Task 4** supplies the checker |
| `pu.testing.fakes` items and histories | Test-only | Real items come from **Task 1** |
| `configs/models.yaml` `support` | Unknown (`null`); the builder refuses to build until it is filled in | **Task 2** support matrix |
| `configs/run.yaml` `estimate.throughput` | Assumptions | Replace after the smoke test |

## Interfaces for the other tasks

- **Task 1:** write items as JSONL matching `schemas.Item`.
  - Each probe has `paraphrase_id` (0–4) and exactly 4 `history_item_ids`.
  - History items are separate `Item`s with `role: history`.
- **Task 2:** provide a factory `make_renderer(model_spec, texts) -> Renderer`, where `Renderer.render(NeutralConversation) -> (prompt_str, n_tokens)`. Pass it as `--renderer pkg.module:make_renderer`.
  - The renderer must apply the model's chat template with `add_generation_prompt=True`, including `tools=[texts.tool_schema]` and `model_spec.chat_template_kwargs` (e.g., `enable_thinking: false`).
  - The runner tokenizes the prompt with `add_special_tokens=False`, so BOS must come from the template.
  - Fill in `support` in `configs/models.yaml`.
- **Task 4:** provide a disclosure check `(RenderedRequest, text) -> bool` for the runner's retry rule, plus the labels.
  - `recog_meta.jsonl` gives each recognition sample's polarity and which option means "yes".
- **Task 5:** the condition key is `keys/<split>.condition_key.jsonl`, keyed by the opaque `request_id`; `keys/salt.txt` makes the IDs reproducible.
  - **Never commit or share `keys/`.**

## Layout

```
configs/      run.yaml (sampling, cells, clock, estimate), models.yaml, texts/v0.yaml
src/pu/       schemas, io, config, texts/, build/, render/, run/, env/, testing/, cli.py
tests/        pytest suite (mock backend only) + golden conversation snapshots
docker/       pinned vLLM image
docs/         ENVIRONMENT.md (GCP setup)
scripts/      idle_shutdown.sh
```
