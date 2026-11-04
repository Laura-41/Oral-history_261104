"""Four-document development-corpus annotation configuration (v3.2).

The event layer keeps a macro-event granularity.  Clause-level detail is
retained as ProcessStage and every extracted block remains a SourceSegment.
"""

from __future__ import annotations

from pilot_entity_config import E, R, CHF_ENTITIES, CRT_ENTITIES, SHARED_ENTITIES


def B(*nums: int) -> list[str]:
    return [f"B{n:04d}" for n in nums]


def S(start: int, end: int) -> list[str]:
    return [f"B{n:04d}" for n in range(start, end + 1)]


CHF_V2_EXTRA = [
    E("PER-AGNESSMEDLEY", "艾格尼丝·史沫特莱", "PERSON", "INDIVIDUAL", (("史沫特莱", "SHORT_NAME"),)),
    E("PER-YANZHENHENG", "严振衡", "PERSON", "INDIVIDUAL"),
    E("PER-YEZAO", "叶藻", "PERSON", "INDIVIDUAL"),
    E("PER-SHENQIZHEN", "沈其震", "PERSON", "INDIVIDUAL"),
    E("PER-CUIYITIAN", "崔义田", "PERSON", "INDIVIDUAL"),
    E("PER-GONGNAIQUAN", "宫乃泉", "PERSON", "INDIVIDUAL"),
    E("PER-QIZHONGHUAN", "齐仲桓", "PERSON", "INDIVIDUAL"),
    E("PER-SUNZHICHENG", "孙志诚", "PERSON", "INDIVIDUAL"),
    E("PER-WUZHILI", "吴之理", "PERSON", "INDIVIDUAL"),
    E("PER-ZHANGYANGFEN", "章央芬", "PERSON", "INDIVIDUAL"),
    E("PER-LIZHENXIANG", "李振湘", "PERSON", "INDIVIDUAL"),
    E("PER-WANGYUXIAN", "王聿先", "PERSON", "INDIVIDUAL"),
    E("PER-CHENFENGQIN", "陈凤琴", "PERSON", "INDIVIDUAL"),
    E("PER-YANGGUANG", "杨光", "PERSON", "INDIVIDUAL"),
    E("PER-FENGDING", "冯定", "PERSON", "INDIVIDUAL"),
    E("PER-LIYIMANG", "李一氓", "PERSON", "INDIVIDUAL"),
    E("PER-PENGHUSHAN", "彭户山（音）", "PERSON", "INDIVIDUAL", (("彭户山", "TRANSCRIPTION_VARIANT"),), authority_status="TRANSCRIPTION_UNCERTAIN", confidence="LOW"),
    E("PER-ZHOUZIKUN", "周子昆", "PERSON", "INDIVIDUAL"),
    E("PER-HUANGXUEMING", "黄学明（音）", "PERSON", "INDIVIDUAL", (("黄学明", "TRANSCRIPTION_VARIANT"),), authority_status="TRANSCRIPTION_UNCERTAIN", confidence="LOW"),
    E("PER-WUYOULIAN", "吴友廉", "PERSON", "INDIVIDUAL", (("吴幼莲", "FORMER_NAME"),)),
    E("PER-ZENGRUQING", "曾如清", "PERSON", "INDIVIDUAL"),
    E("PER-FANGLIANBAI", "方练百（音）", "PERSON", "INDIVIDUAL", (("方练百", "TRANSCRIPTION_VARIANT"),), authority_status="TRANSCRIPTION_UNCERTAIN", confidence="LOW"),
    E("PER-JIANGMING", "姜明", "PERSON", "INDIVIDUAL"),
    E("ORG-N4A-PUBLIC-HEALTH-CLASS", "新四军军医处第二期公共卫生训练班", "ORGANIZATION", "TRAINING_PROGRAM", (("公共卫生训练班", "ABBREVIATION"), ("卫训班", "ABBREVIATION"))),
    E("ORG-N4A-POLITICAL-TEAM", "新四军教导队政治队", "MILITARY_UNIT", "TRAINING_UNIT", (("政治队", "ABBREVIATION"),)),
    E("ORG-N4A-WARD", "新四军医院病房", "ORGANIZATION", "HOSPITAL"),
    E("GRP-N4A-TRAINEES", "公共卫生训练班学员", "OTHER", "GROUP", (("学生", "DESCRIPTIVE_NAME"),)),
    E("ENT-ANATOMY-DONOR", "为解剖教学提供遗体的抗日猎户", "PERSON", "UNNAMED_PERSON", (("尸体", "DESCRIPTIVE_NAME"), ("尸首", "DESCRIPTIVE_NAME"))),
    E("TERM-RALES", "啰音", "OTHER", "MEDICAL_TERM"),
    E("DISEASE-CONFLUENT-SMALLPOX", "融合性天花", "OTHER", "DISEASE"),
]


CHF_V3_EXTRA = [
    E("PER-ZHANGDINGCHENG", "张鼎丞", "PERSON", "INDIVIDUAL"),
    E("PER-ZHANGYUNYI", "张云逸", "PERSON", "INDIVIDUAL"),
    E("PER-TANZHENLIN", "谭震林", "PERSON", "INDIVIDUAL"),
    E("PER-ZHANGZHENGKUN", "张正坤", "PERSON", "INDIVIDUAL"),
    E("PER-YEFEI", "叶飞", "PERSON", "INDIVIDUAL"),
    E("PER-CHENRENHONG", "陈仁洪", "PERSON", "INDIVIDUAL"),
    E("PER-HUANGHUOXING", "黄火星", "PERSON", "INDIVIDUAL"),
    E("PER-FUQIUTAO", "傅秋涛", "PERSON", "INDIVIDUAL"),
    E("PER-XIANGYING", "项英", "PERSON", "INDIVIDUAL"),
    E("PER-YETING", "叶挺", "PERSON", "INDIVIDUAL"),
    E("PER-LIZHIGAO", "李志高", "PERSON", "INDIVIDUAL"),
    E("PER-XIEZHONGLIANG", "谢忠良", "PERSON", "INDIVIDUAL"),
    E("PER-TANGYAN", "唐炎", "PERSON", "INDIVIDUAL"),
    E("PER-LENGXIN", "冷欣", "PERSON", "INDIVIDUAL"),
    E("ORG-N4A-3DET", "新四军第三支队", "MILITARY_UNIT", "MILITARY_FORMATION", (("3支队", "ABBREVIATION"), ("三支队", "ABBREVIATION"))),
    E("ORG-N4A-5REG", "新四军第五团", "MILITARY_UNIT", "MILITARY_FORMATION", (("5团", "ABBREVIATION"),)),
    E("ORG-N4A-6REG", "新四军第六团", "MILITARY_UNIT", "MILITARY_FORMATION", (("6团", "ABBREVIATION"),)),
    E("ORG-N4A-GUARD", "新四军军部警卫团", "MILITARY_UNIT", "MILITARY_FORMATION", (("特务团", "HISTORICAL_NAME"), ("警卫团", "ABBREVIATION"))),
    E("ORG-KMT-52DIV", "国民党军第五十二师", "MILITARY_UNIT", "MILITARY_FORMATION", (("52师", "ABBREVIATION"),)),
    E("ORG-KMT-144DIV", "国民党军第一四四师", "MILITARY_UNIT", "MILITARY_FORMATION", (("144师", "ABBREVIATION"),)),
    E("ORG-KMT-40DIV", "国民党军第四十师", "MILITARY_UNIT", "MILITARY_FORMATION", (("40师", "ABBREVIATION"),)),
    E("PLACE-WUHU", "芜湖", "PLACE", "ADMINISTRATIVE_PLACE"),
    E("PLACE-FANCHANG", "繁昌", "PLACE", "ADMINISTRATIVE_PLACE"),
    E("PLACE-TONGLING", "铜陵", "PLACE", "ADMINISTRATIVE_PLACE"),
    E("PLACE-NANLING", "南陵", "PLACE", "ADMINISTRATIVE_PLACE"),
    E("PLACE-SHUNAN", "顺安镇", "PLACE", "SETTLEMENT"),
    E("PLACE-WUWEI", "无为县", "PLACE", "ADMINISTRATIVE_PLACE", (("无为", "ABBREVIATION"),)),
    E("PLACE-BAIMAZHOU", "白马洲", "PLACE", "LANDMARK"),
    E("PLACE-ZHONGFENXU", "中分徐村", "PLACE", "SETTLEMENT", (("中分徐", "ABBREVIATION"),)),
    E("PLACE-YANZIMU", "燕子牧", "PLACE", "SETTLEMENT"),
    E("PLACE-BADUHE", "八都河", "PLACE", "SETTLEMENT"),
    E("PLACE-MAOSHAN", "茅山", "PLACE", "LANDMARK"),
    E("EVT-WANNAN", "皖南事变", "HISTORICAL_EVENT", "BATTLE"),
    E("EVT-FANCHANG-BATTLES", "八次繁昌战斗", "HISTORICAL_EVENT", "BATTLE", (("繁昌战斗", "ABBREVIATION"),)),
]


