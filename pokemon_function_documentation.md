# Pokemon Pocket Simulator 함수 문서화

## 📋 정리 기준
각 함수별로 다음 9개 항목을 기록:
1. **함수명 + 위치**
2. **목적 (한 줄 설명)**
3. **파라미터 타입**
4. **반환값 구조**
5. **중요도** (⭐⭐⭐)
6. **호출하는 주요 함수**
7. **사용되는 곳**
8. **버전 정보**
9. **핵심 로직 요약**

---

## 🎯 main_simulator.py

### ⭐⭐⭐ simulate_single_game
1. **함수명 + 위치**: `SimulationEngine.simulate_single_game` (main_simulator.py:216)
2. **목적**: 한 게임의 전체 시뮬레이션 실행 (0턴~N턴)
3. **파라미터 타입**: `max_turn: int = 2, verbose: bool = False, target_cards: List[str] = None, target_groups: List[Dict] = None`
4. **반환값 구조**: `{'success': bool, 'turn_results': dict, 'final_hand': list, 'cards_used': list}`
5. **중요도**: ⭐⭐⭐ (모든 확률 계산의 기반)
6. **호출하는 주요 함수**: `initial_draw()`, `start_turn()`, `_use_draw_cards()`
7. **사용되는 곳**: 모든 probability_calculator 함수들
8. **버전 정보**: v1.0 (v2.02에서 target_groups 파라미터 추가)
9. **핵심 로직 요약**: 초기 5장 드로우 → Basic Pokemon 체크 → 턴별 드로우+카드효과 → 최종 결과 반환

### ⭐⭐⭐ _use_draw_cards
1. **함수명 + 위치**: `SimulationEngine._use_draw_cards` (main_simulator.py:258)
2. **목적**: 한 턴에서 모든 드로우 카드들을 순서대로 사용
3. **파라미터 타입**: `game_state: GameState, verbose: bool = False, target_cards: List[str] = None, max_turn: int = None, target_groups: List[Dict] = None`
4. **반환값 구조**: `List[str]` (사용된 카드 이름들)
5. **중요도**: ⭐⭐⭐ (카드 효과 처리 핵심)
6. **호출하는 주요 함수**: `CardEffects.use_card_effect()`, `_should_use_iono_for_multi_or_multi()`
7. **사용되는 곳**: `simulate_single_game()`
8. **버전 정보**: v1.0 (v2.02에서 Iono 분기 로직 추가)
9. **핵심 로직 요약**: 드로우 순서대로 카드 체크 → Iono는 상황별 판단 → 효과 적용 → Supporter 제한 관리

### ⭐⭐⭐ _should_use_iono_for_multi_or_multi
1. **함수명 + 위치**: `SimulationEngine._should_use_iono_for_multi_or_multi` (main_simulator.py:365)
2. **목적**: multi_or_multi 상황에서 Iono 사용 여부를 스마트하게 판단
3. **파라미터 타입**: `game_state: GameState, target_groups: List[Dict], verbose: bool = False`
4. **반환값 구조**: `bool`
5. **중요도**: ⭐⭐⭐ (Iono와 multi_or_multi 충돌 해결의 핵심)
6. **호출하는 주요 함수**: 없음 (순수 로직 함수)
7. **사용되는 곳**: `_use_draw_cards()` 내 Iono 처리 부분
8. **버전 정보**: v2.02 신규 추가
9. **핵심 로직 요약**: 완성 그룹 체크 → 67% 이상 완성 그룹 체크 → 모든 그룹 저조시에만 Iono 사용

### ⭐⭐ validate_deck_input
1. **함수명 + 위치**: `PokemonPocketSimulator.validate_deck_input` (main_simulator.py:410)
2. **목적**: 덱 구성의 유효성 검증 (20장, 카드별 2장 제한 등)
3. **파라미터 타입**: `deck_input: Dict[str, Dict[str, Any]]`
4. **반환값 구조**: `bool`
5. **중요도**: ⭐⭐ (입력 검증)
6. **호출하는 주요 함수**: 없음 (검증 로직)
7. **사용되는 곳**: `setup_simulation()`
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 총 카드 수 체크 → 개별 카드 수량 체크 → 카드 타입 유효성 체크

### ⭐⭐ setup_simulation
1. **함수명 + 위치**: `PokemonPocketSimulator.setup_simulation` (main_simulator.py:477)
2. **목적**: 시뮬레이션 환경 설정 (덱, 드로우 순서, 검증)
3. **파라미터 타입**: `deck_input: Dict[str, Dict[str, Any]], draw_order: List[str] = None`
4. **반환값 구조**: `None` (내부 상태 설정)
5. **중요도**: ⭐⭐ (시뮬레이션 준비)
6. **호출하는 주요 함수**: `validate_deck_input()`, `SimulationEngine()`
7. **사용되는 곳**: 모든 테스트 파일들, `run_calculation()`
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 덱 검증 → 드로우 순서 설정 → 시뮬레이션 엔진 초기화 → ProbabilityCalculator 연결

