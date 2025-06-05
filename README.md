# Pokemon Pocket Simulator

**Pokemon Pocket 카드게임의 확률을 계산하는 Python 시뮬레이터**

덱 구성에 따른 드로우 확률을 정확하게 계산하여 덱 빌딩과 게임 전략 수립을 지원합니다.

---

## 🎯 **현재 버전: v2.01**

### ✨ **주요 기능**
- **3가지 확률 계산**: 선호하는 Opening, 비선호하는 Opening, 멀티카드 드로우
- **카드 효과 시뮬레이션**: Poke Ball, Professor's Research, Galdion, Pokemon Communication
- **수학적 정확 계산**: Hypergeometric Distribution 기반 정확한 확률 계산
- **사용자 정의 덱**: 20장 덱 구성과 드로우 카드 발동 순서 설정

---

## 🚀 **빠른 시작**

### **전체 테스트 실행 (추천)**
`ash
python run_all_tests.py
`

### **Windows에서 한글 오류 해결**
`ash
# PowerShell에서 실행
$env:PYTHONIOENCODING="utf-8"; python run_all_tests.py

# 또는 배치파일 사용
run_simulator.bat
`

### **대화형 실행**
`ash
python main_simulator.py
`

---

## 📊 **계산 가능한 확률**

1. **선호하는 Opening**: 원하는 Basic Pokemon으로 시작할 확률
2. **비선호하는 Opening**: 원하지 않는 Basic Pokemon으로만 시작할 확률  
3. **멀티카드 드로우**: N턴까지 지정된 카드들을 각각 1장 이상 드로우할 확률

---

## 📈 **버전 업데이트 내역**

### **v2.01** (2025-06-05)
- ✅ **Pokemon Communication 카드 완전 구현**
  - 손패 Pokemon과 덱 Pokemon 교환 기능
  - 복잡한 발동 조건 판단 로직 (target_cards 기반)
  - 마지막 턴 연쇄 사용 지원
- ✅ **게임 규칙 정확성 개선**
  - Supporter: 1턴에 1장만 사용
  - Item: 여러 장 자유 사용
  - 정확한 카드 효과 발동 순서

### **v2.0** (2025-06-04)
- 🔄 **확률 계산 시스템 전면 리팩토링**
  - 5가지 계산 방식 → 3가지로 통합 및 최적화
  - 유연한 카드 개수 및 턴 수 설정 (1~N개, 1~N턴)
  - 게임 메커니즘 정확성 대폭 개선
- 📝 **TestCase 구조 개편**: JSON 기반 유연한 설정

### **v1.0** (2025-06-03)
- 🎉 **초기 릴리스**: 5가지 확률 계산, 카드 효과 모듈, 덱 파일 설정

---

## 📚 **문서 및 가이드**

- **[📖 상세 가이드](PROJECT_GUIDE.md)**: 전체 기능 설명, 개발 가이드, 문제 해결
- **[⚙️ 설정 파일](DeckList.txt)**: 덱 구성 설정
- **[🧪 테스트 케이스](TestCase.txt)**: 확률 계산 시나리오 설정

---

## 🛠 **기술 스택**

- **Python 3.7+**
- **수학적 계산**: `math.comb()` 기반 Hypergeometric Distribution
- **시뮬레이션**: Monte Carlo 방법론
- **아키텍처**: 모듈화된 객체지향 설계

---

## 📞 **지원**

- **문제 해결**: [PROJECT_GUIDE.md](PROJECT_GUIDE.md)의 "문제 해결" 섹션 참조
- **카드 효과 추가**: [PROJECT_GUIDE.md](PROJECT_GUIDE.md)의 "개발 가이드" 섹션 참조
- **Windows 한글 오류**: UTF-8 인코딩 설정 필요

---

*Pokemon Pocket Simulator는 덱 빌딩의 과학적 접근을 위한 확률 계산 도구입니다.*
