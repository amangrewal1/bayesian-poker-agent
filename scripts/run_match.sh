#!/usr/bin/env bash
set -euo pipefail

# Run the full 50,000-hand benchmark
python3 main.py --hands 50000