### ⭐⭐ validate_calculation_request
1. **함수명 + 위치**: `PokemonPocketSimulator.validate_calculation_request` (main_simulator.py:433)
2. **목적**: 확률 계산 요청의 유효성 검증 (타입, 필수 파라미터 등)
3. **파라미터 타입**: `calculation_request: Dict[str, Any]`
4. **반환값 구조**: `bool`
5. **중요도**: ⭐⭐ (입력 검증)
6. **호출하는 주요 함수**: 없음 (검증 로직)
7. **사용되는 곳**: `run_calculation()`
8. **버전 정보**: v1.0 (v2.02에서 새 타입들 추가)
9. **핵심 로직 요약**: 계산 타입 체크 → 필수 파라미터 존재 확인 → 타입별 추가 검증

### ⭐⭐ run_calculation (main_simulator)
1. **함수명 + 위치**: `PokemonPocketSimulator.run_calculation` (main_simulator.py:510)
2. **목적**: 확률 계산 요청을 받아 ProbabilityCalculator에 위임하는 인터페이스
3. **파라미터 타입**: `calculation_request: Dict[str, Any], simulation_count: int = 10000`
4. **반환값 구조**: `Dict[str, Any]` (ProbabilityCalculator 결과)
5. **중요도**: ⭐⭐ (외부 인터페이스)
6. **호출하는 주요 함수**: `validate_calculation_request()`, `self.prob_calculator.run_calculation()`
7. **사용되는 곳**: 테스트 파일들
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 요청 검증 → ProbabilityCalculator에 위임 → 결과 반환

### ⭐ load_deck_from_file
1. **함수명 + 위치**: `load_deck_from_file` (main_simulator.py:15)
2. **목적**: DeckList.txt 파일에서 덱 구성을 읽어오는 유틸리티 함수
3. **파라미터 타입**: `filename: str = "DeckList.txt"`
4. **반환값 구조**: `Dict[str, Dict[str, Any]]` (덱 딕셔너리)
5. **중요도**: ⭐ (파일 I/O 유틸리티)
6. **호출하는 주요 함수**: 파일 읽기 함수들
7. **사용되는 곳**: `main()`, 테스트 시 선택적 사용
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 파일 읽기 → 파싱 → 딕셔너리 변환 → 유효성 체크

### ⭐ load_test_cases_from_file
1. **함수명 + 위치**: `load_test_cases_from_file` (main_simulator.py:54)
2. **목적**: TestCase.txt 파일에서 테스트 케이스들을 읽어오는 유틸리티 함수
3. **파라미터 타입**: `filename: str = "TestCase.txt"`
4. **반환값 구조**: `Tuple[List[Dict], List[str], int]` (테스트케이스, 드로우순서, 시뮬레이션수)
5. **중요도**: ⭐ (파일 I/O 유틸리티)
6. **호출하는 주요 함수**: JSON 파싱 함수들
7. **사용되는 곳**: `main()`, `run_test_suite()`
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: JSON 파일 읽기 → 파싱 → 테스트 케이스 분리 → 설정값 추출

### ⭐ create_deck
1. **함수명 + 위치**: `create_deck` (main_simulator.py:125)
2. **목적**: 덱 딕셔너리를 Card 객체 리스트로 변환
3. **파라미터 타입**: `deck_input: Dict[str, Dict[str, Any]]`
4. **반환값 구조**: `List[Card]`
5. **중요도**: ⭐ (데이터 변환 유틸리티)
6. **호출하는 주요 함수**: `Card()` 생성자
7. **사용되는 곳**: `GameState.__init__()`
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 딕셔너리 순회 → count만큼 Card 객체 생성 → 리스트 반환

### ⭐ print_deck_summary
1. **함수명 + 위치**: `print_deck_summary` (main_simulator.py:142)
2. **목적**: 덱 구성 요약 정보를 콘솔에 출력
3. **파라미터 타입**: `deck: List[Card]`
4. **반환값 구조**: `None` (콘솔 출력)
5. **중요도**: ⭐ (디버깅 유틸리티)
6. **호출하는 주요 함수**: `print()`, `defaultdict()`
7. **사용되는 곳**: 디버깅 시 선택적 사용
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 카드별 개수 집계 → 타입별 개수 집계 → 포맷팅해서 출력

### ⭐ print_deck_info
1. **함수명 + 위치**: `PokemonPocketSimulator.print_deck_info` (main_simulator.py:529)
2. **목적**: 현재 설정된 덱 정보를 출력
3. **파라미터 타입**: 없음
4. **반환값 구조**: `None` (콘솔 출력)
5. **중요도**: ⭐ (디버깅 유틸리티)
6. **호출하는 주요 함수**: `print()`
7. **사용되는 곳**: 디버깅 시 선택적 사용
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 설정된 덱 구성 출력 → 드로우 순서 출력

### ⭐ main
1. **함수명 + 위치**: `main` (main_simulator.py:555)
2. **목적**: 프로그램의 진입점, 파일 기반 실행 모드
3. **파라미터 타입**: 없음
4. **반환값 구조**: `None`
5. **중요도**: ⭐ (진입점)
6. **호출하는 주요 함수**: `load_deck_from_file()`, `load_test_cases_from_file()`, `PokemonPocketSimulator()`
7. **사용되는 곳**: `if __name__ == "__main__"`
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 파일에서 덱과 테스트케이스 로드 → 시뮬레이터 실행 → 결과 출력

