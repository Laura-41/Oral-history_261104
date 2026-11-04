# Neo4j 六份工作流Demo

> 更新日期：2026-11-04  
> 数据：陈海峰一访、二访、三访，陈锐霆第01、02份，杨永松第01份  
> 浏览器地址：<http://localhost:7474>  
> Bolt地址：`bolt://localhost:7687`  
> 认证：本机演示实例关闭认证，不对外监听
> 数据角色：六份均为 `WORKFLOW_DEMO`，不作为正式测试金标准
> 当前规模：4708个节点、8187条关系；其中35个 `LifeEpisode`、32条 `BIOGRAPHICAL_NEXT`

本实例使用独立的 `data/`、`logs/`、`run/` 和 `import/` 目录，不会修改“以往工作”中的旧Neo4j数据库。

Neo4j程序统一使用 `/Users/yuqi/Downloads/neo4j-community-1-2026.06.24` 中原有且可正常显示Browser的安装。论文数据库仍保存在本目录的 `data/` 中；启动脚本通过 `/tmp/oral_history_neo4j_demo` 英文软链接访问，避免中文路径被启动器转义。软链接不复制程序或数据库。

## 图谱层次

```text
BiographicalSubject（人物核心）
├── InterviewDocument ──INTERVIEW_OF──> BiographicalSubject
├── HAS_LIFE_EPISODE ──> LifeEpisode ──BIOGRAPHICAL_NEXT──> LifeEpisode
│                             └──SUPPORTED_BY_EVENT──> EventNode（可来自多份访谈）
└── NARRATED_CONTEXT ──> EventNode（只讲述、暂不认定为本人经历）

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

人物生平层是叠加视图。它不修改文档内事件节点和 `NEXT`；人物经历按照真实历史时间排序，不按照访谈文件顺序或叙述顺序。同一经历将来如在多次访谈中重复出现，可以让一个 `LifeEpisode` 同时连接多个来源 `EventNode`。

所有原文都保存在 `SourceSegment.verbatim_text`；即使没有进入事件，也通过文档级 `SourceAttachment` 保留和查询。

## 文件

- `import.cypher`：完整重建图谱；只清理本演示实例中的节点。
- `verify.cypher`：九组演示查询。
- `import/`：由六份工作流Demo CSV及人物生平配置合并形成的Neo4j导入文件。
- `reports/`：导入规模和验证结果。
- `conf/neo4j.conf`：独立端口和目录配置。

## 浏览器中建议先运行

### 1. 陈海峰人物生平图

将姓名替换成 `陈锐霆` 或 `杨永松` 即可查询另外两人。

```cypher
MATCH (person:BiographicalSubject {canonical_name:'陈海峰'})
OPTIONAL MATCH p=(person)-[:HAS_LIFE_EPISODE]->(episode:LifeEpisode)
OPTIONAL MATCH q=(episode)-[:BIOGRAPHICAL_NEXT]->(:LifeEpisode)
OPTIONAL MATCH r=(episode)-[:SUPPORTED_BY_EVENT]->(event:EventNode)<-[:HAS_EVENT]-(d:InterviewDocument)
RETURN person, p, q, r, d;
```

### 2. 陈海峰按时间排列的生平表

```cypher
MATCH (person:BiographicalSubject {canonical_name:'陈海峰'})-[:HAS_LIFE_EPISODE]->(episode:LifeEpisode)
OPTIONAL MATCH (episode)-[:SUPPORTED_BY_EVENT]->(event:EventNode)<-[:HAS_EVENT]-(d:InterviewDocument)
RETURN episode.life_order AS 生平顺序,
       episode.normalized_start AS 起始时间,
       episode.normalized_end AS 结束时间,
       episode.episode_name AS 人物经历,
       episode.episode_scope AS 经历性质,
       collect(DISTINCT d.title) AS 来源访谈
ORDER BY 生平顺序;
```

### 3. 从人物经历回到原文

```cypher
MATCH (:BiographicalSubject {canonical_name:'陈海峰'})-[:HAS_LIFE_EPISODE]->(episode:LifeEpisode)
MATCH (episode)-[:SUPPORTED_BY_EVENT]->(event:EventNode)<-[:HAS_EVENT]-(d:InterviewDocument)
OPTIONAL MATCH (segment:SourceSegment)-[:HAS_ATTACHMENT]->(:SourceAttachment)-[:ATTACHES_TO]->(event)
RETURN episode.life_order AS 生平顺序, episode.episode_name AS 人物经历,
       d.title AS 来源访谈, collect(DISTINCT segment.verbatim_text) AS 原文证据
ORDER BY 生平顺序;
```

### 4. 查看讲述过但没有冒充本人经历的历史背景

```cypher
MATCH (person:BiographicalSubject {canonical_name:'陈海峰'})-[:NARRATED_CONTEXT]->(event:EventNode)
MATCH (d:InterviewDocument)-[:HAS_EVENT]->(event)
RETURN person.canonical_name AS 人物, d.title AS 来源访谈,
       event.event_name AS 叙述背景, event.historical_order AS 文档内顺序
ORDER BY 来源访谈, 文档内顺序;
```

### 5. 原有文档事件图（保持不变）

```cypher
MATCH (d:InterviewDocument)-[:HAS_EVENT]->(e:EventNode)
OPTIONAL MATCH (e)-[:HAS_TIME]->(t:EventTime)
RETURN d, e, t
LIMIT 100;
```

### 6. 查看二级结构

```cypher
MATCH p=(e:EventNode {event_id:'CHF-V1-E03'})-[:HAS_STAGE|HAS_PROCESS|HAS_TYPE|HAS_PARTICIPANT|HAS_CIRCUMSTANCE]->(x)
RETURN p;
```

### 7. 查看跨人物共享实体

```cypher
MATCH (d:InterviewDocument)-[:HAS_SEGMENT]->(:SourceSegment)-[:HAS_MENTION]->(:EntityMention)-[:MENTIONS]->(entity:Entity)
WITH entity, collect(DISTINCT d.interviewee) AS people
WHERE size(people) > 1
RETURN entity.canonical_name, people;
```

### 8. 查看脚注中的实体、日期和挂接事件

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

