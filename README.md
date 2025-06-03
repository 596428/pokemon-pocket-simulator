# Pokemon Pocket Simulator - 프로젝트 가이드

## 📋 프로젝트 개요
Pokemon Pocket 카드게임의 드로우 확률을 계산하는 시뮬레이터입니다. 모듈화된 구조로 설계되어 확장과 유지보수가 용이합니다.

---

## 🎯 주요 기능
- **5가지 확률 계산**: 시작 드로우, 조건부 드로우, 턴별 드로우, 멀티카드 조합 등
- **카드 효과 시뮬레이션**: Poke Ball, Professor's Research, Galdion 등 드로우 카드 효과
- **외부 파일 설정**: 덱 구성과 테스트 케이스를 텍스트 파일로 관리
- **모듈화된 구조**: 기능별로 분리된 파이썬 모듈

---

## 📁 파일 구조 및 기능

### 🔧 **핵심 시뮬레이터 모듈**

#### `main_simulator.py` (메인 엔진 - 약 620줄)
**역할**: 시뮬레이터의 핵심 엔진
- **Card 클래스**: 개별 카드 객체
- **GameState 클래스**: 게임 상태 관리 (덱, 손패, 턴)
- **SimulationEngine 클래스**: 턴별 시뮬레이션 로직
- **PokemonPocketSimulator 클래스**: 메인 인터페이스
- **파일 읽기 함수들**: `load_deck_from_file()`, `load_test_cases_from_file()`

#### `probability_calculator.py` (확률 계산 - 373줄)
**역할**: 5가지 타입별 확률 계산 전문 모듈
- **ProbabilityCalculator 클래스**: 확률 계산 전용
- **타입 1**: 특정 Basic Pokemon이 시작 5장에 포함될 확률
- **타입 2**: Basic Pokemon이 정확히 1장이고 특정 카드일 확률  
- **타입 3**: N턴까지 특정 카드 드로우 확률
- **타입 4**: 2턴까지 Basic + Stage1 조합 확률
- **타입 5**: 2턴까지 Basic + Item + Stage2 조합 확률

#### `card_effects.py` (카드 효과 - 158줄) ⭐ **NEW**
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
Type:Null | Basic Pokemon | 2
Poke Ball | Item | 2
Professor's Research | Supporter | 2
```
- 총 20장 구성
- 13종류 카드 정의
- 파이프(|) 구분자 사용

#### `TestCase.txt` (테스트 케이스)
**형식**: JSON 블록들
```json
{
    "name": "타입 1: Type:Null이 시작 5장에 포함될 확률",
    "request": {
        "type": 1,
        "target_cards": ["Type:Null"]
    }
}
```
- 5개 테스트 케이스 정의
- 드로우 순서 및 시뮬레이션 횟수 설정

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

### **새로운 확률 계산 타입 추가**
`probability_calculator.py`에서:
1. `calculate_type_N()` 메서드 추가
2. `run_calculation()` 메서드에 분기 추가

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

### **v2.0 - 모듈화 완료** (최신)
- ✅ 카드 효과 모듈 분리 (`card_effects.py`)
- ✅ 외부 파일 설정 지원 (DeckList.txt, TestCase.txt)
- ✅ 5가지 확률 계산 타입 완성
- ✅ 포괄적인 테스트 스위트

### **주요 개선사항**
- 모든 설정을 외부 파일로 분리
- 카드 효과 추가가 매우 용이
- 코드 재사용성 및 유지보수성 향상
- 체계적인 테스트 환경 구축

---

## 💡 활용 팁

1. **빠른 확률 확인**: `python run_all_tests.py`
2. **새 덱 테스트**: DeckList.txt 수정 후 실행
3. **카드 효과 추가**: card_effects.py만 수정
4. **대용량 시뮬레이션**: simulation_count를 50,000 이상으로 설정

이 가이드를 통해 다른 세션에서도 프로젝트를 빠르게 이해하고 활용할 수 있습니다.