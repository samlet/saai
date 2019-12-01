#!/bin/bash
export PYTHONPATH=/pi/stack:/pi/ws/sagas-ai:$PYTHONPATH

honcho="$HOME/miniconda3/envs/rasa/bin/honcho"
alias s1="$honcho start"