CRT_V2_EXTRA = [
    E("PER-DINGWEIFEN", "丁惟汾", "PERSON", "INDIVIDUAL"),
    E("PER-SHIYOUSAN", "石友三", "PERSON", "INDIVIDUAL"),
    E("PER-WANGDEMIN", "王德民（音）", "PERSON", "INDIVIDUAL", (("王德民", "TRANSCRIPTION_VARIANT"),), authority_status="TRANSCRIPTION_UNCERTAIN", confidence="LOW"),
    E("PER-HEYINGQIN", "何应钦", "PERSON", "INDIVIDUAL"),
    E("PER-WANGXINGGANG", "王兴纲", "PERSON", "INDIVIDUAL"),
    E("PER-DAILI", "戴笠", "PERSON", "INDIVIDUAL"),
    E("ORG-32ARMY", "第三十二军", "MILITARY_UNIT", "MILITARY_FORMATION", (("32军", "ABBREVIATION"),)),
    E("ORG-32ARMY-GUARD", "第三十二军特务团", "MILITARY_UNIT", "MILITARY_FORMATION", (("特务团", "ABBREVIATION"),)),
    E("ORG-32ARMY-ARTILLERY", "第三十二军特务团炮兵大队", "MILITARY_UNIT", "MILITARY_FORMATION", (("炮兵大队", "ABBREVIATION"),)),
    E("ORG-NANJING-ARTILLERY", "南京汤山炮兵学校", "ORGANIZATION", "SCHOOL", (("南京炮校", "ABBREVIATION"), ("汤山炮校", "ABBREVIATION"))),
    E("PLACE-SHIJIAZHUANG", "石家庄", "PLACE", "ADMINISTRATIVE_PLACE"),
    E("PLACE-NANYUAN", "北京南苑", "PLACE", "SETTLEMENT", (("南苑", "ABBREVIATION"),)),
    E("PLACE-TANGSHAN", "南京汤山", "PLACE", "SETTLEMENT", (("汤山", "ABBREVIATION"),)),
    E("PLACE-SHUAIFUYUAN", "北京帅府园", "PLACE", "ADDRESS", (("帅府园", "ABBREVIATION"),)),
    E("EVT-GREAT-WALL", "长城抗战", "HISTORICAL_EVENT", "BATTLE"),
    E("EVT-HEMEI", "何梅协定", "HISTORICAL_EVENT", "TREATY"),
    E("PUB-WORLD-KNOWLEDGE", "《世界知识》", "PUBLICATION", "PERIODICAL", (("世界知识", "ALIAS"),)),
]


YYS_ENTITIES = SHARED_ENTITIES + [
    E("PER-YYS", "杨永松", "PERSON", "INDIVIDUAL", (("杨老", "DESCRIPTIVE_NAME"),)),
    E("PER-MAO", "毛泽东", "PERSON", "INDIVIDUAL"),
    E("PER-ZHANGWENTIAN", "张闻天", "PERSON", "INDIVIDUAL", (("洛甫", "ALIAS"),)),
    E("PER-HUANGYONGSHENG", "黄永胜", "PERSON", "INDIVIDUAL"),
    E("PER-DENGHUA", "邓华", "PERSON", "INDIVIDUAL"),
    E("PER-PENGMINGZHI", "彭明治", "PERSON", "INDIVIDUAL"),
    E("PER-YANGDEZHI", "杨得志", "PERSON", "INDIVIDUAL"),
    E("PER-CHENZHENGXIANG", "陈正湘", "PERSON", "INDIVIDUAL"),
    E("PER-XIONGBOTAO", "熊伯涛", "PERSON", "INDIVIDUAL"),
    E("PER-YANGCHENGWU", "杨成武", "PERSON", "INDIVIDUAL"),
    E("PER-LIUYALOU", "刘亚楼", "PERSON", "INDIVIDUAL"),
    E("PER-ZHANGSU", "张苏（音）", "PERSON", "INDIVIDUAL", (("张苏", "TRANSCRIPTION_VARIANT"),), authority_status="TRANSCRIPTION_UNCERTAIN", confidence="LOW"),
    E("ORG-RED-FIRST-CORPS", "红军第一军团", "MILITARY_UNIT", "MILITARY_FORMATION", (("一军团", "ABBREVIATION"),)),
    E("ORG-115DIV", "八路军第一一五师", "MILITARY_UNIT", "MILITARY_FORMATION", (("115师", "ABBREVIATION"),)),
    E("ORG-343BRIG", "八路军第一一五师第三四三旅", "MILITARY_UNIT", "MILITARY_FORMATION", (("343旅", "ABBREVIATION"),)),
    E("ORG-685REG", "八路军第一一五师第六八五团", "MILITARY_UNIT", "MILITARY_FORMATION", (("685团", "ABBREVIATION"),)),
    E("ORG-686REG", "八路军第一一五师第六八六团", "MILITARY_UNIT", "MILITARY_FORMATION", (("686团", "ABBREVIATION"),)),
    E("ORG-RED-UNIVERSITY", "中国人民抗日红军大学", "ORGANIZATION", "SCHOOL", (("红大", "ABBREVIATION"),)),
    E("PLACE-SHANGANNING", "陕甘边地区", "PLACE", "REGION"),
    E("PLACE-SANYUAN", "三原", "PLACE", "ADMINISTRATIVE_PLACE"),
    E("PLACE-FUPING", "富平", "PLACE", "ADMINISTRATIVE_PLACE"),
    E("PLACE-HANCHENG", "韩城", "PLACE", "ADMINISTRATIVE_PLACE"),
    E("PLACE-ZHICHUAN", "芝川", "PLACE", "SETTLEMENT"),
    E("PLACE-WANQUAN", "万泉县", "PLACE", "ADMINISTRATIVE_PLACE", (("万泉", "ABBREVIATION"),)),
    E("PLACE-HOUMA", "侯马", "PLACE", "ADMINISTRATIVE_PLACE"),
    E("PLACE-HUANGZHAI", "黄寨镇", "PLACE", "SETTLEMENT"),
    E("PLACE-YUANPING", "原平", "PLACE", "ADMINISTRATIVE_PLACE"),
    E("PLACE-DAYING", "大营", "PLACE", "SETTLEMENT"),
    E("PLACE-RANZHUANG", "冉庄", "PLACE", "SETTLEMENT"),
    E("PLACE-PINGXINGGUAN", "平型关", "PLACE", "LANDMARK"),
    E("EVT-XIAN", "西安事变", "HISTORICAL_EVENT", "POLITICAL_EVENT"),
    E("EVT-LUGOUQIAO", "卢沟桥事变", "HISTORICAL_EVENT", "BATTLE"),
]


