# Pokemon Pocket 인게임 규칙 (Claude 참조용)

## 🎯 빠른 참조 색인
- [필드 구성 요소](#필드-구성-요소-공식-명칭)
- [Basic 포켓몬 배치](#basic-포켓몬-필드-배치-규칙)
- [진화 규칙](#진화-규칙-basic--stage1--stage2)
- [Item 카드 사용](#item-카드-사용법)
- [Pokemon Tool 사용](#pokemon-tool-사용법)

---

## 🏟️ 필드 구성 요소 공식 명칭

### **Field Layout**
```
[Active Spot: 1마리] [Bench: 최대 3마리]
[Energy Zone] [Discard Pile]
```

### **공식 명칭**
- **Active Spot**: 액티브 포켓몬이 앉는 곳. 액티브 포켓몬만이 공격할 수 있음
- **Bench**: 3개 슬롯으로 구성. 각 슬롯은 포켓몬 1마리 수용 가능
- **Energy Zone**: 플레이어가 수동으로 포켓몬에 부착하거나 카드 효과로 끌어올 수 있는 에너지 보관소
- **Discard Pile**: 사용된 아이템, 서포터, 기절한 포켓몬 등이 가는 곳

---

## 🎮 Basic 포켓몬 필드 배치 규칙

### **배치 제한사항**
- **벤치 제한**: 벤치 포켓몬은 3마리로 제한 (기존 TCG 5마리와 대비)
- **필수 요구사항**: 현재 Pokemon TCG Pocket에서는 항상 최소 1마리 Basic 포켓몬으로 시작

### **배치 규칙**
- **턴 중 배치**: 벤치에 Basic 포켓몬을 배치할 수 있음. 벤치에 공간이 있는 한 원하는 만큼 이 액션 가능
- **게임 시작**: 각 플레이어는 Basic 포켓몬을 액티브 스팟에 뒷면으로 배치. 양쪽 플레이어 확인 후 앞면으로 뒤집고 게임 시작

---

## 🔄 진화 규칙 (Basic → Stage1 → Stage2)

### **기본 진화 제한사항**
- **첫 턴 제한**: 첫 턴이나 포켓몬이 필드에 나온 턴에는 진화 불가
- **진화 횟수**: 각 포켓몬은 턴당 한 번만 진화 가능
- **진화 순서**: **Basic > Stage 1 > Stage 2 순서로만 진화 가능**

### **진화 실행 방법**
- **위치**: 벤치나 액티브 스팟에 있는 포켓몬 모두 진화 가능
- **조건**: 손에 "Evolves from X"라고 적힌 카드가 있고, X가 턴 시작 시점에 플레이에 있던 포켓몬 이름이면 진화 가능
- **동작**: 진화 카드를 해당 포켓몬 위에 올려놓음

### **⚡ 진화 규칙 예외: Rare Candy**

**Rare Candy 효과 (영문):**
> "Choose 1 of your Basic Pokemon in play. If you have a Stage 2 card in your hand that evolves from that Pokemon, put that card onto the Basic Pokemon to evolve it, skipping the Stage 1. You can't use this card during your first turn or on a Basic Pokemon that was put into play this turn."

**Rare Candy 규칙:**
- **예외적 진화**: Basic 포켓몬에서 Stage 2로 **직접 진화 가능** (Stage 1 건너뛰기)
- **사용 제한**: 첫 턴에는 사용 불가, 해당 턴에 필드에 나온 Basic 포켓몬에는 사용 불가
- **필요 조건**: 손에 해당 Basic 포켓몬에서 진화하는 Stage 2 카드 보유

---

## 🎴 Item 카드 사용법

### **사용 제한**
- **턴당 사용량**: Item 카드는 턴에 여러 장 사용 가능 (무제한)
- **사용 후 처리**: Trainer 카드는 사용 후 Discard Pile로 버려짐

---

## ⚒️ Pokemon Tool 사용법

### **기본 사용 규칙**
- **부착 제한**: 각 포켓몬은 하나의 Tool만 보유 가능. 기존 Tool이 있으면 새 Tool 부착 불가
- **턴당 사용량**: Item 카드와 마찬가지로 턴당 Tool 부착 횟수 제한 없음
- **최대 부착량**: 최대 4마리 포켓몬이 플레이에 있으므로 턴당 최대 4개 Tool 부착 가능

### **Tool 관리 규칙**
- **교체 조건**: 상대가 Tool을 버리거나 조건 충족으로 자동 버려질 때만 새 Tool 부착 가능
- **제거 불가**: 현재 Pokemon Tool은 수동으로 제거하거나 교체 불가
- **포켓몬 기절 시**: Tool이 부착된 포켓몬이 기절하면 포켓몬과 Tool 모두 discard pile로 이동

---

## 📝 구현 참고사항

### **Field 구현 시 고려사항**
1. **Active Spot**: 1마리 제한, 공격 가능한 유일한 위치
2. **Bench Slots**: 3개 슬롯, 진화/Tool 부착 가능
3. **진화 체크**: 턴 제한, 순서 제한, Rare Candy 예외 처리
4. **Tool 관리**: 포켓몬당 1개 제한, 중복 부착 방지

### **시뮬레이션 액션 목록**
- Basic 포켓몬 배치 (손 → 벤치/액티브)
- 일반 진화 (Basic → Stage1 → Stage2)
- Rare Candy 진화 (Basic → Stage2)
- Tool 부착 (Tool → 포켓몬)
- 포켓몬 기절 처리 (포켓몬+Tool → discard pile)

---

*최종 업데이트: 2025-06-09*  
*참조 목적: Pokemon Pocket 시뮬레이터 Field 구현*