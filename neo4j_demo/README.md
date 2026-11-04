# Neo4j 六份开发语料演示

> 建立日期：2026-11-03  
> 数据：陈海峰一访、二访、三访，陈锐霆第01、02份，杨永松第01份  
> 浏览器地址：<http://localhost:7474>  
> Bolt地址：`bolt://localhost:7687`  
> 认证：本机演示实例关闭认证，不对外监听
> 当前规模：4673个节点、8074条关系

本实例使用独立的 `data/`、`logs/`、`run/` 和 `import/` 目录，不会修改“以往工作”中的旧Neo4j数据库。

Neo4j程序统一使用 `/Users/yuqi/Downloads/neo4j-community-1-2026.06.24` 中原有且可正常显示Browser的安装。论文数据库仍保存在本目录的 `data/` 中；启动脚本通过 `/tmp/oral_history_neo4j_demo` 英文软链接访问，避免中文路径被启动器转义。软链接不复制程序或数据库。

## 图谱层次

```text
InterviewDocument
├── EventNode ──NEXT──> EventNode
│   ├── EventType（韩礼德六类事件）
│   ├── Process
│   ├── Entity（参与者，关系上记录角色）
│   ├── Circumstance
│   ├── EventTime
│   └── ProcessStage ──NEXT_STAGE──> ProcessStage
├── SourceSegment
│   ├── SourceAttachment ──> Document／Event／Stage
│   ├── EntityMention ──> Entity
│   └── TimeExpression（正文、小传、脚注等的日期；不含录音时间戳）
└── DocumentAnnotation ──> Document／Entity／SourceSegment等
```

所有原文都保存在 `SourceSegment.verbatim_text`；即使没有进入事件，也通过文档级 `SourceAttachment` 保留和查询。

## 文件

- `import.cypher`：完整重建图谱；只清理本演示实例中的节点。
- `verify.cypher`：九组演示查询。
- `import/`：由六份开发语料CSV合并形成的Neo4j导入文件。
- `reports/`：导入规模和验证结果。
- `conf/neo4j.conf`：独立端口和目录配置。

## 浏览器中建议先运行

```cypher
MATCH (d:InterviewDocument)-[:HAS_EVENT]->(e:EventNode)
OPTIONAL MATCH (e)-[:HAS_TIME]->(t:EventTime)
RETURN d, e, t
LIMIT 100;
```

查看二级结构：

```cypher
MATCH p=(e:EventNode {event_id:'CHF-V1-E03'})-[:HAS_STAGE|HAS_PROCESS|HAS_TYPE|HAS_PARTICIPANT|HAS_CIRCUMSTANCE]->(x)
RETURN p;
```

查看跨人物共享实体：

```cypher
MATCH (d:InterviewDocument)-[:HAS_SEGMENT]->(:SourceSegment)-[:HAS_MENTION]->(:EntityMention)-[:MENTIONS]->(entity:Entity)
WITH entity, collect(DISTINCT d.interviewee) AS people
WHERE size(people) > 1
RETURN entity.canonical_name, people;
```

查看脚注中的实体、日期和挂接事件：

```cypher
MATCH (d:InterviewDocument)-[:HAS_SEGMENT]->(s:SourceSegment)
WHERE s.source_part='footnotes'
OPTIONAL MATCH (s)-[:HAS_MENTION]->(:EntityMention)-[:MENTIONS]->(entity:Entity)
OPTIONAL MATCH (s)-[:HAS_TIME_EXPRESSION]->(time:TimeExpression)
OPTIONAL MATCH (s)-[:HAS_ATTACHMENT]->(:SourceAttachment)-[:ATTACHES_TO]->(event:EventNode)
RETURN d.interviewee, s.verbatim_text,
       collect(DISTINCT entity.canonical_name) AS 实体,
       collect(DISTINCT time.raw_text + '→' + time.normalized_start) AS 时间,
       collect(DISTINCT event.event_name) AS 挂接事件;
```

