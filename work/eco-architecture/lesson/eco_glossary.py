# -*- coding: utf-8 -*-
"""친환경건축 회독 레슨 공용 용어 사전.

notes/slides_w1.json, notes/slides_w3.json 의 단원 용어를 그대로 옮긴 것이다.
사이트가 정리 슬라이드와 레슨에서 용어를 함께 모으므로 표기를 반드시 같게 쓴다.
키는 en(없으면 ko). 레슨 build 스크립트는 pick("Wood", "Plywood", ...) 로 glossary 를 만든다.
"""

TERMS = {
 "Eco-friendly Architecture": {"ko": "친환경건축", "en": "Eco-friendly Architecture", "say": "자연을 망가뜨린 옛 건축을 반성하며 나온, 자연과 함께 도는 새 건축"},   # E1 w1-1
 "Domination of Nature": {"ko": "자연 지배관", "en": "Domination of Nature", "say": "사람이 자연을 정복하고 마음대로 부려도 된다는 생각"},   # E1 w1-1
 "Industrial Revolution": {"ko": "산업혁명", "en": "Industrial Revolution", "say": "기계로 물건을 많이 만들며 근대화, 산업화가 일어난 큰 변화"},   # E1 w1-1
 "Capitalism": {"ko": "자본주의", "en": "Capitalism", "say": "돈과 이익을 늘리는 쪽으로 움직이는 경제 방식. 자연 지배관을 지원했어요"},   # E1 w1-1
 "Global Ecological Crisis": {"ko": "전지구적 생태위기", "en": "Global Ecological Crisis", "say": "지구 전체의 자연과 사람이 함께 살아남기 어려워진 위기"},   # E1 w1-1
 "Limits to Growth": {"ko": "성장의 한계", "en": "Limits to Growth", "say": "위기를 알아차리게 한 첫 번째 계기"},   # E1 w1-1
 "Rio Conference": {"ko": "리우환경회의", "en": "Rio Conference", "say": "1992년 환경 회의. 위기를 알아차리게 한 두 번째 계기"},   # E1 w1-1
 "Kyoto Protocol": {"ko": "교토의정서", "en": "Kyoto Protocol", "say": "1997년 채택. 위기를 알아차리게 한 세 번째 계기"},   # E1 w1-1
 "Vernacular Architecture": {"ko": "토속건축", "en": "Vernacular Architecture", "say": "그 지역의 바람, 눈, 더위 같은 특성에 맞춰 지은 옛날 집"},   # E1 w1-2
 "Matmata": {"ko": "마트마타", "en": "Matmata", "say": "튀니지 사막에 땅을 파서 만든 지하마을. 사막지방 토속건축 사례"},   # E1 w1-2
 "Modern Architecture": {"ko": "현대건축", "en": "Modern Architecture", "say": "산업혁명 이후 새 구조와 재료로 생긴 거대하고 높은 건축"},   # E1 w1-2
 "Crystal Palace": {"ko": "수정궁", "en": "Crystal Palace", "say": "1851년 런던세계박람회 전시장. 유리와 철로 조립한 현대건축의 대표 건물"},   # E1 w1-2
 "High-tech Architecture": {"ko": "하이테크 건축", "en": "High-tech Architecture", "say": "첨단 재료와 공법을 드러내는 요즘 건축. 수정궁이 그 뿌리예요"},   # E1 w1-2
 "Internationalism": {"ko": "국제주의", "en": "Internationalism", "say": "지역 특성과 상관없이 어디서나 똑같이 퍼져 간 건축 경향"},   # E1 w1-2
 "Curtain Wall": {"ko": "커튼월", "en": "Curtain Wall", "say": "건물 무게는 받치지 않고 커튼처럼 공간만 막아 주는 바깥벽"},   # E1 w1-2
 "Finiteness": {"ko": "유한함", "en": "Finiteness", "say": "언젠가는 바닥난다는 성질. 풍요시대 사람들은 석유의 유한함을 몰랐어요"},   # E1 w1-2
 "Oil Shock": {"ko": "오일쇼크", "en": "Oil Shock", "say": "석유 값이 갑자기 크게 뛰어 세계가 흔들린 사건. 1973년 1차, 1978년 2차"},   # E1 w1-3
 "OPEC": {"ko": "석유수출국기구", "en": "OPEC", "say": "석유를 수출하는 나라들의 모임. 1차 오일쇼크 때 원유 가격 17% 인상 발표"},   # E1 w1-3
 "Production Cut": {"ko": "감산", "en": "Production Cut", "say": "만드는 양을 줄이는 것. 매월 전월에 비해 5%씩 줄이기로 했어요"},   # E1 w1-3
 "Alternative Energy": {"ko": "대체에너지", "en": "Alternative Energy", "say": "석유 대신 쓸 에너지. 두 번의 오일쇼크 뒤 비로소 관심을 가졌어요"},   # E1 w1-3
 "Rating System": {"ko": "등급 평가기준", "en": "Rating System", "say": "건물이 얼마나 친환경인지 점수와 등급을 매기는 기준. 건물의 성적표"},   # E1 w1-3
 "BREEAM": {"ko": "브리암", "en": "BREEAM", "say": "영국의 건축환경등급 평가기준"},   # E1 w1-3
 "LEED": {"ko": "", "en": "LEED", "say": "미국의 친환경건축물등급 평가기준. 1993년 USDBC 설립과 함께 마련"},   # E1 w1-3
 "G-SEED": {"ko": "녹색건축인증", "en": "G-SEED", "say": "한국의 친환경건축물 인증제도(2002년 시행)의 현재 이름"},   # E1 w1-3
 "Sustainable Future": {"ko": "지속가능한 미래", "en": "Sustainable Future", "say": "1992년 리우환경회의의 1993년 환경선언이 내건 핵심 말"},   # E1 w1-3
 "Climate Change Convention": {"ko": "기후변화 협약", "en": "Climate Change Convention", "say": "지구가 더워지는 기후변화에 나라들이 함께 대응하자는 약속"},   # E1 w1-4
 "Ecological Order Restoration": {"ko": "생태질서 회복 움직임", "en": "Ecological Order Restoration", "say": "망가진 자연의 질서를 되살리려는 여섯 가지 실천"},   # E1 w1-4
 "Biotop": {"ko": "비오톱", "en": "Biotop", "say": "여러 생물이 모여 사는 작은 생물 서식 공간. 소생물권이라고도 해요"},   # E1 w1-4
 "Ecology": {"ko": "생태학", "en": "Ecology", "say": "생물체끼리 서로 어떤 관계인지 연구하는 학문"},   # E1 w1-4
 "Ecologism": {"ko": "생태주의", "en": "Ecologism", "say": "생태학의 기본정신. 친환경건축은 이 정신에 입각해요"},   # E1 w1-4
 "Mechanistic Worldview": {"ko": "기계론적 세계관", "en": "Mechanistic Worldview", "say": "세상을 기계처럼 보는 인간중심의 눈. 20세기 건축의 주류"},   # E1 w1-4
 "Ecological Worldview": {"ko": "생태학적 세계관", "en": "Ecological Worldview", "say": "세상을 살아 있는 관계로 보는 자연중심의 눈. 주류에서 일탈"},   # E1 w1-4
 "Machine Aesthetic": {"ko": "기계미학", "en": "Machine Aesthetic", "say": "기계처럼 반듯하고 효율적인 모습을 아름답다고 보는 생각"},   # E1 w1-4
 "Organic Architecture": {"ko": "유기적 건축철학", "en": "Organic Architecture", "say": "건축을 자연과 어우러진 살아 있는 몸처럼 짓자는 생각"},   # E1 w1-4
 "Falling water": {"ko": "낙수장", "en": "Falling water", "say": "F.L Wright 가 설계한, 폭포 위 숲속의 집"},   # E1 w1-4
 "Alternative Architecture": {"ko": "대안건축", "en": "Alternative Architecture", "say": "기존 건축의 문제를 반성하고 새 길을 내놓는 건축. 친환경건축이 그 대안이에요"},   # E1 w1-5
 "Community": {"ko": "공동체", "en": "Community", "say": "사람과 자연이 더불어 사는 무리"},   # E1 w1-5
 "Sustainable Development": {"ko": "지속가능한 개발", "en": "Sustainable Development", "say": "다음 세대도 쓸 수 있게 자연을 아끼며 발전하는 방식"},   # E1 w1-5
 "Maintenance": {"ko": "유지관리", "en": "Maintenance", "say": "다 지은 건물을 쓰면서 고치고 돌보는 일"},   # E1 w1-5
 "Renewable Resources": {"ko": "재생이 가능한 자원", "en": "Renewable Resources", "say": "써도 자연이 다시 채워 주는 자원"},   # E1 w1-5
 "Habitat": {"ko": "서식", "en": "Habitat", "say": "동물과 식물이 자리 잡고 사는 것"},   # E1 w1-5
 "Landscape": {"ko": "경관", "en": "Landscape", "say": "건물 주위에 펼쳐진 풍경"},   # E1 w1-5
 "Consumption-dependent Economy": {"ko": "소비 의존형 경제체계", "en": "Consumption-dependent Economy", "say": "한 방향으로 쓰고 버리는 데 기대는 경제. 과소비와 환경오염을 불렀어요"},   # E1 w1-5
 "Natural Ecosystem": {"ko": "자연생태계", "en": "Natural Ecosystem", "say": "생물과 환경이 서로 주고받으며 도는 자연 전체"},   # E1 w1-5
 "Circulation Loop": {"ko": "순환고리", "en": "Circulation Loop", "say": "건물과 주변환경이 서로 주고받으며 빙글 도는 연결 고리"},   # E1 w1-6
 "One-Way Process": {"ko": "원웨이 프로세스", "en": "One-Way Process", "say": "들어온 것이 한 방향으로만 흘러 더러워져 나가는 기존 건축의 방식"},   # E1 w1-6
 "Circulation System": {"ko": "순환체계", "en": "Circulation System", "say": "에너지, 재료, 녹지, 대기, 물이 건물 안팎을 돌게 짜 놓은 틀"},   # E1 w1-6
 "Human-centered Design Methodology": {"ko": "인간위주 건축설계방법론", "en": "Human-centered Design Methodology", "say": "사람 편한 것만 생각하고 자연은 뒷전인 옛 설계 방식"},   # E1 w1-6
 "Environmental Load": {"ko": "환경부하", "en": "Environmental Load", "say": "건물이 지구와 주변환경에 지우는 짐"},   # E1 w1-6
 "Comfort": {"ko": "쾌적", "en": "Comfort", "say": "건물 안의 사람이 편하고 기분 좋게 지내는 상태"},   # E1 w1-6
 "Applied Technology": {"ko": "적용기술", "en": "Applied Technology", "say": "순환체계마다 실제 설계에 쓰는 방법 한 줄"},   # E1 w1-6
 "Fossil Energy": {"ko": "화석에너지", "en": "Fossil Energy", "say": "석유, 석탄처럼 땅속에서 캐서 쓰고 나면 없어지는 에너지"},   # E1 w1-7
 "Renewable Energy": {"ko": "신재생에너지", "en": "Renewable Energy", "say": "탄소를 내보내지 않고 자연에서 다시 얻는 에너지"},   # E1 w1-7
 "Microclimate": {"ko": "미기후", "en": "Microclimate", "say": "지표면에서 1.5m 정도까지의, 건물 바로 옆 작은 날씨"},   # E1 w1-7
 "Broadleaf Tree": {"ko": "활엽수", "en": "Broadleaf Tree", "say": "잎이 넓은 나무. 예시에서 남쪽에 심어요"},   # E1 w1-7
 "Conifer": {"ko": "침엽수", "en": "Conifer", "say": "잎이 바늘처럼 가는 나무. 예시에서 북쪽에 심어요"},   # E1 w1-7
 "Biomass": {"ko": "바이오매스", "en": "Biomass", "say": "식물 같은 생물 자원을 에너지로 쓰는 대체에너지"},   # E1 w1-7
 "Local Natural Material": {"ko": "지역적 자연적 재료", "en": "Local Natural Material", "say": "주변에서 구하기 쉽고 자연에서 온 건축 재료"},   # E1 w1-7
 "Recycling": {"ko": "재활용", "en": "Recycling", "say": "쓰던 자재를 버리지 않고 다시 살려 쓰는 것"},   # E1 w1-7
 "Regional Green Network": {"ko": "광역녹지체계", "en": "Regional Green Network", "say": "단지 하나를 넘어 넓은 지역의 녹지가 이어진 연결망"},   # E1 w1-8
 "Transpiration": {"ko": "증산작용", "en": "Transpiration", "say": "식물이 잎으로 물을 수증기로 내보내 주변을 식히는 일"},   # E1 w1-8
 "Heat Island": {"ko": "열섬화 현상", "en": "Heat Island", "say": "도시가 주변보다 섬처럼 뜨거워지는 현상"},   # E1 w1-8
 "Roof Greening": {"ko": "지붕녹화", "en": "Roof Greening", "say": "건물 지붕 위에 흙을 깔고 식물을 심는 것"},   # E1 w1-8
 "Rain Garden": {"ko": "레인가든", "en": "Rain Garden", "say": "빗물을 모아 두는 기능을 가진 정원"},   # E1 w1-8
 "Eco Road": {"ko": "에코로드", "en": "Eco Road", "say": "미사 강변 센트럴 자이 외곽을 따라 흙길로 포장한 약 1.0km 길"},   # E1 w1-8
 "Crystal Garden": {"ko": "크리스탈 가든", "en": "Crystal Garden", "say": "미사 강변 센트럴 자이에서 빗물로 만든 생태연못"},   # E1 w1-8
 "Artificial Biotop": {"ko": "인공형 비오톱", "en": "Artificial Biotop", "say": "옥상정원처럼 사람이 새로 만들어 준 생물의 서식공간"},   # E1 w1-8
 "IFLA": {"ko": "세계조경가협회", "en": "IFLA", "say": "2019년 미사 강변 센트럴 자이에 우수상을 준 세계 조경가 모임"},   # E1 w1-8
 "Water Cycle": {"ko": "수순환", "en": "Water Cycle", "say": "비가 내려 땅에 스며들고 다시 증발해 하늘로 가는 물의 돌고 도는 길"},   # E1 w1-9
 "Rainwater": {"ko": "우수", "en": "Rainwater", "say": "하늘에서 내린 빗물"},   # E1 w1-9
 "Wastewater": {"ko": "오수", "en": "Wastewater", "say": "사람이 쓰고 난 더러워진 물"},   # E1 w1-9
 "Infiltration": {"ko": "침투", "en": "Infiltration", "say": "빗물이 흙 속으로 스며드는 것"},   # E1 w1-9
 "Permeable Pavement": {"ko": "투수성 포장", "en": "Permeable Pavement", "say": "블록 틈 같은 곳으로 빗물이 땅에 스며들게 만든 바닥 포장"},   # E1 w1-9
 "Rainwater Storage Facility": {"ko": "우수저장시설", "en": "Rainwater Storage Facility", "say": "빗물을 모아 두었다가 다시 쓰게 하는 탱크 같은 시설"},   # E1 w1-9
 "Water Purification": {"ko": "수질정화", "en": "Water Purification", "say": "더러운 물을 깨끗하게 만드는 일"},   # E1 w1-9
 "Pollutant": {"ko": "공해물질", "en": "Pollutant", "say": "공기를 더럽혀 지구와 사람에게 해를 주는 물질"},   # E1 w1-10
 "Greenhouse Gas": {"ko": "온실가스", "en": "Greenhouse Gas", "say": "지구를 온실처럼 덥게 만드는 기체. 관리해서 지구온난화에 대비해요"},   # E1 w1-10
 "Indoor Air Quality": {"ko": "실내공기질", "en": "Indoor Air Quality", "say": "건물 안 공기가 얼마나 깨끗하고 건강한지"},   # E1 w1-10
 "VOCs": {"ko": "휘발성유기화합물", "en": "VOCs", "say": "마감재 같은 화학재료에서 공기 중으로 날아 나오는 유해 물질", "more": "1강 대기 순환의 실내공기질 개선에서도 VOCs 억제가 나왔어요."},   # E1 w1-10
 "Pollution Source": {"ko": "오염원", "en": "Pollution Source", "say": "더러운 물질이 처음 나오는 곳. 실내재료와 마감재가 대표예요"},   # E1 w1-10
 "Bake-out": {"ko": "베이크아웃", "en": "Bake-out", "say": "실내를 데워 자재 속 유해 물질을 미리 빼내는 기법"},   # E1 w1-10
 "Mechanical Ventilation System": {"ko": "기계적 환기시스템", "en": "Mechanical Ventilation System", "say": "팬 같은 기계로 실내외 공기를 바꿔 주는 설비"},   # E1 w1-10
 "Heat Recovery System": {"ko": "열회수시스템", "en": "Heat Recovery System", "say": "나가는 공기의 열을 들어오는 공기에 넘겨 에너지를 아끼는 설비"},   # E1 w1-10
 "Ecosystem": {"ko": "생태시스템", "en": "Ecosystem", "say": "물, 공기, 토양, 생물, 재생산이 안 되는 자연 재료를 한데 부르는 말", "more": "건축 재료를 만들고, 건물을 짓고, 건물을 쓰는 동안 이것들이 소모돼요. 되돌릴 수 없게 훼손되거나 쓰레기로 나오기도 해요."},   # E2 w3-1
 "Third Skin": {"ko": "제3의 피부", "en": "Third Skin", "say": "우리 몸을 감싸는 세 번째 껍질, 곧 집", "more": "첫째 피부는 몸의 피부, 제2의 피부는 옷(의복), 제3의 피부는 집이에요. 그래서 집 재료가 건강에 크게 영향을 줘요."},   # E2 w3-1
 "Protective Function": {"ko": "보호 기능", "en": "Protective Function", "say": "화학, 기계, 열의 영향을 막아 주는 건축재료의 기능"},   # E2 w3-1
 "Ventilation Function": {"ko": "환기 기능", "en": "Ventilation Function", "say": "신선한 공기는 들이고 오염된 공기는 내보내는 건축재료의 기능", "more": "통기가 전혀 안 되는 재료를 쓰면 실내공기가 나빠져요."},   # E2 w3-1
 "Resource Circulation": {"ko": "자원의 순환활용", "en": "Resource Circulation", "say": "공급량에 한계가 있는 자원을 버리지 않고 다시 돌려 쓰는 것"},   # E2 w3-1
 "Surface Treatment": {"ko": "표면처리", "en": "Surface Treatment", "say": "재료 겉면에 칠하거나 코팅하는 마무리 작업", "more": "유해한 물질이 발산되거나 마모가 일어나지 않아야 해요. 무해한 목재도 표면처리를 잘못하면 자연 특성을 잃어요."},   # E2 w3-2
 "Sick House Syndrome": {"ko": "새집증후군", "en": "Sick House Syndrome", "say": "새로 지은 집의 재료에서 나온 유해 물질 때문에 몸이 불편해지는 증상", "more": "슬라이드는 목재의 잘못된 표면처리가 새집증후군의 원인을 제공할 수 있다고 들었어요."},   # E2 w3-2
 "Local Material": {"ko": "지역 생산 재료", "en": "Local Material", "say": "가까운 지역에서 만들어 쓰는 재료. 목재, 흙, 석재가 대표예요", "more": "재료를 멀리 나르지 않아서 수송에서 쓰는 에너지를 줄여요."},   # E2 w3-2
 "Transport Energy": {"ko": "수송 에너지", "en": "Transport Energy", "say": "재료를 나르는 데 드는 에너지", "more": "대규모 생산, 대량 판매 재료는 여러 번 운송해서 교통량, 도로 이용, 탄소배출이 늘어요."},   # E2 w3-2
 "Decentralized Production": {"ko": "분산적 생산", "en": "Decentralized Production", "say": "자원을 여러 곳에서 나누어 생산한 뒤 그 지역 안에서 쓰는 방식", "more": "슬라이드는 이 방안이 효과적이라고 정리했어요."},   # E2 w3-2
 "Renewable Material": {"ko": "재생가능 재료", "en": "Renewable Material", "say": "식물, 동물처럼 다시 자라나는 원료로 만든 재료", "more": "이런 원료를 쓰면 자연계로의 물질순환이 거의 완벽하게 이루어져요."},   # E2 w3-2
 "Building Envelope": {"ko": "외피", "en": "Building Envelope", "say": "건물의 바깥 껍질. 사람으로 치면 피부", "more": "실내외 환경을 조절해요. 일사열과 자연광, 실내외 열류, 틈새바람을 조절해요."},   # E2 w3-2
 "Natural Material": {"ko": "천연건축재료", "en": "Natural Material", "say": "흙, 나무, 돌을 캐서 자르거나 갈기만 한 순수 자연 재료", "more": "생산, 가공, 사용 과정에 화학적 성분이 전혀 들어가지 않아요. 예: 황토, 목재, 석재, 짚."},   # E2 w3-3
 "Environmental Material": {"ko": "친환경재료", "en": "Environmental Material", "say": "천연은 아니지만 나라별 환경 기준치에 맞춰 만든 몸에 해롭지 않은 재료", "more": "자연소재를 섞거나 천연소재와 인공재료를 합성해요. 예: 자연소재 혼합단열재, 분해성 플라스틱, 친환경 페인트."},   # E2 w3-3
 "Sustainable Material": {"ko": "지속가능한 재료", "en": "Sustainable Material", "say": "훼손되지 않고 영구적으로 쓸 수 있는 재료. 금속재가 대표", "more": "재활용, 폐기 때는 환경부하가 적지만 생산 때는 에너지를 많이 쓰고 오염을 일으켜요. 예: 스틸, 동판, 알루미늄, 강철."},   # E2 w3-3
 "Recycling Material": {"ko": "재활용재료", "en": "Recycling Material", "say": "폐자재를 다시 원료로 써서 만든 재료", "more": "폐콘크리트, 폐목재, 폐지, 폐플라스틱 등으로 만들어요. 예: 재생섬유 흡음재, 재활용 섬유판재, 재활용골재."},   # E2 w3-3
 "한국공기청정협회": {"ko": "한국공기청정협회", "en": "", "say": "국내에서 친환경재료(건축자재)의 품질을 인증하는 곳"},   # E2 w3-3
 "Recycled Aggregate": {"ko": "재활용골재", "en": "Recycled Aggregate", "say": "폐콘크리트 같은 폐자재를 부숴 다시 만든 자갈, 모래 같은 재료", "more": "슬라이드 사진은 콘크리트용, 도로공사용, 아스팔트콘크리트용 순환골재예요."},   # E2 w3-3
 "Human": {"ko": "인체유해성", "en": "Human", "say": "재료가 사람 몸에 얼마나 해로운지 보는 평가 분야", "more": "H1 은 채취, 생산, 가공, 사용 중 인체에 미치는 유해성의 정도, H2 는 실내 환경을 조절하거나 건강을 좋게 하는 효과의 정도예요."},   # E2 w3-4
 "Energy": {"ko": "에너지소비", "en": "Energy", "say": "재료를 만들고 나르고 버리는 데 드는 에너지를 보는 평가 분야", "more": "채취, 생산, 가공 / 운송, 이용 / 폐기 세 과정의 에너지소비 정도를 모두 E 로 표시해요."},   # E2 w3-4
 "Environmental Impact": {"ko": "환경부하", "en": "Environmental Impact", "say": "재료가 자연에 주는 부담을 보는 평가 분야", "more": "E.I1 은 환경외손이나 자원고갈로 인한 부하, E.I2 는 독성, 가스, 미세먼지의 발생 정도예요."},   # E2 w3-4
 "Recycling or Reuse": {"ko": "재생 또는 재활용", "en": "Recycling or Reuse", "say": "폐기 뒤 다시 쓸 수 있는지 보는 평가 분야. 기호 R1"},   # E2 w3-4
 "Life Cycle": {"ko": "전과정", "en": "Life Cycle", "say": "재료가 만들어지고, 쓰이고, 버려지거나 다시 쓰이기까지의 모든 과정", "more": "슬라이드 표는 제조, 생산 / 사용 / 폐기, 활용 세 과정으로 나눠 평가해요."},   # E2 w3-4
 "Clay Brick": {"ko": "점토벽돌", "en": "Clay Brick", "say": "점토를 구워 만든 벽돌. 벽과 지붕(기와)에 써요", "more": "점토 제품이라 에너지 투입이 매우 많고, 채굴 때 자연을 훼손하며 유한 자원을 소모해요."},   # E2 w3-4
 "Wood": {"ko": "목재", "en": "Wood", "say": "나무를 잘라 만든 건축재료. 재생될 수 있는 재료 중 가장 많이 쓰여요", "more": "건축 수명 100년 이상, 모든 건축재료의 95%까지 대체할 수 있어요. 대신 부패, 벌레, 버섯, 화재에 약해요."},   # E2 w3-5
 "Breathability": {"ko": "통기성", "en": "Breathability", "say": "공기와 습기가 재료를 통해 드나드는 성질", "more": "목재는 미세기공 덕분에 통기성과 흡수 능력이 높아요."},   # E2 w3-5
 "Micropore": {"ko": "미세기공", "en": "Micropore", "say": "재료 속의 아주 작은 구멍. 나무의 숨구멍 같은 것"},   # E2 w3-5
 "Preservative": {"ko": "방부제", "en": "Preservative", "say": "썩지 않게 하려고 넣는 약품", "more": "유독성 방부제를 쓰면 목재를 자연으로 순환시키기 어려워서 쓰면 안 된다고 했어요."},   # E2 w3-5
 "Formalin": {"ko": "포르말린", "en": "Formalin", "say": "산업용 목재 가공 때 유독성 접합제로 들어갈 수 있는 물질", "more": "슬라이드는 페놀 또는 포르말린이 첨가되면 인체에 해로울 가능성이 있다고 했어요."},   # E2 w3-5
 "Phenol": {"ko": "페놀", "en": "Phenol", "say": "산업용 목재 가공 때 유독성 접합제로 들어갈 수 있는 물질"},   # E2 w3-5
 "Structural Panel": {"ko": "구조용 판넬", "en": "Structural Panel", "say": "합판, OSB 판넬, 집성판넬처럼 넓은 판으로 된 구조용 목재", "more": "강도와 내구성이 우수하고 바닥, 벽, 천정, 거푸집, 가구, I-Joist 웹 부분 등 다양하게 써요."},   # E2 w3-6
 "Plywood": {"ko": "합판", "en": "Plywood", "say": "얇은 목재 단판을 결 방향이 서로 교차되게 쌓아 붙인 판", "more": "결을 엇갈려 쌓아서 강도가 높아져요."},   # E2 w3-6
 "Oriented Strand Board": {"ko": "OSB 판넬", "en": "Oriented Strand Board", "say": "나무 조각들을 접착제로 붙여 만든 판"},   # E2 w3-6
 "Glue Laminated Timbers": {"ko": "글루램", "en": "Glue Laminated Timbers", "say": "두께 5cm 미만의 각재를 접착해 만든 목재(집성재)", "more": "끝을 이어 긴 판재를 만들고 적층, 접착해서 직선, 곡선 모양으로 만들어요. 강도와 내구성이 좋아 구조용으로 적절해요."},   # E2 w3-6
 "집성재": {"ko": "집성재", "en": "", "say": "작은 목재를 접착제로 붙여 크게 만든 접착가공목재. 글루램이 대표"},   # E2 w3-6
 "Laminated Veneer Lumber": {"ko": "LVL", "en": "Laminated Veneer Lumber", "say": "얇은 단판을 나뭇결이 길이 방향으로 나란하게 쌓아 만든 목재", "more": "큰 장작 모양으로 만든 뒤 제품 크기로 잘라요. 보, 서까래, I-Joist 플랜지 부분 등에 써요."},   # E2 w3-6
 "I-Joist": {"ko": "아이조이스트", "en": "I-Joist", "say": "알파벳 I 모양의 목재 보. 웹은 합판이나 OSB, 플랜지는 LVL", "more": "시공이 간단하고 가볍고 긴 제품을 만들 수 있어요. 바닥 또는 지붕 구조용 자재로 써요."},   # E2 w3-6
 "Preservative-treated Wood": {"ko": "방부목", "en": "Preservative-treated Wood", "say": "습기에 썩지 않게 약품을 처리한 목재", "more": "발코니, 담장, 옥외 조경물 등에 써요."},   # E2 w3-6
 "Earth Architecture": {"ko": "흙건축", "en": "Earth Architecture", "say": "흙을 주재료로 짓는 건축", "more": "흙은 습도 조절, 단열과 축열, 공기 정화, 항균과 방충, 폐기물 없음이 장점이고, 수분에 약하고 갈라질 수 있어요."},   # E2 w3-7
 "Humidity Control": {"ko": "습도 조절", "en": "Humidity Control", "say": "실내 습도를 알맞게 유지해 주는 기능. 흙의 첫 번째 특성"},   # E2 w3-7
 "Heat Storage": {"ko": "축열", "en": "Heat Storage", "say": "열을 머금었다가 천천히 내놓는 것. 기초 다지기의 뚝배기 이야기", "more": "흙집은 여름 최고기온이 실외보다 3~10도 정도 낮고, 겨울 최저기온이 실외보다 5~7도 정도 높아요."},   # E2 w3-7
 "Compressive Strength": {"ko": "압축강도", "en": "Compressive Strength", "say": "누르는 힘을 물체가 어느 정도 견디는지", "more": "흙을 구조재료(기둥, 내력벽)나 실외 마감재료로 쓸 때 필요해요."},   # E2 w3-7
 "Bond Strength": {"ko": "부착강도", "en": "Bond Strength", "say": "재료가 견고하게 잘 붙어 있는지", "more": "흙을 실내 마감재료(미장, 벽돌, 패널)로 쓸 때 필요해요."},   # E2 w3-7
 "Frost Resistance": {"ko": "동해저항", "en": "Frost Resistance", "say": "추위로 얼어서 망가지지 않는 성능"},   # E2 w3-7
 "Non-shrinkage": {"ko": "비수축성", "en": "Non-shrinkage", "say": "마르면서 줄어들지 않는 성질. 흙을 어디에 쓰든 필요해요"},   # E2 w3-7
 "Incombustibility": {"ko": "불연성", "en": "Incombustibility", "say": "불에 타지 않는 성질"},   # E2 w3-7
 "Load-bearing Wall": {"ko": "내력벽", "en": "Load-bearing Wall", "say": "지붕과 건물의 무게를 받치는 벽", "more": "흙으로 내력벽을 만들 때는 일정 강도를 유지하도록 흙을 가공해서 써요."},   # E2 w3-8
 "Non-load-bearing Wall": {"ko": "비내력벽", "en": "Non-load-bearing Wall", "say": "무게는 받치지 않고 공간만 나누는 벽", "more": "비내력벽, 천정, 지붕에는 다양한 흙건축 재료를 쓸 수 있어요."},   # E2 w3-8
 "Rammed Earth": {"ko": "담틀 공법", "en": "Rammed Earth", "say": "거푸집에 흙을 채워 다져서 벽을 쌓는 방법", "more": "흙벽 자체가 내력벽이 되고, 밀도 1700~2200kg/m³ 로 흙건축 형태 중 밀도가 가장 높아요."},   # E2 w3-8
 "Clay Straw": {"ko": "흙짚", "en": "Clay Straw", "say": "물에 갠 점토에 짚을 담갔다가 거푸집에 채워 다지는 방식", "more": "북유럽에서 발전했고 단열효과가 뛰어나요. 완전히 마르면 밀도 1200~1700kg/m³ 예요."},   # E2 w3-8
 "심벽": {"ko": "심벽", "en": "", "say": "목구조 사이에 대나무, 나뭇가지, 수숫깡으로 심을 얽고 흙을 안팎으로 바르는 벽"},   # E2 w3-8
 "Adobe": {"ko": "아도브", "en": "Adobe", "say": "틀 속에 흙을 채워 만드는 흙벽돌 방식", "more": "현장 기계로 찍는 흙벽돌(15톤 하중 정도), 공장 기계압 벽돌(35톤 하중 정도), 압축 흙벽돌이 있어요."},   # E2 w3-8
 "Bloc Terre Comprimé": {"ko": "압축 흙벽돌", "en": "Bloc Terre Comprimé", "say": "흙을 틀에 넣고 높은 압력을 가해 강도를 높인 벽돌"},   # E2 w3-8
 "Plaster": {"ko": "플라스터", "en": "Plaster", "say": "벽에 바르는 흙이나 석회 반죽. 슬라이드는 회반죽(도장 등에 사용)이라고 풀었어요"},   # E2 w3-8
 "Minke House": {"ko": "밍케하우스", "en": "Minke House", "say": "독일 카셀 생태단지 안의 돔형 흙집. 흙 국외 적용사례", "more": "목구조와 흙벽돌로 짓고, 지붕은 모두 잔디로 덮었어요. 벽체, 지붕, 바닥 대부분에 어도비 벽돌을 썼어요."},   # E2 w3-9
 "Adobe Brick": {"ko": "어도비 벽돌", "en": "Adobe Brick", "say": "굽지 않은 흙벽돌. 밍케하우스 건물 대부분에 쓰였어요", "more": "내부 디자인 효과와 습도 조절 기능을 줘요."},   # E2 w3-9
 "Green Roof": {"ko": "지붕 녹화", "en": "Green Roof", "say": "지붕을 흙과 풀로 덮어 푸르게 만드는 것", "more": "밍케하우스에서는 단열효과를 주고 열손실이 거의 없는 구조를 만들었어요. 빗물도 스며들게 해요."},   # E2 w3-9
 "잔디지붕": {"ko": "잔디지붕", "en": "", "say": "흙과 잔디로 덮은 지붕. 밍케하우스는 처마 끝에 통나무를 대 흙이 흘러내리지 않게 했어요"},   # E2 w3-9
 "Straw Bale": {"ko": "스트로베일", "en": "Straw Bale", "say": "건초(짚)를 네모나게 묶은 블록. 벽돌처럼 쌓아 벽을 만들어요", "more": "자연에서 재생산되는 지속가능한 자연재료로, 습도조절, 탈취, 방음, 단열성능이 우수하고 값이 싸요."},   # E2 w3-9
 "골조방식": {"ko": "골조방식", "en": "", "say": "가구식 구조(뼈대)를 먼저 세우고 건초블록을 쌓아 벽을 만드는 스트로베일 공법. 5층 이상 가능", "more": "슬라이드는 현재는 7층 이상도 가능하다고 했어요."},   # E2 w3-9
 "무골조방식": {"ko": "무골조방식", "en": "", "say": "건초블록 자체가 내력벽이 되는 스트로베일 공법. 2층까지 시공 가능"},   # E2 w3-9
 "Ricehouse": {"ko": "라이스하우스", "en": "Ricehouse", "say": "볏짚, 쌀겨, 왕겨 같은 쌀 생산 부산물로 건축자재를 만드는 이탈리아 사례", "more": "천연석회 등 100% 친환경 천연 재료로 단열재 외 다양한 자재(RH시리즈)를 만들어요."},   # E2 w3-9
 "Insulation": {"ko": "단열재", "en": "Insulation", "say": "열이 드나드는 것을 막아 건물 에너지를 아끼게 하는 재료. 겨울 패딩", "more": "건물에서 소모되거나 방출되는 에너지를 줄여 탄소배출도 줄여요. 성분이 친환경적이고 인체에 해롭지 않아야 해요."},   # E2 w3-10
 "Asbestos": {"ko": "석면", "en": "Asbestos", "say": "인체에 해로워서 단열재 성분의 유해성 예로 나온 물질"},   # E2 w3-10
 "Polystyrene": {"ko": "폴리스티렌", "en": "Polystyrene", "say": "석유로 만든 단열재. EPS, XPS 스티로폼", "more": "단열 특성과 기후 내구성이 좋아 지하실, 지붕, 벽 같은 외부 영역에 써요. 제조 때 독성, 발암 물질과 온실가스가 나와요."},   # E2 w3-10
 "PUR": {"ko": "폴리우레탄", "en": "PUR", "say": "석유로 만든 단열재. 폴리스티렌과 같은 줄에 묶여 나와요"},   # E2 w3-10
 "Mineral Wool": {"ko": "미네랄울", "en": "Mineral Wool", "say": "유리면과 암면을 함께 부르는 말. 70%까지 폐유리로 만들어요", "more": "경사진 지붕 단열에 써요. 1995년 이전 제품은 직물구조 때문에 암을 일으킬 수 있고, 이후 제품은 발암지수 40 을 충족해요."},   # E2 w3-10
 "Glass Wool": {"ko": "유리면", "en": "Glass Wool", "say": "유리를 솜처럼 만든 미네랄울"},   # E2 w3-10
 "Rock Wool": {"ko": "암면", "en": "Rock Wool", "say": "돌을 솜처럼 만든 미네랄울"},   # E2 w3-10
 "발암지수": {"ko": "발암지수", "en": "", "say": "단열재가 암을 일으킬 수 있는 정도를 나타낸 수치. 40 미만이면 인체에 무해한 것으로 봐요"},   # E2 w3-10
 "천연단열재": {"ko": "천연단열재", "en": "", "say": "양모 같은 동물성 원료나 코르크, 코코넛 섬유, 목재섬유, 폐지 같은 식물성 원료로 만든 단열재", "more": "천연이라도 살충제, 유해물질 첨가 여부, 인체에 무해한 성분(암모늄 화합물 등)으로 만들었는지 확인해야 해요."},   # E2 w3-10
 "Cellulose Insulation": {"ko": "셀룰로우스 단열재", "en": "Cellulose Insulation", "say": "목재펄프를 주원료로 만들어 구조체 속에 분쇄해 채우는 단열재", "more": "폐기 때 재활용 가능, 가벼워 건물 하중을 줄이고, 단열과 방음이 뛰어나고, 오염물질 배출이 없어요."},   # E2 w3-10
 "Natural Paint": {"ko": "천연도료", "en": "Natural Paint", "say": "수지, 오일, 용제 같은 주요 성분을 재생산 가능한 순수 천연원료로 만든 페인트", "more": "중금속과 VOCs 를 쓰지 않아 인체에 무해하고, 인화성 물질이 없어 화재 때 유독가스가 없어요."},   # E2 w3-11
 "Eco-friendly Paint": {"ko": "친환경도료", "en": "Eco-friendly Paint", "say": "석유화학을 쓰지만 중금속과 VOCs 를 적게 넣은 저공해 페인트", "more": "1970년대 초 독일에서 가장 먼저 연구 개발됐어요. 국내는 천연도료보다 저공해, 저독성, 저VOCs 페인트 개발이 중심이에요."},   # E2 w3-11
 "Wooden Window": {"ko": "목재창", "en": "Wooden Window", "say": "자연목재를 가공해 만든 창호. 공극이 많아 단열성이 높지만 물에 약해요"},   # E2 w3-11
 "PVC Window": {"ko": "합성수지창", "en": "PVC Window", "say": "PVC 로 만든 창호. 단열성, 기밀성, 방음성이 좋지만 석유 기반이라 재사용이 어려워요", "more": "내부식성, 내후성(기후변화에 견디는 능력), 방로효과(이슬방지)도 높아요."},   # E2 w3-11
 "Airtightness": {"ko": "기밀성", "en": "Airtightness", "say": "틈으로 공기가 새지 않는 성질"},   # E2 w3-11
 "Natural Adhesive": {"ko": "천연접착제", "en": "Natural Adhesive", "say": "무독성 천연원료로 만든 접착제. 아교, 송진, 라텍스 등", "more": "대부분 수용성이라 불연성, 무독성 면에서 유리하고 실내공기질에도 유리해요."},   # E2 w3-11
 "Synthetic Adhesive": {"ko": "합성접착제", "en": "Synthetic Adhesive", "say": "수지, 고무, 비닐 등의 혼합물질로 만든 접착제"},   # E2 w3-11
 "Finishing Material": {"ko": "마감재", "en": "Finishing Material", "say": "건축공사 마무리 단계에 쓰는 재료. 사람에게 직접 영향을 줘요", "more": "환경친화 마감재는 목재, 리놀륨, 타일, 코르크 같은 천연 가공 재료, 석유원료 마감재는 PVC, 합성고무예요."},   # E2 w3-11
 "Linoleum": {"ko": "리놀륨", "en": "Linoleum", "say": "바닥 마감재의 하나. 코르크계 리놀륨은 천연재료만 섞어 만든 친환경 바닥재", "more": "고무계와 혼합해 만든 PVC, 비닐 계통 바닥과 구분해야 해요."},   # E2 w3-11
}


def pick(*names):
    """이 범위에서 쓰는 용어만 골라 glossary 배열로 만든다."""
    out, seen = [], set()
    for n in names:
        if n in seen:
            continue
        seen.add(n)
        if n not in TERMS:
            raise KeyError("용어 사전에 없는 이름: " + n)
        out.append(dict(TERMS[n]))
    return out


def label(name):
    """본문에 쓸 **한국어(English)** 표기. 영어 이름이 없으면 **한국어** 만."""
    t = TERMS[name]
    if t["ko"] and t["en"]:
        return "**%s(%s)**" % (t["ko"], t["en"])
    return "**%s**" % (t["ko"] or t["en"])
