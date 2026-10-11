#!/usr/bin/env python3
import sys
import os
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from forge.weight_provider import WeightProvider, rss_bytes


MODEL = Path("/home/user/.ollama/models/blobs/sha256-6c2c13cef89238c3604d756b07b3ef5fafebbd61095feb8553ff449c95e4c1c6")


def main():
    if not MODEL.exists():
        print("qwen3.8 weight provider: SKIP (model absent)")
        return 0
    before = rss_bytes()
    with WeightProvider(MODEL) as provider:
        assert provider.reader.data_offset == 10994976
        layer0 = provider.load_layer(0)
        layer0_capacity = provider.buffer_capacity
        assert layer0_capacity == sum(t.nbytes for t in layer0.descriptors)
        assert layer0.view("blk.0.ssm_dt.bias")
        # Validate the provider bytes against the GGUF offset directly.
        d = provider.descriptor("blk.0.ssm_dt.bias")
        with open(MODEL, "rb", buffering=0) as raw:
            expected = os.pread(raw.fileno(), d.nbytes, d.absolute_offset)
        actual = bytes(layer0.view(d.name))
        assert actual == expected
        assert hashlib.sha256(actual).hexdigest() == hashlib.sha256(expected).hexdigest()
        after_layer0 = rss_bytes()
        layer1 = provider.load_layer(1)
        assert provider.buffer_capacity == layer0_capacity
        assert layer1.buffer is layer0.buffer
        assert layer1.view("blk.1.ssm_conv1d.weight")
        # Layer 3 is a full-attention section with a different tensor layout.
        layer3 = provider.load_layer(3)
        assert layer3.buffer is layer0.buffer
        assert layer3.view("blk.3.attn_q.weight")
        after_layer1 = rss_bytes()
        provider.release()
    # The model itself was never mapped; resident growth is the working buffer
    # plus Python metadata, not the 16.8 GB GGUF.
    growth = max(after_layer0, after_layer1) - before
    assert growth < 512 * 1024 * 1024, growth
    print("qwen3.8 weight provider: PASS")
    print(f"data_offset=10994976 layer0_bytes={layer0_capacity} "
          f"rss_before={before} rss_peak={max(after_layer0, after_layer1)} "
          f"rss_growth={growth} buffer_reused=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
