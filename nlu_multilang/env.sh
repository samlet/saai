#!/bin/bash
export PYTHONPATH=/pi/stack:..:$PYTHONPATH

# alias s1='/Users/xiaofeiwu/miniconda3/envs/bigdata/bin/python -m honcho start'
honcho='/Users/xiaofeiwu/miniconda3/envs/rasa/bin/honcho'
alias s1="$honcho start"
