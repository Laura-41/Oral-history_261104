# 完整一级事件展开示例：CHF-V1-E03

> 数据源：本地 Neo4j 演示实例 `neo4j://127.0.0.1:7687`（浏览器 http://localhost:7474，认证已关闭）  
> 生成时间：2026-11-07 17:37  
> 数据角色：`WORKFLOW_DEMO`，六份人工确认 Demo 之一，不作正式测试金标准  
> 原文逐字取自 `SourceSegment.verbatim_text`，未作改写；查询实时跑库生成，非人工誊抄。

## 一、图谱里的挂接结构

```text
(InterviewDocument)-[:HAS_EVENT]->(EventNode)-[:HAS_STAGE]->(ProcessStage)
(ProcessStage)-[:NEXT_STAGE {logic}]->(ProcessStage)
(SourceSegment)-[:HAS_ATTACHMENT]->(SourceAttachment)-[:ATTACHES_TO]->(EventNode | ProcessStage)
(EventNode)-[:HAS_PROCESS]->(Process)   (EventNode)-[:HAS_TYPE]->(EventType)
(EventNode)-[:HAS_PARTICIPANT]->(Entity) (EventNode)-[:HAS_CIRCUMSTANCE]->(Circumstance)
(EventNode)-[:HAS_TIME]->(EventTime)
```

`SourceAttachment.function` 区分同一段原文的用途；本实例全库挂接统计：

| 挂接目标 | 功能 | 条数 |
|---|---|---:|
| DOCUMENT | COMMENT（叙述者评价） | 8 |
| DOCUMENT | DOCUMENT_NOTE（编者注/文档注） | 8 |
| DOCUMENT | DOCUMENT_ONLY（文档级兜底） | 122 |
| EVENT | BACKGROUND（背景说明） | 229 |
| EVENT | DOCUMENT_NOTE（编者注/文档注） | 25 |
| EVENT | EVIDENCE（逐字证据） | 306 |
| EVENT | INTERVIEWER_PROMPT（采访者提问） | 101 |
| STAGE | EVIDENCE（逐字证据） | 237 |

> 阶段层目前只挂 `EVIDENCE`；事件层另有背景、提问、编者注。文档级 `DOCUMENT_ONLY` 保留与任何事件无关的原文。

## 二、一级事件元信息

| 字段 | 值 |
|---|---|
| 文档 | 陈海峰一访01（CHF-V1-01） |
| 事件 ID | CHF-V1-E03 |
| 一级事件 | 在印书馆接触进步思想并支援地下党活动 |
| 事件类型 | 心理事件 |
| 核心过程 | 接触并形成初步革命认识 |
| 事件时间 | 1931年至1935年前后 |
| 结果状态 | 形成初步革命认识，并以秘密印刷和收入支援地下党活动 |
| 事实性 / 置信度 | FACT / HIGH |
| 复核状态 | CONFIRMED |
| 边界说明 | 从接触地下党学生的印刷材料开始，以形成认识并持续支援地下党活动为阶段结果 |
| 边界判断置信度 | HIGH |

**参与者**：Phenomenon＝进步书刊和革命思想；Senser＝陈海峰

**环境成分**：LOCATION＝上海荣华印书馆及地下党夜校；MANNER＝阅读进步书刊、参加夜校、秘密印刷并资助哥哥；TIME＝1931年至1935年前后

## 三、第一层：一级事件原文（21 条）

按功能分组、组内按 `segment_order` 排列。只有 `EVIDENCE` 可作为史实逐字证据。

### EVIDENCE（逐字证据）

- `CHF-V1-01-S0024` · 片段顺序 24 · 功能 `EVIDENCE`  ← 同时挂接二级阶段

```text
    陈海峰：但是这个时候呢，就有很多的地下党的一些知识分子，主要（是）大学生。上海当时有上海大夏大学、上海大学、复旦大学、同济大学。这些里头的一些地下党的学生要求我们印一些材料，后来宣传抗日了，开始是传播《大众哲学》里的一些内容啊，邹韬奋的《生活周刊》里面的一些内容啊，那么看了一些书的感想啊。都一篇一篇小的，活页的，像传单一样的，印这些东西。
```

