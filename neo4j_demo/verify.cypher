// 1. 总体规模
MATCH (n)
RETURN labels(n) AS labels, count(*) AS node_count
ORDER BY node_count DESC;

// 2. 每位受访者的一级事件链
MATCH (d:InterviewDocument)-[:HAS_EVENT]->(e:EventNode)
OPTIONAL MATCH (e)-[:HAS_TIME]->(t:EventTime)
RETURN d.interviewee AS 人物, e.historical_order AS 顺序, e.event_name AS 事件,
       t.raw_text AS 原文时间, t.normalized_start AS 规范起点
ORDER BY 人物, 顺序;

// 3. 事件—类型—过程—参与者—环境的理论框架展示
MATCH (e:EventNode)-[:HAS_TYPE]->(type:EventType)
MATCH (e)-[:HAS_PROCESS]->(p:Process)
OPTIONAL MATCH (e)-[pr:HAS_PARTICIPANT]->(participant:Entity)
OPTIONAL MATCH (e)-[:HAS_CIRCUMSTANCE]->(c:Circumstance)
RETURN e.event_name AS 事件, type.name AS 类型, p.process_normalized AS 过程,
       collect(DISTINCT pr.role + '：' + participant.canonical_name) AS 参与者,
       collect(DISTINCT c.kind + '：' + c.value_text) AS 环境
ORDER BY e.event_id;

// 4. 跨人物共享实体
MATCH (d:InterviewDocument)-[:HAS_SEGMENT]->(s:SourceSegment)-[:HAS_MENTION]->(:EntityMention)-[:MENTIONS]->(entity:Entity)
WITH entity, collect(DISTINCT d.interviewee) AS people, count(*) AS mentions
WHERE size(people) > 1
RETURN entity.canonical_name AS 共享实体, entity.entity_type AS 类型,
       people AS 涉及人物, mentions AS 提及次数
ORDER BY mentions DESC, 共享实体;

// 5. 陈海峰某一长事件展开至二级阶段和原文
MATCH (e:EventNode {event_id:'CHF-V1-E03'})-[:HAS_STAGE]->(stage:ProcessStage)
OPTIONAL MATCH (segment:SourceSegment)-[:HAS_ATTACHMENT]->(:SourceAttachment)-[:ATTACHES_TO]->(stage)
RETURN e.event_name AS 一级事件, stage.stage_order AS 阶段顺序,
       stage.stage_summary AS 二级阶段,
       collect(DISTINCT segment.verbatim_text) AS 原文
ORDER BY 阶段顺序;

// 6. 没有进入事件节点的文档级原文仍可查询
MATCH (d:InterviewDocument)-[:HAS_SEGMENT]->(s:SourceSegment)
MATCH (s)-[:HAS_ATTACHMENT]->(a:SourceAttachment)-[:ATTACHES_TO]->(d)
RETURN d.interviewee AS 人物, s.segment_order AS 原文顺序,
       s.segment_type AS 类型, a.function AS 挂接功能, s.verbatim_text AS 原文
ORDER BY 人物, 原文顺序;

// 7. 人工已核验、但现实指称仍不确定的实体
MATCH (e:Entity {review_status:'CONFIRMED'})
WHERE e.authority_status IN ['TRANSCRIPTION_UNCERTAIN', 'UNRESOLVED']
OPTIONAL MATCH (m:EntityMention)-[:MENTIONS]->(e)
OPTIONAL MATCH (s:SourceSegment)-[:HAS_MENTION]->(m)
RETURN e.canonical_name AS 实体, e.review_status AS 人工核验状态,
       e.authority_status AS 现实指称状态,
       collect(DISTINCT s.verbatim_text)[0..3] AS 原文示例
ORDER BY 实体;

// 8. 全文时间表达（正文、人物小传、脚注等），不含录音时间戳
MATCH (d:InterviewDocument)-[:HAS_SEGMENT]->(s:SourceSegment)-[:HAS_TIME_EXPRESSION]->(t:TimeExpression)
RETURN d.interviewee AS 人物, s.source_part AS 来源部分,
       t.raw_text AS 原文时间, t.normalized_start AS 规范起点,
       t.normalized_end AS 规范终点, t.precision AS 精度,
       s.verbatim_text AS 原文
