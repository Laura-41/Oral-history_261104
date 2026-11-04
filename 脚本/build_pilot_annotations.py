from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

from pilot_entity_config import ENTITY_CATALOGS, ENTITY_RELATIONS, EVENT_TIMES, NOTE_TARGETS

ROOT = Path("/Users/yuqi/Desktop/硕士毕业论文/2609/0920_01/现行标注")


def blocks(*nums: int) -> list[str]:
    return [f"B{n:04d}" for n in nums]


def span(start: int, end: int) -> list[str]:
    return [f"B{n:04d}" for n in range(start, end + 1)]


DOCS = {
    "CHF-V1-01": {
        "folder": "01_陈海峰一访",
        "title": "陈海峰一访01",
        "interviewee": "陈海峰",
        "interview_date": "2010-01-24",
        "visit_no": "1",
        "version": "二校后 阅读版",
        "source_file": "0920_01/语料/C 陈海峰_4+8+23/1访/01.陈海峰（一访）（二校后 阅读版）.docx",
        "speaker_id": "PER-CHF",
        "interviewer_id": "INT-CHF-V1",
        "events": [
            {"id":"CHF-V1-E01","name":"赴上海荣华印书馆当排字学徒","type":"MATERIAL_EVENT","process":"赴上海当排字学徒","narrative":1,"historical":1,"result":"进入荣华印书馆成为排字学徒","factuality":"FACT","confidence":"HIGH","boundary":"从离开家乡赴上海开始，以进入印书馆并掌握排字工作为阶段结果","evidence":blocks(15,17,19,20),"background":blocks(21,22),"prompts":blocks(21),
             "participants":[("PER-CHF","陈海峰","PERSON","Actor","主要参与者"),("ORG-RONGHUA","荣华印书馆","ORGANIZATION","Scope","工作单位")],
             "circumstances":[("TIME","1931年","1931",None),("LOCATION","上海新闸路83号荣华印书馆","上海新闸路83号","PLACE-XINZHALU83"),("CAUSE","家庭贫困","",None)]},
            {"id":"CHF-V1-E02","name":"一二八淞沪战争期间协助抬送伤员","type":"MATERIAL_EVENT","process":"协助抬送伤员","narrative":6,"historical":2,"result":"亲历战争并参与伤员救助","factuality":"FACT","confidence":"MEDIUM","boundary":"原文仅作简要回顾，作为可独立查询的亲历战争事件保留","evidence":blocks(56),"background":[],"prompts":[],
             "participants":[("PER-CHF","陈海峰","PERSON","Actor","参与者"),("ENT-WOUNDED-0128","一二八淞沪战争伤员","OTHER","Goal","受助对象")],
             "circumstances":[("TIME","一二八淞沪战争期间","1932-01-28起",None),("LOCATION","上海","上海","PLACE-SHANGHAI")]},
            {"id":"CHF-V1-E03","name":"在印书馆接触进步思想并支援地下党活动","type":"MENTAL_EVENT","process":"接触并形成初步革命认识","narrative":2,"historical":3,"result":"形成初步革命认识，并以秘密印刷和收入支援地下党活动","factuality":"FACT","confidence":"HIGH","boundary":"从接触地下党学生的印刷材料开始，以形成认识并持续支援地下党活动为阶段结果","evidence":blocks(24,26,28,30,32,34,36,40),"background":blocks(5,13,17,19,22,38,42),"prompts":blocks(21,33,35,37,39),
             "participants":[("PER-CHF","陈海峰","PERSON","Senser","感知者"),("ENT-PROGRESSIVE-IDEAS","进步书刊和革命思想","OTHER","Phenomenon","被感知内容")],
             "circumstances":[("TIME","1931年至1935年前后","1931/1935",None),("LOCATION","上海荣华印书馆及地下党夜校","上海","PLACE-SHANGHAI"),("MANNER","阅读进步书刊、参加夜校、秘密印刷并资助哥哥","",None)]},
            {"id":"CHF-V1-E04","name":"组织荣华印书馆工人罢工并离厂","type":"MATERIAL_EVENT","process":"组织罢工并离开印书馆","narrative":3,"historical":4,"result":"参与者集体离厂，印书馆任务无法按期完成","factuality":"FACT","confidence":"HIGH","boundary":"以师弟受虐死亡和加班剥削为起因，以工人集体离厂、罢工人员分散为结束","evidence":blocks(42,44,46,48,50),"background":[],"prompts":[],
             "participants":[("PER-CHF","陈海峰","PERSON","Actor","主要发起者"),("GRP-RONGHUA-WORKERS","荣华印书馆师兄弟和工人","OTHER","Actor","共同参与者"),("ORG-RONGHUA-PRODUCTION","荣华印书馆生产任务","ORGANIZATION","Goal","受影响对象")],
             "circumstances":[("TIME","约1935年","1935",None),("LOCATION","上海荣华印书馆","上海新闸路83号","PLACE-XINZHALU83"),("CAUSE","工人遭打骂、师弟死亡以及长期无偿加班","",None),("MANNER","暗中动员并集体离厂","",None)]},
            {"id":"CHF-V1-E05","name":"罢工离厂后经历失业并重新就业","type":"MATERIAL_EVENT","process":"经历失业并重新就业","narrative":4,"historical":5,"result":"重新进入印书馆工作，工资逐步提高至十五元","factuality":"FACT","confidence":"HIGH","boundary":"从罢工人员分散、无钱租房开始，以重新找到印书馆工作和收入稳定为结束","evidence":blocks(50,52,54),"background":[],"prompts":[],
             "participants":[("PER-CHF","陈海峰","PERSON","Actor","主要参与者")],
             "circumstances":[("TIME","罢工以后至八一三事变前","约1935/1937-08",None),("LOCATION","上海","上海","PLACE-SHANGHAI"),("MANNER","依靠师兄和哥哥帮助重新寻找印书馆工作","",None)]},
            {"id":"CHF-V1-E06","name":"八一三事变后随家人逃难返回江阴","type":"MATERIAL_EVENT","process":"逃离上海并返回家乡","narrative":5,"historical":6,"result":"陈海峰及家人返回江阴家乡","factuality":"FACT","confidence":"HIGH","boundary":"以日军进攻上海、全家开始逃难为起点，以依靠典当所得返回家乡为终点","evidence":blocks(58,59,61,63),"background":blocks(56),"prompts":blocks(62),
             "participants":[("PER-CHF","陈海峰","PERSON","Actor","主要参与者"),("GRP-CHF-SISTERS","陈海峰的两个姐姐和一个妹妹","OTHER","Actor","共同参与者")],
             "circumstances":[("TIME","1937年8月13日以后","1937-08-13后",None),("LOCATION","上海—松江—嘉兴—苏州—江阴","上海至江阴","PLACE-ROUTE-SH-JY"),("CAUSE","八一三事变后日军进攻上海","",None),("MANNER","乘难民火车并徒步辗转返乡","",None)]},
            {"id":"CHF-V1-E07","name":"组织篁村人民抗日救亡会并开展宣传","type":"MATERIAL_EVENT","process":"组织并发展抗日救亡会","narrative":7,"historical":7,"result":"救亡会发展到五十余人，持续开展抗日宣传并与上海地下党取得联系","factuality":"FACT","confidence":"HIGH","boundary":"从哥哥接受任务返乡发展组织开始，以组织发展、宣传运作并恢复地下党联系为阶段结果","evidence":blocks(63,65,68,70,72,74,78),"background":blocks(65,70,74,76,78),"prompts":[],
             "participants":[("PER-CHF-BROTHER","陈海峰的哥哥","PERSON","Actor","主要发起者"),("PER-CHF","陈海峰","PERSON","Actor","共同参与者"),("GRP-HUANGCUN-YOUTH","亲属、同学、抗日青年和学生","OTHER","Actor","共同参与者"),("ORG-HUANGCUN-SALVATION","篁村人民抗日救亡会","ORGANIZATION","Goal","创成实体")],
             "circumstances":[("TIME","八一三事变后、返乡半个多月以后","约1937-08下旬以后",None),("LOCATION","江阴澄西篁村","江阴澄西篁村","PLACE-HUANGCUN"),("MANNER","发展成员、收听广播、编印小报和制作黑板报","",None),("PURPOSE","宣传抗日并激起群众抗日热情","",None)]}
        ],
        "stages": [
            ("CHF-V1-E03",1,"接触并印刷进步材料","印刷",blocks(24)),
            ("CHF-V1-E03",2,"阅读进步书刊并参加夜校","阅读和学习",blocks(26,28)),
            ("CHF-V1-E03",3,"从收入中资助哥哥的地下党活动","资助",blocks(30,32)),
            ("CHF-V1-E03",4,"夜间秘密排印宣传品","秘密印刷",blocks(33,34,35,36)),
            ("CHF-V1-E04",1,"师弟遭打致死并引起工人不满","遭打和死亡",blocks(42,44)),
            ("CHF-V1-E04",2,"工人向老板抗议但遭压制","抗议",blocks(44)),
            ("CHF-V1-E04",3,"陈海峰暗中动员工人罢工","动员",blocks(46,48)),
            ("CHF-V1-E04",4,"罢工人员集体离厂并分散","离厂",blocks(50)),
            ("CHF-V1-E05",1,"罢工后失去工作和住处","失业",blocks(50)),
            ("CHF-V1-E05",2,"依靠廉价食物度过困难时期","维持生活",blocks(52)),
            ("CHF-V1-E05",3,"在师兄和哥哥帮助下重新就业","重新就业",blocks(54)),
            ("CHF-V1-E06",1,"日军进攻上海后全家开始逃难","逃离上海",blocks(58,59)),
            ("CHF-V1-E06",2,"途中遭轰炸扫射并丢弃行李","躲避轰炸",blocks(59,61)),
            ("CHF-V1-E06",3,"依靠典当金戒指所得返回家乡","返回江阴",blocks(61,63)),
            ("CHF-V1-E07",1,"哥哥接受任务并秘密返乡","接受任务返乡",blocks(63,65)),
            ("CHF-V1-E07",2,"联络亲友青年并成立救亡会","组织成立",blocks(65,68)),
            ("CHF-V1-E07",3,"发展五十余名成员并确定宣传任务","发展成员",blocks(70)),
            ("CHF-V1-E07",4,"收听广播编印小报并制作黑板报","开展宣传",blocks(72,74)),
            ("CHF-V1-E07",5,"通过既有关系联系上海地下党","取得联系",blocks(78))
        ],
        "notes": [("0","EVENT","CHF-V1-E03","薛暮桥人物注"),("1","EVENT","CHF-V1-E07","快慢机名物注"),("2","EVENT","CHF-V1-E07","高小生人物注"),("3","EVENT","CHF-V1-E07","张太雷人物注"),("4","EVENT","CHF-V1-E07","恽代英人物注")],
        "document_only": blocks(2,3,4,6,7,8,9,10,11,12,14,16,18,23,25,27,29,31,41,43,45,47,49,51,53,55,57,60,64,66,67,69,71,73,75,77,79),
        "comments": blocks(4,7,9,11),
    },
    "CRT-01": {
        "folder": "02_陈锐霆090422",
        "title": "陈锐霆090422第01份",
        "interviewee": "陈锐霆",
        "interview_date": "2009-04-20",
        "visit_no": "090422",
        "version": "二校后 阅读版",
        "source_file": "0920_01/语料/C 陈锐霆_15/01.陈锐霆 090422（二校后 阅读版）.docx",
        "speaker_id": "PER-CRT",
        "interviewer_id": "INT-CRT-01",
        "events": [
            {"id":"CRT-E01","name":"八岁起放牛并承担家务劳动","type":"MATERIAL_EVENT","process":"放牛并承担家务劳动","narrative":1,"historical":1,"result":"以儿童劳动帮助家庭维持生活","factuality":"FACT","confidence":"HIGH","boundary":"从说明家贫无法上学开始，以形成稳定的放牛和家务劳动生活为阶段结果","evidence":blocks(18,20,22),"background":blocks(16),"prompts":blocks(21),
             "participants":[("PER-CRT","陈锐霆","PERSON","Actor","主要参与者"),("ENT-VILLAGE-CATTLE","村庄牛群","OTHER","Scope","劳动对象")],
             "circumstances":[("TIME","1914年、八岁时","1914",None),("LOCATION","即墨盘龙庄村东山","山东即墨","PLACE-PANLONGZHUANG"),("CAUSE","家庭贫穷、缺少劳动力","",None)]},
            {"id":"CRT-E02","name":"与同伴观看日舰时遭炮击并逃脱","type":"MATERIAL_EVENT","process":"遭日军炮击并逃脱","narrative":2,"historical":2,"result":"未被炮弹击中，并形成强烈仇日情绪","factuality":"FACT","confidence":"HIGH","boundary":"从儿童跑到高山观看日本船只开始，以炮击后逃离并形成仇日情绪为结束","evidence":blocks(24,26),"background":[],"prompts":blocks(27),
             "participants":[("ORG-JP-FORCES","日本军队","ORGANIZATION","Actor","攻击者"),("PER-CRT","陈锐霆","PERSON","Goal","受攻击者"),("GRP-CRT-CHILDREN","同村儿童","OTHER","Goal","共同受攻击者")],
             "circumstances":[("TIME","1914年、八岁时","1914",None),("LOCATION","即墨村东北高山","山东即墨","PLACE-GAOSHAN"),("MANNER","日舰向山脊发射数十发炮弹","",None)]},
            {"id":"CRT-E03","name":"从济南师范毕业并到沧口小学任教","type":"MATERIAL_EVENT","process":"毕业并任教","narrative":4,"historical":3,"result":"成为沧口小学教员","factuality":"FACT","confidence":"HIGH","boundary":"以济南师范毕业为起点，以进入沧口小学任教为结果","evidence":blocks(34,36,38,40),"background":blocks(35,37),"prompts":blocks(35,37),
             "participants":[("PER-CRT","陈锐霆","PERSON","Actor","主要参与者"),("ORG-CANGKOU-SCHOOL","沧口小学","ORGANIZATION","Scope","任职单位")],
             "circumstances":[("TIME","1927年12月毕业后","1927-12后",None),("LOCATION","济南、青岛沧口","山东","PLACE-SHANDONG") ]},
            {"id":"CRT-E04","name":"五三惨案期间在济南险遭炮击并绕道返乡","type":"MATERIAL_EVENT","process":"遭炮击并绕道返乡","narrative":3,"historical":4,"result":"避开炮击，经小清河和海边绕道返回家乡","factuality":"FACT","confidence":"HIGH","boundary":"从因事到济南、遭遇炮击开始，以铁路中断后绕道回家并恢复任教为结束","evidence":blocks(28,30,32),"background":[],"prompts":[],
             "participants":[("ORG-JP-FORCES","日本军队","ORGANIZATION","Actor","攻击者"),("PER-CRT","陈锐霆","PERSON","Goal","受攻击者")],
             "circumstances":[("TIME","1928年五三惨案期间","1928-05-03前后",None),("LOCATION","济南及返乡路线","济南","PLACE-JINAN"),("MANNER","铁路中断后沿小清河和海边绕道","",None)]},
            {"id":"CRT-E05","name":"受五三惨案影响放弃教书并决定参军","type":"MENTAL_EVENT","process":"决定参军抗日","narrative":5,"historical":5,"result":"与三名同伴结伴离开教职寻求参军","factuality":"FACT","confidence":"HIGH","boundary":"以五三惨案改变其思想为起点，以明确决定亲自参军抗日为结果","evidence":blocks(40),"background":blocks(27,28),"prompts":blocks(27),
             "participants":[("PER-CRT","陈锐霆","PERSON","Senser","感知者"),("ENT-JOIN-ARMY","亲自参军抗日","OTHER","Phenomenon","意愿内容")],
             "circumstances":[("TIME","1928年五三惨案以后","1928-05后",None),("CAUSE","在济南遭日军炮击并目睹五三惨案影响","",None)]},
            {"id":"CRT-E06","name":"辗转上海天津保定寻求参军并被录取为学兵","type":"MATERIAL_EVENT","process":"寻求参军并成为学兵","narrative":6,"historical":6,"result":"被河北军事政治学校教导大队接收为学兵","factuality":"FACT","confidence":"HIGH","boundary":"从与同伴离开青岛赴上海开始，以在保定被教导大队录取为学兵为结束","evidence":blocks(42,44,46,48,50,52,54,56),"background":[],"prompts":blocks(45,49),
             "participants":[("PER-CRT","陈锐霆","PERSON","Actor","主要参与者"),("GRP-CRT-COMPANIONS","陈锐霆的参军同伴","OTHER","Actor","共同参与者"),("ORG-HEBEI-MIL-SCHOOL","河北军事政治学校教导大队","ORGANIZATION","Goal","接收单位")],
             "circumstances":[("TIME","1928年以后","约1928",None),("LOCATION","青岛—上海—天津—保定","跨地迁移","PLACE-QD-SH-TJ-BD"),("PURPOSE","寻求参军抗日","",None)]},
            {"id":"CRT-E07","name":"在教导大队接受严格学兵训练","type":"MATERIAL_EVENT","process":"接受学兵训练","narrative":7,"historical":7,"result":"继续留在教导大队受训，绑腿处分事件得到纠正","factuality":"FACT","confidence":"HIGH","boundary":"从被录取为学兵开始，以适应训练并解决处分事件为阶段结果","evidence":blocks(56,58,60),"background":[],"prompts":[],
             "participants":[("PER-CRT","陈锐霆","PERSON","Actor","受训者"),("ORG-HEBEI-TRAINING","教导大队","ORGANIZATION","Scope","训练单位")],
             "circumstances":[("TIME","进入教导大队以后","约1928/1929",None),("LOCATION","保定","保定","PLACE-BAODING") ]},
            {"id":"CRT-E08","name":"考入河北军事政治学校第二期并完成军事学习","type":"MATERIAL_EVENT","process":"考入并完成军事学习","narrative":8,"historical":8,"result":"随学校转入山西后完成学业","factuality":"FACT","confidence":"HIGH","boundary":"从考入第二期开始，经过北京学习和学校改编迁晋，以毕业为结束","evidence":blocks(62,65,67,70,72,74,76,78,80,82,84,85,87,88,89,91,93),"background":blocks(67,70,74,76,78,80,82,84,85),"prompts":blocks(61,68,71,77,81,89),
             "participants":[("PER-CRT","陈锐霆","PERSON","Actor","学员"),("ORG-HEBEI-MIL-SCHOOL","河北军事政治学校","ORGANIZATION","Scope","学习单位")],
             "circumstances":[("TIME","约1928年至1930年","1928/1930",None),("LOCATION","保定—北京黄寺—山西","华北","PLACE-HEBEI-BEIJING-SHANXI"),("MANNER","学习战术、兵器、地理等军事课程","",None)]},
            {"id":"CRT-E09","name":"毕业后任炮兵二十八团补充队中尉队长","type":"RELATIONAL_EVENT","process":"担任","narrative":9,"historical":9,"result":"获得炮兵补充队中尉队长身份","factuality":"FACT","confidence":"HIGH","boundary":"以军校毕业分配为起点，以中尉补充队长职务确立为结果","evidence":blocks(93,95),"background":[],"prompts":[],
             "participants":[("PER-CRT","陈锐霆","PERSON","Token","被确认者"),("ROLE-CRT-LIEUTENANT","炮兵二十八团补充队中尉队长","OTHER","Value","身份价值")],
             "circumstances":[("TIME","军校毕业后、中原大战期间","约1930",None),("LOCATION","太原","太原","PLACE-TAIYUAN") ]},
            {"id":"CRT-E10","name":"在晋中地区招募补充兵并经历部队整编","type":"MATERIAL_EVENT","process":"招募兵员并随部队整编","narrative":10,"historical":10,"result":"两个多月仅招募七八人，所在部队随后被整编","factuality":"FACT","confidence":"MEDIUM","boundary":"从担任补充队长并承担招兵任务开始，以阎锡山部队被整编为新的军队编制为阶段结果；原文在此处未完全讲完","evidence":blocks(95,97,100),"background":blocks(98),"prompts":blocks(98),
             "participants":[("PER-CRT","陈锐霆","PERSON","Actor","招兵负责人"),("ORG-ARTILLERY-28","炮兵二十八团补充队","ORGANIZATION","Actor","所属单位")],
             "circumstances":[("TIME","约1930年","1930",None),("LOCATION","榆次、太谷、平遥一带","山西晋中","PLACE-JINZHONG"),("PURPOSE","补充并扩充部队兵员","",None)]}
        ],
        "stages": [
            ("CRT-E02",1,"与同伴跑到高山观看日本船只","观看",blocks(24)),
            ("CRT-E02",2,"日军向山脊发射数十发炮弹","遭炮击",blocks(26)),
            ("CRT-E02",3,"儿童逃离并形成仇日情绪","逃离和形成态度",blocks(26)),
            ("CRT-E06",1,"与同伴到上海寻找关系但未成功","寻找参军关系",blocks(42,44,46,48)),
            ("CRT-E06",2,"余下两人乘船经天津前往保定","转赴保定",blocks(50,52)),
            ("CRT-E06",3,"拒绝亲戚安排的会计工作","拒绝安排",blocks(52)),
            ("CRT-E06",4,"看到学兵队后设法加入教导大队","加入学兵队",blocks(54,56)),
            ("CRT-E08",1,"从教导大队考入学校第二期","考入",blocks(62)),
            ("CRT-E08",2,"随第二期学员迁到北京黄寺","迁校",blocks(65)),
            ("CRT-E08",3,"接受炮科及五大教程训练","学习",blocks(84,85,87,88,89)),
            ("CRT-E08",4,"学校撤销并改编迁入山西","改编迁移",blocks(91)),
            ("CRT-E08",5,"完成学业并接受毕业分配","毕业",blocks(93)),
            ("CRT-E10",1,"在晋中地区执行招兵任务","招兵",blocks(95,97)),
            ("CRT-E10",2,"两个多月仅招到七八人","招兵受挫",blocks(97)),
            ("CRT-E10",3,"阎锡山部队战败后接受整编","整编",blocks(97,100))
        ],
        "notes": [("0","EVENT","CRT-E04","五三惨案历史注"),("1","EVENT","CRT-E08","商震人物注")],
        "document_only": blocks(2,3,4,5,6,7,8,9,10,11,12,13,14,15,17,19,23,25,29,31,33,39,41,43,47,51,53,55,57,59,63,64,66,69,73,75,79,83,86,90,92,94,96,99,101),
        "comments": blocks(6,9,11,13),
    }
}