- `CHF-V1-01-S0026` · 片段顺序 26 · 功能 `EVIDENCE`  ← 同时挂接二级阶段

```text
    陈海峰：那么我们在排字过程中间呢，也得到一些启示，也得到一些先进思想的熏陶。哥哥比我大10岁，那么哥哥早就学徒满了，满了以后，就是老师傅了。他参加地下党，那么在里面发展地下党。我那个时候小啊，我11岁去的，是不是？我满13岁等于14岁。这个中间呢，就是我们在厂里面这个排字间，我小时候个儿不是太高，但是以年龄来讲，就是冒充的是不是，那时候比较强壮，身体比较好。所以那个时候呢，我开些夜工都没问题，所以11岁、12岁、13岁耽误的事情比较多，那么这个老板剥削是很厉害的了。
```

- `CHF-V1-01-S0028` · 片段顺序 28 · 功能 `EVIDENCE`  ← 同时挂接二级阶段

```text
    陈海峰：（在）剥削厉害中间，我受到了熏陶，就是看些书。我的哥哥有意识地给我看些这种书，《铁流》啊、《使命图》（音）啊、《钢铁是怎样炼成的》。这许多书呢，慢慢地看，以后逐步引导，一步一步引导深入，那么来熏陶我们，信息就有了。慢慢地对革命有一点模糊的认识，人还小嘛。那时候，白天（还）差不多要干10个小时到12个小时的工作，晚上要读夜校。在上海爱文义路，现在的北京西路，当时有个国光商业专科学校（音），这里有个地下党办的夜校。我们在那里，从初中一直往那，一年一年读，还读夜校。
```

- `CHF-V1-01-S0030` · 片段顺序 30 · 功能 `EVIDENCE`  ← 同时挂接二级阶段

```text
    陈海峰：老板给我们的钱很少啊，那时候给我们的零用费，一个月一块钱，满师以后是3块钱。但是你别看那3块钱，当时3块钱就可以买一亩地。那时候买一根油条两个铜板，吃一个牛肉包子也是两个铜板，吃一大包花生米一个铜板。两毛小洋可以（换）48个铜板了，一毛小洋要24个铜板是不是。那就是说你别看那一块钱，一块钱够用，咱们零用也够了。这个零用钱塞在哪里呢？不是我一个人用，私底下还要支援我哥哥的地下党活动，地下党没钱。
```

- `CHF-V1-01-S0032` · 片段顺序 32 · 功能 `EVIDENCE`  ← 同时挂接二级阶段

```text
    陈海峰：一块钱，你给他五毛，有的时候需要给他八毛，我只能留两毛。这样，满四年3块钱，就（用）2块钱做我哥哥的活动经费。地下党没钱，他要活动，印什么宣传品啦，什么东西。
```

- `CHF-V1-01-S0034` · 片段顺序 34 · 功能 `EVIDENCE`  ← 同时挂接二级阶段

```text
    陈海峰：印书馆印，都晚上排。
```

- `CHF-V1-01-S0036` · 片段顺序 36 · 功能 `EVIDENCE`  ← 同时挂接二级阶段

```text
    陈海峰：偷偷排。
```

- `CHF-V1-01-S0040` · 片段顺序 40 · 功能 `EVIDENCE`

```text
    陈海峰：他开始只有十五岁，我1931年去的了，他是1934年参加革命，他比我大四岁，那个时候他已经满师了，当师傅了。
```

### BACKGROUND（背景说明）

- `CHF-V1-01-S0005` · 片段顺序 5 · 功能 `BACKGROUND`

```text
我是新四军的老战士，也是老卫生，1939年到现在，（做）卫生工作70年了。新四军没有到我们的家乡之前，我是在上海的，是工人。那么我们那个地区呢，是有地下党的，归上海党领导的。所以我们家庭、地区都有比较悠久的革命的传统历史
```

