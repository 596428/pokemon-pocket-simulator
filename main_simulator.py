# Pokemon Pocket Simulator - 메인 실행 함수 (확률 계산 모듈 분리 버전)
import random
import copy
from collections import defaultdict
from typing import Dict, List, Tuple, Any

# 확률 계산기 모듈 import
from probability_calculator import ProbabilityCalculator
# 카드 효과 모듈 import
from card_effects import CardEffects, DRAW_CARDS, get_draw_cards_list, is_draw_card
import json
import os

# 파일 읽기 함수들
def load_deck_from_file(filename: str = "DeckList.txt") -> Dict[str, Dict[str, Any]]:
    """DeckList.txt 파일에서 덱 정보를 읽어와서 딕셔너리로 변환"""
    deck = {}
    draw_order = []
    
    # 절대 경로 생성
    if not os.path.isabs(filename):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, filename)
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 주석이나 빈 줄 건너뛰기
                if not line or line.startswith('#'):
                    continue
                
                # 카드 정보 파싱 (카드명 | 카드타입 | 장수)
                if '|' in line:
                    parts = [part.strip() for part in line.split('|')]
                    if len(parts) == 3:
                        card_name = parts[0]
                        card_type = parts[1]
                        count = int(parts[2])
                        deck[card_name] = {"type": card_type, "count": count}
        
        # 드로우 순서는 하드코딩으로 설정 (나중에 파일에서 읽도록 개선 가능)
        draw_order = ["Poke Ball", "Professor's Research", "Galdion"]
        
    except FileNotFoundError:
        print(f"❌ {filename} 파일을 찾을 수 없습니다.")
        return None, None
    except Exception as e:
        print(f"❌ 덱 파일 읽기 오류: {e}")
        return None, None
    
    return deck, draw_order

def load_test_cases_from_file(filename: str = "TestCase.txt") -> Tuple[List[Dict], List[str], int]:
    """TestCase.txt 파일에서 테스트 케이스들을 읽어와서 리스트로 변환"""
    test_cases = []
    draw_order = []
    simulation_count = 2000
    
    # 절대 경로 생성
    if not os.path.isabs(filename):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, filename)
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # JSON 블록들을 찾아서 파싱
        lines = content.split('\n')
        json_lines = []
        in_json = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('{'):
                in_json = True
                json_lines = [line]
            elif line.startswith('}'):
                json_lines.append(line)
                in_json = False
                # JSON 파싱 시도
                try:
                    json_str = '\n'.join(json_lines)
                    data = json.loads(json_str)
                    
                    # 테스트 케이스인지 설정인지 구분
                    if 'request' in data:
                        test_cases.append(data)
                    elif 'draw_order' in data:
                        draw_order = data.get('draw_order', [])
                        simulation_count = data.get('simulation_count', 2000)
                except json.JSONDecodeError:
                    continue
            elif in_json:
                json_lines.append(line)
        
    except FileNotFoundError:
        print(f"❌ {filename} 파일을 찾을 수 없습니다.")
        return None, None, None
    except Exception as e:
        print(f"❌ 테스트 케이스 파일 읽기 오류: {e}")
        return None, None, None
    
    return test_cases, draw_order, simulation_count

# 카드 클래스
class Card:
    def __init__(self, name: str, card_type: str):
        self.name = name
        self.card_type = card_type
    
    def __str__(self):
        return f"{self.name} ({self.card_type})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.name == other.name and self.card_type == other.card_type
        return False

# 덱 생성 함수
def create_deck(deck_input: Dict[str, Dict[str, Any]]) -> List[Card]:
    deck = []
    total_cards = 0
    
    for card_name, card_info in deck_input.items():
        card_type = card_info["type"]
        count = card_info["count"]
        
        for _ in range(count):
            deck.append(Card(card_name, card_type))
            total_cards += 1
    
    if total_cards != 20:
        raise ValueError(f"덱은 반드시 20장이어야 합니다. 현재: {total_cards}장")
    
    return deck

