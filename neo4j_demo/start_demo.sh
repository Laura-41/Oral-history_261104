#!/bin/zsh
set -euo pipefail

DEMO_DIR="/Users/yuqi/Desktop/硕士毕业论文/2609/0920_01/现行标注/neo4j_demo"
NEO4J_DIST="/Users/yuqi/Downloads/neo4j-community-1-2026.06.24"
DEMO_LINK="/tmp/oral_history_neo4j_demo"
NEO4J_HOME_LINK="/tmp/oral_history_neo4j_home"

# 数据仍在论文工程中；英文软链接只解决Neo4j对中文路径的转义问题。
ln -sfn "$DEMO_DIR" "$DEMO_LINK"
ln -sfn "$NEO4J_DIST" "$NEO4J_HOME_LINK"

cd "$DEMO_DIR"
env NEO4J_CONF="$DEMO_LINK/conf" "$NEO4J_HOME_LINK/bin/neo4j" console




# 第一步：启动新实例
# 不要关闭现在运行旧Neo4j的终端，另外打开一个终端窗口或标签页，粘贴：

# cd '/Users/yuqi/Desktop/硕士毕业论文/2609'
# '0920_01/现行标注/neo4j_demo/start_demo.sh'
