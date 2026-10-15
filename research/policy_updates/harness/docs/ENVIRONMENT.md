# Environment and GCP setup (Task 3)

## Pinned versions

| Component | Pin | Where |
|---|---|---|
| vLLM | 0.31.0 | `pyproject.toml` `[gpu]` extra, `uv.lock`, `docker/Dockerfile` (image digest pinned) |
| transformers | 5.17.0 | vLLM 0.31.0 requires `>=5.10.4,<5.18.0` |
| torch | 2.13.0 | resolved by `uv.lock`; bundled in the vLLM image |
| Python | 3.11–3.13 | `requires-python` |

The lockfile is `uv.lock`; regenerate it only deliberately (`uv lock`) and record why in `DEVIATIONS.md`.

## 1. GCP account

These steps are for the lead.

1. **Sign up and upgrade.** Create the project, start the free trial, then **upgrade the billing account to paid**. Without the upgrade you cannot attach GPUs or request quota ([docs](https://docs.cloud.google.com/free/docs/free-cloud-features)). Unused trial credit stays usable until day 90.
2. **Set a budget alert at $100.** Go to Billing → Budgets & alerts.
3. **Request GPU quota in one region:**
   - NVIDIA L4 for the 8B models;
   - A100 80GB for the 24–32B models, unless you use 4-bit quantization on L4. If you quantize, record it in `models.yaml` as a deviation.
4. **Grant access.** Only the Task 3 owner and the blinded analyst get project access.

## 2. VM

```bash
# Check the current Deep Learning VM image families first:
gcloud compute images list --project deeplearning-platform-release --filter="family~cu" --format="value(family)" | sort -u

# 8B models: G2 machine types come with one L4 attached.
gcloud compute instances create pu-l4 \
  --zone=us-central1-a --machine-type=g2-standard-8 \
  --provisioning-model=SPOT --instance-termination-action=STOP --maintenance-policy=TERMINATE \
  --image-project=deeplearning-platform-release --image-family=<CUDA image family from above> \
  --boot-disk-size=300GB --metadata=install-nvidia-driver=True
```

- **Spot VMs** are cheaper but can be interrupted. Every `pu` job is resumable, so just rerun the same command after an interruption.
- **24–32B models:** use an `a2-ultragpu-1g` machine (1× A100 80GB) the same way.
- **Before relying on these flags,** check them against current `gcloud` documentation.

## 3. Software on the VM

```bash
git clone <repo> /opt/policy-updates && cd /opt/policy-updates
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --extra gpu            # exact versions from uv.lock
uv run pytest                  # must pass on the VM too
# or the container:
docker build -f docker/Dockerfile -t policy-updates .
```

Install the idle-shutdown guard. It stops the VM after 30 idle GPU minutes with no `pu` job running:

```bash
sudo cp scripts/idle_shutdown.sh /usr/local/bin/ && sudo chmod +x /usr/local/bin/idle_shutdown.sh
(sudo crontab -l 2>/dev/null; echo "* * * * * /usr/local/bin/idle_shutdown.sh") | sudo crontab -
```

## 4. Weights

1. **Accept the licenses (gated models).** Llama-3.1 and Gemma-3 require accepting each license on huggingface.co. Then set `export HF_TOKEN=...` on the VM.
2. **Download each model:**

   ```bash
   uv run pu download-weights --model m1 --dest /data/models
   ```

   This pins the exact commit and writes `revision` and `weights_sha256` into `configs/models.yaml`.
3. **Commit the updated `models.yaml`.** This freezes the models.
4. **Re-hash at any time** to verify nothing changed:

   ```bash
   uv run pu hash-weights --dir /data/models/m1
   ```

## 5. Smoke test (first real-model contact; lead decides when)

Use a non-study prompt. For example, render a single conversation with Task 2's renderer and run it with `--backend vllm --model-path /data/models/m1`.

Things to check:

- the output text is sensible;
- `finish_reason` is reported;
- there is no thinking block (`reasoning_stripped` is false in the responses);
- the run manifest records the GPU and the vLLM version.

Then measure throughput (tokens/s from the manifest timestamps and token counts) and replace the `estimate.throughput` assumptions in `configs/run.yaml`.

## 6. GPU-hour estimate

```bash
uv run pu estimate
```

**Current output** (assumed throughputs; 4 candidate models; all channels assumed supported):

| Phase | Per model | All 4 models |
|---|---|---|
| W2 family screen | ~3.4k calls, ~0.4 h | ~1.8 h |
| W3 manipulation check | ~0.8k calls, ~0.1 h | ~0.4 h |
| W3 exploration + pilot (incl. histories) | ~1.9k calls, ~0.3 h | ~1.2 h |
| W6 confirmatory (incl. histories) | ~22k calls, ~3.4–4.3 h | ~15.5 h |
| **Total** | | **~19 GPU-hours** |

This is within the design's 1–2 GPU-day budget. It uses chars/4 token counts from the plain test renderer and assumed throughputs, so treat it as ±2× until the smoke test.