ORDER BY 规范起点, 人物, s.segment_order;

// 9. 脚注及其统一实体和时间表达
MATCH (d:InterviewDocument)-[:HAS_SEGMENT]->(s:SourceSegment)
WHERE s.source_part='footnotes'
OPTIONAL MATCH (s)-[:HAS_MENTION]->(:EntityMention)-[:MENTIONS]->(entity:Entity)
OPTIONAL MATCH (s)-[:HAS_TIME_EXPRESSION]->(time:TimeExpression)
OPTIONAL MATCH (s)-[:HAS_ATTACHMENT]->(:SourceAttachment)-[:ATTACHES_TO]->(event:EventNode)
RETURN d.interviewee AS 人物, s.verbatim_text AS 脚注原文,
       collect(DISTINCT entity.canonical_name) AS 实体,
       collect(DISTINCT time.raw_text + '→' + time.normalized_start) AS 时间表达,
       collect(DISTINCT event.event_name) AS 挂接事件
ORDER BY 人物;

// 10. 以人物为中心查看按真实时间整理的生平经历表
MATCH (person:BiographicalSubject {canonical_name:'陈海峰'})-[:HAS_LIFE_EPISODE]->(episode:LifeEpisode)
OPTIONAL MATCH (episode)-[:SUPPORTED_BY_EVENT]->(event:EventNode)<-[:HAS_EVENT]-(d:InterviewDocument)
RETURN episode.life_order AS 生平顺序,
       episode.normalized_start AS 起始时间,
       episode.normalized_end AS 结束时间,
       episode.episode_name AS 人物经历,
       episode.episode_scope AS 经历性质,
       collect(DISTINCT d.title) AS 来源访谈,
       collect(DISTINCT event.event_id) AS 来源事件
ORDER BY 生平顺序;

// 11. 以人物为中心显示可连成一条线的图形；原文档NEXT不受影响
MATCH (person:BiographicalSubject {canonical_name:'陈海峰'})
OPTIONAL MATCH p=(person)-[:HAS_LIFE_EPISODE]->(episode:LifeEpisode)
OPTIONAL MATCH q=(episode)-[:BIOGRAPHICAL_NEXT]->(:LifeEpisode)
OPTIONAL MATCH r=(episode)-[:SUPPORTED_BY_EVENT]->(event:EventNode)<-[:HAS_EVENT]-(d:InterviewDocument)
RETURN person, p, q, r, d;

// 12. 从人物经历返回各次访谈中的事件和原文证据
MATCH (person:BiographicalSubject {canonical_name:'陈海峰'})-[:HAS_LIFE_EPISODE]->(episode:LifeEpisode)
MATCH (episode)-[:SUPPORTED_BY_EVENT]->(event:EventNode)<-[:HAS_EVENT]-(d:InterviewDocument)
OPTIONAL MATCH (segment:SourceSegment)-[:HAS_ATTACHMENT]->(:SourceAttachment)-[:ATTACHES_TO]->(event)
RETURN episode.life_order AS 生平顺序,
       episode.episode_name AS 人物经历,
       d.title AS 来源访谈,
       event.event_name AS 来源事件,
       collect(DISTINCT segment.verbatim_text) AS 原文证据
ORDER BY 生平顺序;

// 13. 查询某人物讲述、但当前不作为本人经历的历史背景
MATCH (person:BiographicalSubject {canonical_name:'陈海峰'})-[:NARRATED_CONTEXT]->(event:EventNode)
MATCH (d:InterviewDocument)-[:HAS_EVENT]->(event)
RETURN person.canonical_name AS 人物, d.title AS 来源访谈,
       event.event_name AS 叙述背景, event.historical_order AS 文档内顺序
ORDER BY 来源访谈, 文档内顺序;