- `CHF-V1-01-S0013` · 片段顺序 13 · 功能 `BACKGROUND`

```text
    陈海峰：所以呢，抗日战争初期，我是搞这个工作。到新四军教导队学习以后，才送去学医，以后我再讲这个事。我的家庭是一个贫农家庭，就是家里三亩地，七八口人。我的叔父、我的表兄、我的哥哥，我的亲戚里头，有很多都是地下党员。我们一块参加革命的，我们这个庄子里头有二十多个人，现在是只剩我一个人了，其他都牺牲了。我的表兄、表弟、堂兄、堂弟都牺牲了。
```

- `CHF-V1-01-S0017` · 片段顺序 17 · 功能 `BACKGROUND`

```text
    陈海峰：冒充13岁人家才收，当学徒。那这个排字呢，当时一个字一个字排的，不像现在这样子有电脑了，知不知道？这个排字呢，三个月可以学会了。当时我们定的合同呢，就是要三年，那两年半多的时间，等于资本家剥削了我们的劳动力了。以后我们到了新四军教导队学《政治经济学》，那个薛暮桥，很有名的。薛暮桥给我们讲《政治经济学》的时候，讲到剥削剩余价值这个问题，我们才理解到资本家（用）什么手段来剥削我们工人的。
```

- `CHF-V1-01-S0019` · 片段顺序 19 · 功能 `BACKGROUND`

```text
    陈海峰：学徒呢，我们印书馆开始不大，以后慢慢地扩大了。三年中间，扩大差不多一倍到两倍，工人越来越多，设备越来越好。那么这个呢，就是说当时我的哥哥是1934年参加地下党的了，我是1931年到上海的了。那么我们这个印书馆呢，就是在上海新闸路83号，叫荣华印书馆，“光荣”的“荣”，“中华人民共和国”的“华”。
```

- `CHF-V1-01-S0022` · 片段顺序 22 · 功能 `BACKGROUND`

```text
    陈海峰：什么东西都印，人家写的著作，小册子，厚的都有，各种各样的书，他们里面都挂着，老板他自己赚钱嘛。
```

- `CHF-V1-01-S0038` · 片段顺序 38 · 功能 `BACKGROUND`

```text
    陈海峰：大四岁。
```

- `CHF-V1-01-S0042` · 片段顺序 42 · 功能 `BACKGROUND`

```text
    陈海峰： 1934年，他参加地下党，就离开我们印书馆了，他到到别的印书馆去了，不在我们这里了，就是私下联系了。这个地方里面还有地下党，这个我们不知道，当时是保密的。那么受这些熏陶以后呢，我只有十四岁，虚岁是十五岁，刚满师，受了地下党的影响。这个印书馆里面，资本家剥削我们剩余劳动，因为晚上经常加班，他任务来了，以他为主啊，那个资本家晚上要来查的。我们疲劳得睡觉，半夜里，有的打瞌睡了。打瞌睡查到了不行，查到了，他就要处分的。
```

### INTERVIEWER_PROMPT（采访者提问）

- `CHF-V1-01-S0021` · 片段顺序 21 · 功能 `INTERVIEWER_PROMPT`

```text
    记者：当时这个印书馆都是印什么书？
```

- `CHF-V1-01-S0033` · 片段顺序 33 · 功能 `INTERVIEWER_PROMPT`  ← 同时挂接二级阶段

```text
    记者：陈老，当时印这个印刷品也是在咱们印书馆印吗？
```

- `CHF-V1-01-S0035` · 片段顺序 35 · 功能 `INTERVIEWER_PROMPT`  ← 同时挂接二级阶段

```text
    记者：偷偷地。
```

- `CHF-V1-01-S0037` · 片段顺序 37 · 功能 `INTERVIEWER_PROMPT`

```text
    记者：当时您哥哥比您大几岁？
```