### ⭐ run_test_suite
1. **함수명 + 위치**: `run_test_suite` (main_simulator.py:629)
2. **목적**: 여러 테스트 케이스를 일괄 실행
3. **파라미터 타입**: 없음
4. **반환값 구조**: `None`
5. **중요도**: ⭐ (테스트 유틸리티)
6. **호출하는 주요 함수**: `load_test_cases_from_file()`, `PokemonPocketSimulator()`
7. **사용되는 곳**: `main()` 내에서 선택적 실행
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 테스트 케이스들 로드 → 순차 실행 → 결과 요약

---

## 🎮 GameState 클래스 함수들

### ⭐⭐ GameState.__init__
1. **함수명 + 위치**: `GameState.__init__` (main_simulator.py:161)
2. **목적**: 게임 상태 초기화 (덱, 손패, 턴 등)
3. **파라미터 타입**: `deck_input: Dict[str, Dict[str, Any]], draw_order: List[str] = None`
4. **반환값 구조**: `None` (객체 초기화)
5. **중요도**: ⭐⭐ (게임 상태 관리 핵심)
6. **호출하는 주요 함수**: `create_deck()`, `reset_game()`
7. **사용되는 곳**: `SimulationEngine.simulate_single_game()`
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 덱 생성 → 게임 상태 변수 초기화 → 드로우 순서 설정

### ⭐⭐ SimulationEngine.__init__
1. **함수명 + 위치**: `SimulationEngine.__init__` (main_simulator.py:211)
2. **목적**: 시뮬레이션 엔진 초기화
3. **파라미터 타입**: `deck_input: Dict[str, Dict[str, Any]], draw_order: List[str] = None`
4. **반환값 구조**: `None` (객체 초기화)
5. **중요도**: ⭐⭐ (시뮬레이션 엔진 핵심)
6. **호출하는 주요 함수**: 없음
7. **사용되는 곳**: `PokemonPocketSimulator.setup_simulation()`
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 덱 구성과 드로우 순서 저장

### ⭐ PokemonPocketSimulator.__init__
1. **함수명 + 위치**: `PokemonPocketSimulator.__init__` (main_simulator.py:404)
2. **목적**: 메인 시뮬레이터 객체 초기화
3. **파라미터 타입**: 없음
4. **반환값 구조**: `None` (객체 초기화)
5. **중요도**: ⭐ (시뮬레이터 초기화)
6. **호출하는 주요 함수**: 없음
7. **사용되는 곳**: 모든 테스트 파일들, `main()`
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 내부 변수들 None으로 초기화

### ⭐⭐ reset_game
1. **함수명 + 위치**: `GameState.reset_game` (main_simulator.py:169)
2. **목적**: 게임 상태를 초기값으로 리셋
3. **파라미터 타입**: 없음
4. **반환값 구조**: `None`
5. **중요도**: ⭐⭐ (게임 상태 관리)
6. **호출하는 주요 함수**: `copy.deepcopy()`
7. **사용되는 곳**: `GameState.__init__()`, 새 게임 시작 시
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 덱 복사 → 손패 초기화 → 턴/상태 변수 리셋

### ⭐⭐ draw_cards
1. **함수명 + 위치**: `GameState.draw_cards` (main_simulator.py:175)
2. **목적**: 덱에서 지정된 수만큼 카드를 드로우
3. **파라미터 타입**: `count: int`
4. **반환값 구조**: `List[Card]` (드로우한 카드들)
5. **중요도**: ⭐⭐ (핵심 게임 액션)
6. **호출하는 주요 함수**: `random.shuffle()`
7. **사용되는 곳**: `initial_draw()`, `start_turn()`, 카드 효과들
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 덱 셔플 → 요청 수만큼 카드 뽑기 → 손패에 추가 → 덱에서 제거

### ⭐⭐ initial_draw
1. **함수명 + 위치**: `GameState.initial_draw` (main_simulator.py:184)
2. **목적**: 게임 시작 시 5장 드로우 및 Basic Pokemon 체크
3. **파라미터 타입**: 없음
4. **반환값 구조**: `bool` (유효한 드로우 여부)
5. **중요도**: ⭐⭐ (게임 시작 핵심)
6. **호출하는 주요 함수**: `draw_cards()`, `_is_basic_pokemon()`
7. **사용되는 곳**: `simulate_single_game()`
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 5장 드로우 → Basic Pokemon 존재 체크 → 없으면 재드로우

### ⭐ start_turn
1. **함수명 + 위치**: `GameState.start_turn` (main_simulator.py:205)
2. **목적**: 새 턴 시작 시 1장 드로우 및 턴 카운터 증가
3. **파라미터 타입**: 없음
4. **반환값 구조**: `None`
5. **중요도**: ⭐ (턴 관리)
6. **호출하는 주요 함수**: `draw_cards()`
7. **사용되는 곳**: `simulate_single_game()`
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 턴 카운터 증가 → 1장 드로우

---

## 🎯 Card 클래스 함수들

### ⭐ Card.__init__
1. **함수명 + 위치**: `Card.__init__` (main_simulator.py:109)
2. **목적**: 카드 객체 초기화
3. **파라미터 타입**: `name: str, card_type: str`
4. **반환값 구조**: `None` (객체 초기화)
5. **중요도**: ⭐ (데이터 모델)
6. **호출하는 주요 함수**: 없음
7. **사용되는 곳**: `create_deck()`
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 카드명과 타입 저장