def print_deck_summary(deck: List[Card]):
    card_count = defaultdict(int)
    type_count = defaultdict(int)
    
    for card in deck:
        card_count[card.name] += 1
        type_count[card.card_type] += 1
    
    print(f"=== 덱 구성 (총 {len(deck)}장) ===")
    for card_name, count in sorted(card_count.items()):
        card_type = next(card.card_type for card in deck if card.name == card_name)
        print(f"{card_name} ({card_type}): {count}장")
    
    print("\n=== 타입별 분포 ===")
    for card_type, count in sorted(type_count.items()):
        print(f"{card_type}: {count}장")

# 게임 상태 관리 클래스
class GameState:
    def __init__(self, deck_input: Dict[str, Dict[str, Any]], draw_order: List[str] = None):
        self.original_deck = create_deck(deck_input)
        self.deck = copy.deepcopy(self.original_deck)
        self.hand = []
        self.turn = 0
        self.draw_order = draw_order or []
        random.shuffle(self.deck)
    
    def reset_game(self):
        self.deck = copy.deepcopy(self.original_deck)
        self.hand = []
        self.turn = 0
        random.shuffle(self.deck)
    
    def draw_cards(self, count: int) -> List[Card]:
        drawn = []
        for _ in range(min(count, len(self.deck))):
            if self.deck:
                card = self.deck.pop(0)
                self.hand.append(card)
                drawn.append(card)
        return drawn
    
    def initial_draw(self) -> bool:
        max_attempts = 50
        attempts = 0
        
        while attempts < max_attempts:
            self.hand = []
            self.deck = copy.deepcopy(self.original_deck)
            random.shuffle(self.deck)
            
            self.draw_cards(5)
            
            has_basic_pokemon = any(card.card_type == "Basic Pokemon" for card in self.hand)
            
            if has_basic_pokemon:
                return True
                
            attempts += 1
        
        print(f"경고: {max_attempts}번 시도 후에도 Basic Pokemon을 찾지 못했습니다.")
        return False
    
    def start_turn(self):
        if self.turn > 0:
            self.draw_cards(1)

