from pathlib import Path

import yaml

from pu.config import ModelSpec, load_models
from pu.env.estimate import estimate, format_table
from pu.env.weights import hash_model_dir, record_in_models_yaml


def test_hash_model_dir(tmp_path):
    (tmp_path / "model-00001.safetensors").write_bytes(b"abc")
    (tmp_path / "config.json").write_text("{}")
    (tmp_path / "README.md").write_text("ignored")
    (tmp_path / ".cache").mkdir()
    (tmp_path / ".cache" / "x.json").write_text("ignored")
    h1, files = hash_model_dir(tmp_path)
    assert set(files) == {"model-00001.safetensors", "config.json"}
    assert hash_model_dir(tmp_path)[0] == h1
    (tmp_path / "config.json").write_text('{"a": 1}')
    assert hash_model_dir(tmp_path)[0] != h1


def test_record_in_models_yaml(tmp_path):
    src = Path(__file__).parents[1] / "configs" / "models.yaml"
    dst = tmp_path / "models.yaml"
    dst.write_text(src.read_text())
    record_in_models_yaml("m1", "deadbeef", "f00d", dst)
    m = load_models(dst)["m1"]
    assert m.revision == "deadbeef" and m.weights_sha256 == "f00d"
    assert yaml.safe_load(dst.read_text())["models"][1]["revision"] is None


def test_candidate_models_config_loads():
    specs = load_models()
    cands = [m for m in specs.values() if m.role == "candidate"]
    assert len(cands) == 4 and len({m.hf_repo.split("/")[0] for m in cands}) == 4
    assert specs["m1"].chat_template_kwargs == {"enable_thinking": False}


def test_estimate(cfg, texts):
    models = [
        ModelSpec(
            id="m8",
            hf_repo="x",
            size_class="8b",
            support={"C1": True, "C2": True, "C3": True, "C4": True},
        ),
        ModelSpec(
            id="m32",
            hf_repo="y",
            size_class="32b",
            support={"C1": True, "C2": False, "C3": True, "C4": True},
        ),
    ]
    lines = estimate(models, cfg, texts)
    assert len(lines) == 8
    conf = {ln.model_id: ln for ln in lines if ln.phase.startswith("W6")}
    # 12k primary + 0.9k recog + 0.9k calibration + 2.4k descriptive + 4.8k history turns, +5%
    assert conf["m8"].calls == int((12000 + 1800 + 2400 + 4800) * 1.05)
    assert conf["m32"].calls == int((12000 + 1800 + 1200 + 4800) * 1.05)  # no C2
    assert all(ln.gpu_hours > 0 for ln in lines)
    assert "**total**" in format_table(lines)