- `CHF-V1-01-S0039` · 片段顺序 39 · 功能 `INTERVIEWER_PROMPT`

```text
    记者：大四岁，当时他也才十五岁。
```

### DOCUMENT_NOTE（编者注/文档注）

- `CHF-V1-01-N001` · 片段顺序 80 · 功能 `DOCUMENT_NOTE`

```text
 薛暮桥：（1904—2005），江苏无锡人。抗战期间，曾任新四军教导总队训练处副处长。建国后，曾任国家统计局局长、国家计委副主任等职。
```

## 四、第二层：二级阶段（4 个）与各自原文

**阶段链**：`CHF-V1-E03-P01` —SEQUENCE→ `CHF-V1-E03-P02` —SEQUENCE→ `CHF-V1-E03-P03` —SEQUENCE→ `CHF-V1-E03-P04`（终点，无后继）

| 顺序 | 阶段 ID | 二级阶段 | 关键过程 | 推进逻辑 | 下一阶段 | 阶段原文条数 | 复核 |
|---:|---|---|---|---|---|---:|---|
| 1 | CHF-V1-E03-P01 | 接触并印刷进步材料 | 印刷 | SEQUENCE | 阅读进步书刊并参加夜校 | 1 | CONFIRMED |
| 2 | CHF-V1-E03-P02 | 阅读进步书刊并参加夜校 | 阅读和学习 | SEQUENCE | 从收入中资助哥哥的地下党活动 | 2 | CONFIRMED |
| 3 | CHF-V1-E03-P03 | 从收入中资助哥哥的地下党活动 | 资助 | SEQUENCE | 夜间秘密排印宣传品 | 2 | CONFIRMED |
| 4 | CHF-V1-E03-P04 | 夜间秘密排印宣传品 | 秘密印刷 | — | — | 4 | CONFIRMED |

### 阶段 1 · 接触并印刷进步材料（CHF-V1-E03-P01）

- 关键过程：印刷
- 推进逻辑：SEQUENCE → 阅读进步书刊并参加夜校
- 挂接原文：1 条（全部 `EVIDENCE`）

- `CHF-V1-01-S0024` · 片段顺序 24  ← 同时挂接一级事件

```text
    陈海峰：但是这个时候呢，就有很多的地下党的一些知识分子，主要（是）大学生。上海当时有上海大夏大学、上海大学、复旦大学、同济大学。这些里头的一些地下党的学生要求我们印一些材料，后来宣传抗日了，开始是传播《大众哲学》里的一些内容啊，邹韬奋的《生活周刊》里面的一些内容啊，那么看了一些书的感想啊。都一篇一篇小的，活页的，像传单一样的，印这些东西。
```

### 阶段 2 · 阅读进步书刊并参加夜校（CHF-V1-E03-P02）

- 关键过程：阅读和学习
- 推进逻辑：SEQUENCE → 从收入中资助哥哥的地下党活动
- 挂接原文：2 条（全部 `EVIDENCE`）

- `CHF-V1-01-S0026` · 片段顺序 26  ← 同时挂接一级事件

```text
    陈海峰：那么我们在排字过程中间呢，也得到一些启示，也得到一些先进思想的熏陶。哥哥比我大10岁，那么哥哥早就学徒满了，满了以后，就是老师傅了。他参加地下党，那么在里面发展地下党。我那个时候小啊，我11岁去的，是不是？我满13岁等于14岁。这个中间呢，就是我们在厂里面这个排字间，我小时候个儿不是太高，但是以年龄来讲，就是冒充的是不是，那时候比较强壮，身体比较好。所以那个时候呢，我开些夜工都没问题，所以11岁、12岁、13岁耽误的事情比较多，那么这个老板剥削是很厉害的了。
```

- `CHF-V1-01-S0028` · 片段顺序 28  ← 同时挂接一级事件