# 시뮬레이션 엔진
class SimulationEngine:
    def __init__(self, deck_input: Dict[str, Dict[str, Any]], draw_order: List[str] = None):
        self.deck_input = deck_input
        self.draw_order = draw_order or []
        self.available_draw_cards = [card_name for card_name in deck_input.keys() if card_name in DRAW_CARDS]
    
    def simulate_single_game(self, max_turn: int = 2, verbose: bool = False, target_cards: List[str] = None) -> Dict[str, Any]:
        game_state = GameState(self.deck_input, self.draw_order)
        result = {
            'success': False,
            'turn_results': {},
            'final_hand': [],
            'cards_used': []
        }
        
        # 0턴: 초기 5장 드로우
        success = game_state.initial_draw()
        if not success:
            return result
        
        result['success'] = True
        
        # 각 턴 시뮬레이션
        for turn in range(max_turn + 1):
            game_state.turn = turn
            
            if turn > 0:
                game_state.start_turn()
            
            turn_hand = [card.name for card in game_state.hand]
            result['turn_results'][turn] = {
                'hand_before_effects': turn_hand.copy(),
                'cards_used_this_turn': [],
                'hand_after_effects': []
            }
            
            # 1턴부터 카드 효과 사용
            if turn > 0:
                cards_used_this_turn = self._use_draw_cards(game_state, verbose, target_cards, max_turn)
                result['turn_results'][turn]['cards_used_this_turn'] = cards_used_this_turn
                result['cards_used'].extend(cards_used_this_turn)
            
            final_turn_hand = [card.name for card in game_state.hand]
            result['turn_results'][turn]['hand_after_effects'] = final_turn_hand
        
        result['final_hand'] = [card.name for card in game_state.hand]
        return result
    
    def _use_draw_cards(self, game_state: GameState, verbose: bool = False, target_cards: List[str] = None, max_turn: int = None) -> List[str]:
        """
        한 턴에서 드로우 카드들을 사용하는 함수 (올바른 게임 규칙 + Pokemon Communication 연쇄 로직)
        
        게임 규칙:
        - Supporter: 1턴에 1장만 사용 가능
        - Item: 1턴에 여러장 사용 가능
        - Supporter 사용해도 Item은 계속 사용 가능
        """
        cards_used = []
        supporter_used = False  # Supporter 사용 여부 추적
        max_iterations = 10  # 무한루프 방지
        
        for iteration in range(max_iterations):
            cards_used_this_iteration = 0
            
            if verbose and iteration > 0:
                print(f"  === 연쇄 사용 루프 {iteration + 1}회차 ===")
            
            # 1단계: 일반 드로우카드들 사용 (Pokemon Communication 제외)
            regular_draw_cards = [card_name for card_name in self.draw_order if card_name != "Pokemon Communication"]
            
            for card_name in regular_draw_cards:
                cards_in_hand = [card for card in game_state.hand if card.name == card_name]
                
                for card in cards_in_hand:
                    # Supporter 제한 체크
                    if card.card_type == "Supporter" and supporter_used:
                        if verbose:
                            print(f"  {card_name} (Supporter) 건너뜀 - 이미 Supporter 사용함")
                        continue
                    
                    if verbose:
                        print(f"  {card_name} 사용 시도...")
                    
                    effect_result = CardEffects.use_card_effect(card_name, game_state)
                    
                    if verbose:
                        print(f"    결과: {effect_result['description']}")
                    
                    game_state.hand.remove(card)
                    cards_used.append(card_name)
                    cards_used_this_iteration += 1
                    
                    # Supporter 사용 체크
                    if card.card_type == "Supporter":
                        supporter_used = True
                        if verbose:
                            print(f"    Supporter 사용됨 - 이번 턴 추가 Supporter 사용 불가")
            
            # 2단계: Pokemon Communication 평가 (마지막 턴에서만)
            if target_cards and max_turn is not None and game_state.turn == max_turn:
                pokemon_comm_cards = [card for card in game_state.hand if card.name == "Pokemon Communication"]
                
                for pokemon_comm_card in pokemon_comm_cards:
                    # Pokemon Communication 사용 여부 판단
                    decision = CardEffects.should_use_pokemon_communication(game_state, target_cards, max_turn)
                    
                    if decision["should_use"]:
                        if verbose:
                            print(f"  Pokemon Communication 사용 결정: {decision['reason']}")
                            print(f"  교환 대상 Pokemon: {decision.get('chosen_pokemon', 'auto')}")
                        
                        # Pokemon Communication 사용
                        chosen_pokemon = decision.get("chosen_pokemon")
                        pc_result = CardEffects.pokemon_communication(game_state, chosen_pokemon)
                        
                        if pc_result["success"]:
                            if verbose:
                                print(f"    결과: {pc_result['description']}")
                            
                            game_state.hand.remove(pokemon_comm_card)
                            cards_used.append("Pokemon Communication")
                            cards_used_this_iteration += 1
                        else:
                            if verbose:
                                print(f"    실패: {pc_result['description']}")
                    else:
                        if verbose:
                            print(f"  Pokemon Communication 사용 안함: {decision['reason']}")
            
            # 3단계: 더 이상 사용할 카드가 없으면 루프 종료
            if cards_used_this_iteration == 0:
                if verbose and iteration > 0:
                    print(f"  연쇄 사용 완료 (총 {iteration + 1}회 반복)")
                break
        
        if verbose and cards_used_this_iteration > 0:
            print(f"  ⚠️ 최대 반복 횟수({max_iterations})에 도달하여 강제 종료")
        
        return cards_used

# ==================== 메인 실행 함수 ====================

