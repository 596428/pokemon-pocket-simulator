# Pokemon Pocket Simulator - 프로젝트 가이드 v2.0

## 📋 프로젝트 개요
Pokemon Pocket 카드게임의 드로우 확률을 계산하는 시뮬레이터입니다. 모듈화된 구조로 설계되어 확장과 유지보수가 용이합니다.

**프로젝트 경로**: `C:\Users\dev\Documents\GitHub\pokemon-pocket-simulator`

---

## 🎯 주요 기능
- **3가지 확률 계산 타입**: 선호하는 Opening, 비선호하는 Opening, 멀티카드 드로우
- **동적 설정 지원**: 카드 개수(1~3개) 및 턴 수(1~N턴) 자유 설정
- **카드 효과 시뮬레이션**: Poke Ball, Professor's Research, Galdion 등 드로우 카드 효과
- **외부 파일 설정**: 덱 구성과 테스트 케이스를 텍스트 파일로 관리
- **모듈화된 구조**: 기능별로 분리된 파이썬 모듈

---

## 📁 파일 구조 및 기능

### 🔧 **핵심 시뮬레이터 모듈**

#### `main_simulator.py` (메인 엔진 - 약 580줄)
**역할**: 시뮬레이터의 핵심 엔진
- **Card 클래스**: 개별 카드 객체
- **GameState 클래스**: 게임 상태 관리 (덱, 손패, 턴)
- **SimulationEngine 클래스**: 턴별 시뮬레이션 로직
- **PokemonPocketSimulator 클래스**: 메인 인터페이스 (v2.0 업데이트)
- **파일 읽기 함수들**: `load_deck_from_file()`, `load_test_cases_from_file()`

#### `probability_calculator.py` (확률 계산 - 약 230줄) ⭐ **v2.0 대폭 개선**
**역할**: 3가지 타입별 확률 계산 전문 모듈
- **ProbabilityCalculator 클래스**: 확률 계산 전용 (완전 리팩토링)
- **선호하는 Opening**: 원하는 Basic Pokemon으로 시작할 수 있는 확률
- **비선호하는 Opening**: 원하지 않는 Basic Pokemon으로만 시작해야 하는 확률  
- **멀티카드 드로우**: N턴까지 지정된 카드들을 각각 1장 이상 드로우할 확률
- **동적 설정**: 카드 개수(1~3개), 턴 수(1~N턴) 자유 설정

#### `card_effects.py` (카드 효과 - 158줄)
**역할**: 카드별 효과 구현 및 관리
- **DRAW_CARDS**: 드로우 카드 목록 정의
- **CardEffects 클래스**: 카드 효과 구현
  - `poke_ball()`: 랜덤 Basic Pokemon 서치
  - `professors_research()`: 2장 드로우
  - `galdion()`: Type:Null/Silvally 서치
  - `use_card_effect()`: 통합 실행 함수
- **유틸리티 함수들**: 드로우 카드 판별, 효과 설명 등

---

### 📋 **설정 파일**

#### `DeckList.txt` (덱 구성)
**형식**: `카드명 | 카드타입 | 장수`
```
Blacephalon | Basic Pokemon | 2
Type:Null | Basic Pokemon | 2
Silvally | Stage1 Pokemon | 2
Poke Ball | Item | 2
Giant Cape | Pokemon Tool | 2
Professor's Research | Supporter | 2
```
- 총 20장 구성
- 11종류 카드 정의
- 파이프(|) 구분자 사용

#### `TestCase.txt` (테스트 케이스) ⭐ **v2.0 완전 개편**
**형식**: JSON 블록들
```json
{
    "name": "선호하는 Opening: Type:Null 또는 Blacephalon으로 시작",
    "request": {
        "type": "preferred_opening",
        "preferred_basics": ["Type:Null", "Blacephalon"]
    }
}
{
    "name": "3턴까지 Blacephalon + BalsaMine 각각 1장 이상 드로우 확률",
    "request": {
        "type": "multi_card",
        "target_cards": ["Blacephalon", "BalsaMine"],
        "turn": 3
    }
}
```
- 3가지 새로운 계산 타입 지원
- 동적 카드 개수 및 턴 수 설정

