#!/usr/bin/env python3
"""Utility script to download models from HuggingFace."""

import argparse
import os
import shutil

from huggingface_hub import snapshot_download

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Script to download models from HuggingFace"
    )
    parser.add_argument(
        "-l", "--local-dir", required=True, help="Directory to download model to"
    )
    parser.add_argument("-r", "--hf-repo-id", required=True, help="Model repo id")
    args = parser.parse_args()

    os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

    snapshot_download(repo_id=args.hf_repo_id, local_dir=args.local_dir)

    # workaround for https://github.com/UKPLab/sentence-transformers/pull/2460
    os.makedirs(os.path.join(args.local_dir, "2_Normalize"), exist_ok=True)

    # OLS-823: sanitize local directory
    local_directory = os.path.normpath("/" + args.local_dir).lstrip("/")
    if local_directory == "":
        local_directory = "."

    # pretend local_dir is HF cache
    with open(os.path.join(local_directory, "version.txt"), "w", encoding="utf-8") as f:
        f.write("1")

    # remove pytorch_model.bin, load the model from model.safetensors
    os.remove(os.path.join(args.local_dir, "pytorch_model.bin"))

    # remove onnx and openvino models
    shutil.rmtree(os.path.join(args.local_dir, "onnx"))
    shutil.rmtree(os.path.join(args.local_dir, "openvino"))