### ⭐ Card.__str__
1. **함수명 + 위치**: `Card.__str__` (main_simulator.py:113)
2. **목적**: 카드 객체의 문자열 표현
3. **파라미터 타입**: 없음
4. **반환값 구조**: `str`
5. **중요도**: ⭐ (디버깅 지원)
6. **호출하는 주요 함수**: 없음
7. **사용되는 곳**: 디버깅, 로깅
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: "카드명 (타입)" 형태로 반환

### ⭐ Card.__repr__
1. **함수명 + 위치**: `Card.__repr__` (main_simulator.py:116)
2. **목적**: 카드 객체의 개발자용 표현
3. **파라미터 타입**: 없음
4. **반환값 구조**: `str`
5. **중요도**: ⭐ (디버깅 지원)
6. **호출하는 주요 함수**: 없음
7. **사용되는 곳**: 디버깅
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: `__str__()` 호출

### ⭐ Card.__eq__
1. **함수명 + 위치**: `Card.__eq__` (main_simulator.py:119)
2. **목적**: 카드 객체 간 동등성 비교
3. **파라미터 타입**: `other: Card`
4. **반환값 구조**: `bool`
5. **중요도**: ⭐ (객체 비교)
6. **호출하는 주요 함수**: 없음
7. **사용되는 곳**: 카드 검색, 비교 연산
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 이름과 타입이 모두 같으면 True

---

## 🎲 probability_calculator.py

### ⭐⭐⭐ calculate_multi_card_probability
1. **함수명 + 위치**: `ProbabilityCalculator.calculate_multi_card_probability` (probability_calculator.py:200)
2. **목적**: N턴까지 여러 카드를 각각 1장씩 확보할 확률 계산
3. **파라미터 타입**: `target_cards: List[str], max_turn: int, num_simulations: int = 10000`
4. **반환값 구조**: `{'calculation_type': str, 'probability_percent': float, 'success_count': int, 'total_valid_games': int, 'simulation_count': int}`
5. **중요도**: ⭐⭐⭐ (가장 많이 사용되는 확률 계산)
6. **호출하는 주요 함수**: `self.sim_engine.simulate_single_game()`
7. **사용되는 곳**: `run_calculation()`, test_iono_count.py, 기본 확률 계산
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 시뮬레이션 루프 → 각 게임 실행 → 모든 타겟 카드 보유 체크 → 성공률 계산

### ⭐⭐⭐ calculate_multi_or_multi_probability
1. **함수명 + 위치**: `ProbabilityCalculator.calculate_multi_or_multi_probability` (probability_calculator.py:646)
2. **목적**: 여러 목표 그룹 중 하나라도 완성하는 확률 계산 (OR 조건)
3. **파라미터 타입**: `target_groups: List[Dict], max_turn: int, num_simulations: int = 10000`
4. **반환값 구조**: `{'calculation_type': str, 'probability_percent': float, 'success_count': int, 'total_valid_games': int, 'simulation_count': int}`
5. **중요도**: ⭐⭐⭐ (v2.02 핵심 신규 기능)
6. **호출하는 주요 함수**: `self.sim_engine.simulate_single_game()` (target_groups 파라미터로)
7. **사용되는 곳**: test_composite.py
8. **버전 정보**: v2.02 신규 추가
9. **핵심 로직 요약**: 모든 그룹 카드 합치기 → 시뮬레이션 실행 → 각 결과에서 그룹별 완성 체크 → 하나라도 완성시 성공

### ⭐⭐⭐ calculate_preferred_and_multi_probability
1. **함수명 + 위치**: `ProbabilityCalculator.calculate_preferred_and_multi_probability` (probability_calculator.py:537)
2. **목적**: 선호하는 Basic Pokemon으로 시작하면서 목표 카드들을 모두 확보하는 확률 (AND 조건)
3. **파라미터 타입**: `preferred_basics: List[str], target_cards: List[str], max_turn: int, num_simulations: int = 10000`
4. **반환값 구조**: `{'calculation_type': str, 'probability_percent': float, 'success_count': int, 'total_valid_games': int, 'simulation_count': int, 'preferred_basics': list, 'target_cards': list}`
5. **중요도**: ⭐⭐⭐ (v2.02 핵심 신규 기능)
6. **호출하는 주요 함수**: `self.sim_engine.simulate_single_game()`, `_is_basic_pokemon()`
7. **사용되는 곳**: test_composite.py
8. **버전 정보**: v2.02 신규 추가
9. **핵심 로직 요약**: 시뮬레이션 실행 → 초기 패 Basic Pokemon 체크 → 목표 카드 확보 체크 → 두 조건 모두 만족시 성공

### ⭐⭐⭐ calculate_non_preferred_and_multi_probability
1. **함수명 + 위치**: `ProbabilityCalculator.calculate_non_preferred_and_multi_probability` (probability_calculator.py:608)
2. **목적**: 비선호하는 Basic Pokemon으로 시작했지만 목표 카드들을 확보하는 확률 (리커버리 확률)
3. **파라미터 타입**: `non_preferred_basics: List[str], target_cards: List[str], max_turn: int, num_simulations: int = 10000`
4. **반환값 구조**: `{'calculation_type': str, 'probability_percent': float, 'success_count': int, 'total_valid_games': int, 'simulation_count': int}`
5. **중요도**: ⭐⭐⭐ (v2.02 핵심 신규 기능)
6. **호출하는 주요 함수**: `self.sim_engine.simulate_single_game()`, `_is_basic_pokemon()`
7. **사용되는 곳**: test_composite.py
8. **버전 정보**: v2.02 신규 추가
9. **핵심 로직 요약**: 시뮬레이션 실행 → 초기 패가 모두 비선호 Basic인지 체크 → 목표 카드 확보 체크 → 두 조건 모두 만족시 성공