class PokemonPocketSimulator:
    def __init__(self):
        self.sim_engine = None
        self.prob_calculator = None
        self.current_deck = None
        self.current_draw_order = None
    
    def validate_deck_input(self, deck_input: Dict[str, Dict[str, Any]]) -> bool:
        """덱 입력값 검증"""
        try:
            total_cards = sum(card_info["count"] for card_info in deck_input.values())
            if total_cards != 20:
                print(f"❌ 오류: 덱은 반드시 20장이어야 합니다. 현재: {total_cards}장")
                return False
            
            # 각 카드가 최대 2장인지 확인
            for card_name, card_info in deck_input.items():
                if card_info["count"] > 2:
                    print(f"❌ 오류: '{card_name}'이 {card_info['count']}장입니다. 같은 카드는 최대 2장까지만 가능합니다.")
                    return False
            
            # 덱 생성 테스트
            create_deck(deck_input)
            print("✅ 덱 입력값 검증 통과")
            return True
            
        except Exception as e:
            print(f"❌ 덱 입력값 오류: {e}")
            return False
    
    def validate_calculation_request(self, calculation_request: Dict[str, Any]) -> bool:
        """계산 요청 검증 (v2.0)"""
        try:
            calc_type = calculation_request.get("type")
            supported_types = ["preferred_opening", "non_preferred_opening", "multi_card"]
            
            if calc_type not in supported_types:
                print(f"❌ 오류: 지원하지 않는 계산 타입입니다: {calc_type}")
                print(f"지원되는 타입: {', '.join(supported_types)}")
                return False
            
            # 타입별 필수 필드 검증
            if calc_type == "preferred_opening":
                preferred_basics = calculation_request.get("preferred_basics", [])
                if not preferred_basics:
                    print("❌ 오류: preferred_basics가 비어있습니다.")
                    return False
                    
            elif calc_type == "non_preferred_opening":
                non_preferred_basics = calculation_request.get("non_preferred_basics", [])
                if not non_preferred_basics:
                    print("❌ 오류: non_preferred_basics가 비어있습니다.")
                    return False
                    
            elif calc_type == "multi_card":
                target_cards = calculation_request.get("target_cards", [])
                if not target_cards:
                    print("❌ 오류: target_cards가 비어있습니다.")
                    return False
                if len(target_cards) > 3:
                    print("❌ 오류: target_cards는 최대 3개까지만 지원합니다.")
                    return False
                    
                turn = calculation_request.get("turn", 2)
                if not isinstance(turn, int) or turn < 1:
                    print("❌ 오류: turn은 1 이상의 정수여야 합니다.")
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ 계산 요청 오류: {e}")
            return False
    
    def setup_simulation(self, deck_input: Dict[str, Dict[str, Any]], draw_order: List[str] = None):
        """시뮬레이션 설정"""
        print("\n" + "="*60)
        print("시뮬레이션 설정 중...")
        print("="*60)
        
        # 덱 입력값 검증
        if not self.validate_deck_input(deck_input):
            return False
        
        # 드로우 순서 설정
        available_draw_cards = [card_name for card_name in deck_input.keys() if card_name in DRAW_CARDS]
        
        if draw_order is None:
            draw_order = available_draw_cards
            print(f"드로우 카드 발동 순서 (기본값): {draw_order}")
        else:
            # 입력된 순서가 유효한지 확인
            invalid_cards = [card for card in draw_order if card not in available_draw_cards]
            if invalid_cards:
                print(f"❌ 오류: 다음 카드들은 덱에 없거나 드로우 카드가 아닙니다: {invalid_cards}")
                return False
            print(f"드로우 카드 발동 순서 (사용자 설정): {draw_order}")
        
        # 시뮬레이션 엔진 및 확률 계산기 생성
        self.sim_engine = SimulationEngine(deck_input, draw_order)
        self.prob_calculator = ProbabilityCalculator(self.sim_engine)  # 분리된 모듈 사용
        self.current_deck = deck_input
        self.current_draw_order = draw_order
        
        print("✅ 시뮬레이션 설정 완료")
        return True
    
    def run_calculation(self, calculation_request: Dict[str, Any], simulation_count: int = 10000):
        """확률 계산 실행 (v2.0)"""
        
        # 계산 요청 검증
        if not self.validate_calculation_request(calculation_request):
            return None
        
        # 시뮬레이션이 설정되어 있는지 확인
        if self.sim_engine is None or self.prob_calculator is None:
            print("❌ 오류: 시뮬레이션이 설정되어 있지 않습니다. setup_simulation()을 먼저 호출하세요.")
            return None
        
        print("✅ 계산 요청 검증 통과")
        
        # ProbabilityCalculator의 run_calculation 메서드에 위임
        result = self.prob_calculator.run_calculation(calculation_request, simulation_count)
        
        return result
    
    def print_deck_info(self):
        """현재 덱 정보 출력"""
        if self.current_deck is None:
            print("❌ 덱이 설정되어 있지 않습니다.")
            return
        
        print("\n" + "="*60)
        print("현재 덱 정보")
        print("="*60)
        
        deck = create_deck(self.current_deck)
        print_deck_summary(deck)
        
        # 드로우 카드 정보
        draw_cards_in_deck = [card.name for card in deck if card.name in DRAW_CARDS]
        unique_draw_cards = list(set(draw_cards_in_deck))
        
        if unique_draw_cards:
            print(f"\n=== 드로우 카드 ===")
            for card_name in unique_draw_cards:
                count = draw_cards_in_deck.count(card_name)
                print(f"{card_name}: {count}장")
            print(f"발동 순서: {self.current_draw_order}")
        else:
            print("\n=== 드로우 카드 없음 ===")

