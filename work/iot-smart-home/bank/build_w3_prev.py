# -*- coding: utf-8 -*-
r"""3주차(I3) basic 문제은행 재생성기. 실행: python build_w3_prev.py -> w3_prev.json

이 문항들은 구 형식 회독 원고에서 옮겨 온 것이라 본문 원본이 따로 있다.
  원본: ..\_src\prev\unit3\bank_unit3.json (문항 순서 그대로, level 과 id 가 없는 상태)
스크립트가 하는 일은 넷이다.
  1) 원본 문항마다 level "basic" 과 IDS 의 id 를 붙인다. id 해시 생성기는 남아 있지 않아
     IDS 에 원본 순서대로 박아 둔다. 순서를 바꾸거나 id 를 새로 매기지 말 것.
  2) TEXT_FIX: 사이트가 본문을 KaTeX 로 렌더링해서 홀로 있는 '$' 가 수식 시작으로 읽혀
     뒤 문장이 깨진다. 그래서 '$99' 를 한국어 표기 '99달러' 로 바꾼다.
  3) ESSAY: 서술형에 모범답안을 붙인다(slides, model, qko, answer, answer_ko).
     근거는 lesson\I3_*.json 의 pass3(자세히)와 notes\slides_w3.json, I3 슬라이드 그림이다.
     points 배열이 채점 항목이므로 answer 는 그 항목을 순서대로 담는다.
  4) REWRITE: 원본 문항의 내용을 바꿔 쓰는 자리. 지금은 비어 있고, 되도록 비워 둔다.
     이미 커밋된 id 의 내용을 바꾸면 그 번호를 푼 학생의 오답노트가 다른 문제를 가리킨다.
     문항을 새로 쓰기로 했다면 id 도 새로 주고 옛 번호는 물린다
     (tools\checkers\bank_history.py 가 이것을 잡는다).
"""
import json, os
import optshuffle
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "_src", "prev", "unit3", "bank_unit3.json")
OUT = os.path.join(HERE, "w3_prev.json")

