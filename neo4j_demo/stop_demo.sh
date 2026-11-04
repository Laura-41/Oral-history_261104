#!/bin/zsh
set -euo pipefail

DEMO_LINK="/tmp/oral_history_neo4j_demo"
NEO4J_HOME_LINK="/tmp/oral_history_neo4j_home"

env NEO4J_CONF="$DEMO_LINK/conf" "$NEO4J_HOME_LINK/bin/neo4j" stop

