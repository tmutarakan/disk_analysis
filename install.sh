#!/bin/bash
if [ -e .venv ]
then
    rm -rfv .venv
fi
python3 -m venv .venv
.venv/bin/python3 -m pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
