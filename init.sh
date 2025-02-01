#!/usr/bin/env bash
set -e

python3 -m venv ./venv/
source "./venv/bin/activate"
python3 -m pip install -U pip
python3 -m pip install django~=4.1 typer[all]~=0.9