```text
    陈海峰：（在）剥削厉害中间，我受到了熏陶，就是看些书。我的哥哥有意识地给我看些这种书，《铁流》啊、《使命图》（音）啊、《钢铁是怎样炼成的》。这许多书呢，慢慢地看，以后逐步引导，一步一步引导深入，那么来熏陶我们，信息就有了。慢慢地对革命有一点模糊的认识，人还小嘛。那时候，白天（还）差不多要干10个小时到12个小时的工作，晚上要读夜校。在上海爱文义路，现在的北京西路，当时有个国光商业专科学校（音），这里有个地下党办的夜校。我们在那里，从初中一直往那，一年一年读，还读夜校。
```

### 阶段 3 · 从收入中资助哥哥的地下党活动（CHF-V1-E03-P03）

- 关键过程：资助
- 推进逻辑：SEQUENCE → 夜间秘密排印宣传品
- 挂接原文：2 条（全部 `EVIDENCE`）

- `CHF-V1-01-S0030` · 片段顺序 30  ← 同时挂接一级事件

```text
    陈海峰：老板给我们的钱很少啊，那时候给我们的零用费，一个月一块钱，满师以后是3块钱。但是你别看那3块钱，当时3块钱就可以买一亩地。那时候买一根油条两个铜板，吃一个牛肉包子也是两个铜板，吃一大包花生米一个铜板。两毛小洋可以（换）48个铜板了，一毛小洋要24个铜板是不是。那就是说你别看那一块钱，一块钱够用，咱们零用也够了。这个零用钱塞在哪里呢？不是我一个人用，私底下还要支援我哥哥的地下党活动，地下党没钱。
```

- `CHF-V1-01-S0032` · 片段顺序 32  ← 同时挂接一级事件

```text
    陈海峰：一块钱，你给他五毛，有的时候需要给他八毛，我只能留两毛。这样，满四年3块钱，就（用）2块钱做我哥哥的活动经费。地下党没钱，他要活动，印什么宣传品啦，什么东西。
```

### 阶段 4 · 夜间秘密排印宣传品（CHF-V1-E03-P04）

- 关键过程：秘密印刷
- 推进逻辑：— → 无后继
- 挂接原文：4 条（全部 `EVIDENCE`）

- `CHF-V1-01-S0033` · 片段顺序 33  ← 同时挂接一级事件

```text
    记者：陈老，当时印这个印刷品也是在咱们印书馆印吗？
```

- `CHF-V1-01-S0034` · 片段顺序 34  ← 同时挂接一级事件

```text
    陈海峰：印书馆印，都晚上排。
```

- `CHF-V1-01-S0035` · 片段顺序 35  ← 同时挂接一级事件

```text
    记者：偷偷地。
```

- `CHF-V1-01-S0036` · 片段顺序 36  ← 同时挂接一级事件

```text
    陈海峰：偷偷排。
```

## 五、双重挂接说明

实现方案 §5.10 允许「同时说明整体和阶段时双重挂接」。本事件中，既挂在事件层又挂在阶段层的片段共 9 个：

```text
CHF-V1-01-S0024, CHF-V1-01-S0026, CHF-V1-01-S0028, CHF-V1-01-S0030, CHF-V1-01-S0032, CHF-V1-01-S0033, CHF-V1-01-S0034, CHF-V1-01-S0035, CHF-V1-01-S0036
```

因此「事件原文合计」与「阶段原文合计」不能简单相加当作独立语料量。

## 六、可复用查询口令

### 1. 一级事件原文清单

```cypher
MATCH (d:InterviewDocument)-[:HAS_EVENT]->(e:EventNode)
MATCH (seg:SourceSegment)-[:HAS_ATTACHMENT]->(a:SourceAttachment)-[:ATTACHES_TO]->(e)
RETURN d.title AS 文档, e.event_id AS 事件ID, e.event_name AS 一级事件,
       a.function AS 功能, seg.segment_order AS 片段顺序, seg.segment_id AS 片段ID,
       seg.verbatim_text AS 原文
ORDER BY 文档, 事件ID, 功能, 片段顺序;
```

### 2. 二级阶段原文清单