DEVELOPMENT_DOCS = {
    "CHF-V2-01": {
        "folder":"03_陈海峰二访01", "title":"陈海峰二访01", "interviewee":"陈海峰", "interview_date":"2010-02-27", "visit_no":"2", "version":"二校后 阅读版",
        "source_file":"0920_01/语料/C 陈海峰_4+8+23/2访/01.陈海峰（二访）（二校后 阅读版）.docx", "speaker_id":"PER-CHF", "interviewer_id":"INT-CHF-V2",
        "events":[
            {"id":"CHF-V2-E01","name":"从江抗选调赴皖南新四军教导队学习","type":"MATERIAL_EVENT","process":"选调并赴教导队学习","narrative":1,"historical":1,"result":"进入新四军教导队政治队接受训练","factuality":"FACT","confidence":"HIGH","boundary":"从江抗选拔首名干部开始，以抵达皖南并进入政治队为阶段结果","evidence":B(7,9,16,18,20,22,24),"background":B(12,14),"prompts":B(3,6,10,13,19,23),"participants":[("PER-CHF","陈海峰","PERSON","Actor","被选调者"),("ORG-JIANGNAN-ANTI-JAPANESE","江南抗日义勇军第三路","MILITARY_UNIT","Actor","选送单位"),("ORG-N4A-POLITICAL-TEAM","新四军教导队政治队","MILITARY_UNIT","Goal","接收单位")],"circumstances":[("TIME","1938年12月至1939年1月","1938-12/1939-01",None),("LOCATION","江南至皖南新四军军部","皖南",None),("CAUSE","选送有作战考验和文化基础的工农干部","",None)]},
            {"id":"CHF-V2-E02","name":"由政治队转入公共卫生训练班","type":"MATERIAL_EVENT","process":"转入并参加公共卫生训练","narrative":2,"historical":2,"result":"成为第二期公共卫生训练班学员","factuality":"FACT","confidence":"HIGH","boundary":"从史沫特莱动员和按文化程度选人开始，以陈海峰同意并正式入班为结束","evidence":B(18,24,26,28,30),"background":B(25,27,29),"prompts":B(23,27,29),"participants":[("PER-CHF","陈海峰","PERSON","Actor","转训学员"),("PER-AGNESSMEDLEY","艾格尼丝·史沫特莱","PERSON","Actor","动员者"),("ORG-N4A-PUBLIC-HEALTH-CLASS","新四军军医处第二期公共卫生训练班","ORGANIZATION","Goal","接收单位")],"circumstances":[("TIME","1939年1月","1939-01",None),("CAUSE","抗战和部队需要医疗干部","",None),("MANNER","半自愿半抽调并征求本人意见","",None)]},
            {"id":"CHF-V2-E03","name":"在严格淘汰制度下完成卫训班学习","type":"MATERIAL_EVENT","process":"接受严格医学训练并完成学习","narrative":3,"historical":3,"result":"六十六名学员中二十三人毕业并成为卫生骨干","factuality":"FACT","confidence":"HIGH","boundary":"从六十六人开学和周考月考开始，以二十三人完成训练为阶段结果","evidence":B(32,35,37,39,43,45,47,49,51,67,70,72,74,76,78,80,82,84),"background":B(34,40,42,46,68,81,83),"prompts":B(34,40,42,46,66,68,81),"participants":[("PER-CHF","陈海峰","PERSON","Actor","学员兼第三班班长"),("GRP-N4A-TRAINEES","公共卫生训练班学员","OTHER","Actor","受训群体"),("ORG-N4A-PUBLIC-HEALTH-CLASS","新四军军医处第二期公共卫生训练班","ORGANIZATION","Scope","训练机构")],"circumstances":[("TIME","1939年1月至8月前后","1939-01/1939-08",None),("MANNER","周考、月考、毕业考、竞赛和医师带徒","",None),("PURPOSE","培养前方急需的医务人员","",None)]},
            {"id":"CHF-V2-E04","name":"通过病房实习掌握战地临床诊断","type":"MATERIAL_EVENT","process":"在病房实习并诊断常见疾病","narrative":4,"historical":4,"result":"能够依靠体征识别常见病并实施基础护理","factuality":"FACT","confidence":"HIGH","boundary":"从上午理论授课、下午进入病房开始，以掌握典型体征和实际护理为阶段结果","evidence":B(51,53,55,57,59,61,63,65),"background":B(56,58,60,62,64),"prompts":B(56,58,62,66),"participants":[("PER-CHF","陈海峰","PERSON","Actor","实习学员"),("ORG-N4A-WARD","新四军医院病房","ORGANIZATION","Scope","实习场所")],"circumstances":[("TIME","卫训班学习期间","1939",None),("MANNER","理论联系实际、望闻问切、物理诊断和床旁实习","",None)]},
            {"id":"CHF-V2-E05","name":"秘密取回遗体开展解剖教学并进行医德教育","type":"MATERIAL_EVENT","process":"取回遗体、实施解剖并送还安葬","narrative":5,"historical":5,"result":"完成解剖教学并形成尊重遗体贡献者的医德认识","factuality":"FACT","confidence":"HIGH","boundary":"从白天侦察墓地、夜间取回遗体开始，以解剖、缝合和送还遗体为结束","evidence":B(86,88,90,92,94),"background":B(87,89,91,93),"prompts":[],"participants":[("PER-CHF","陈海峰","PERSON","Actor","取回遗体者和学员"),("ENT-ANATOMY-DONOR","为解剖教学提供遗体的抗日猎户","PERSON","Goal","解剖对象"),("GRP-N4A-TRAINEES","公共卫生训练班学员","OTHER","Recipient","受教群体")],"circumstances":[("TIME","1939年卫训班学习期间","1939",None),("LOCATION","皖南山区墓地及训练班","皖南",None),("MANNER","夜间三人秘密取回、汽灯下教学、解剖后缝合送还","",None),("PURPOSE","学习解剖并进行医学道德教育","",None)]},
            {"id":"CHF-V2-E06","name":"完成基础训练并具备营级战场救护能力","type":"RELATIONAL_EVENT","process":"具备","narrative":6,"historical":6,"result":"毕业学员能够到营级单位独立承担战场急救和基础医疗任务","factuality":"FACT","confidence":"HIGH","boundary":"从说明前方医疗人才缺乏和培养目标开始，以明确学员毕业后的岗位与能力要求为结束","evidence":B(98,100,102,104,107,109,111,113,115),"background":B(95,97,99,101,103,105,106,108,110,112,114,116),"prompts":B(95,97,99,105,110,114),"participants":[("PER-CHF","陈海峰","PERSON","Carrier","毕业学员"),("ORG-N4A-PUBLIC-HEALTH-CLASS","新四军军医处第二期公共卫生训练班","ORGANIZATION","Attribute","基础训练经历")],"circumstances":[("TIME","1939年训练结束时","1939-08",None),("PURPOSE","为前方部队抢救伤病员并服务抗战","",None)]},
        ],
        "stages":[
            ("CHF-V2-E01",1,"在江抗中接受作战和宣传情报工作考验","任职与作战",B(7,16,18)),("CHF-V2-E01",2,"被选为首名赴教导队学习的干部","选调",B(20,22)),("CHF-V2-E01",3,"抵达皖南并进入政治队","入队",B(24)),
            ("CHF-V2-E02",1,"史沫特莱动员教导队学员学医","动员",B(18,24)),("CHF-V2-E02",2,"按文化程度筛选并征求本人意见","筛选",B(24,26)),("CHF-V2-E02",3,"正式进入第二期公共卫生训练班","转训",B(28,30)),
            ("CHF-V2-E03",1,"六十六人开学并实行连续考试","考核",B(32)),("CHF-V2-E03",2,"不合格或不能适应者退出","淘汰",B(35,37)),("CHF-V2-E03",3,"以正规课程和医师带徒开展训练","训练",B(49,67,72,74)),("CHF-V2-E03",4,"男女学员竞赛强化学习","竞赛",B(82,84)),("CHF-V2-E03",5,"二十三人毕业并成为卫生骨干","毕业",B(37,39)),
            ("CHF-V2-E04",1,"上午学习理论下午进入病房","床旁实习",B(51,63)),("CHF-V2-E04",2,"依靠体征诊断常见病","临床诊断",B(53,59,61)),("CHF-V2-E04",3,"为传染病患者实施护理","护理",B(63,65)),
            ("CHF-V2-E05",1,"白天侦察墓地夜间取回遗体","取回遗体",B(86,88)),("CHF-V2-E05",2,"教师说明遗体贡献者的抗日经历","医德讲授",B(90)),("CHF-V2-E05",3,"实施解剖并保存标本","解剖",B(92)),("CHF-V2-E05",4,"缝合并送还遗体","送还",B(92)),("CHF-V2-E05",5,"学员形成尊重贡献者的医德认识","形成认识",B(94)),
            ("CHF-V2-E06",1,"说明前方医务人员紧缺和培养目标","明确目标",B(100,102)),("CHF-V2-E06",2,"毕业后配置到营级医疗岗位","岗位配置",B(107)),("CHF-V2-E06",3,"掌握止血夹板包扎等战场急救","形成能力",B(109)),("CHF-V2-E06",4,"通过后续轮训逐阶段提高技术","继续进修",B(111,113,115)),
        ],
        "document_only":[], "comments":[],
    },
    "CHF-V3-01": {
        "folder":"04_陈海峰三访01", "title":"陈海峰三访01", "interviewee":"陈海峰", "interview_date":"2011-03-13", "visit_no":"3", "version":"三校后 阅读版（由旧版DOC转换）",
        "source_file":"0920_01/语料/C 陈海峰_4+8+23/3访/01.陈海峰（三访）20110808（三校后 阅读版）.doc", "speaker_id":"PER-CHF", "interviewer_id":"INT-CHF-V3",
        "events":[
            {"id":"CHF-V3-E01","name":"第三支队由谭震林实际统一指挥并完成指挥更替","type":"RELATIONAL_EVENT","process":"由谭震林实际统一指挥","narrative":1,"historical":1,"result":"第三支队形成由谭震林实际统筹党政军、后由张正坤接任的指挥结构","factuality":"FACT","confidence":"HIGH","boundary":"从介绍新四军四支队建制开始，以张正坤接任并在皖南事变中牺牲为阶段终点","evidence":B(4,5,7,9,10,16,17,20,22,23,24,27),"background":B(2,3,11,12,13,15,18,21,25),"prompts":B(2,11),"participants":[("ORG-N4A-3DET","新四军第三支队","MILITARY_UNIT","Carrier","被描述单位"),("PER-TANZHENLIN","谭震林","PERSON","Attribute","实际指挥者"),("PER-ZHANGZHENGKUN","张正坤","PERSON","Attribute","后任司令员")],"circumstances":[("TIME","新四军成立至皖南事变前","1938/1940",None),("LOCATION","皖南及江南地区","皖南/江南",None)]},
            {"id":"CHF-V3-E02","name":"叶飞率第六团主力东进后第三支队压缩为五个作战营","type":"MATERIAL_EVENT","process":"抽调东进并重组作战力量","narrative":2,"historical":2,"result":"第三支队由第五团三个营、第六团三营和司令部警卫营构成主要作战力量","factuality":"FACT","confidence":"HIGH","boundary":"从1939年叶飞率第六团团部和两个营东进开始，以第三支队直接指挥五个营为结果","evidence":B(28,29,31,32,34,38,39,40,42,43,45,46,47,49,50,51,53),"background":B(30,33,35,37,41,44,48,52),"prompts":B(41,48),"participants":[("PER-YEFEI","叶飞","PERSON","Actor","东进带队者"),("ORG-N4A-6REG","新四军第六团","MILITARY_UNIT","Goal","被抽调单位"),("ORG-N4A-3DET","新四军第三支队","MILITARY_UNIT","Actor","重组单位")],"circumstances":[("TIME","1939年至皖南事变前","1939/1940",None),("PURPOSE","支援江南发展并维持皖南作战","",None)]},
            {"id":"CHF-V3-E03","name":"第三支队在铜南繁一线执行防御和游击作战","type":"MATERIAL_EVENT","process":"防御正面并开展游击阻击伏击","narrative":3,"historical":3,"result":"牵制芜湖方向日军并维持皖南军部前沿安全","factuality":"FACT","confidence":"HIGH","boundary":"从说明面对芜湖南京方向的任务开始，以界定铜陵南陵繁昌防区及八次繁昌战斗为阶段结果","evidence":B(54,55,59,60,61,62,64,67,69,70,71,73,99,101,102,103,107,108,109,110,112,113,115,117,118,120,121,123,124,128,129,130,132,134,136,137,140,141,143),"background":B(56,57,63,65,66,68,72,104,105,106,111,114,116,119,122,125,126,127,131,133,135,138,139,142,144),"prompts":B(56,90,91,93,97,98,114,122,127,135),"participants":[("ORG-N4A-3DET","新四军第三支队","MILITARY_UNIT","Actor","作战单位"),("ORG-JP-FORCES","日军","MILITARY_UNIT","Goal","作战对象")],"circumstances":[("TIME","1939年至皖南事变前","1939/1940",None),("LOCATION","铜陵—南陵—繁昌及芜湖方向","铜南繁",None),("MANNER","游击、阻击、伏击和运动战结合","",None),("PURPOSE","牵制敌人并保卫军部前沿","",None)]},
            {"id":"CHF-V3-E04","name":"第三支队维持顺安至无为的军部过江交通线","type":"MATERIAL_EVENT","process":"护送人员物资并保障交通线","narrative":4,"historical":4,"result":"皖南军部与江北之间的人员、弹药和信息往来得以维持","factuality":"FACT","confidence":"HIGH","boundary":"从说明军部需要与江北联系开始，以明确地下兵站、交通站和护送机制为阶段结果","evidence":B(74,75,77,78,79,80,82,83,84,87,88,92,94,95,96),"background":B(76,81,85,86,89,90,91,93),"prompts":B(85,86,90,91,93,97),"participants":[("ORG-N4A-3DET","新四军第三支队","MILITARY_UNIT","Actor","交通保障单位"),("ORG-N4A-5REG-2BAT","新四军五团二营","MILITARY_UNIT","Actor","主要护送单位"),("ORG-N4A","新四军","MILITARY_UNIT","Client","交通线使用者")],"circumstances":[("TIME","皖南军部时期","1938/1940",None),("LOCATION","顺安镇—长江岛洲—无为县","顺安/无为",None),("MANNER","派连队掩护并设置地下兵站、交通站","",None)]},
            {"id":"CHF-V3-E05","name":"皖南军部筹划并分批向江北撤离","type":"MATERIAL_EVENT","process":"侦察路线并组织分批撤离","narrative":5,"historical":5,"result":"后方机关先行分批撤出，作战部队准备轻装撤离","factuality":"FACT","confidence":"HIGH","boundary":"从国民党多次逼迫新四军北撤开始，以后方机关已分批撤离和路线争议形成为阶段结果","evidence":B(153,155,156,157,158,160,161,162,164,165,167,169,170,171,172,173,174,176,177,178,180,182),"background":B(145,146,147,148,149,150,151,152,154,159,163,166,168,175,179,181,183),"prompts":B(145,147,149,151),"participants":[("ORG-N4A","新四军","MILITARY_UNIT","Actor","撤离主体"),("PER-XIANGYING","项英","PERSON","Actor","军部领导"),("PER-YETING","叶挺","PERSON","Actor","路线主张者")],"circumstances":[("TIME","1939年下半年至皖南事变前","1939-07/1940",None),("LOCATION","皖南—江南—江北","皖南/江北",None),("CAUSE","国民党逼迫北撤并形成军事包围","",None),("MANNER","多次侦察渡江路线、后方机关先撤、分批撤离","",None)]},
        ],
        "stages":[
            ("CHF-V3-E01",1,"张云逸名义任司令员、谭震林实际指挥","确立指挥",B(7,10,16)),("CHF-V3-E01",2,"谭震林转赴江南统一指挥东进部队","转移指挥",B(17,20,22)),("CHF-V3-E01",3,"张正坤接任第三支队司令员","接任",B(23,24)),
            ("CHF-V3-E02",1,"叶飞率第六团团部和两个营东进","抽调",B(28,29)),("CHF-V3-E02",2,"第六团三营并入第五团指挥","并编",B(31,32)),("CHF-V3-E02",3,"司令部直接指挥四个营和警卫营","重组",B(34,40)),("CHF-V3-E02",4,"以有限武器维持约两千人作战力量","维持战力",B(42,43,45,49,51,53)),
            ("CHF-V3-E03",1,"面对芜湖方向日军据点构筑正面防御","部署",B(54,55,60)),("CHF-V3-E03",2,"以游击阻击伏击和运动战牵制敌人","作战",B(61,62,64)),("CHF-V3-E03",3,"与第一四四师联络并获得弹药支援","联络友军",B(69,70,71,73)),("CHF-V3-E03",4,"划定铜南繁防区和纵深驻地","驻防",B(107,128,129,136,140)),("CHF-V3-E03",5,"在繁昌战斗中阻击日军进攻","阻击",B(113,115,117,118)),
            ("CHF-V3-E04",1,"确定顺安至无为为重要交通路线","确定路线",B(74,75,87,88)),("CHF-V3-E04",2,"第五团二营派连队掩护交通","护送",B(77,78,79)),("CHF-V3-E04",3,"运送人员弹药并维持地下交通站","维持交通",B(80,82,83)),
            ("CHF-V3-E05",1,"中央与国民党谈判并同意撤至江北","形成决定",B(155,156,157,158)),("CHF-V3-E05",2,"多次侦察渡江路线并评估风险","侦察",B(160,162,164,165)),("CHF-V3-E05",3,"国民党调集部队形成包围压力","形成包围",B(167,169,170)),("CHF-V3-E05",4,"后方机关分批先撤、作战部队轻装准备","分批撤离",B(174,176,177)),("CHF-V3-E05",5,"围绕撤离路线形成不同方案","路线争议",B(178,180,182)),
        ], "document_only":[], "comments":[],
    },
    "CRT-02": {
        "folder":"05_陈锐霆090422_02", "title":"陈锐霆090422第02份", "interviewee":"陈锐霆", "interview_date":"2009-04-20", "visit_no":"090422-02", "version":"二校后 阅读版",
        "source_file":"0920_01/语料/C 陈锐霆_15/02.陈锐霆 090422（二校后 阅读版）.docx", "speaker_id":"PER-CRT", "interviewer_id":"INT-CRT-02",
        "events":[
            {"id":"CRT-02-E01","name":"随商震部离晋赴冀并任炮兵大队区队长","type":"MATERIAL_EVENT","process":"转赴河北并担任炮兵区队长","narrative":1,"historical":1,"result":"进入第三十二军特务团炮兵大队并担任相当于连长的区队长","factuality":"FACT","confidence":"HIGH","boundary":"从阎锡山补充部队撤销、回教导团开始，以在邢台完成三十二军建制并任炮兵区队长为结束","evidence":B(20,22,24,26,28,30,32),"background":S(3,19),"prompts":B(9,11,15,27),"participants":[("PER-CRT","陈锐霆","PERSON","Actor","随队军官"),("PER-SHANGZHEN","商震","PERSON","Actor","部队领导"),("ORG-32ARMY-ARTILLERY","第三十二军特务团炮兵大队","MILITARY_UNIT","Goal","任职单位")],"circumstances":[("TIME","1930年9月前后","1930-09",None),("LOCATION","山西—石家庄—邢台","山西/河北",None),("CAUSE","补充部队撤销及商震召集旧部","",None)]},
            {"id":"CRT-02-E02","name":"九一八事变后参与抗日游行示威","type":"MATERIAL_EVENT","process":"参加抗日游行示威","narrative":2,"historical":2,"result":"军民公开表达坚决抗日和反对不抵抗的立场","factuality":"FACT","confidence":"HIGH","boundary":"从部队招兵完成并得知九一八事变开始，以军队和群众共同上街示威为结束","evidence":B(33,35),"background":B(34,36,37),"prompts":[],"participants":[("PER-CRT","陈锐霆","PERSON","Actor","参与者"),("ORG-32ARMY","第三十二军","MILITARY_UNIT","Actor","参与部队")],"circumstances":[("TIME","1931年九一八事变后","1931-09-18后",None),("LOCATION","邢台","邢台","PLACE-XINGTAI"),("CAUSE","反对日本侵略和不抵抗政策","",None)]},
            {"id":"CRT-02-E03","name":"部队驻南苑等待装备并自行整修营房生产生活","type":"MATERIAL_EVENT","process":"驻训并整修营房、开荒生产","narrative":3,"historical":3,"result":"在缺少炮弹的情况下维持部队驻训和生活","factuality":"FACT","confidence":"HIGH","boundary":"从第三十二军赴长城抗战而炮兵因无炮弹留守开始，以在南苑驻扎一年并获知炮校招生为结束","evidence":B(44,46,48,50,52),"background":B(45,47,49,51,53),"prompts":B(43,49),"participants":[("PER-CRT","陈锐霆","PERSON","Actor","炮兵军官"),("ORG-32ARMY-ARTILLERY","第三十二军特务团炮兵大队","MILITARY_UNIT","Actor","驻训单位")],"circumstances":[("TIME","1933年至1934年12月","1933/1934-12",None),("LOCATION","北京南苑","北京南苑","PLACE-NANYUAN"),("CAUSE","炮兵有炮无弹无法赴前线","",None),("MANNER","整修旧营房、开荒种菜","",None)]},
            {"id":"CRT-02-E04","name":"考入南京汤山炮兵学校第二期并完成学习","type":"MATERIAL_EVENT","process":"应考、入校并完成炮兵学习","narrative":4,"historical":4,"result":"完成南京炮校第二期学习并返回第三十二军","factuality":"FACT","confidence":"HIGH","boundary":"从获知炮校招生并准备英文和三民主义考试开始，以毕业返回部队为结束","evidence":B(52,54,56,58),"background":B(53,55,57,59),"prompts":[],"participants":[("PER-CRT","陈锐霆","PERSON","Actor","学员"),("ORG-NANJING-ARTILLERY","南京汤山炮兵学校","ORGANIZATION","Scope","学习单位")],"circumstances":[("TIME","1934年12月至1935年以后","1934-12/1935",None),("LOCATION","南京丁家桥、汤山","南京","PLACE-NANJING"),("MANNER","临时学习三民主义和英文后应试入学","",None)]},
            {"id":"CRT-02-E05","name":"与王兴纲交往并逐渐形成亲共抗日倾向","type":"MENTAL_EVENT","process":"了解并认同共产党的抗日和社会主张","narrative":5,"historical":5,"result":"对共产党产生好感并在思想上逐渐倾向共产党","factuality":"FACT","confidence":"HIGH","boundary":"从1931年在军部写标语时结识王兴纲开始，以1935年前后联系中断但亲共倾向形成作为阶段结果","evidence":B(60,62,64,66,68,70,72,74,76,79,81),"background":B(61,63,65,67,69,71,73,75,77,78,80,82,83,84,85,86,87,88,89,90,91,92,93),"prompts":B(61,78,82,84,86,90,92),"participants":[("PER-CRT","陈锐霆","PERSON","Senser","思想转变者"),("PER-WANGXINGGANG","王兴纲","PERSON","Phenomenon","教育和影响来源"),("ORG-CCP","中国共产党","ORGANIZATION","Phenomenon","逐渐认同对象")],"circumstances":[("TIME","1931年至1935年前后","1931/1935",None),("LOCATION","邢台、北京、南京","华北/南京",None),("MANNER","交友谈话、阅读进步书籍和口头教育","",None),("CAUSE","反感不抵抗和腐败，认同积极抗日主张","",None)]},
        ],
        "stages":[
            ("CRT-02-E01",1,"补充部队撤销后回到军官教导团","回归",B(20,22)),("CRT-02-E01",2,"随商震旧部转赴河北","转移",B(24,26,28)),("CRT-02-E01",3,"在邢台组建军部和特务团","建制",B(28)),("CRT-02-E01",4,"被任命为炮兵大队区队长","任职",B(30)),
            ("CRT-02-E03",1,"获得重迫击炮但缺少炮弹","装备不足",B(44)),("CRT-02-E03",2,"第三十二军开赴长城抗战、炮兵留守南苑","留守",B(46,48)),("CRT-02-E03",3,"整修营房并开荒种菜","生产生活",B(50,52)),
            ("CRT-02-E04",1,"准备英文和三民主义考试","备考",B(52,54)),("CRT-02-E04",2,"考入南京炮校第二期","入学",B(54)),("CRT-02-E04",3,"由丁家桥转入汤山新校学习","转校",B(54,56)),("CRT-02-E04",4,"毕业返回南撤中的部队","毕业返队",B(58)),
            ("CRT-02-E05",1,"在军部写标语时结识王兴纲","结识",B(60,62,64)),("CRT-02-E05",2,"通过交往建立信任并得知其党员身份","建立联系",B(66,68)),("CRT-02-E05",3,"接受进步书籍和共产主义口头教育","接受教育",B(70,72)),("CRT-02-E05",4,"反感不抵抗并认同共产党抗日主张","形成倾向",B(74,76)),("CRT-02-E05",5,"王兴纲随商震离开后联系中断","失去联系",B(76,79,81)),
        ], "document_only":[], "comments":[],
    },
    "YYS-01": {
        "folder":"06_杨永松100506_01", "title":"杨永松100506第01份", "interviewee":"杨永松", "interview_date":"2010-04-27", "visit_no":"1", "version":"二校后 阅读版",
        "source_file":"0920_01/语料/Y 杨永松_10/01.杨永松100506（二校后 阅读版）.docx", "speaker_id":"PER-YYS", "interviewer_id":"INT-YYS-01",
        "events":[
            {"id":"YYS-E01","name":"西安事变后红军北撤整训并准备全面抗战","type":"MATERIAL_EVENT","process":"北撤、整训并进行抗战准备","narrative":1,"historical":1,"result":"中共中央和红军形成统一战线与全面抗战的政治军事准备","factuality":"FACT","confidence":"HIGH","boundary":"从西安事变和平解决、红军北撤开始，以卢沟桥事变后向西安附近集结为结束","evidence":B(8,10,12,14,16,18),"background":B(3,4,5,6,7,9,11,13,15,17,19),"prompts":B(3,5,7),"participants":[("ORG-RED-FIRST-CORPS","红军第一军团","MILITARY_UNIT","Actor","整训部队"),("ORG-CCP","中国共产党","ORGANIZATION","Actor","政治领导")],"circumstances":[("TIME","西安事变和平解决后至1937年7月","1936-12/1937-07",None),("LOCATION","陕甘边地区及西安附近","陕甘",None),("PURPOSE","准备全国抗战和国共合作","",None)]},
            {"id":"YYS-E02","name":"红军第一军团改编为八路军第一一五师","type":"MATERIAL_EVENT","process":"改编并重新编成旅团","narrative":2,"historical":2,"result":"红二师改编为第一一五师第三四三旅第六八五团","factuality":"FACT","confidence":"HIGH","boundary":"从第一军团在三原接受改编开始，以各师旅团番号和编制确定为结束","evidence":B(20,22,24),"background":B(21,23),"prompts":[],"participants":[("ORG-RED-FIRST-CORPS","红军第一军团","MILITARY_UNIT","Goal","被改编单位"),("ORG-115DIV","八路军第一一五师","MILITARY_UNIT","Goal","改编后单位"),("ORG-685REG","八路军第一一五师第六八五团","MILITARY_UNIT","Goal","杨永松所在单位")],"circumstances":[("TIME","1937年8月23日前后","1937-08-23",None),("LOCATION","三原","三原","PLACE-SANYUAN"),("PURPOSE","统一编制并开赴抗日前线","",None)]},
            {"id":"YYS-E03","name":"红军战士接受换装并誓师开赴抗日前线","type":"MENTAL_EVENT","process":"克服不舍并接受换帽换装","narrative":3,"historical":3,"result":"战士服从统一战线和抗战需要，换装后出发","factuality":"FACT","confidence":"HIGH","boundary":"从誓师大会宣布换装要求开始，以战士保存红星帽作纪念并服从出发命令为结束","evidence":B(24,26,28,30),"background":B(25,27,29),"prompts":B(27),"participants":[("PER-YYS","杨永松","PERSON","Senser","亲历者"),("ORG-685REG","八路军第一一五师第六八五团","MILITARY_UNIT","Senser","接受换装群体"),("EVT-ANTI-JAPANESE-WAR","抗日战争","HISTORICAL_EVENT","Phenomenon","共同目标")],"circumstances":[("TIME","1937年8月23日至24日前后","1937-08-23/1937-08-24",None),("CAUSE","国家利益、统一战线和开赴抗日前线需要","",None),("MANNER","忍痛摘下红星帽保存纪念并戴青天白日帽","",None)]},
            {"id":"YYS-E04","name":"第六八五团由三原行军渡黄河抵达侯马","type":"MATERIAL_EVENT","process":"行军、渡河并抵达侯马","narrative":4,"historical":4,"result":"部队抵达侯马等待铁路输送","factuality":"FACT","confidence":"HIGH","boundary":"从第六八五团作为前卫出发开始，以经富平韩城芝川渡河、经过万泉抵达侯马为结束","evidence":B(30,33,35,37,39,41),"background":B(31,32,34,36,38,40),"prompts":B(32,34,40),"participants":[("ORG-685REG","八路军第一一五师第六八五团","MILITARY_UNIT","Actor","行军部队"),("PER-YYS","杨永松","PERSON","Actor","随军人员")],"circumstances":[("TIME","1937年8月24日以后","1937-08-24后",None),("LOCATION","三原—富平—韩城—芝川—万泉—侯马","晋陕路线",None),("MANNER","步行、乘船渡黄河","",None)]},
            {"id":"YYS-E05","name":"第六八五团在侯马完成团级主官调整","type":"RELATIONAL_EVENT","process":"由杨得志接任团长","narrative":5,"historical":5,"result":"杨得志任团长、陈正湘任副团长、彭明治任参谋长","factuality":"FACT","confidence":"HIGH","boundary":"从原团长黄永胜和参谋长熊伯涛被调出开始，以新团级主官配置确立为结束","evidence":B(41,43,50,52,54,56,58,60,62,67,69),"background":B(42,44,51,53,55,57,59,61,63,64,65,66,68),"prompts":B(50,53,57,59,61,63,66),"participants":[("ORG-685REG","八路军第一一五师第六八五团","MILITARY_UNIT","Carrier","被调整单位"),("PER-YANGDEZHI","杨得志","PERSON","Attribute","新任团长"),("PER-CHENZHENGXIANG","陈正湘","PERSON","Attribute","新任副团长"),("PER-PENGMINGZHI","彭明治","PERSON","Attribute","参谋长")],"circumstances":[("TIME","1937年8月抵达侯马后","1937-08",None),("LOCATION","侯马","侯马","PLACE-HOUMA"),("CAUSE","开辟晋察冀根据地的人事部署","",None)]},
            {"id":"YYS-E06","name":"第六八五团经铁路和徒步辗转到达大营集结","type":"MATERIAL_EVENT","process":"乘车、修路、躲避轰炸并转进集结","narrative":6,"historical":6,"result":"第三四三旅在大营完成集结并准备平型关作战","factuality":"FACT","confidence":"HIGH","boundary":"从侯马登上敞篷火车开始，以经太原黄寨原平和徒步转运后在大营集结为结束","evidence":B(45,47,49,71,73,75,77),"background":B(46,48,70,72,74,76,78),"prompts":B(48),"participants":[("ORG-685REG","八路军第一一五师第六八五团","MILITARY_UNIT","Actor","转进部队"),("PER-YYS","杨永松","PERSON","Actor","随军人员")],"circumstances":[("TIME","1937年9月平型关战斗前","1937-09",None),("LOCATION","侯马—太原—黄寨—原平—大营","山西",None),("MANNER","乘敞篷火车、途中修路、夜间避空袭并徒步转进","",None)]},
            {"id":"YYS-E07","name":"部队向平型关前进并发现国民党防御准备不足","type":"MENTAL_EVENT","process":"观察并判断抗日工事准备不足","narrative":7,"historical":7,"result":"形成国民党未认真进行抗日防御准备的判断，并在冉庄附近完成战前集结","factuality":"FACT","confidence":"HIGH","boundary":"从离开大营向平型关方向前进开始，以发现闲置建材、判断工事不足并抵达战前集结地为结束","evidence":B(79,81,83,85,87),"background":B(80,82,84,86,88),"prompts":B(80,84),"participants":[("PER-YYS","杨永松","PERSON","Senser","观察判断者"),("ENT-KMT-DEFENSE-PREP","国民党抗日防御准备","OTHER","Phenomenon","被判断对象"),("ORG-685REG","八路军第一一五师第六八五团","MILITARY_UNIT","Actor","集结部队")],"circumstances":[("TIME","平型关战斗前一至数日","1937-09",None),("LOCATION","大营至平型关方向、冉庄附近","平型关地区",None),("MANNER","观察未使用的钢筋水泥和未修工事","",None)]},
        ],
        "stages":[
            ("YYS-E01",1,"西安事变和平解决后红军向北撤离","北撤",B(8)),("YYS-E01",2,"在陕甘边地区整训并召开代表会议","整训与会议",B(10,12)),("YYS-E01",3,"调整土地政策并开展国共谈判","政策调整",B(14,16)),("YYS-E01",4,"卢沟桥事变后向西安附近集结","集结",B(18)),
            ("YYS-E02",1,"第一军团改编为第一一五师","师级改编",B(20)),("YYS-E02",2,"红二师和红四师分别改编为六八五团、六八六团","团级改编",B(20)),("YYS-E02",3,"红一师以独立团名义单独行动后并入旅属团","调整编制",B(22,24)),
            ("YYS-E03",1,"誓师大会动员换装和抗战","动员",B(24)),("YYS-E03",2,"战士不舍红星帽并保存纪念","情感反应",B(26,28)),("YYS-E03",3,"服从统一战线和抗战需要完成换装","接受",B(30)),
            ("YYS-E04",1,"从三原经富平韩城行军","行军",B(30)),("YYS-E04",2,"在芝川乘船渡过黄河","渡河",B(33,35)),("YYS-E04",3,"经万泉接受群众欢迎欢送","沿途行军",B(37,39)),("YYS-E04",4,"抵达侯马等待列车","抵达",B(41)),
            ("YYS-E05",1,"黄永胜和熊伯涛调离团部","调出",B(43)),("YYS-E05",2,"杨得志等从红大赶到部队","到任",B(43)),("YYS-E05",3,"确立新团长、副团长和参谋长","任命",B(43)),("YYS-E05",4,"说明人事调整与开辟根据地部署","解释",B(52,56,62)),
            ("YYS-E06",1,"乘脏旧敞篷列车离开侯马","乘车",B(45,47)),("YYS-E06",2,"因路基塌陷多次下车修路","修路",B(71)),("YYS-E06",3,"为躲避日机轰炸在黄寨夜间转运","避空袭",B(73)),("YYS-E06",4,"在原平下车后徒步并转乘汽车","转运",B(75,77)),("YYS-E06",5,"第三四三旅在大营集结完毕","集结",B(77)),
            ("YYS-E07",1,"向平型关方向行军并观察沿途工事材料","观察",B(79,81)),("YYS-E07",2,"判断防御工事未得到实际建设","判断",B(79,83,85)),("YYS-E07",3,"在冉庄附近完成战前集结","集结",B(85,87)),
        ], "document_only":[], "comments":[],
    },
}