# ---------------------------------------------------------------- 원본 id (순서 고정)
IDS = [
    "w3p-c8070579",
    "w3p-7f4ca8fa",
    "w3p-27f5ce8e",
    "w3p-4612cd2a",
    "w3p-7ed61e10",
    "w3p-f7d3faf3",
    "w3p-558d3821",
    "w3p-ec700cbf",
    "w3p-7a2f02b0",
    "w3p-4af70ae1",
    "w3p-0c397124",
    "w3p-f1b59734",
    "w3p-5161fed0",
    "w3p-48165cdf",
    "w3p-382df745",
    "w3p-bfb5277d",
    "w3p-67246f44",
    "w3p-2b9b39f0",
    "w3p-91526dfb",
    "w3p-100a707b",
    "w3p-c8b1db5c",
    "w3p-7b079eaf",
    "w3p-41683ec7",
    "w3p-966a39e7",
    "w3p-9b7128df",
    "w3p-c295f52d",
    "w3p-77379809",
    "w3p-1b722263",
    "w3p-b8f88795",
    "w3p-6c59bb14",
    "w3p-b74e219e",
    "w3p-e782417a",
    "w3p-70a21cb4",
    "w3p-c5830f60",
    "w3p-6c69644d",
    "w3p-4335ac74",
    "w3p-8c73a219",
    "w3p-e2e92091",
    "w3p-ddaa2ecf",
    "w3p-975440fc",
    "w3p-dd7fa663",
    "w3p-6caf53b3",
    "w3p-35bd549d",
    "w3p-168ea070",
    "w3p-b9733089",
    "w3p-1be7c13a",
    "w3p-2f3e605e",
    "w3p-54b42102",
    "w3p-045273e5",
    "w3p-9bda4c3d",
    "w3p-c8b47f82",
    "w3p-67b17178",
    "w3p-423c85a1",
    "w3p-f9e341e2",
    "w3p-3be5661c",
    "w3p-47fe329c",
    "w3p-1e5cd9b6",
    "w3p-4f93e5e3",
    "w3p-42b770d5",
    "w3p-cf20082d",
    "w3p-2a894815",
    "w3p-8e9ea2cf",
    "w3p-d49161cd",
    "w3p-63195dd5",
    "w3p-a0e0d13d",
    "w3p-9b656903",
    "w3p-8d533937",
    "w3p-5708f0f5",
    "w3p-e0e20a1d",
    "w3p-e76a3705",
    "w3p-4ad0f607",
    "w3p-c67d097f",
    "w3p-102b0aa9",
    "w3p-012099ef",
    "w3p-0d0b234c",
    "w3p-f55cf0e1",
    "w3p-cc1b0b89",
    "w3p-273e8f88",
    "w3p-f7ea5e6c",
    "w3p-20a4e78d",
    "w3p-fc2eaa0e",
    "w3p-1cba291f",
    "w3p-a3011c1b",
    "w3p-936235f4",
    "w3p-0db098fc",
    "w3p-4e80dada",
    "w3p-15f1561a",
    "w3p-2e9d9ab3",
    "w3p-b6cfe17e",
    "w3p-609e35c3",
    "w3p-3cf913bb",
    "w3p-622f01bd",
    "w3p-ea63f820",
    "w3p-522e69b5",
    "w3p-df4d9d2f",
    "w3p-8758738a",
    "w3p-3c78c921",
    "w3p-0da8b152",
    "w3p-26c848bc",
    "w3p-5d7c6344",
    "w3p-49acb435",
    "w3p-786e3efd",
    "w3p-a5dc1f58",
    "w3p-d6b606dc",
    "w3p-635a20b7",
    "w3p-aa0c1bf9",
    "w3p-a6522ffa",
    "w3p-ec65b7f8",
    "w3p-a64986cc",
    "w3p-85605c1d",
    "w3p-05162272",
    "w3p-d43f6c08",
    "w3p-df497b70",
    "w3p-9858821e",
    "w3p-e6150727",
    "w3p-3835c33d",
    "w3p-5c0602d5",
    "w3p-549783aa",
    "w3p-e0b01732",
    "w3p-5c31c7d0",
    "w3p-8a925644",
    "w3p-255bfad8",
    "w3p-e9527102",
    "w3p-bd91051e",
    "w3p-b4d6eeeb",
    "w3p-5333879f",
    "w3p-8a9692f2",
    "w3p-2c94863c",
    "w3p-25607e14",
    "w3p-a152d528",
    "w3p-eb84b0c6",
    "w3p-1a24766b",
    "w3p-46a7312b",
    "w3p-9f19d14e",
    "w3p-192462e9",
    "w3p-3c8c2a3f",
    "w3p-0adfc31d",
    "w3p-267b5a3e",
    "w3p-004a442d",
    "w3p-a8788069",
    "w3p-5aa23657",
    "w3p-d9b977de",
    "w3p-1724bd99",
    "w3p-fe63649a",
    "w3p-b4d0fded",
    "w3p-7199c4ac",
    "w3p-d5073655",
    "w3p-c90736db",
    "w3p-d6d136fa",
    "w3p-0dc4570e",
    "w3p-0e6a7445",
    "w3p-c1552452",
    "w3p-61d6c9de",
    "w3p-ea5b9ff9",
    "w3p-afd3d4e4",
    "w3p-b021c263",
    "w3p-6824040f",
    "w3p-a4c43965"
]

# ---------------------------------------------------------------- KaTeX 깨짐 방지
TEXT_FIX = {"$99": "99달러"}