```cypher
MATCH (d:InterviewDocument)-[:HAS_EVENT]->(e:EventNode)-[:HAS_STAGE]->(s:ProcessStage)
MATCH (seg:SourceSegment)-[:HAS_ATTACHMENT]->(a:SourceAttachment)-[:ATTACHES_TO]->(s)
RETURN e.event_id AS 事件ID, s.stage_id AS 阶段ID, s.stage_order AS 顺序,
       s.stage_summary AS 二级阶段, a.function AS 功能, seg.segment_order AS 片段顺序,
       seg.verbatim_text AS 原文
ORDER BY 事件ID, 顺序, 片段顺序;
```

### 3. 一条完整一级事件：事件原文 + 二级阶段 + 阶段原文（把 event_id 换成别的即可）

```cypher
MATCH (d:InterviewDocument)-[:HAS_EVENT]->(e:EventNode {event_id:'CHF-V1-E03'})
OPTIONAL MATCH (e)-[:HAS_PROCESS]->(p:Process)
OPTIONAL MATCH (e)-[:HAS_TYPE]->(t:EventType)
OPTIONAL MATCH (e)-[:HAS_TIME]->(tm:EventTime)
WITH d, e, p, t, tm,
     [(seg:SourceSegment)-[:HAS_ATTACHMENT]->(a:SourceAttachment)-[:ATTACHES_TO]->(e) |
        {片段ID:seg.segment_id, 顺序:seg.segment_order, 功能:a.function, 原文:seg.verbatim_text}] AS 事件原文
OPTIONAL MATCH (e)-[:HAS_STAGE]->(s:ProcessStage)
WITH d, e, p, t, tm, 事件原文, s ORDER BY s.stage_order
OPTIONAL MATCH (s)-[n:NEXT_STAGE]->(s2:ProcessStage)
RETURN d.title AS 文档, d.doc_id AS 文档ID, e.event_name AS 一级事件, t.name AS 类型,
       p.process_normalized AS 过程, tm.raw_text AS 事件时间, 事件原文,
       collect({阶段ID:s.stage_id, 顺序:s.stage_order, 阶段:s.stage_summary, 关键过程:s.process_text,
                下一阶段:s2.stage_summary, 推进逻辑:n.logic, 复核状态:s.review_status,
                阶段原文:[(seg:SourceSegment)-[:HAS_ATTACHMENT]->(a:SourceAttachment)-[:ATTACHES_TO]->(s) |
                          {片段ID:seg.segment_id, 顺序:seg.segment_order, 功能:a.function, 原文:seg.verbatim_text}]}) AS 二级阶段
```

### 4. 图形化查看

```cypher
MATCH p=(:InterviewDocument)-[:HAS_EVENT]->(e:EventNode {event_id:'CHF-V1-E03'})-[:HAS_STAGE]->(s:ProcessStage)
OPTIONAL MATCH q=(s)-[:NEXT_STAGE]->(:ProcessStage)
OPTIONAL MATCH r=(seg:SourceSegment)-[:HAS_ATTACHMENT]->(:SourceAttachment)-[:ATTACHES_TO]->(e)
OPTIONAL MATCH u=(seg2:SourceSegment)-[:HAS_ATTACHMENT]->(:SourceAttachment)-[:ATTACHES_TO]->(s)
RETURN p, q, r, u LIMIT 300;
```

> **只要逐字证据时**：清单查询在 `MATCH` 后加 `WHERE a.function = 'EVIDENCE'`；嵌套查询则写在 pattern comprehension 内部，即 `[(seg)-[:HAS_ATTACHMENT]->(a)-[:ATTACHES_TO]->(e) WHERE a.function='EVIDENCE' | ...]`。本事件 21 条事件层原文中，只有 8 条是 `EVIDENCE`。  
> 图形查询同时展开事件层与阶段层原文会产生较多路径（本事件实测 189 行），若只想看骨架，删去最后两条 `OPTIONAL MATCH r/u`。