def main():
    """메인 실행 함수 (파일에서 설정 읽기)"""
    print("Pokemon Pocket Card Draw Simulator")
    print("="*60)
    print("확률 계산 모듈이 분리된 버전입니다.")
    print("📁 파일에서 덱 설정과 테스트 케이스를 읽어옵니다.\n")
    
    # 시뮬레이터 인스턴스 생성
    simulator = PokemonPocketSimulator()
    
    # 파일에서 덱 정보 읽기
    print("📁 DeckList.txt에서 덱 정보를 읽는 중...")
    deck, draw_order = load_deck_from_file()
    if deck is None or draw_order is None:
        print("❌ 덱 파일 읽기 실패")
        return
    
    # 파일에서 테스트 케이스 읽기 (첫 번째 케이스만 사용)
    print("📁 TestCase.txt에서 첫 번째 테스트 케이스를 읽는 중...")
    test_cases, file_draw_order, simulation_count = load_test_cases_from_file()
    if test_cases is None or len(test_cases) == 0:
        print("❌ 테스트 케이스 파일 읽기 실패")
        return
    
    # 파일에 있는 드로우 순서가 있으면 그것을 우선 사용
    if file_draw_order:
        draw_order = file_draw_order
    
    # 첫 번째 테스트 케이스 사용
    calculation_request = test_cases[0]["request"]
    
    print(f"✅ 덱 정보 로드 완료: {len(deck)}종류 카드")
    print(f"✅ 테스트 케이스: {test_cases[0]['name']}")
    print(f"✅ 드로우 순서: {' → '.join(draw_order)}")
    print(f"✅ 시뮬레이션 횟수: {simulation_count:,}회")
    
    print("\n=== 단일 테스트 실행 ===")
    print(f"- 계산 타입: {calculation_request['type']}")
    
    # 계산 타입에 따른 추가 정보 출력
    calc_type = calculation_request['type']
    if calc_type == "preferred_opening":
        print(f"- 선호 Basic Pokemon: {calculation_request.get('preferred_basics', [])}")
    elif calc_type == "non_preferred_opening":
        print(f"- 비선호 Basic Pokemon: {calculation_request.get('non_preferred_basics', [])}")
    elif calc_type == "multi_card":
        print(f"- 대상 카드: {calculation_request.get('target_cards', [])}")
        print(f"- 턴 수: {calculation_request.get('turn', 2)}")
    else:
        print(f"- 요청 내용: {calculation_request}")
    
    print(f"- 시뮬레이션 횟수: {simulation_count:,}회")
    
    # 1. 시뮬레이션 설정
    setup_success = simulator.setup_simulation(deck, draw_order)
    if not setup_success:
        print("❌ 시뮬레이션 설정 실패")
        return
    
    # 2. 덱 정보 출력
    simulator.print_deck_info()
    
    # 3. 확률 계산 실행
    result = simulator.run_calculation(calculation_request, simulation_count)
    
    if result:
        print("\n" + "="*60)
        print("시뮬레이션 완료!")
        print("="*60)
        print("✅ 테스트가 성공적으로 완료되었습니다.")
        print("📁 파일에서 성공적으로 읽어와 실행하였습니다.")
    else:
        print("\n❌ 시뮬레이션 실행 중 오류가 발생하였습니다.")