# ---------------------------------------------------------------- 문항 내용 교체 (비어 있음)
# 원본은 "Zigbee PAN을 최초 생성하고 보안 및 라우팅 테이블을 총괄하는 장치는?" 을
# mcq(w3p-b8f88795) 와 short(w3p-eb84b0c6) 로 두 번 묻는다. 같은 주차 안에서 같은 사실을
# 유형만 바꿔 두세 번 묻는 것은 work\_rules\문제은행_작성규칙.md 가 허용하는 형태라
# 중복이 아니다. 한때 short 자리를 다른 문항으로 바꿔 썼으나, 이미 커밋된 id 의 내용을
# 바꾸면 그 번호를 푼 학생의 기록이 엉뚱한 문제를 가리키므로 원본으로 되돌렸다.
# 이 칸은 비워 두고, 문항을 새로 쓸 일이 있으면 id 를 새로 준다.
REWRITE = {}

# ---------------------------------------------------------------- 서술형 모범답안
ESSAY = {
    "w3p-0e6a7445": {
        "slides": "I3 p.4-6",
        "model": "hub-vs-hubless-tradeoff",
        "qko": "두 연결 방식을 철학, 연결 구조, 확장성, 인터넷 단절, 배터리, 실무 판단까지 나란히 비교해 쓰라는 문제예요.",
        "answer": "허브 방식(Hub-based Type)은 집 전체를 한 팀으로 보는 공간 중심(Space-centric) 로컬 자율망이고, 논허브 방식(Hubless Type)은 기기 하나하나를 따로 보는 기기 중심(Device-centric) 직결망이다. 연결 구조를 보면 허브 방식은 Zigbee, Thread, Z-Wave, Matter 기기가 세대 내 전용 허브를 경유하고, 논허브 방식은 개별 기기가 Wi-Fi 공유기나 스마트폰(BLE Mesh)에 직접 연결된다. 기기 확장성은 허브 1대당 100~200개 이상을 안정적으로 관제하는 반면, 논허브 방식은 기기 과다 접속 시 AP(Access Point) 성능 저하가 우려된다. 인터넷 단절 시 허브 방식은 로컬 1-Loop(Local 1-Loop) 자율 제어를 유지하지만, 논허브 방식은 클라우드 의존 기능의 제어가 제한될 수 있다. 배터리 지속성도 허브 방식 센서는 2~3년 이상 장기 구동하고, 논허브 방식은 상시 전원 위주여서 잦은 충전이 필요하다. 실무 판단은 여러 센서와 기기를 하나의 자동화 시나리오로 통합해야 하면 허브 투자가 필수이고, 조명 품질과 개별 제어만 필요하면 허브 없이도 충분하므로 두 방식은 우열이 아니라 대등한 대안이다.",
        "answer_ko": "허브 방식은 반 반장이 있는 반이에요. 센서들이 반장에게 먼저 말하고, 반장이 집 안에서 판단해요. 논허브 방식은 반장 없이 기기마다 공유기나 스마트폰에 바로 붙는 반이에요. 반장이 있으면 기기를 100~200개 이상 붙일 수 있고, 배터리 센서도 2~3년 가고, 인터넷이 끊겨도 집 안에서 계속 돌아요. 반장이 없으면 처음 돈은 덜 들지만 기기가 많아지면 공유기가 힘들어하고, 먼 곳의 큰 도서관(클라우드)에 기대는 기능은 멈출 수 있어요. 조명만 예쁘게 쓰고 싶으면 반장이 없어도 되고, 문과 센서와 조명을 함께 움직이려면 반장이 꼭 필요해요."
    },
    "w3p-c1552452": {
        "slides": "I3 p.7",
        "model": "wpan-low-power-tradeoff",
        "qko": "빠른 Wi-Fi가 이미 있는데도 느린 WPAN을 쓰는 까닭을 전력, 배터리, 크기, 공간 적용까지 이어서 설명하라는 문제예요.",
        "answer": "WPAN(Wireless Personal Area Network)은 IEEE 802.15 표준을 기반으로 사람이나 가정을 중심으로 수 미터에서 수십 미터 반경의 기기를 저전력으로 연결하는 무선망이다. Wi-Fi는 고속 전송 특성상 전력 소모가 매우 커서, 배터리로 구동하면 기기가 두껍고 투박해져 인테리어를 해친다. 그래서 WPAN은 속도를 양보하는 대신 초소형 동전 배터리 1개로 2~3년 작동하는 초저전력 센서 환경을 얻는 물리적 트레이드오프(Trade-off)를 택한다. 실제로 Wi-Fi 센서는 2~3개월마다 충전해야 하지만 WPAN 센서는 24~36개월, 곧 2~3년을 지속한다. 배터리가 작아지면 센서의 부피도 크게 줄어 벽, 천장, 가구 속에 눈에 띄지 않게 매립할 수 있고, 슬라이드는 이를 보이지 않음(Invisibility)이라고 부른다. 결과적으로 배선 공사의 한계를 극복해 공간 배치의 자유도를 확보하는 것이 저속 WPAN을 쓰는 이유이다.",
        "answer_ko": "센서가 보내는 말은 '문 열렸어요' 같은 아주 짧은 소식이라 빠를 필요가 없어요. 그런데 Wi-Fi처럼 빠른 무선은 전기를 많이 먹어서, 배터리가 커지고 센서가 두꺼워져요. 그래서 속도를 조금 포기하고 전기를 아주 적게 쓰는 WPAN을 골라요. Wi-Fi 센서는 2~3개월마다 충전해야 하는데, WPAN 센서는 동전 배터리 하나로 24~36개월, 곧 2~3년을 버텨요. 센서가 작고 얇아지니 벽이나 가구 속에 숨길 수 있어서, 감각기관 같은 센서를 인테리어를 해치지 않고 원하는 자리에 둘 수 있어요."
    },
    "w3p-61d6c9de": {
        "slides": "I3 p.8, p.11",
        "model": "hub-roles-and-placement",
        "qko": "허브가 하는 일 세 가지와 허브를 어디에 둘지 정하는 원칙 세 가지를 차례로 쓰라는 문제예요.",
        "answer": "역할 ① 프로토콜 번역(Protocol Translation, 이종 통신 브릿지)은 저전력 센서의 WPAN 신호를 TCP/IP 기반 인터넷과 홈 네트워크 언어로 상호 변환하는 일이다. 역할 ② 로컬 오케스트레이션(Local Orchestration, 1-Loop 로컬 실행)은 외부 인터넷망이 마비되어도 허브가 센싱 데이터를 판단해 조명과 밸브를 제어하는 일이다. 역할 ③ 보안 및 디바이스 관리(네트워크 게이트웨이)는 기기 등록(Commissioning), 암호화 키 분배, 상태 동기화, 펌웨어 업데이트를 맡는다.\n원칙 1 기하학적 중심 배치는 현관 구석이 아니라 거실 중앙에 두어 반경 10m의 구형 무선 커버리지를 확보하는 것이다. 원칙 2 상시 전원(L1) 콘센트 단독 확보는 스위치로 꺼지는 콘센트를 금지하고 24시간 안정 전원을 쓰는 것이다. 원칙 3 금속 차폐 및 전파 간섭 회피는 금속 분전반 속이나 대형 냉장고 뒤편 매립을 금지해 신호 차단과 모터 노이즈를 막는 것이다.",
        "answer_ko": "허브는 반 반장이에요. 첫째, 센서가 쓰는 말과 인터넷이 쓰는 말이 달라서 반장이 통역을 해요. 둘째, 인터넷이 끊겨도 반장이 집 안에서 판단해 불을 켜고 밸브를 잠가요. 셋째, 새 기기를 등록하고 비밀 열쇠를 나눠 주고 상태를 맞추고 업데이트를 챙겨요. 앉힐 자리는 세 가지만 기억해요. 집 한가운데(거실 중앙)에 두어 반경 10m가 고르게 퍼지게 하고, 절대 꺼지지 않는 콘센트를 혼자 쓰게 하고, 금속 분전함 속이나 냉장고 뒤는 피해요."
    },
    "w3p-ea5b9ff9": {
        "slides": "I3 p.14, p.17",
        "model": "frequency-dual-design",
        "qko": "두 주파수 대역을 프로토콜, 파장, 정책, 혼잡도, 쓰임새로 비교한 뒤 설계 황금률까지 쓰라는 문제예요.",
        "answer": "2.4GHz 대역은 지그비(Zigbee), BLE와 BLE Mesh, 스레드(Thread), 와이파이(Wi-Fi)가 쓰고, 900MHz(Sub-1GHz) 대역은 지웨이브(Z-Wave)가 쓴다. 2.4GHz는 파장이 짧아 직진성이 강하고 벽체를 통과할 때 감쇠가 크지만, 900MHz는 파장이 길어 회절(Diffraction)과 투과력(Penetration)이 우수하다. 주파수 정책에서 2.4GHz는 전 세계 공용 ISM 비면허 대역이고, 900MHz는 국가별 전용 할당으로 한국은 920.9~923.1MHz이다. 채널 혼잡도는 2.4GHz가 Wi-Fi, 전자레인지 등과 간섭해 혼잡한 반면, 900MHz는 Wi-Fi 간섭이 없어 매우 쾌적하다. 그래서 공간 설계에서는 실내 조명, 환경 센서, 스마트 플러그를 2.4GHz에 두고 도어락, 침입 감지 센서 같은 보안 설비를 900MHz에 둔다. 주파수 설계 황금률은 대량의 조명과 환경 센서는 2.4GHz Zigbee/Thread로, 도어락과 보안 센서는 900MHz Z-Wave로 이원화하는 것이다.",
        "answer_ko": "주파수 대역은 라디오 채널과 같아요. 2.4GHz는 모두가 듣는 인기 채널이라 조명, 온습도 센서, 플러그가 다 여기 있고, 대신 붐벼서 전자레인지나 공유기와 부딪히고 벽을 만나면 힘이 많이 빠져요. 900MHz는 한적한 채널이라 벽을 잘 돌아 들어가고 Wi-Fi와 부딪히지 않아서, 끊기면 안 되는 도어락과 침입 감지 센서에 좋아요. 다만 이 한적한 채널 번호는 나라마다 달라서, 국내용은 920.9~923.1MHz인지 꼭 확인해요. 그래서 수가 많은 조명과 센서는 2.4GHz Zigbee/Thread, 문단속 기기는 900MHz Z-Wave로 나누는 것이 황금률이에요."
    },
    "w3p-afd3d4e4": {
        "slides": "I3 p.15, p.21",
        "model": "zigbee-mesh-nodes",
        "qko": "Zigbee의 세 가지 노드 역할을 쓰고, 그물망 구조가 왜 유리한지까지 설명하라는 문제예요.",
        "answer": "지그비(Zigbee)는 IEEE 802.15.4 표준을 기반으로 한 2.4GHz 저전력 무선 통신 규격으로, 기기 간 메쉬(Mesh)로 신호를 중계해 넓은 통신 거리를 확보한다. 코디네이터(Coordinator)는 Zigbee PAN을 최초로 생성하고 보안과 라우팅 테이블을 총괄하는 중심 장치로, 실제로는 스마트 허브가 맡는다. 라우터(Router)는 220V 상시 전원을 받는 스마트 스위치, 플러그, 조명으로, 신호를 중계해 네트워크 범위를 확장한다. 엔드 디바이스(End Device)는 배터리 센서류로, 전력을 아끼기 위해 평소 Sleep 상태를 유지하고 신호를 중계하지 않는다. 메쉬 구조의 장점은 라우터끼리 서로 연결되어 있어 하나가 끊겨도 다른 경로로 우회할 수 있다는 점, 곧 자가 치유(Self-Healing)이다. 또 상시전원 라우터가 중계해 주므로 배터리 센서는 통신 거리를 늘리면서도 저전력을 유지해 수년간 교체 없이 쓸 수 있다.",
        "answer_ko": "메시 네트워크는 친구끼리 쪽지 릴레이예요. 반장(코디네이터)은 반을 처음 만들고 보안과 길 안내를 맡는 스마트 허브예요. 늘 깨어 있는 친구(라우터)는 벽 전기를 받는 스위치, 플러그, 조명이고, 쪽지를 옆으로 건네 신호가 닿는 범위를 넓혀요. 잠자는 친구(엔드 디바이스)는 배터리 센서라서 필요할 때만 깨서 말하고, 쪽지를 건네지는 않아요. 릴레이 길이 여러 갈래라 한 친구가 빠져도 다른 길로 돌아가고(자가 치유), 깨어 있는 친구가 대신 날라 주니 배터리 센서는 몇 년씩 전기를 아낄 수 있어요."
    },
    "w3p-b021c263": {
        "slides": "I3 p.18, p.20",
        "model": "nfc-vs-uwb",
        "qko": "NFC와 UWB를 원리, 막아 주는 공격, 도면 적용까지 나란히 비교해 쓰라는 문제예요.",
        "answer": "NFC(Near Field Communication)는 13.56MHz 전자기 유도를 이용해 10cm 이내에서 데이터를 교환하는 근거리 무선 통신으로, 표준 규격은 ISO/IEC 18092이고 최대 연결은 1:1 페어링이다. 물리적 접촉 수준의 거리만 인식하므로 멀리서 몰래 엿듣는 스니핑(Sniffing)을 원천 차단하며, 도면 적용은 현관 스마트 도어락 카드키와 월패드 출입 인증 모듈이다. UWB(Ultra Wide Band)는 500MHz 이상의 광대역 주파수와 나노초 펄스로 cm 단위의 거리와 방향을 측정하는 기술로, 표준 규격은 IEEE 802.15.4z이고 주파수 대역은 3.1~10.6GHz이다. 오차 5~10cm 수준의 정밀도로 실제 거리를 재기 때문에, 멀리 있는 열쇠 신호를 이어 붙이는 릴레이 공격(Relay Attack)을 완벽히 차단한다. 도면 적용은 주머니 속 폰이나 키 태그를 지니면 자동으로 열리는 핸즈프리 도어락이다. 정리하면 NFC는 가까워야 통하는 성질로 접촉 인증을 지키고, UWB는 떨어져도 정확히 재는 성질로 정밀 측위와 보안을 지킨다.",
        "answer_ko": "NFC는 교통카드처럼 톡 갖다 대야 통하는 무선이에요. 10cm 안에서만 통하니까 멀리서 몰래 엿듣기(스니핑)가 안 되고, 현관 도어락 카드키나 월패드 출입 인증에 써요. UWB는 아주 넓은 대역으로 짧은 펄스를 쏘아 거리와 방향을 5~10cm 오차로 재는 무선이에요. 거리를 정확히 재니까, 멀리 있는 열쇠 신호를 몰래 끌어와 문을 여는 속임수(릴레이 공격)에 속지 않아요. 그래서 주머니에 폰만 넣고 다가가면 열리는 핸즈프리 도어락에 써요. 숫자는 NFC 13.56MHz에 10cm 이내, UWB 3.1~10.6GHz에 오차 5~10cm로 짝지어 외우면 편해요."
    },
    "w3p-6824040f": {
        "slides": "I3 p.23-26, p.32",
        "model": "matter-thread-hca-strategy",
        "qko": "Matter, Thread, HCA가 각각 무엇인지 정리하고 이 셋을 어떻게 나눠 쓰는지 전략까지 쓰라는 문제예요.",
        "answer": "매터(Matter)는 기존 Zigbee Alliance가 Apple, Google, Amazon, Samsung 등을 모아 개편한 CSA(Connectivity Standards Alliance) 주도로 2022년 출시된 IP 기반 통합 애플리케이션 계층 표준으로, 경쟁 플랫폼 간 파편화를 해결하고 로컬 직접 제어로 클라우드 의존을 낮추어 보안을 높인다. Matter 프로토콜 스택은 BLE로 기기를 간편하게 초기 등록하고, 저전력 센서는 스레드(Thread, IPv6/UDP)로, 대용량 가전은 Wi-Fi/Ethernet(IPv6/TCP)으로 분업하며, 물리 계층은 표준 2.4GHz 무선 칩셋을 쓴다. Thread는 Zigbee와 같은 2.4GHz를 쓰면서도 모든 기기에 독립된 IPv6 주소를 부여해 IP 네트워크와 직접 통신하는 Matter 최적화 저전력 메쉬 프로토콜이다. Thread 보더 라우터(Thread Border Router)는 Wi-Fi망과 Thread망 사이에서 별도 게이트웨이 번역 없이 패킷을 직접 전달하며, HomePod mini, Nest Hub 같은 Matter 지원 허브와 스피커에 내장된 기능이고, 한 대가 다운되어도 다른 보더 라우터가 즉시 복구하는 자가 치유(Self-Healing)를 제공한다. HCA(Home Connectivity Alliance)는 대형 가전 제조사가 빅테크에 가전 생태계 주도권을 넘겨주지 않기 위해 결성한 클라우드(C2C) 연합으로, 제조사 서버를 경유해 통신한다. 따라서 차세대 표준 전략은 소형 센서 인프라는 Matter/Thread 로컬망으로 구축하고, 대형 가전은 HCA 클라우드 연동을 보조적으로 활용하는 이원화이다.",
        "answer_ko": "Matter는 회사가 달라도 서로 알아듣는 공통 언어(프로토콜)예요. 애플, 구글, 아마존, 삼성이 함께 만든 약속이라 어느 앱에서나 같은 기기를 쓸 수 있어요. Thread는 그 말을 나르는 길이에요. 기기마다 인터넷 주소(IPv6)가 있어서 통역사 없이 바로 대화하고, 집 안 스피커나 허브에 든 보더 라우터가 Wi-Fi와 이어 줘요. HCA는 대형 가전 회사들이 뭉친 쪽인데, 먼 곳의 큰 도서관(클라우드)을 거쳐 연결해요. 그래서 작고 빨라야 하는 센서와 조명은 Matter와 Thread로 집 안에서 처리하고, 냉장고나 세탁기 같은 큰 가전은 HCA를 보조로 쓰는 것이 전략이에요."
    },
    "w3p-a4c43965": {
        "slides": "I3 p.27-30",
        "model": "attenuation-and-diagnosis",
        "qko": "어떤 마감재가 전파를 얼마나 막는지 쓰고, 신호 품질을 재는 네 지표의 기준값까지 쓰라는 문제예요.",
        "answer": "철근 콘크리트 내력벽은 2.4GHz 전파를 강하게 차단해 10~15dB가 감쇠하므로, 벽을 넘어가는 방마다 상시전원 라우터를 배치해야 한다. 금속 중문과 대형 가전 외판은 전파를 통과시키지 못하고 대부분 반사하며, 대형 거울은 뒷면 은막 코팅 때문에 반사, 차단이 일어나므로 냉장고 뒤편과 드레스룸, 욕실 거울 뒤편 센서 매립은 회피한다. 대형 수족관이나 플랜테리어는 물 분자가 2.4GHz 고주파를 직접 흡수하므로 신호가 돌아가도록 우회 라우터를 둔다.\nRSSI(Received Signal Strength Indicator)는 전파의 물리적 세기로, -50dBm 이상이면 우수하고 -75dBm 이하면 음영지역과 패킷 손실이 발생한다. LQI(Link Quality Indicator)는 0~255 스케일의 통신 건전성으로, 200 이상이면 안정적이고 100 이하면 통신 에러와 반응 지연이 빈발한다. SNR(Signal to Noise Ratio)은 유효 신호 대비 주변 잡음(Noise Floor)의 비율로, 20dB 이상이면 양호하고 10dB 이하면 전자레인지, 공유기 등의 간섭이 심각하다. 패킷 재전송률(Packet Retry Rate)은 통신 에러로 재전송한 비율로, 5% 미만이면 정상이고 15% 이상이면 지연과 배터리 조기방전이 생겨 라우터를 추가해야 한다.",
        "answer_ko": "전파는 벽을 지날 때마다 힘이 빠져요. 철근 콘크리트 벽 한 장이 10~15dB, 곧 세기를 10배에서 30배쯤 줄이니까 벽 넘어 방마다 늘 깨어 있는 중계 기기를 둬요. 금속 중문과 냉장고 외판은 전파를 튕겨 내고, 큰 거울도 뒤에 바른 금속 막이 막고, 수족관은 물이 전파를 먹어 버려요. 신호 상태는 건강검진표처럼 네 가지로 봐요. 목소리 크기 RSSI는 -50dBm 이상이면 좋고 -75dBm 이하면 그늘, 또렷함 LQI는 200 이상이면 좋고 100 이하면 나쁨, 소음 대비 목소리 SNR은 20dB 이상이면 좋고 10dB 이하면 시끄러움, 같은 말 반복인 재전송률은 5% 미만이면 정상이고 15% 이상이면 중계 기기를 더 놓아야 해요."
    }
}

