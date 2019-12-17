#!/bin/bash
export PYTHONPATH=/pi/stack:$PYTHONPATH

honcho="$HOME/miniconda3/envs/rasa/bin/honcho"
python="$HOME/miniconda3/envs/rasa/bin/python"

alias s1="$honcho start"
alias train="$python -m saai.nlu_mod_procs train_all"
alias view_nlu="$python -m saai.nlu_data_procs view_file"