def run_test_suite():
    """모든 테스트의 확률 계산 테스트 실행 (파일에서 설정 읽기)"""
    print("Pokemon Pocket Simulator - 전체 테스트 스위트")
    print("="*60)
    
    # 시뮬레이터 인스턴스 생성
    simulator = PokemonPocketSimulator()
    
    # 파일에서 덱 정보 읽기
    print("📁 DeckList.txt에서 덱 정보를 읽는 중...")
    deck, draw_order = load_deck_from_file()
    if deck is None or draw_order is None:
        print("❌ 덱 파일 읽기 실패")
        return
    
    # 파일에서 테스트 케이스 읽기
    print("📁 TestCase.txt에서 테스트 케이스를 읽는 중...")
    test_cases, file_draw_order, simulation_count = load_test_cases_from_file()
    if test_cases is None:
        print("❌ 테스트 케이스 파일 읽기 실패")
        return
    
    # 파일에 있는 드로우 순서가 있으면 그것을 우선 사용
    if file_draw_order:
        draw_order = file_draw_order
    
    print(f"✅ 덱 정보 로드 완료: {len(deck)}종류 카드")
    print(f"✅ 테스트 케이스 로드 완료: {len(test_cases)}개 케이스")
    print(f"✅ 드로우 순서: {' → '.join(draw_order)}")
    print(f"✅ 시뮬레이션 횟수: {simulation_count:,}회")
    
    # 시뮬레이션 설정
    setup_success = simulator.setup_simulation(deck, draw_order)
    if not setup_success:
        print("❌ 시뮬레이션 설정 실패")
        return
    
    # 덱 정보 출력
    simulator.print_deck_info()
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n" + "="*80)
        print(f"테스트 {i}/{len(test_cases)}: {test_case['name']}")
        print("="*80)
        
        result = simulator.run_calculation(test_case["request"], simulation_count)
        if result:
            results.append(result)
        else:
            print(f"❌ 테스트 {i} 실패")
    
    # 전체 결과 요약
    print(f"\n" + "="*80)
    print("전체 테스트 결과 요약")
    print("="*80)
    
    for i, result in enumerate(results, 1):
        print(f"테스트 {i}: {result['description']}")
        print(f"  확률: {result['probability_percent']:.2f}%")
        print()
    
    print(f"✅ 전체 테스트 완료: {len(results)}/{len(test_cases)}개 성공")
    print("📁 모든 설정이 파일에서 성공적으로 로드되었습니다.")

if __name__ == "__main__":
    # 사용에 따라 단일 테스트 또는 전체 테스트 실행
    print("실행 모드를 선택하세요:")
    print("1. 단일 테스트 (타입 1)")
    print("2. 전체 테스트 스위트 (타입 1~5)")
    
    # 기본값: 단일 테스트
    try:
        choice = input("선택 (1/2, 기본값: 1): ").strip() or "1"
        
        if choice == "2":
            run_test_suite()
        else:
            main()
    except KeyboardInterrupt:
        print("\n\n프로그램이 종료되었습니다.")
    except Exception as e:
        print(f"\n오류가 발생하였습니다: {e}")