### ⭐⭐ calculate_preferred_opening_probability
1. **함수명 + 위치**: `ProbabilityCalculator.calculate_preferred_opening_probability` (probability_calculator.py:74)
2. **목적**: 특정 Basic Pokemon으로 시작할 확률 계산
3. **파라미터 타입**: `preferred_basics: List[str], num_simulations: int = 10000`
4. **반환값 구조**: `{'calculation_type': str, 'probability_percent': float, 'success_count': int, 'total_valid_games': int}`
5. **중요도**: ⭐⭐ (기본 확률 계산)
6. **호출하는 주요 함수**: `self.sim_engine.simulate_single_game()`, `_is_basic_pokemon()`
7. **사용되는 곳**: `run_calculation()` (type: preferred_opening)
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 시뮬레이션 실행 → 초기 5장 중 Basic Pokemon 추출 → 선호 Basic 포함 여부 체크

### ⭐⭐ calculate_non_preferred_opening_probability
1. **함수명 + 위치**: `ProbabilityCalculator.calculate_non_preferred_opening_probability` (probability_calculator.py:136)
2. **목적**: 특정 Basic Pokemon이 아닌 카드로 시작할 확률 계산
3. **파라미터 타입**: `non_preferred_basics: List[str], num_simulations: int = 10000`
4. **반환값 구조**: `{'calculation_type': str, 'probability_percent': float, 'success_count': int, 'total_valid_games': int}`
5. **중요도**: ⭐⭐ (기본 확률 계산)
6. **호출하는 주요 함수**: `self.sim_engine.simulate_single_game()`, `_is_basic_pokemon()`
7. **사용되는 곳**: `run_calculation()` (type: non_preferred_opening)
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 시뮬레이션 실행 → 초기 5장 중 Basic Pokemon 추출 → 비선호 Basic만 있는지 체크

### ⭐⭐ run_calculation (probability_calculator)
1. **함수명 + 위치**: `ProbabilityCalculator.run_calculation` (probability_calculator.py:466)
2. **목적**: 계산 요청 타입에 따라 적절한 확률 계산 함수 호출하는 라우터
3. **파라미터 타입**: `calculation_request: Dict[str, Any], simulation_count: int = 10000, use_mathematical: bool = True`
4. **반환값 구조**: `Dict[str, Any]` (계산 결과)
5. **중요도**: ⭐⭐ (확률 계산 라우터)
6. **호출하는 주요 함수**: 모든 `calculate_*_probability()` 함수들
7. **사용되는 곳**: `PokemonPocketSimulator.run_calculation()`
8. **버전 정보**: v1.0 (v2.02에서 새 타입들 추가)
9. **핵심 로직 요약**: 요청 타입 분석 → 해당 계산 함수 호출 → 결과 가공 후 반환

### ⭐⭐ calculate_preferred_opening_mathematical
1. **함수명 + 위치**: `ProbabilityCalculator.calculate_preferred_opening_mathematical` (probability_calculator.py:264)
2. **목적**: 수학적 계산으로 선호 Basic Pokemon 시작 확률 계산 (시뮬레이션 없이)
3. **파라미터 타입**: `preferred_basics: List[str]`
4. **반환값 구조**: `Dict[str, Any]` (수학적 계산 결과)
5. **중요도**: ⭐⭐ (수학적 검증)
6. **호출하는 주요 함수**: `_hypergeometric_probability()`, `_combination()`
7. **사용되는 곳**: `run_calculation()` (use_mathematical=True일 때)
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 하이퍼지오메트릭 분포 계산 → 조합론 적용 → 정확한 확률 도출

### ⭐⭐ calculate_non_preferred_opening_mathematical
1. **함수명 + 위치**: `ProbabilityCalculator.calculate_non_preferred_opening_mathematical` (probability_calculator.py:332)
2. **목적**: 수학적 계산으로 비선호 Basic Pokemon 시작 확률 계산
3. **파라미터 타입**: `non_preferred_basics: List[str]`
4. **반환값 구조**: `Dict[str, Any]` (수학적 계산 결과)
5. **중요도**: ⭐⭐ (수학적 검증)
6. **호출하는 주요 함수**: `_hypergeometric_probability()`, `_combination()`, `_probability_basic_at_least_one()`
7. **사용되는 곳**: `run_calculation()` (use_mathematical=True일 때)
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 전체 확률에서 선호 확률을 빼서 비선호 확률 도출

### ⭐ ProbabilityCalculator.__init__
1. **함수명 + 위치**: `ProbabilityCalculator.__init__` (probability_calculator.py:8)
2. **목적**: ProbabilityCalculator 객체 초기화
3. **파라미터 타입**: `simulation_engine: SimulationEngine`
4. **반환값 구조**: `None` (객체 초기화)
5. **중요도**: ⭐ (초기화)
6. **호출하는 주요 함수**: 없음
7. **사용되는 곳**: `PokemonPocketSimulator.setup_simulation()`
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 시뮬레이션 엔진 참조 저장