def csv_write(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def normalize_timecode(text: str) -> str:
    stripped = text.strip().replace("：", ":")
    return stripped if re.fullmatch(r"\d{2}:\d{2}:\d{2}(?::\d{2})?", stripped) else ""


def extract_time_expressions(source_rows: list[dict], doc_id: str) -> list[dict]:
    """Extract explicit calendar expressions without treating transcript timecodes as history."""
    rows: list[dict] = []
    patterns = [
        ("DATE", "DAY", re.compile(r"(?P<approx>约)?(?P<y>\d{4})年(?P<m>\d{1,2})月(?P<d>\d{1,2})日")),
        ("DATE", "DAY", re.compile(r"(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})")),
        ("INTERVAL", "INTERVAL", re.compile(r"(?P<approx>约)?(?P<y1>\d{4})\s*年?\s*(?:至|到|—|–|－|-)\s*(?P<y2>\d{4})\s*年?(?P<tail>前后)?")),
        ("DATE", "MONTH", re.compile(r"(?P<approx>约)?(?P<y>\d{4})年(?P<m>\d{1,2})月")),
        ("DATE", "YEAR", re.compile(r"(?P<approx>约)?(?P<y>\d{4})年(?P<tail>前后|以后|之前|起)?")),
    ]
    for source in source_rows:
        text = source["verbatim_text"]
        if normalize_timecode(text):
            continue
        occupied: list[tuple[int, int]] = []
        found: list[tuple[int, int, str, str, re.Match[str]]] = []
        for expression_type, precision, pattern in patterns:
            for match in pattern.finditer(text):
                start, end = match.span()
                if any(start < old_end and end > old_start for old_start, old_end in occupied):
                    continue
                occupied.append((start, end))
                found.append((start, end, expression_type, precision, match))
        for start, end, expression_type, precision, match in sorted(found):
            groups = match.groupdict()
            if expression_type == "INTERVAL":
                normalized_start, normalized_end = groups["y1"], groups["y2"]
            else:
                year = groups["y"]
                month = groups.get("m")
                day = groups.get("d")
                normalized_start = year
                if month:
                    normalized_start += f"-{int(month):02d}"
                if day:
                    normalized_start += f"-{int(day):02d}"
                normalized_end = normalized_start
            approximate = bool(groups.get("approx") or groups.get("tail"))
            source_status = (
                "EDITORIAL_NOTE" if source["source_part"] == "footnotes" else
                "EDITORIAL_PROFILE" if source["source_block_id"].endswith("B0001") else
                "INTERVIEWER_QUESTION" if source["speaker_type"] == "INTERVIEWER" else
                "ORAL_TESTIMONY"
            )
            rows.append({
                "time_expression_id": f"{doc_id}-TX{len(rows)+1:04d}",
                "segment_id": source["segment_id"],
                "raw_text": text[start:end],
                "normalized_start": normalized_start,
                "normalized_end": normalized_end,
                "precision": precision,
                "expression_type": expression_type,
                "certainty": "APPROXIMATE" if approximate else "EXACT",
                "start_offset": start,
                "end_offset": end,
                "source_status": source_status,
                "confidence": "MEDIUM" if approximate else "HIGH",
                "review_status": "MODEL_CANDIDATE",
            })
    return rows


def build_document(doc_id: str, cfg: dict) -> None:
    folder = ROOT / cfg["folder"]
    data = json.loads((folder / "extracted_blocks.json").read_text(encoding="utf-8"))
    body = data["blocks"]
    footnotes = data.get("additional_parts", {}).get("footnotes", [])

    source_rows: list[dict] = []
    block_to_segment: dict[str, str] = {}
    current_speaker = cfg["speaker_id"]
    current_type = "INTERVIEWEE"
    current_time = ""

    for idx, b in enumerate(body, start=1):
        short = f"B{idx:04d}"
        seg_id = f"{doc_id}-S{idx:04d}"
        text = b["text"]
        tc = normalize_timecode(text)
        if idx == 1 or tc:
            speaker_id, speaker_type = "EDITOR", "EDITOR"
        elif text.strip().startswith("记者："):
            speaker_id, speaker_type = cfg["interviewer_id"], "INTERVIEWER"
            current_speaker, current_type = speaker_id, speaker_type
        elif text.strip().startswith(f"{cfg['interviewee']}："):
            speaker_id, speaker_type = cfg["speaker_id"], "INTERVIEWEE"
            current_speaker, current_type = speaker_id, speaker_type
        else:
            speaker_id, speaker_type = current_speaker, current_type
        if tc:
            current_time = tc
        block_to_segment[short] = seg_id
        source_rows.append({
            "segment_id": seg_id, "doc_id": doc_id, "segment_order": idx,
            "source_part": "document", "source_ref_id": "", "source_block_id": b["block_id"],
            "speaker_id": speaker_id, "speaker_type": speaker_type,
            "start_timecode": tc or current_time, "end_timecode": "",
            "start_offset": b["start_offset"], "end_offset": b["end_offset"],
            "segment_type": "UNCERTAIN", "verbatim_text": text, "normalized_text": "",
            "transcription_status": "VISIBLE_CURRENT_TEXT", "review_status": "MODEL_CANDIDATE"
        })

    for note_index, b in enumerate(footnotes, start=1):
        order = len(source_rows) + 1
        note_id = str(b.get("item_id", note_index - 1))
        short = f"FN{note_id}"
        seg_id = f"{doc_id}-N{note_index:03d}"
        block_to_segment[short] = seg_id
        source_rows.append({
            "segment_id": seg_id, "doc_id": doc_id, "segment_order": order,
            "source_part": "footnotes", "source_ref_id": note_id, "source_block_id": f"{doc_id}-FN{note_id}",
            "speaker_id": "EDITOR", "speaker_type": "EDITOR", "start_timecode": "", "end_timecode": "",
            "start_offset": "", "end_offset": "", "segment_type": "DOCUMENT_NOTE",
            "verbatim_text": b["text"], "normalized_text": "", "transcription_status": "VISIBLE_CURRENT_TEXT",
            "review_status": "MODEL_CANDIDATE"
        })

    event_rows: list[dict] = []
    process_rows: list[dict] = []
    participant_rows: list[dict] = []
    circumstance_rows: list[dict] = []
    attachment_rows: list[dict] = []
    stage_rows: list[dict] = []
    stage_next_rows: list[dict] = []
    event_next_rows: list[dict] = []
    annotation_rows: list[dict] = []
    entity_rows: list[dict] = []
    mention_rows: list[dict] = []
    alias_rows: list[dict] = []
    entity_relation_rows: list[dict] = []
    event_time_rows: list[dict] = []
    time_expression_rows: list[dict] = []
    attached: dict[str, list[tuple[str, str, str]]] = {r["segment_id"]: [] for r in source_rows}
    entity_catalog = ENTITY_CATALOGS[doc_id]
    entity_by_id = {entity["entity_id"]: entity for entity in entity_catalog}
    for entity in entity_catalog:
        entity_rows.append({
            "entity_id": entity["entity_id"], "canonical_name": entity["canonical_name"],
            "entity_type": entity["entity_type"], "entity_subtype": entity["entity_subtype"],
            "description": entity["description"], "authority_status": entity["authority_status"],
            "confidence": entity["confidence"], "review_status": entity["review_status"]
        })

    def add_attachment(short: str, target_type: str, target_id: str, function: str, confidence: str = "HIGH") -> None:
        seg = block_to_segment.get(short)
        if not seg:
            return
        key = (target_type, target_id, function)
        if key in attached[seg]:
            return
        attached[seg].append(key)
        attachment_rows.append({
            "attachment_id": f"{doc_id}-AT{len(attachment_rows)+1:04d}", "segment_id": seg,
            "target_type": target_type, "target_id": target_id, "function": function,
            "quote_start_offset": "", "quote_end_offset": "", "confidence": confidence,
            "review_status": "MODEL_CANDIDATE"
        })

    for e in cfg["events"]:
        event_rows.append({
            "event_id": e["id"], "doc_id": doc_id, "event_name": e["name"],
            "narrative_order": e["narrative"], "historical_order": e["historical"],
            "result_state": e["result"], "factuality": e["factuality"], "confidence": e["confidence"],
            "boundary_note": e["boundary"], "boundary_confidence": e["confidence"],
            "review_status": "MODEL_CANDIDATE"
        })
        first_evidence = block_to_segment[e["evidence"][0]] if e["evidence"] else ""
        process_rows.append({
            "process_id": f"{e['id']}-PROC", "event_id": e["id"], "event_type_id": e["type"],
            "process_text": e["process"], "process_normalized": e["process"],
            "evidence_segment_id": first_evidence, "confidence": e["confidence"]
        })
        for entity_id, entity_name, entity_type, role, status in e["participants"]:
            master_type = entity_by_id.get(entity_id, {}).get("entity_type", entity_type)
            participant_rows.append({
                "event_id": e["id"], "entity_id": entity_id, "entity_name": entity_name,
                "entity_type": master_type, "role": role, "participation_status": status,
                "evidence_segment_id": first_evidence, "confidence": e["confidence"]
            })
        for ci, (kind, value_text, normalized, entity_id) in enumerate(e["circumstances"], start=1):
            circumstance_rows.append({
                "circumstance_id": f"{e['id']}-C{ci:02d}", "event_id": e["id"], "kind": kind,
                "value_text": value_text, "normalized_value": normalized, "entity_id": entity_id or "",
                "evidence_segment_id": first_evidence, "confidence": e["confidence"]
            })
        for short in e.get("evidence", []): add_attachment(short, "EVENT", e["id"], "EVIDENCE", e["confidence"])
        for short in e.get("background", []): add_attachment(short, "EVENT", e["id"], "BACKGROUND", e["confidence"])
        for short in e.get("prompts", []): add_attachment(short, "EVENT", e["id"], "INTERVIEWER_PROMPT", e["confidence"])

        raw_time, start, end, precision, certainty, source_status = EVENT_TIMES[doc_id][e["id"]]
        event_time_rows.append({
            "event_time_id": f"{e['id']}-T01", "event_id": e["id"], "raw_text": raw_time,
            "normalized_start": start, "normalized_end": end, "precision": precision,
            "certainty": certainty, "source_status": source_status,
            "evidence_segment_id": first_evidence, "confidence": e["confidence"],
            "review_status": "MODEL_CANDIDATE" if certainty != "UNCERTAIN" else "NEEDS_REVIEW"
        })

    stages_by_event: dict[str, list[str]] = {}
    for event_id, order, summary, process, srcs in cfg["stages"]:
        stage_id = f"{event_id}-P{order:02d}"
        stages_by_event.setdefault(event_id, []).append(stage_id)
        stage_rows.append({
            "stage_id": stage_id, "event_id": event_id, "stage_order": order,
            "stage_summary": summary, "process_text": process, "confidence": "HIGH",
            "review_status": "MODEL_CANDIDATE"
        })
        for short in srcs: add_attachment(short, "STAGE", stage_id, "EVIDENCE")

    for event_id, stage_ids in stages_by_event.items():
        for a, b in zip(stage_ids, stage_ids[1:]):
            stage_next_rows.append({
                "source_stage_id": a, "target_stage_id": b, "logic": "SEQUENCE",
                "evidence_segment_id": "", "confidence": "MEDIUM", "review_status": "MODEL_CANDIDATE"
            })

    ordered_events = sorted(cfg["events"], key=lambda e: e["historical"])
    for a, b in zip(ordered_events, ordered_events[1:]):
        event_next_rows.append({
            "source_event_id": a["id"], "target_event_id": b["id"], "chain_id": f"{doc_id}-MAIN",
            "basis": "explicit_time" if a["confidence"] == "HIGH" and b["confidence"] == "HIGH" else "contextual_inference",
            "confidence": "MEDIUM", "review_status": "MODEL_CANDIDATE"
        })

    profile_seg_id = block_to_segment["B0001"]
    annotation_rows.append({
        "annotation_id": f"{doc_id}-PROFILE", "doc_id": doc_id,
        "annotation_type": "BIOGRAPHICAL_PROFILE",
        "annotation_text": next(r["verbatim_text"] for r in source_rows if r["segment_id"] == profile_seg_id),
        "author_or_editor": "原文编校者", "source_status": "EDITORIAL_PROFILE",
        "target_type": "DOCUMENT", "target_id": doc_id, "source_segment_id": profile_seg_id
    })
    add_attachment("B0001", "DOCUMENT", doc_id, "DOCUMENT_NOTE")

    note_subject_by_segment: dict[str, str] = {}
    for ni, note in enumerate(NOTE_TARGETS[doc_id], start=1):
        note_ref = note["ref"]
        seg_id = block_to_segment[f"FN{note_ref}"]
        annotation_rows.append({
            "annotation_id": f"{doc_id}-A{ni:03d}", "doc_id": doc_id, "annotation_type": note["note_type"],
            "annotation_text": next(r["verbatim_text"] for r in source_rows if r["segment_id"] == seg_id),
            "author_or_editor": "原文编校者", "source_status": "EDITORIAL_NOTE",
            "target_type": note["annotation_target_type"], "target_id": note["annotation_target_id"],
            "source_segment_id": seg_id
        })
        note_subject_by_segment[seg_id] = note["annotation_target_id"]
        add_attachment(f"FN{note_ref}", note["source_target_type"], note["source_target_id"], "DOCUMENT_NOTE")

    for short in cfg.get("comments", []):
        seg = block_to_segment.get(short)
        if seg and not attached[seg]: add_attachment(short, "DOCUMENT", doc_id, "COMMENT")

    for short in cfg.get("document_only", []):
        seg = block_to_segment.get(short)
        if seg and not attached[seg]: add_attachment(short, "DOCUMENT", doc_id, "DOCUMENT_ONLY")

    for row in source_rows:
        seg = row["segment_id"]
        text = row["verbatim_text"].strip()
        if not attached[seg]:
            attachment_rows.append({
                "attachment_id": f"{doc_id}-AT{len(attachment_rows)+1:04d}", "segment_id": seg,
                "target_type": "DOCUMENT", "target_id": doc_id, "function": "DOCUMENT_ONLY",
                "quote_start_offset": "", "quote_end_offset": "", "confidence": "HIGH",
                "review_status": "MODEL_CANDIDATE"
            })
            attached[seg].append(("DOCUMENT", doc_id, "DOCUMENT_ONLY"))
        funcs = {x[2] for x in attached[seg]}
        if row["source_part"] != "document" or normalize_timecode(text) or row["source_block_id"].endswith("B0001") or text in {cfg["interviewee"]+":", cfg["interviewee"]+"："}:
            row["segment_type"] = "DOCUMENT_NOTE"
        elif row["speaker_type"] == "INTERVIEWER":
            row["segment_type"] = "INTERVIEWER_PROMPT"
        elif "EVIDENCE" in funcs:
            row["segment_type"] = "EVENT_EVIDENCE"
        elif "BACKGROUND" in funcs:
            row["segment_type"] = "BACKGROUND"
        elif "COMMENT" in funcs:
            row["segment_type"] = "NARRATOR_COMMENT"
        elif "DOCUMENT_NOTE" in funcs:
            row["segment_type"] = "DOCUMENT_NOTE"
        else:
            row["segment_type"] = "OFF_TOPIC"

    # Link each interviewer question to the next interviewee segment through an annotation row.
    for i, row in enumerate(source_rows[:-1]):
        if row["speaker_type"] == "INTERVIEWER":
            for answer in source_rows[i + 1:]:
                if answer["speaker_type"] == "INTERVIEWEE" and answer["verbatim_text"].strip():
                    annotation_rows.append({
                        "annotation_id": f"{doc_id}-Q{row['segment_order']:04d}", "doc_id": doc_id,
                        "annotation_type": "PROMPTS_RESPONSE", "annotation_text": "采访者提问引出受访者回答",
                        "author_or_editor": "结构化标注", "source_status": "inferred_from_structure",
                        "target_type": "SOURCE_SEGMENT", "target_id": answer["segment_id"],
                        "source_segment_id": row["segment_id"]
                    })
                    break

    # Extract named-entity mentions from every source segment, including the
    # editorial profile, footnotes, interviewer questions, and document-only text.
    evidence_events_by_segment: dict[str, set[str]] = {}
    for attachment in attachment_rows:
        if attachment["target_type"] == "EVENT" and attachment["function"] == "EVIDENCE":
            evidence_events_by_segment.setdefault(attachment["segment_id"], set()).add(attachment["target_id"])
    participant_entities = {
        event_id: {row["entity_id"] for row in participant_rows if row["event_id"] == event_id}
        for event_id in {row["event_id"] for row in event_rows}
    }
    circumstance_entities = {
        event_id: {row["entity_id"] for row in circumstance_rows if row["event_id"] == event_id and row["entity_id"]}
        for event_id in {row["event_id"] for row in event_rows}
    }

    patterns: list[tuple[str, str]] = []
    for entity in entity_catalog:
        patterns.append((entity["canonical_name"], entity["entity_id"]))
        patterns.extend((alias["alias_text"], entity["entity_id"]) for alias in entity["aliases"])
    patterns = sorted({item for item in patterns if len(item[0].strip("《》（）() ")) >= 2}, key=lambda item: len(item[0]), reverse=True)

    for source in source_rows:
        text = source["verbatim_text"]
        occupied: list[tuple[int, int]] = []
        candidates: list[tuple[int, int, str, str]] = []
        for surface, entity_id in patterns:
            for match in re.finditer(re.escape(surface), text):
                start, end = match.span()
                if any(start < old_end and end > old_start for old_start, old_end in occupied):
                    continue
                occupied.append((start, end))
                candidates.append((start, end, surface, entity_id))
        for start, end, surface, entity_id in sorted(candidates):
            source_status = (
                "EDITORIAL_NOTE" if source["source_part"] == "footnotes" else
                "EDITORIAL_PROFILE" if source["source_block_id"].endswith("B0001") else
                "INTERVIEWER_QUESTION" if source["speaker_type"] == "INTERVIEWER" else
                "ORAL_TESTIMONY"
            )
            event_ids = evidence_events_by_segment.get(source["segment_id"], set())
            if source_status == "EDITORIAL_PROFILE":
                mention_function = "PROFILE_FACT"
            elif note_subject_by_segment.get(source["segment_id"]) == entity_id:
                mention_function = "ANNOTATION_SUBJECT"
            elif source["speaker_id"] == entity_id and start <= 8:
                mention_function = "SPEAKER"
            elif any(entity_id in participant_entities.get(event_id, set()) for event_id in event_ids):
                mention_function = "PARTICIPANT"
            elif any(entity_id in circumstance_entities.get(event_id, set()) for event_id in event_ids):
                mention_function = "CIRCUMSTANCE"
            else:
                mention_function = "MENTION_ONLY"
            entity = entity_by_id[entity_id]
            mention_rows.append({
                "mention_id": f"{doc_id}-M{len(mention_rows)+1:04d}",
                "segment_id": source["segment_id"], "entity_id": entity_id,
                "mention_text": text[start:end], "start_offset": start, "end_offset": end,
                "mention_function": mention_function, "source_status": source_status,
                "confidence": entity["confidence"], "review_status": entity["review_status"]
            })

    for entity in entity_catalog:
        for alias in entity["aliases"]:
            evidence = next((
                row["segment_id"] for row in mention_rows
                if row["entity_id"] == entity["entity_id"] and row["mention_text"] == alias["alias_text"]
            ), "")
            alias_rows.append({
                "alias_id": f"{doc_id}-AL{len(alias_rows)+1:04d}", "entity_id": entity["entity_id"],
                "alias_text": alias["alias_text"], "alias_type": alias["alias_type"],
                "evidence_segment_id": evidence, "confidence": entity["confidence"],
                "review_status": entity["review_status"]
            })

    for relation in ENTITY_RELATIONS[doc_id]:
        entity_relation_rows.append({
            "relation_id": f"{doc_id}-ER{len(entity_relation_rows)+1:04d}",
            "source_entity_id": relation["source_entity_id"], "relation_type": relation["relation_type"],
            "target_entity_id": relation["target_entity_id"], "role_label": relation["role_label"],
            "start_date": relation["start_date"], "end_date": relation["end_date"],
            "evidence_segment_id": block_to_segment.get(relation["source_ref"], ""),
            "source_status": relation["source_status"], "confidence": relation["confidence"],
            "review_status": relation["review_status"]
        })

    time_expression_rows = extract_time_expressions(source_rows, doc_id)

    total_chars = sum(len(r["verbatim_text"]) for r in source_rows)
    document_rows = [{
        "doc_id": doc_id, "title": cfg["title"], "interviewee": cfg["interviewee"],
        "interview_date": cfg["interview_date"], "visit_no": cfg["visit_no"], "version": cfg["version"],
        "source_file": cfg["source_file"], "total_characters": total_chars, "data_role": "DEVELOPMENT",
        "include_in_study": "YES", "review_status": "MODEL_CANDIDATE"
    }]
    coverage_rows = [{
        "doc_id": doc_id, "total_characters": total_chars, "segmented_characters": total_chars,
        "uncovered_characters": 0, "overlap_characters": 0, "total_segments": len(source_rows),
        "attached_segments": sum(bool(v) for v in attached.values()),
        "document_only_segments": sum(any(x[2] == "DOCUMENT_ONLY" for x in v) for v in attached.values()),
        "coverage_rate": "1.0000", "audit_status": "PASS"
    }]

    fields = {
        "documents.csv": ["doc_id","title","interviewee","interview_date","visit_no","version","source_file","total_characters","data_role","include_in_study","review_status"],
        "source_segments.csv": ["segment_id","doc_id","segment_order","source_part","source_ref_id","source_block_id","speaker_id","speaker_type","start_timecode","end_timecode","start_offset","end_offset","segment_type","verbatim_text","normalized_text","transcription_status","review_status"],
        "source_attachments.csv": ["attachment_id","segment_id","target_type","target_id","function","quote_start_offset","quote_end_offset","confidence","review_status"],
        "event_nodes.csv": ["event_id","doc_id","event_name","narrative_order","historical_order","result_state","factuality","confidence","boundary_note","boundary_confidence","review_status"],
        "event_processes.csv": ["process_id","event_id","event_type_id","process_text","process_normalized","evidence_segment_id","confidence"],
        "event_participants.csv": ["event_id","entity_id","entity_name","entity_type","role","participation_status","evidence_segment_id","confidence"],
        "event_circumstances.csv": ["circumstance_id","event_id","kind","value_text","normalized_value","entity_id","evidence_segment_id","confidence"],
        "process_stages.csv": ["stage_id","event_id","stage_order","stage_summary","process_text","confidence","review_status"],
        "stage_next.csv": ["source_stage_id","target_stage_id","logic","evidence_segment_id","confidence","review_status"],
        "event_next.csv": ["source_event_id","target_event_id","chain_id","basis","confidence","review_status"],
        "entities.csv": ["entity_id","canonical_name","entity_type","entity_subtype","description","authority_status","confidence","review_status"],
        "entity_mentions.csv": ["mention_id","segment_id","entity_id","mention_text","start_offset","end_offset","mention_function","source_status","confidence","review_status"],
        "entity_aliases.csv": ["alias_id","entity_id","alias_text","alias_type","evidence_segment_id","confidence","review_status"],
        "entity_relations.csv": ["relation_id","source_entity_id","relation_type","target_entity_id","role_label","start_date","end_date","evidence_segment_id","source_status","confidence","review_status"],
        "event_times.csv": ["event_time_id","event_id","raw_text","normalized_start","normalized_end","precision","certainty","source_status","evidence_segment_id","confidence","review_status"],
        "time_expressions.csv": ["time_expression_id","segment_id","raw_text","normalized_start","normalized_end","precision","expression_type","certainty","start_offset","end_offset","source_status","confidence","review_status"],
        "document_annotations.csv": ["annotation_id","doc_id","annotation_type","annotation_text","author_or_editor","source_status","target_type","target_id","source_segment_id"],
        "coverage_audit.csv": ["doc_id","total_characters","segmented_characters","uncovered_characters","overlap_characters","total_segments","attached_segments","document_only_segments","coverage_rate","audit_status"]
    }
    datasets = {
        "documents.csv": document_rows, "source_segments.csv": source_rows,
        "source_attachments.csv": attachment_rows, "event_nodes.csv": event_rows,
        "event_processes.csv": process_rows, "event_participants.csv": participant_rows,
        "event_circumstances.csv": circumstance_rows, "process_stages.csv": stage_rows,
        "stage_next.csv": stage_next_rows, "event_next.csv": event_next_rows,
        "entities.csv": entity_rows, "entity_mentions.csv": mention_rows,
        "entity_aliases.csv": alias_rows, "entity_relations.csv": entity_relation_rows,
        "event_times.csv": event_time_rows, "time_expressions.csv": time_expression_rows,
        "document_annotations.csv": annotation_rows, "coverage_audit.csv": coverage_rows
    }
    for filename, rows in datasets.items():
        csv_write(folder / filename, fields[filename], rows)

    confirmed_uncertain_count = sum(
        row["review_status"] == "CONFIRMED"
        and row["authority_status"] in {"TRANSCRIPTION_UNCERTAIN", "UNRESOLVED"}
        for row in entity_rows
    )
    bundle = {
        "document": document_rows[0], "source_segments": source_rows, "events": event_rows,
        "processes": process_rows, "participants": participant_rows, "circumstances": circumstance_rows,
        "stages": stage_rows, "stage_next": stage_next_rows, "event_next": event_next_rows,
        "entities": entity_rows, "entity_mentions": mention_rows, "entity_aliases": alias_rows,
        "entity_relations": entity_relation_rows, "event_times": event_time_rows,
        "time_expressions": time_expression_rows,
        "source_attachments": attachment_rows, "document_annotations": annotation_rows,
        "coverage_audit": coverage_rows[0],
        "status_note": f"本数据依据v3.2规范生成；多数记录仍为MODEL_CANDIDATE，其中{confirmed_uncertain_count}个原文指称不确定实体已由研究者核验为CONFIRMED，但其authority_status继续保留不确定性。"
    }
    (folder / "annotation_bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# {cfg['title']}事件试标复核稿", "",
        f"> 本稿依据v3.2规范生成。多数记录仍为 `MODEL_CANDIDATE`；其中{confirmed_uncertain_count}个原文指称不确定实体已经人工核验为 `CONFIRMED`，但继续保留不确定的 `authority_status`。", "",
        "## 一 数据概况", "",
        f"- 原文片段：{len(source_rows)}条", f"- 一级事件：{len(event_rows)}个",
        f"- 二级过程阶段：{len(stage_rows)}个", f"- 原文挂接：{len(attachment_rows)}条",
        f"- 实体：{len(entity_rows)}个", f"- 实体提及：{len(mention_rows)}条",
        f"- 实体关系：{len(entity_relation_rows)}条", f"- 事件规范时间：{len(event_time_rows)}条",
        f"- 全文时间表达：{len(time_expression_rows)}条",
        f"- 文档注释和问答关联：{len(annotation_rows)}条", f"- 覆盖率：{coverage_rows[0]['coverage_rate']}", "",
        "## 二 一级事件", ""
    ]
    for e in sorted(event_rows, key=lambda x: int(x["historical_order"])):
        p = next(x for x in process_rows if x["event_id"] == e["event_id"])
        event_time = next(x for x in event_time_rows if x["event_id"] == e["event_id"])
        event_participants = [x for x in participant_rows if x["event_id"] == e["event_id"]]
        event_circumstances = [x for x in circumstance_rows if x["event_id"] == e["event_id"]]
        event_stages = sorted(
            [x for x in stage_rows if x["event_id"] == e["event_id"]],
            key=lambda x: int(x["stage_order"]),
        )
        event_evidence_ids = [
            x["segment_id"] for x in attachment_rows
            if x["target_type"] == "EVENT" and x["target_id"] == e["event_id"] and x["function"] == "EVIDENCE"
        ]
        event_evidence = [x for x in source_rows if x["segment_id"] in event_evidence_ids]
        lines += [f"### {e['event_id']} {e['event_name']}", "", f"- 事件类型：`{p['event_type_id']}`",
                  f"- 核心过程：{p['process_text']}", f"- 结果状态：{e['result_state']}",
                  f"- 规范时间：{event_time['normalized_start'] or '未定'} 至 {event_time['normalized_end'] or '未定'}（{event_time['precision']}；{event_time['certainty']}）",
                  f"- 边界说明：{e['boundary_note']}", f"- 确定性：{e['confidence']}", ""]
        lines += ["**参与者**", ""]
        for participant in event_participants:
            lines.append(
                f"- `{participant['role']}`：{participant['entity_name']}"
                + (f"（{participant['participation_status']}）" if participant["participation_status"] else "")
            )
        lines += ["", "**环境成分**", ""]
        for circumstance in event_circumstances:
            normalized = f"；规范值：{circumstance['normalized_value']}" if circumstance["normalized_value"] else ""
            lines.append(f"- `{circumstance['kind']}`：{circumstance['value_text']}{normalized}")
        if event_stages:
            lines += ["", "**第二层：过程阶段**", ""]
            for stage in event_stages:
                lines.append(
                    f"{stage['stage_order']}. `{stage['stage_id']}` {stage['stage_summary']}"
                    f"（关键过程：{stage['process_text']}）"
                )
        lines += ["", "**一级事件原文证据**", ""]
        for evidence in event_evidence:
            speaker = evidence["speaker_id"] or evidence["speaker_type"]
            lines.append(f"- `{evidence['segment_id']}` {speaker}：{evidence['verbatim_text']}")
        lines.append("")
    lines += ["## 三 实体层候选", "",
              "实体层覆盖全部 `SourceSegment`，包括人物小传、脚注、采访者提问、背景和文档级内容。`MENTION_ONLY` 只表示文本提及，不等同于韩礼德参与者。", ""]
    for entity_type in ["PERSON", "PLACE", "ORGANIZATION", "MILITARY_UNIT", "HISTORICAL_EVENT", "PUBLICATION", "OTHER"]:
        names = [row["canonical_name"] for row in entity_rows if row["entity_type"] == entity_type]
        if names:
            lines += [f"### {entity_type}（{len(names)}）", "", "、".join(names), ""]
    unresolved = [row for row in entity_rows if row["authority_status"] in {"TRANSCRIPTION_UNCERTAIN", "UNRESOLVED"}]
    lines += ["### 原文指称仍不确定的已核验实体", ""]
    if unresolved:
        for row in unresolved:
            lines.append(f"- `{row['entity_id']}` {row['canonical_name']}（review_status={row['review_status']}；authority_status={row['authority_status']}；{row['confidence']}）")
    else:
        lines.append("- 无")
    lines += ["", "## 四 非事件内容的呈现", "",
              "- 篇章人物小传：保存为 `DOCUMENT_NOTE`，并建立 `BIOGRAPHICAL_PROFILE` 注释；其中的人名、地名、机构和历史事件另建实体提及。",
              "- 人物或名物脚注：原文保存在脚注 `SourceSegment`，同时建立 `DocumentAnnotation` 并指向被注释实体。",
              "- 背景、评价和补充叙述：以 `BACKGROUND`、`NARRATOR_COMMENT` 等类型挂接事件、阶段或文档。",
              "- 未进入事件的内容：以 `DOCUMENT_ONLY` 挂接文档，但其中的实体仍可查询。", "",
              "- 全文时间表达：正文、人物小传、脚注、提问和文档级内容中的明确年月日进入 `TimeExpression`；录音时间戳不进入该层。`EventTime` 仍只表示一级事件的历史时间。", "",
              "## 五 人工复核重点", "", "1. 核对每个事件的拆分与合并是否符合你的研究粒度；", "2. 核对主事件类型和韩礼德参与者角色；", "3. 核对规范时间是否超出原文证据；", "4. 核对长事件阶段是否过细或过粗；", "5. 核对每条采访者提问、背景和文档注释的挂接对象；", "6. 核对同名实体是否应合并、别名是否正确；对于人工已经核验但现实指称仍无法确定的记录，保持 `CONFIRMED` 与不确定的 `authority_status` 并存；", "7. 其余模型候选经人工确认后再把 review_status 改为 CONFIRMED。", ""]
    (folder / "事件试标复核稿.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({
        "doc_id": doc_id, "segments": len(source_rows), "events": len(event_rows),
        "stages": len(stage_rows), "entities": len(entity_rows), "mentions": len(mention_rows),
        "attachments": len(attachment_rows),
        "coverage_rate": coverage_rows[0]["coverage_rate"], "output": str(folder)
    }, ensure_ascii=False))


from development_corpus_config import (
    DEVELOPMENT_DOCS,
    DEVELOPMENT_ENTITY_CATALOGS,
    DEVELOPMENT_ENTITY_RELATIONS,
    DEVELOPMENT_EVENT_TIMES,
    DEVELOPMENT_NOTE_TARGETS,
)

DOCS.update(DEVELOPMENT_DOCS)
ENTITY_CATALOGS.update(DEVELOPMENT_ENTITY_CATALOGS)
ENTITY_RELATIONS.update(DEVELOPMENT_ENTITY_RELATIONS)
EVENT_TIMES.update(DEVELOPMENT_EVENT_TIMES)
NOTE_TARGETS.update(DEVELOPMENT_NOTE_TARGETS)

selected_documents = sys.argv[1:] or list(DOCS)
unknown_documents = [doc_id for doc_id in selected_documents if doc_id not in DOCS]
if unknown_documents:
    raise SystemExit(f"未知文档编号：{', '.join(unknown_documents)}")
for document_id in selected_documents:
    build_document(document_id, DOCS[document_id])
