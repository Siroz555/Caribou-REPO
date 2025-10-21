#!/usr/bin/env python3

import json
import hashlib
import os
from pathlib import Path
from datetime import datetime, timezone


def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def update_metadata():
    script_dir = Path(__file__).parent.absolute()
    root_dir = script_dir.parent

    print(f"Working directory: {root_dir}")
    os.chdir(root_dir)

    data_path = Path("data")
    if not data_path.exists():
        print("The ‘data’ folder does not exist!")
        return

    metadata_path = Path("metadata.json")
    if metadata_path.exists():
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        print(f"Current version: {metadata.get('version', 'undefined')}")
    else:
        metadata = {
            "version": "0.0.0",
            "last_updated": "",
            "files": {}
        }
        print("Creating a new metadata.json file")

    print("\nScanning files...")

    files_info = {}
    for filepath in data_path.rglob("*.json"):
        relative_path = filepath.resolve().relative_to(root_dir).as_posix()

        file_hash = calculate_sha256(filepath)
        file_size = filepath.stat().st_size

        files_info[relative_path] = {
            "hash": file_hash,
            "size": file_size
        }
        print(f"  ✓ {relative_path}")

    if not files_info:
        print("No Json files found in 'data/'")
        return

    metadata["files"] = files_info
    metadata["last_updated"] = datetime.now(timezone.utc).isoformat() + "Z"

    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"\nMetadata updated")
    print(f"   Version: {metadata['version']}")
    print(f"   Files: {len(files_info)}")


if __name__ == "__main__":
    update_metadata()
