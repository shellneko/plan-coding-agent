#!/bin/bash

AGENT_DIR=$HOME/kuzuhara_ws/plan-coding-agent
EXEC_PATH=$AGENT_DIR/run_agent.py

mamba run -n nav_agent python $EXEC_PATH