### ⭐ _is_basic_pokemon
1. **함수명 + 위치**: `ProbabilityCalculator._is_basic_pokemon` (probability_calculator.py:30)
2. **목적**: 카드명이 Basic Pokemon인지 판별하는 헬퍼 함수
3. **파라미터 타입**: `card_name: str`
4. **반환값 구조**: `bool`
5. **중요도**: ⭐ (유틸리티)
6. **호출하는 주요 함수**: 없음 (덱 검색)
7. **사용되는 곳**: 모든 Basic Pokemon 관련 확률 계산
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 시뮬레이션 엔진의 덱에서 해당 카드 찾아서 타입 체크

### ⭐ _combination
1. **함수명 + 위치**: `ProbabilityCalculator._combination` (probability_calculator.py:36)
2. **목적**: 조합 계산 (nCk) 수학 유틸리티
3. **파라미터 타입**: `n: int, k: int`
4. **반환값 구조**: `int`
5. **중요도**: ⭐ (수학 유틸리티)
6. **호출하는 주요 함수**: `math.factorial()`
7. **사용되는 곳**: 수학적 확률 계산 함수들
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: n! / (k! × (n-k)!) 계산

### ⭐ _hypergeometric_probability
1. **함수명 + 위치**: `ProbabilityCalculator._hypergeometric_probability` (probability_calculator.py:42)
2. **목적**: 하이퍼지오메트릭 분포 확률 계산
3. **파라미터 타입**: `N: int, K: int, n: int, k: int`
4. **반환값 구조**: `float`
5. **중요도**: ⭐ (수학 유틸리티)
6. **호출하는 주요 함수**: `_combination()`
7. **사용되는 곳**: 수학적 확률 계산 함수들
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: C(K,k) × C(N-K,n-k) / C(N,n) 계산

### ⭐ _probability_basic_at_least_one
1. **함수명 + 위치**: `ProbabilityCalculator._probability_basic_at_least_one` (probability_calculator.py:63)
2. **목적**: 5장 드로우에서 Basic Pokemon이 최소 1장 나올 확률 계산
3. **파라미터 타입**: 없음
4. **반환값 구조**: `float`
5. **중요도**: ⭐ (수학적 기본 확률)
6. **호출하는 주요 함수**: `_hypergeometric_probability()`
7. **사용되는 곳**: 수학적 확률 계산 함수들
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 1 - P(Basic Pokemon 0장) = P(Basic Pokemon 1장 이상)

### ⭐ print_calculation_result
1. **함수명 + 위치**: `ProbabilityCalculator.print_calculation_result` (probability_calculator.py:432)
2. **목적**: 확률 계산 결과를 포맷팅해서 콘솔에 출력
3. **파라미터 타입**: `result: Dict[str, Any]`
4. **반환값 구조**: `None` (콘솔 출력)
5. **중요도**: ⭐ (출력 유틸리티)
6. **호출하는 주요 함수**: `print()`
7. **사용되는 곳**: `run_calculation()`, 테스트 파일들
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 결과 타입별 포맷팅 → 확률, 성공률, 시뮬레이션 정보 출력

---

## 🃏 card_effects.py

### ⭐⭐⭐ use_card_effect
1. **함수명 + 위치**: `CardEffects.use_card_effect` (card_effects.py:308)
2. **목적**: 카드명에 따라 적절한 카드 효과 함수를 호출하는 총괄 함수
3. **파라미터 타입**: `card_name: str, game_state: GameState`
4. **반환값 구조**: `Dict[str, Any]` (카드별로 다름, 공통적으로 'description' 키 포함)
5. **중요도**: ⭐⭐⭐ (모든 카드 효과의 진입점)
6. **호출하는 주요 함수**: `poke_ball()`, `professors_research()`, `galdion()`, `iono()`, `pokemon_communication()`
7. **사용되는 곳**: `_use_draw_cards()`
8. **버전 정보**: v1.0 (지속적으로 새 카드 추가)
9. **핵심 로직 요약**: 카드명 매칭 → 해당 카드 효과 함수 호출 → 결과 반환 또는 오류 처리

### ⭐⭐⭐ iono
1. **함수명 + 위치**: `CardEffects.iono` (card_effects.py:141)
2. **목적**: Iono 카드 효과 - 손패와 드로우더미 셔플 후 3장 드로우
3. **파라미터 타입**: `game_state: GameState`
4. **반환값 구조**: `{'cards_drawn': int, 'description': str}`
5. **중요도**: ⭐⭐⭐ (v2.02에서 핵심 개선 대상)
6. **호출하는 주요 함수**: `game_state.draw_cards()`
7. **사용되는 곳**: `use_card_effect()` → `_use_draw_cards()`
8. **버전 정보**: v2.01 추가
9. **핵심 로직 요약**: 현재 손패를 덱에 합치기 → 전체 셔플 → 3장 드로우 → 새로운 손패 구성