---

### 🧪 **테스트 및 유틸리티**

#### `run_all_tests.py` - **추천 실행 파일** ⭐
**용도**: 전체 5개 테스트 케이스 일괄 실행
- 모든 확률 결과를 한 번에 출력
- 요약 통계 제공
- 가장 실용적인 실행 방법

---

## 🚀 사용 방법

### **기본 실행**
```bash
# 전체 확률 계산 (추천)
python run_all_tests.py

# 대화형 실행
python main_simulator.py
```

### **설정 변경**
1. **덱 구성 변경**: `DeckList.txt` 편집
2. **테스트 케이스 변경**: `TestCase.txt` 편집
3. **시뮬레이션 횟수**: TestCase.txt의 `"simulation_count"` 값 수정

---

## 🎯 새로운 확률 계산 타입 (v2.0)

### **1. 선호하는 Opening (`preferred_opening`)**
**목적**: 원하는 Basic Pokemon으로 시작할 수 있는 확률
```json
{
    "type": "preferred_opening",
    "preferred_basics": ["Type:Null", "Blacephalon"]
}
```
**계산 로직**: 첫 5장에 선호하는 Basic 중 1장 이상 포함될 확률

### **2. 비선호하는 Opening (`non_preferred_opening`)**
**목적**: 원하지 않는 Basic Pokemon으로만 시작해야 하는 확률
```json
{
    "type": "non_preferred_opening",
    "non_preferred_basics": ["Charmander", "Squirtle"]
}
```
**계산 로직**: 첫 5장에 Basic은 있지만 모두 비선호 카드인 확률

### **3. 멀티카드 드로우 (`multi_card`)**
**목적**: N턴까지 지정된 카드들을 각각 1장 이상 드로우할 확률
```json
{
    "type": "multi_card",
    "target_cards": ["Blacephalon", "BalsaMine"],
    "turn": 3
}
```
**지원 범위**: 카드 1~3개, 턴 수 1~N턴

---

## 🔧 개발 가이드

### **새로운 카드 효과 추가**
`card_effects.py`에서 다음 단계 수행:

1. **DRAW_CARDS에 추가**:
```python
DRAW_CARDS = {
    "새카드명": "효과설명"
}
```

2. **CardEffects 클래스에 메서드 추가**:
```python
@staticmethod
def 새카드_효과(game_state) -> bool:
    # 효과 구현
    return result
```

3. **use_card_effect에 분기 추가**:
```python
elif card_name == "새카드명":
    result = CardEffects.새카드_효과(game_state)
```

### **새로운 테스트 케이스 추가**
`TestCase.txt`에 JSON 블록 추가:
```json
{
    "name": "새로운 테스트 케이스",
    "request": {
        "type": "multi_card",
        "target_cards": ["카드1", "카드2"],
        "turn": 2
    }
}
```

---

## 📊 현재 구현된 카드 효과

| 카드명 | 효과 | 구현 상태 |
|--------|------|-----------|
| Poke Ball | 덱에서 랜덤 Basic Pokemon 서치 | ✅ 완료 |
| Professor's Research | 2장 드로우 | ✅ 완료 |
| Galdion | Type:Null 또는 Silvally 서치 | ✅ 완료 |

---

## 🎮 게임 규칙

### **기본 규칙**
- 덱: 20장 고정
- 같은 카드 최대 2장
- 시작: 5장 드로우 (Basic Pokemon 필수)
- 턴 정의: 0턴=시작5장, 1턴=+1드로우, 2턴=+2드로우

### **Opening 메커니즘** ⭐ **v2.0에서 중요성 강조**
- **0턴 프로세스**: 첫 5장 드로우 → Basic Pokemon 1장을 전열에 배치
- **선택권**: Basic이 여러 장 → 플레이어가 원하는 것 선택 가능
- **재드로우**: Basic이 0장 → 덱과 손패를 섞고 재드로우

### **카드 타입**
- Basic Pokemon, Stage1 Pokemon, Stage2 Pokemon
- Item, Pokemon Tool, Item(fossil), Supporter