DEVELOPMENT_ENTITY_CATALOGS = {
    "CHF-V2-01": CHF_ENTITIES + CHF_V2_EXTRA,
    "CHF-V3-01": CHF_ENTITIES + CHF_V3_EXTRA,
    "CRT-02": CRT_ENTITIES + CRT_V2_EXTRA,
    "YYS-01": YYS_ENTITIES + [E("ENT-KMT-DEFENSE-PREP", "国民党抗日防御准备", "OTHER", "ABSTRACT_CONCEPT")],
}


DEVELOPMENT_ENTITY_RELATIONS = {
    "CHF-V2-01": [
        R("PER-CHF", "MEMBER_OF", "ORG-JIANGNAN-ANTI-JAPANESE", role_label="宣传、情报干部", source_ref="B0007", source_status="ORAL_TESTIMONY"),
        R("PER-CHF", "STUDIED_AT", "ORG-N4A-POLITICAL-TEAM", start_date="1938-12", source_ref="B0024", source_status="ORAL_TESTIMONY"),
        R("PER-CHF", "STUDIED_AT", "ORG-N4A-PUBLIC-HEALTH-CLASS", start_date="1939-01", end_date="1939-08", source_ref="B0030", source_status="ORAL_TESTIMONY"),
    ],
    "CHF-V3-01": [
        R("PER-TANZHENLIN", "COMMANDED", "ORG-N4A-3DET", role_label="实际指挥者", source_ref="B0010", source_status="ORAL_TESTIMONY"),
        R("PER-ZHANGZHENGKUN", "COMMANDED", "ORG-N4A-3DET", role_label="司令员", source_ref="B0023", source_status="ORAL_TESTIMONY"),
        R("ORG-N4A-5REG", "PART_OF", "ORG-N4A-3DET", source_ref="B0028", source_status="ORAL_TESTIMONY"),
        R("ORG-N4A-6REG", "PART_OF", "ORG-N4A-3DET", source_ref="B0028", source_status="ORAL_TESTIMONY"),
    ],
    "CRT-02": [
        R("PER-CRT", "HELD_POSITION_AT", "ORG-32ARMY-ARTILLERY", role_label="区队长", start_date="1930-09", source_ref="B0030", source_status="ORAL_TESTIMONY"),
        R("PER-CRT", "STUDIED_AT", "ORG-NANJING-ARTILLERY", role_label="第二期学员", start_date="1935", source_ref="B0054", source_status="ORAL_TESTIMONY"),
        R("PER-WANGXINGGANG", "INFLUENCED", "PER-CRT", role_label="政治思想教育", start_date="1931", end_date="1935", source_ref="B0070", source_status="ORAL_TESTIMONY"),
    ],
    "YYS-01": [
        R("PER-YYS", "MEMBER_OF", "ORG-685REG", start_date="1937-08", source_ref="B0020", source_status="ORAL_TESTIMONY"),
        R("ORG-685REG", "PART_OF", "ORG-343BRIG", source_ref="B0020", source_status="ORAL_TESTIMONY"),
        R("ORG-343BRIG", "PART_OF", "ORG-115DIV", source_ref="B0020", source_status="ORAL_TESTIMONY"),
        R("PER-YANGDEZHI", "COMMANDED", "ORG-685REG", role_label="团长", start_date="1937-08", source_ref="B0043", source_status="ORAL_TESTIMONY"),
    ],
}