### ⭐⭐⭐ should_use_iono
1. **함수명 + 위치**: `CardEffects.should_use_iono` (card_effects.py:182)
2. **목적**: 기존 multi_card 상황에서 Iono 사용 여부를 판단
3. **파라미터 타입**: `game_state: GameState, target_cards: List[str]`
4. **반환값 구조**: `{'should_use': bool, 'reason': str, 'current_count': int, 'target_count': int}`
5. **중요도**: ⭐⭐⭐ (Iono 스마트 사용의 핵심)
6. **호출하는 주요 함수**: 없음 (순수 판단 로직)
7. **사용되는 곳**: `_use_draw_cards()` (기존 multi_card 처리)
8. **버전 정보**: v2.01 추가 (v2.02에서 multi_or_multi와 분리)
9. **핵심 로직 요약**: 현재 보유 목표 카드 수 체크 → 목표 대비 비율 계산 → 30% 이하일 때만 Iono 사용

### ⭐⭐ poke_ball
1. **함수명 + 위치**: `CardEffects.poke_ball` (card_effects.py:25)
2. **목적**: Poke Ball 효과 - 덱에서 랜덤 Basic Pokemon을 손으로
3. **파라미터 타입**: `game_state: GameState`
4. **반환값 구조**: `bool` (성공 여부)
5. **중요도**: ⭐⭐ (기본 드로우 카드)
6. **호출하는 주요 함수**: `random.choice()`
7. **사용되는 곳**: `use_card_effect()`
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 덱에서 Basic Pokemon 필터링 → 랜덤 선택 → 손패로 이동 → 덱에서 제거

### ⭐⭐ professors_research
1. **함수명 + 위치**: `CardEffects.professors_research` (card_effects.py:49)
2. **목적**: Professor's Research 효과 - 덱에서 2장 드로우
3. **파라미터 타입**: `game_state: GameState`
4. **반환값 구조**: `int` (드로우한 카드 수)
5. **중요도**: ⭐⭐ (기본 드로우 카드)
6. **호출하는 주요 함수**: `game_state.draw_cards()`
7. **사용되는 곳**: `use_card_effect()`
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 덱에서 2장 드로우 → 손패에 추가 → 드로우한 카드 수 반환

### ⭐⭐ galdion
1. **함수명 + 위치**: `CardEffects.galdion` (card_effects.py:63)
2. **목적**: Galdion 효과 - 덱에서 랜덤 'Type:Null' 또는 'Silvally'를 손으로
3. **파라미터 타입**: `game_state: GameState`
4. **반환값 구조**: `bool` (성공 여부)
5. **중요도**: ⭐⭐ (특수 서치 카드)
6. **호출하는 주요 함수**: `random.choice()`
7. **사용되는 곳**: `use_card_effect()`
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 덱에서 Type:Null/Silvally 필터링 → 랜덤 선택 → 손패로 이동 → 덱에서 제거

### ⭐⭐ pokemon_communication
1. **함수명 + 위치**: `CardEffects.pokemon_communication` (card_effects.py:87)
2. **목적**: Pokemon Communication 효과 - Pokemon 교환 (손패 → 덱, 덱 → 손패)
3. **파라미터 타입**: `game_state: GameState, sacrifice_pokemon_name: str = None`
4. **반환값 구조**: `Dict[str, Any]` (교환 결과 정보)
5. **중요도**: ⭐⭐ (v2.01 추가 카드)
6. **호출하는 주요 함수**: `random.choice()`, `game_state.deck.append()`
7. **사용되는 곳**: `use_card_effect()`
8. **버전 정보**: v2.01 추가
9. **핵심 로직 요약**: 손패 Pokemon 선택 → 덱으로 보냄 → 덱에서 다른 Pokemon 선택 → 손패로 가져옴

### ⭐⭐ should_use_pokemon_communication
1. **함수명 + 위치**: `CardEffects.should_use_pokemon_communication` (card_effects.py:245)
2. **목적**: Pokemon Communication 사용 여부 및 교환 대상 결정
3. **파라미터 타입**: `game_state: GameState, target_cards: List[str], max_turn: int`
4. **반환값 구조**: `Dict[str, Any]` (사용 여부, 이유, 교환 대상)
5. **중요도**: ⭐⭐ (스마트 사용 로직)
6. **호출하는 주요 함수**: 없음 (순수 로직 함수)
7. **사용되는 곳**: `_use_draw_cards()` (마지막 턴에서만)
8. **버전 정보**: v2.01 추가
9. **핵심 로직 요약**: 목표 Pokemon 부족 체크 → 교환 가능 Pokemon 존재 체크 → 마지막 턴에서만 사용

### ⭐ get_draw_cards_list
1. **함수명 + 위치**: `get_draw_cards_list` (card_effects.py:398)
2. **목적**: 드로우 효과가 있는 모든 카드 목록 반환
3. **파라미터 타입**: 없음
4. **반환값 구조**: `List[str]` (드로우 카드명 목록)
5. **중요도**: ⭐ (정보 제공 유틸리티)
6. **호출하는 주요 함수**: 없음
7. **사용되는 곳**: 드로우 순서 설정, 검증
8. **버전 정보**: v1.0 (지속적으로 새 카드 추가)
9. **핵심 로직 요약**: 하드코딩된 드로우 카드 리스트 반환

### ⭐ is_draw_card
1. **함수명 + 위치**: `is_draw_card` (card_effects.py:402)
2. **목적**: 특정 카드가 드로우 효과를 가지는지 판별
3. **파라미터 타입**: `card_name: str`
4. **반환값 구조**: `bool`
5. **중요도**: ⭐ (유틸리티)
6. **호출하는 주요 함수**: `get_draw_cards_list()`
7. **사용되는 곳**: 드로우 카드 필터링
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 드로우 카드 목록에서 해당 카드명 검색