### **드로우 카드 사용 순서**
TestCase.txt에서 설정: `["Poke Ball", "Professor's Research", "Galdion"]`

---

## 🐛 문제 해결

### **시뮬레이션 오류**
1. 덱이 정확히 20장인지 확인
2. Basic Pokemon이 포함되어 있는지 확인
3. 대상 카드가 덱에 존재하는지 확인

### **성능 최적화**
- 시뮬레이션 횟수 조정 (TestCase.txt의 `simulation_count`)
- 빠른 테스트: 1,000~2,000회
- 정확한 결과: 10,000~50,000회

---

## 📈 최근 업데이트

### **v2.0 - 확률 계산 시스템 완전 리팩토링** ⭐ **NEW**
- ✅ **3개 새로운 확률 함수**: 선호/비선호 Opening + 멀티카드 드로우
- ✅ **동적 설정 지원**: 카드 개수(1~3개), 턴 수(1~N턴) 자유 설정
- ✅ **게임 메커니즘 반영**: Opening 선택권 및 선호도 구분
- ✅ **코드 간소화**: 5개 함수 → 3개 함수로 통합
- ✅ **TestCase 구조 개편**: JSON 기반 동적 설정

### **v1.0 - 모듈화 완료** (이전 버전)
- ✅ 카드 효과 모듈 분리 (`card_effects.py`)
- ✅ 외부 파일 설정 지원 (DeckList.txt, TestCase.txt)
- ✅ 5가지 확률 계산 타입 완성
- ✅ 포괄적인 테스트 스위트

### **주요 개선사항 (v1.0 → v2.0)**
- **기존**: 고정된 타입 1~5 + 하드코딩된 매개변수
- **개선**: 동적 타입 시스템 + 유연한 설정
- **기존**: Opening 계산의 게임 메커니즘 미반영
- **개선**: 실제 게임 규칙에 맞는 선호도 기반 Opening 계산
- **기존**: 개별 함수별 고정 턴 수
- **개선**: 통합 함수로 동적 턴 수 지원

---

## 🎯 **v2.0 실제 사용 예시**

### **현재 덱 구성 기준 결과**
```
테스트 1: 100.00% - 선호하는 Opening (Type:Null 또는 Blacephalon)
테스트 2: 0.00%   - 비선호하는 Opening (현재 덱에 해당 카드 없음)
테스트 3: 66.88%  - 2턴까지 Leaf 드로우
테스트 4: 70.80%  - 3턴까지 Blacephalon + BalsaMine 조합
테스트 5: 3.35%   - 2턴까지 Type:Null + Silvally + Poke Ball 조합
```

### **설정 변경 예시**
```json
// 더 긴 턴 수 테스트
{
    "type": "multi_card",
    "target_cards": ["Rare_Card"],
    "turn": 5
}

// 다른 선호도 설정
{
    "type": "preferred_opening",
    "preferred_basics": ["Strong_Pokemon_A", "Strong_Pokemon_B", "Strong_Pokemon_C"]
}
```

---

## 💡 활용 팁

1. **빠른 확률 확인**: `python run_all_tests.py`
2. **새 덱 테스트**: DeckList.txt 수정 후 실행
3. **카드 효과 추가**: card_effects.py만 수정
4. **동적 설정 활용**: TestCase.txt에서 턴 수와 카드 조합 자유 변경
5. **Opening 분석**: 선호/비선호 Basic을 구분해서 덱 성능 평가
6. **대용량 시뮬레이션**: simulation_count를 50,000 이상으로 설정

---

## 🔮 향후 개발 계획

- [ ] **더 많은 카드 효과**: 실제 게임의 다양한 카드 구현
- [ ] **고급 통계**: 표준편차, 신뢰구간 등 통계적 분석
- [ ] **시각화**: 확률 분포 그래프 및 차트
- [ ] **덱 최적화**: AI 기반 최적 덱 구성 제안
- [ ] **배치 분석**: 여러 덱 구성을 한 번에 비교 분석

이 가이드를 통해 v2.0의 모든 새로운 기능을 완전히 활용할 수 있습니다! 🚀