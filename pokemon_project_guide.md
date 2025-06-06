# Pokemon Pocket Simulator 프로젝트 가이드

## 📋 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [파일 구조 및 역할](#파일-구조-및-역할)
3. [데이터 형식 및 규칙](#데이터-형식-및-규칙)
4. [사용법 가이드](#사용법-가이드)
5. [확률 계산 타입 가이드](#확률-계산-타입-가이드)
6. [테스트 파일 가이드](#테스트-파일-가이드)
7. [개발 가이드](#개발-가이드)
8. [확장성 및 향후 계획](#확장성-및-향후-계획)

---

## 🎯 프로젝트 개요

### 목적
Pokemon Pocket 모바일 카드게임의 확률 계산을 위한 Python 시뮬레이터

### 주요 기능
- 덱 구성별 확률 계산
- 카드 효과 시뮬레이션
- 복합 조건 확률 분석
- 드로우 순서 최적화

### 현재 버전: v2.02
- **v1.0**: 기본 시뮬레이션 + 확률 계산
- **v2.01**: Iono 카드 + Pokemon Communication 추가
- **v2.02**: 복합 확률 계산 3종 + Iono 스마트 로직

---

## 📁 파일 구조 및 역할

### 🔧 핵심 모듈
```
pokemon-pocket-simulator/
├── main_simulator.py      # 메인 시뮬레이션 엔진 (25개 함수)
├── probability_calculator.py  # 확률 계산 로직 (15개 함수)
├── card_effects.py        # 카드 효과 구현 (11개 함수)
└── run_all_tests.py       # 통합 테스트 실행기
```

### 📊 설정 파일
```
├── DeckList.txt          # 덱 구성 입력 파일
├── TestCase.txt          # 테스트 케이스 정의 파일
├── run_simulator.bat     # Windows 실행 스크립트
└── run_simulator.ps1     # PowerShell 실행 스크립트
```

### 🧪 테스트 파일
```
├── test_iono_count.py    # Iono 장수별 성능 비교 (v2.02)
├── test_composite.py     # 복합 확률 계산 테스트 (v2.02)
└── __pycache__/          # Python 캐시 폴더
```

### 📚 문서 파일
```
├── README.md             # 프로젝트 개요 및 버전 정보
├── PROJECT_GUIDE.md      # 상세 기술 문서
└── pokemon_project_Github_guide.md  # GitHub 워크플로우 가이드
```

---

## 🎮 데이터 형식 및 규칙

### 카드 타입 (7가지)
```python
CARD_TYPES = [
    "Basic Pokemon",      # 기본 포켓몬
    "Stage1 Pokemon",     # 1진화 포켓몬  
    "Stage2 Pokemon",     # 2진화 포켓몬
    "Item",              # 아이템
    "Pokemon Tool",      # 포켓몬의 도구
    "Item(fossil)",      # 아이템(화석)
    "Supporter"          # 서포트
]
```

### 덱 구성 제약사항
- **총 카드 수**: 정확히 20장
- **카드별 제한**: 동일 카드 최대 2장 (0~2장)
- **Basic Pokemon 필수**: 시작 5장에 최소 1장 보장

### 드로우 카드 목록 (v2.02 기준)
```python
DRAW_CARDS = [
    "Poke Ball",              # Basic Pokemon 서치
    "Professor's Research",   # 2장 드로우
    "Galdion",               # Type:Null/Silvally 서치
    "Iono"                   # 손패 셔플 후 3장 드로우
]
```

### 카드명 규칙
- **한글 카드**: "파이리", "리자몽", "꼬부기" 등
- **영어 카드**: "Poke Ball", "Professor's Research" 등
- **특수 카드**: "Type:Null", "rare candy" 등
- **대소문자 구분**: 정확한 카드명 사용 필수

---

## 📖 사용법 가이드

### DeckList.txt 작성법

#### 형식
```
카드명 | 카드타입 | 장수
```

#### 실제 예시
```
Blacephalon | Basic Pokemon | 2
Type:Null | Basic Pokemon | 2
Silvally | Stage1 Pokemon | 2
Poke Ball | Item | 2
Giant Cape | Pokemon Tool | 2
Professor's Research | Supporter | 2
```

#### 작성 규칙
1. **구분자**: 파이프(`|`) 사용, 앞뒤 공백 허용
2. **총 20장**: 모든 카드 count 합계가 정확히 20
3. **카드명**: 대소문자 정확히 입력
4. **카드타입**: 7가지 중 정확한 타입명 사용
5. **장수**: 0~2 사이의 정수

### TestCase.txt 작성법

#### 형식 (JSON)
```json
{
    "name": "테스트 케이스 설명",
    "request": {
        "type": "계산_타입",
        "target_cards": ["카드1", "카드2"],
        "turn": 턴수
    }
}
```

#### 실제 예시
```json
{
    "name": "선호 시작: Type:Null 또는 Blacephalon으로 시작",
    "request": {
        "type": "preferred_opening",
        "preferred_basics": ["Type:Null", "Blacephalon"]
    }
}
{
    "name": "3턴까지 Blacephalon + BalsMine 각각 1장 이상 드로우 확률",
    "request": {
        "type": "multi_card",
        "target_cards": ["Blacephalon", "BalsMine"],
        "turn": 3
    }
}
```

#### 작성 규칙
1. **JSON 형식**: 각 테스트 케이스는 독립된 JSON 객체
2. **name 필수**: 테스트 케이스 설명
3. **request 필수**: 계산 요청 내용
4. **타입별 필수 필드**: 각 계산 타입마다 다름

---

## 🎲 확률 계산 타입 가이드

### 기본 확률 계산 (v1.0-v2.01)

#### 1. preferred_opening
**목적**: 특정 Basic Pokemon으로 시작할 확률
```json
{
    "type": "preferred_opening",
    "preferred_basics": ["파이리", "꼬부기"]
}
```
**출력**: `{'probability_percent': 65.50, 'success_count': 1310, 'total_valid_games': 2000}`

#### 2. non_preferred_opening  
**목적**: 특정 Basic Pokemon이 아닌 카드로 시작할 확률
```json
{
    "type": "non_preferred_opening", 
    "non_preferred_basics": ["파이리"]
}
```

#### 3. multi_card
**목적**: N턴까지 여러 카드를 각각 1장씩 확보할 확률
```json
{
    "type": "multi_card",
    "target_cards": ["파이리", "리자몽"],
    "turn": 2
}
```

#### 4. specific_by_turn
**목적**: N턴까지 특정 카드를 드로우할 확률  
```json
{
    "type": "specific_by_turn",
    "target_cards": ["파이리"],
    "turn": 1
}
```

#### 5. three_cards_by_turn
**목적**: N턴까지 3종류 카드를 각각 1장씩 확보할 확률
```json
{
    "type": "three_cards_by_turn",
    "target_cards": ["파이리", "리자몽", "rare candy"],
    "turn": 2
}
```

### 복합 확률 계산 (v2.02 신규)

#### 6. preferred_and_multi
**목적**: 선호 Basic으로 시작하면서 목표 카드들을 모두 확보하는 확률 (AND 조건)
```json
{
    "type": "preferred_and_multi",
    "preferred_basics": ["파이리"],
    "target_cards": ["파이리", "리자몽", "rare candy"],
    "turn": 2
}
```
**활용**: "좋은 시작 + 콤보 완성" 확률

#### 7. non_preferred_and_multi
**목적**: 나쁜 시작이지만 리커버리 카드를 확보하는 확률
```json
{
    "type": "non_preferred_and_multi",
    "non_preferred_basics": ["꼬부기"],
    "target_cards": ["LEAF"],
    "turn": 2
}
```
**활용**: "나쁜 시작 → 리커버리" 확률

#### 8. multi_or_multi
**목적**: 여러 목표 그룹 중 하나라도 완성하는 확률 (OR 조건)
```json
{
    "type": "multi_or_multi",
    "target_groups": [
        {"name": "파이리 라인", "target_cards": ["파이리", "리자몽", "rare candy"]},
        {"name": "꼬부기 라인", "target_cards": ["꼬부기", "거북왕", "rare candy"]}
    ],
    "turn": 3
}
```
**활용**: "전략 A OR 전략 B" 확률

### 시뮬레이션 횟수 권장값
- **빠른 테스트**: 1,000~2,000회 (±1% 오차)
- **일반 사용**: 5,000~10,000회 (±0.5% 오차)  
- **정밀 분석**: 50,000~100,000회 (±0.2% 오차)

---

## 🧪 테스트 파일 가이드

### test_iono_count.py
**목적**: Iono 카드 장수별 성능 비교
**생성일**: 2025-06-05 (v2.02)
**배경**: Iono가 0장, 1장, 2장일 때 어떤 차이가 있는지 분석 필요
```python
# 테스트 내용
- Iono 0장 (Red Card 2장 대체)
- Iono 1장 (Red Card 1장 혼용) 
- Iono 2장 (Red Card 0장)
```
**결과 예시**: 0장(48.40%) → 1장(53.52%) → 2장(54.02%)
**실행법**: `python test_iono_count.py`

### test_composite.py
**목적**: v2.02 신규 복합 확률 계산 기능 테스트
**생성일**: 2025-06-05 (v2.02)
**배경**: preferred_and_multi, non_preferred_and_multi, multi_or_multi 검증 필요
```python
# 테스트 내용
1. 파이리 시작 + 파이리 라인 완성 (preferred_and_multi)
2. 꼬부기 시작 + LEAF 확보 (non_preferred_and_multi)
3. 파이리 라인 OR 꼬부기 라인 완성 (multi_or_multi)
```
**특징**: probability_calculator 함수들을 직접 호출
**실행법**: `python test_composite.py`

### run_all_tests.py
**목적**: 모든 테스트를 일괄 실행
**생성일**: v1.0 초기
**배경**: 개별 테스트들을 하나씩 실행하기 번거로움
**실행법**: `python run_all_tests.py`

### 테스트 파일 작성 규칙
1. **명명 규칙**: `test_기능명.py` 형식
2. **독립 실행**: 각 테스트 파일은 단독 실행 가능해야 함
3. **시뮬레이터 설정**: 반드시 `setup_simulation()` 호출
4. **결과 출력**: 명확한 성공/실패 결과 표시
5. **문서화**: 파일 상단에 목적과 사용법 주석

## 🎯 확장성 및 향후 계획

### 단기 목표
- **인게임 규칙 완벽 구현**
  - 현재 미구현된 게임 메커니즘 추가
  - 턴 제한, 에너지 시스템, 진화 규칙 등
  - 실제 게임과 100% 일치하는 시뮬레이션 환경 구축

- **확률 계산 함수 개선**
  - 기존 8가지 타입의 정확도 향상
  - 복잡한 조건 조합 지원
  - 수학적 계산과 시뮬레이션 결과 일치도 개선

- **추가적인 드로우 효과 구현**
  - 현재 4개 카드 외 추가 드로우 카드 지원
  - 조건부 드로우 효과 (특정 상황에서만 발동)
  - 연쇄 드로우 효과 및 복잡한 카드 상호작용

### 애플리케이션 기능 개발 시 목표

- **Flutter 베이스의 모바일 앱 개발**
  - Python으로 구현한 확률 계산 알고리즘을 Dart로 포팅하여 내장
  - 크로스 플랫폼 지원 (iOS/Android)
  - 오프라인 동작 가능한 독립형 앱

- **덱 이미지에서 리스트 추출**
  - 카메라/갤러리에서 덱 구성 이미지 업로드
  - 이미지 인식을 통한 자동 카드 리스트 생성
  - 인식 오류 수정을 위한 수동 편집 기능

- **이용자에 의한 추출한 덱 리스트 자유로운 수정**
  - 직관적인 카드 추가/제거 인터페이스
  - 드래그&드롭으로 카드 수량 조절
  - 덱 유효성 실시간 검증 (20장, 2장 제한 등)

- **언어 설정 (영어, 한국어, 일본어)**
  - 다국어 카드명 데이터베이스 구축
  - 언어별 카드 이미지 지원
  - 지역별 카드 메타 정보 제공

- **드로우, 플레이 시뮬레이터**
  - 단기 목표에서 구현한 인게임 규칙을 토대로 구현
  - 실제 카드를 드로우하고 플레이해보는 기능
  - 상대 플레이어까지 구현할 필요는 없음
  - 실시간 확률 계산 및 최적 플레이 제안

---

## 🔍 빠른 참조

### 필수 파일 체크리스트
- ✅ `DeckList.txt` (20장, 올바른 형식)
- ✅ `TestCase.txt` (유효한 JSON)
- ✅ 핵심 Python 파일들 존재

### 일반적인 워크플로우
1. **덱 구성** → DeckList.txt 작성
2. **테스트 설계** → TestCase.txt 작성  
3. **시뮬레이션 실행** → Python 실행
4. **결과 분석** → 확률 및 성능 검토
5. **덱 최적화** → 카드 구성 조정 후 재테스트

### 문제 해결 순서
1. **에러 메시지 확인** → 구체적인 오류 내용
2. **파일 형식 검증** → DeckList.txt, TestCase.txt
3. **환경 설정 확인** → Python, 인코딩, 권한
4. **작은 테스트** → 간단한 케이스로 검증
5. **문서 참조** → 이 가이드 + 함수 문서화

---

*최종 업데이트: 2025-06-05*  
*대상 버전: v2.02*  
*문서 목적: 프로젝트 전체 이해 및 반복 작업 최소화*