### ⭐ get_card_effect_description
1. **함수명 + 위치**: `get_card_effect_description` (card_effects.py:406)
2. **목적**: 카드별 효과 설명 텍스트 반환
3. **파라미터 타입**: `card_name: str`
4. **반환값 구조**: `str` (효과 설명)
5. **중요도**: ⭐ (정보 제공 유틸리티)
6. **호출하는 주요 함수**: 없음
7. **사용되는 곳**: 사용자 인터페이스, 도움말
8. **버전 정보**: v1.0
9. **핵심 로직 요약**: 카드명별 효과 설명 딕셔너리에서 검색 후 반환

---

## 📊 완전한 함수 목록 요약

### 📈 **총 함수 개수**: 51개

### **⭐⭐⭐ 핵심 함수** (11개)
- **시뮬레이션 엔진**: `simulate_single_game`, `_use_draw_cards`, `_should_use_iono_for_multi_or_multi`
- **확률 계산**: `calculate_multi_card_probability`, `calculate_multi_or_multi_probability`, `calculate_preferred_and_multi_probability`, `calculate_non_preferred_and_multi_probability`
- **카드 효과**: `use_card_effect`, `iono`, `should_use_iono`

### **⭐⭐ 중요 함수** (20개)  
- **시뮬레이션 관리**: `validate_deck_input`, `validate_calculation_request`, `setup_simulation`, `run_calculation (main)`, `GameState.__init__`, `SimulationEngine.__init__`, `reset_game`, `draw_cards`, `initial_draw`
- **확률 계산**: `calculate_preferred_opening_probability`, `calculate_non_preferred_opening_probability`, `run_calculation (prob)`, `calculate_preferred_opening_mathematical`, `calculate_non_preferred_opening_mathematical`
- **카드 효과**: `poke_ball`, `professors_research`, `galdion`, `pokemon_communication`, `should_use_pokemon_communication`

### **⭐ 보조 함수** (20개)
- **유틸리티**: `load_deck_from_file`, `load_test_cases_from_file`, `create_deck`, `print_deck_summary`, `print_deck_info`, `main`, `run_test_suite`
- **데이터 모델**: `Card.__init__`, `Card.__str__`, `Card.__repr__`, `Card.__eq__`, `PokemonPocketSimulator.__init__`, `start_turn`
- **수학 계산**: `_is_basic_pokemon`, `_combination`, `_hypergeometric_probability`, `_probability_basic_at_least_one`, `ProbabilityCalculator.__init__`
- **카드 효과 지원**: `get_draw_cards_list`, `is_draw_card`, `get_card_effect_description`
- **출력**: `print_calculation_result`

### **🎯 파일별 분포**
- **main_simulator.py**: 25개 함수 (시뮬레이션 엔진 + 관리 + 유틸리티)
- **probability_calculator.py**: 15개 함수 (확률 계산 + 수학 유틸리티)
- **card_effects.py**: 11개 함수 (카드 효과 + 지원 함수)

### **📅 버전별 추가 현황**
- **v1.0**: 기본 시뮬레이션 + 확률 계산 + 기본 카드 효과 (44개)
- **v2.01**: Iono 카드 + Pokemon Communication (4개)
- **v2.02**: 복합 확률 계산 3종 + multi_or_multi Iono 충돌 해결 (3개)

### **🔍 함수 검색 가이드**
이 문서를 활용해 다음과 같이 빠르게 함수를 찾을 수 있습니다:
- **기능별 검색**: "확률 계산" → ⭐⭐⭐ 섹션의 calculate_ 함수들
- **파일별 검색**: "main_simulator.py" → 해당 섹션에서 25개 함수 확인
- **버전별 검색**: "v2.02" → 새로 추가된 3개 함수 확인
- **중요도별 검색**: 핵심 작업은 ⭐⭐⭐, 일반 작업은 ⭐⭐ 위주로 확인

---

*생성일: 2025-06-05*  
*대상 버전: v2.02*  
*전체 함수 수: 51개*  
*참조 목적: 중복 함수 작성 방지 및 빠른 함수 탐색*

---

## 📊 함수 중요도별 요약

### ⭐⭐⭐ 핵심 함수 (11개)
- **시뮬레이션 엔진**: `simulate_single_game`, `_use_draw_cards`, `_should_use_iono_for_multi_or_multi`
- **확률 계산**: `calculate_multi_card_probability`, `calculate_multi_or_multi_probability`, `calculate_preferred_and_multi_probability`, `calculate_non_preferred_and_multi_probability`
- **카드 효과**: `use_card_effect`, `iono`, `should_use_iono`

### ⭐⭐ 중요 함수 (5개)
- **시뮬레이션 관리**: `validate_deck_input`, `setup_simulation`
- **확률 계산**: `calculate_preferred_opening_probability`
- **카드 효과**: `poke_ball`, `professors_research`

### 📈 버전별 추가 현황
- **v1.0**: 기본 시뮬레이션 + 확률 계산 + 기본 카드 효과
- **v2.01**: Iono 카드 추가 + 스마트 사용 로직
- **v2.02**: 복합 확률 계산 3종 + multi_or_multi Iono 충돌 해결

---

*생성일: 2025-06-05*
*대상 버전: v2.02*