# ================================================================= 조립


def fix(o):
    if isinstance(o, str):
        for a, b in TEXT_FIX.items():
            o = o.replace(a, b)
        return o
    if isinstance(o, list):
        return [fix(x) for x in o]
    if isinstance(o, dict):
        return {k: fix(v) for k, v in o.items()}
    return o


src = json.load(open(SRC, encoding="utf-8"))
assert len(src) == len(IDS), f"원본 {len(src)}문항 vs IDS {len(IDS)}개"

bank = []
for q, qid in zip(src, IDS):
    it = fix(dict(q))
    it["level"] = "basic"
    it["id"] = qid
    if it["type"] == "essay":
        assert qid in ESSAY, f"{qid}: 모범답안 없음"
        it.update(ESSAY[qid])
    if qid in REWRITE:
        before = set(it)
        it.update(REWRITE[qid])
        assert set(it) == before, f"{qid}: REWRITE 가 필드 구성을 바꿈"
    bank.append(it)

assert len(ESSAY) == sum(1 for q in bank if q["type"] == "essay"), "ESSAY 개수 불일치"
assert set(REWRITE) <= {q["id"] for q in bank}, "REWRITE id 불일치"
assert len({q["id"] for q in bank}) == len(bank), "id 중복"
# 한 파일은 한 주차다. 같은 주차 안에서 같은 사실을 객관식과 단답으로 두 번 묻는 것은
# work\_rules\문제은행_작성규칙.md 가 허용하는 형태이므로 유형을 키에 넣는다.
assert len({(q["type"], " ".join(q["q"].split())) for q in bank}) == len(bank), "같은 유형의 질문 문장 중복"

# ------------------------------------------------- 보기 자리 섞기
# 정답이 한 자리에 몰리면 내용을 몰라도 같은 번호만 찍어 맞힐 수 있다. 그래서
# 파일에 쓰기 직전에 보기 자리를 섞는다(까닭과 예외는 optshuffle.py 에). id 는 IDS 가 지킨다.
optshuffle.shuffle_bank(bank)

json.dump(bank, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

txt = open(OUT, encoding="utf-8").read()
for ch in ("\u2014", "\u2013", "\u00b7", "\uff65"):
    assert ch not in txt, f"금지 문자 {repr(ch)}"


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, list):
        for x in o:
            yield from strings(x)
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)


for q in bank:
    for s in strings(q):
        assert s.count("$") % 2 == 0, f"{q['id']}: $ 짝 안 맞음 {s[:40]}"
    if q["type"] == "essay":
        for f in ("slides", "model", "q", "qko", "answer", "answer_ko", "points"):
            assert q.get(f), f"{q['id']}: '{f}' 없음"

print(OUT, len(bank), dict(Counter(q["type"] for q in bank)))
print("서술형", sum(1 for q in bank if q["type"] == "essay"), "개 모범답안 확인")