DEVELOPMENT_EVENT_TIMES = {
    "CHF-V2-01": {
        "CHF-V2-E01": ("1938年12月至1939年1月", "1938-12", "1939-01", "INTERVAL", "APPROXIMATE", "ORAL_TESTIMONY"),
        "CHF-V2-E02": ("1939年1月", "1939-01", "1939-01", "MONTH", "EXACT", "ORAL_TESTIMONY"),
        "CHF-V2-E03": ("1939年1月至8月前后", "1939-01", "1939-08", "INTERVAL", "APPROXIMATE", "MIXED"),
        "CHF-V2-E04": ("卫训班学习期间", "1939-01", "1939-08", "INTERVAL", "APPROXIMATE", "CONTEXTUAL_INFERENCE"),
        "CHF-V2-E05": ("1939年卫训班学习期间", "1939-01", "1939-08", "INTERVAL", "APPROXIMATE", "CONTEXTUAL_INFERENCE"),
        "CHF-V2-E06": ("1939年训练结束时", "1939-08", "1939-08", "MONTH", "APPROXIMATE", "EDITORIAL_PROFILE"),
    },
    "CHF-V3-01": {
        "CHF-V3-E01": ("新四军成立至皖南事变前", "1938", "1940", "INTERVAL", "APPROXIMATE", "ORAL_TESTIMONY"),
        "CHF-V3-E02": ("1939年至皖南事变前", "1939", "1940", "INTERVAL", "APPROXIMATE", "ORAL_TESTIMONY"),
        "CHF-V3-E03": ("1939年至皖南事变前", "1939", "1940", "INTERVAL", "APPROXIMATE", "ORAL_TESTIMONY"),
        "CHF-V3-E04": ("皖南军部时期", "1938", "1940", "INTERVAL", "APPROXIMATE", "CONTEXTUAL_INFERENCE"),
        "CHF-V3-E05": ("1939年下半年至皖南事变前", "1939-07", "1940-12", "INTERVAL", "APPROXIMATE", "ORAL_TESTIMONY"),
    },
    "CRT-02": {
        "CRT-02-E01": ("1930年9月前后", "1930-09", "1930-09", "MONTH", "APPROXIMATE", "ORAL_TESTIMONY"),
        "CRT-02-E02": ("九一八事变后", "1931-09-18", "", "RELATIVE", "OPEN_END", "ORAL_TESTIMONY"),
        "CRT-02-E03": ("1933年至1934年12月", "1933", "1934-12", "INTERVAL", "APPROXIMATE", "ORAL_TESTIMONY"),
        "CRT-02-E04": ("1934年12月至1935年以后", "1934-12", "1935", "INTERVAL", "APPROXIMATE", "ORAL_TESTIMONY"),
        "CRT-02-E05": ("1931年至1935年前后", "1931", "1935", "INTERVAL", "APPROXIMATE", "ORAL_TESTIMONY"),
    },
    "YYS-01": {
        "YYS-E01": ("西安事变和平解决后至1937年7月", "1936-12", "1937-07", "INTERVAL", "APPROXIMATE", "ORAL_TESTIMONY"),
        "YYS-E02": ("1937年8月23日前后", "1937-08-23", "1937-08-23", "DAY", "APPROXIMATE", "ORAL_TESTIMONY"),
        "YYS-E03": ("1937年8月23日至24日前后", "1937-08-23", "1937-08-24", "INTERVAL", "APPROXIMATE", "ORAL_TESTIMONY"),
        "YYS-E04": ("1937年8月24日以后", "1937-08-24", "1937-08", "RELATIVE", "APPROXIMATE", "ORAL_TESTIMONY"),
        "YYS-E05": ("1937年8月抵达侯马后", "1937-08", "1937-08", "MONTH", "APPROXIMATE", "ORAL_TESTIMONY"),
        "YYS-E06": ("1937年9月平型关战斗前", "1937-09", "1937-09", "MONTH", "APPROXIMATE", "ORAL_TESTIMONY"),
        "YYS-E07": ("平型关战斗前一至数日", "1937-09", "1937-09", "MONTH", "APPROXIMATE", "ORAL_TESTIMONY"),
    },
}


