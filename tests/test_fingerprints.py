from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from forge.fingerprints import fingerprint
from forge.adapters import discover_adapter


CASES = [
    ("/home/user/models/qwen/Qwen2.5-Coder-3B-Instruct-abliterated-Q4_K_M.gguf", "qwen2", "Qwen2/Qwen2.5"),
    ("/home/user/.ollama/models/blobs/sha256-afb707b6b8fac6e475acc42bc8380fc0b8d2e0e4190be5a969fbf62fcc897db5", "qwen35", "Qwen3.5"),
    ("/home/user/.ollama/models/blobs/sha256-dec52a44569a2a25341c4e4d3fee25846eed4f6f0b936278e3a3c900bb99d37c", "qwen35", "Qwen3.5"),
    ("/home/user/.ollama/models/blobs/sha256-6c2c13cef89238c3604d756b07b3ef5fafebbd61095feb8553ff449c95e4c1c6", "qwen38", "Qwen3.8"),
    ("/home/user/Downloads/DeepSeek-R1-Llama-8B-Abliterated-Q4_K_M.gguf", "llama", "Llama/DeepSeek"),
    ("/home/user/models/bitnet/bitnet-abliterated-i2s-run17.gguf", "bitnet", "BitNet"),
]


def main():
    for path, adapter_name, family in CASES:
        p = Path(path)
        assert p.exists(), p
        fp = fingerprint(p)
        assert fp.family == family, (p, fp)
        assert discover_adapter(fp.architecture, fp.family).name == adapter_name
        assert fp.layer_count > 0
    print(f"forge fingerprint registry: PASS ({len(CASES)} local models)")


if __name__ == "__main__":
    main()