DEVELOPMENT_NOTE_TARGETS = {
    "CHF-V2-01": [
        {"ref":"2","note_type":"严振衡人物注","annotation_target_type":"ENTITY","annotation_target_id":"PER-YANZHENHENG","source_target_type":"EVENT","source_target_id":"CHF-V2-E01"},
        {"ref":"3","note_type":"蒲锦泉姓名校注","annotation_target_type":"DOCUMENT","annotation_target_id":"CHF-V2-01","source_target_type":"DOCUMENT","source_target_id":"CHF-V2-01"},
        {"ref":"4","note_type":"宫乃泉学历校注","annotation_target_type":"ENTITY","annotation_target_id":"PER-GONGNAIQUAN","source_target_type":"EVENT","source_target_id":"CHF-V2-E03"},
        {"ref":"5","note_type":"啰音医学名词注","annotation_target_type":"ENTITY","annotation_target_id":"TERM-RALES","source_target_type":"EVENT","source_target_id":"CHF-V2-E04"},
        {"ref":"6","note_type":"融合性天花医学名词注","annotation_target_type":"ENTITY","annotation_target_id":"DISEASE-CONFLUENT-SMALLPOX","source_target_type":"EVENT","source_target_id":"CHF-V2-E04"},
        {"ref":"7","note_type":"吴友廉人物注","annotation_target_type":"ENTITY","annotation_target_id":"PER-WUYOULIAN","source_target_type":"EVENT","source_target_id":"CHF-V2-E03"},
        {"ref":"8","note_type":"曾如清人物注","annotation_target_type":"ENTITY","annotation_target_id":"PER-ZENGRUQING","source_target_type":"EVENT","source_target_id":"CHF-V2-E03"},
    ],
    "CHF-V3-01": [
        {"ref":"3","note_type":"张鼎丞人物注","annotation_target_type":"ENTITY","annotation_target_id":"PER-ZHANGDINGCHENG","source_target_type":"EVENT","source_target_id":"CHF-V3-E01"},
        {"ref":"4","note_type":"张云逸籍贯校注","annotation_target_type":"ENTITY","annotation_target_id":"PER-ZHANGYUNYI","source_target_type":"EVENT","source_target_id":"CHF-V3-E01"},
        {"ref":"5","note_type":"张正坤人物注","annotation_target_type":"ENTITY","annotation_target_id":"PER-ZHANGZHENGKUN","source_target_type":"EVENT","source_target_id":"CHF-V3-E01"},
        {"ref":"6","note_type":"陈仁洪人物注","annotation_target_type":"ENTITY","annotation_target_id":"PER-CHENRENHONG","source_target_type":"EVENT","source_target_id":"CHF-V3-E02"},
        {"ref":"8","note_type":"冷欣人物注","annotation_target_type":"ENTITY","annotation_target_id":"PER-LENGXIN","source_target_type":"EVENT","source_target_id":"CHF-V3-E03"},
        {"ref":"11","note_type":"侦察科长史实校注","annotation_target_type":"ENTITY","annotation_target_id":"PER-XIEZHONGLIANG","source_target_type":"EVENT","source_target_id":"CHF-V3-E05"},
    ],
    "CRT-02": [
        {"ref":"2","note_type":"丁惟汾人物注","annotation_target_type":"ENTITY","annotation_target_id":"PER-DINGWEIFEN","source_target_type":"DOCUMENT","source_target_id":"CRT-02"},
        {"ref":"3","note_type":"石友三人物注","annotation_target_type":"ENTITY","annotation_target_id":"PER-SHIYOUSAN","source_target_type":"EVENT","source_target_id":"CRT-02-E01"},
        {"ref":"4","note_type":"何梅协定历史注","annotation_target_type":"ENTITY","annotation_target_id":"EVT-HEMEI","source_target_type":"EVENT","source_target_id":"CRT-02-E04"},
        {"ref":"5","note_type":"何应钦人物注","annotation_target_type":"ENTITY","annotation_target_id":"PER-HEYINGQIN","source_target_type":"EVENT","source_target_id":"CRT-02-E04"},
        {"ref":"6","note_type":"王兴纲人物注","annotation_target_type":"ENTITY","annotation_target_id":"PER-WANGXINGGANG","source_target_type":"EVENT","source_target_id":"CRT-02-E05"},
    ],
    "YYS-01": [
        {"ref":"2","note_type":"张闻天人物注","annotation_target_type":"ENTITY","annotation_target_id":"PER-ZHANGWENTIAN","source_target_type":"EVENT","source_target_id":"YYS-E01"},
        {"ref":"3","note_type":"红军大学史实注","annotation_target_type":"ENTITY","annotation_target_id":"ORG-RED-UNIVERSITY","source_target_type":"EVENT","source_target_id":"YYS-E05"},
    ],
}
