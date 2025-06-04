# probability_calculator.py - 확률 계산 전용 모듈 (v2.0)
from typing import Dict, List, Any

class ProbabilityCalculator:
    """Pokemon Pocket 시뮬레이터용 확률 계산기 v2.0"""
    
    def __init__(self, simulation_engine):
        """
        확률 계산기 초기화
        
        Args:
            simulation_engine: SimulationEngine 인스턴스
        """
        self.sim_engine = simulation_engine
    
    def _is_basic_pokemon(self, card_name: str) -> bool:
        """카드가 Basic Pokemon인지 확인"""
        deck_input = self.sim_engine.deck_input
        if card_name in deck_input:
            return deck_input[card_name]['type'] == 'Basic Pokemon'
        return False
    
    def calculate_preferred_opening_probability(self, preferred_basics: List[str], num_simulations: int = 10000) -> Dict[str, Any]:
        """
        선호하는 Basic Pokemon으로 시작할 수 있는 확률
        첫 5장에 선호하는 Basic Pokemon 중 1장 이상이 포함될 확률
        
        Args:
            preferred_basics: 선호하는 Basic Pokemon 카드명 리스트
            num_simulations: 시뮬레이션 횟수
        
        Returns:
            Dict: 확률 계산 결과
        """
        print(f"=== 선호하는 Opening 확률 계산 시작 ===")
        print(f"선호하는 Basic Pokemon: {', '.join(preferred_basics)}")
        print(f"시뮬레이션 횟수: {num_simulations:,}회")
        
        success_count = 0
        total_valid_games = 0
        checkpoint = max(1, num_simulations // 10)
        
        for i in range(num_simulations):
            # 진행 상황 출력
            if (i + 1) % checkpoint == 0 or i == 0:
                progress = ((i + 1) / num_simulations) * 100
                print(f"진행률: {progress:.1f}% ({i+1:,}/{num_simulations:,})")
            
            # 0턴(시작 5장)만 시뮬레이션
            game_result = self.sim_engine.simulate_single_game(max_turn=0, verbose=False)
            
            # 게임이 성공적으로 진행된 경우만 체크
            if game_result['success']:
                total_valid_games += 1
                
                # 0턴 손패에서 선호하는 Basic 중 하나라도 있는지 확인
                turn_0_hand = game_result['turn_results'][0]['hand_before_effects']
                
                has_preferred = any(card in turn_0_hand for card in preferred_basics)
                if has_preferred:
                    success_count += 1
        
        # 결과 계산
        if total_valid_games == 0:
            probability = 0.0
        else:
            probability = (success_count / total_valid_games) * 100
        
        result = {
            'calculation_type': 'preferred_opening',
            'description': f'선호하는 Basic Pokemon({", ".join(preferred_basics)})으로 시작할 수 있는 확률',
            'preferred_basics': preferred_basics,
            'probability_percent': round(probability, 2),
            'success_count': success_count,
            'total_valid_games': total_valid_games,
            'simulation_count': num_simulations
        }
        
        print(f"\n=== 선호하는 Opening 확률 계산 완료 ===")
        print(f"성공: {success_count:,}회 / 유효 게임: {total_valid_games:,}회")
        print(f"확률: {probability:.2f}%")
        
        return result

    def calculate_non_preferred_opening_probability(self, non_preferred_basics: List[str], num_simulations: int = 10000) -> Dict[str, Any]:
        """
        비선호하는 Basic Pokemon으로만 시작해야 하는 확률
        첫 5장에 Basic은 있지만 모두 비선호하는 카드인 확률
        
        Args:
            non_preferred_basics: 비선호하는 Basic Pokemon 카드명 리스트
            num_simulations: 시뮬레이션 횟수
        
        Returns:
            Dict: 확률 계산 결과
        """
        print(f"=== 비선호하는 Opening 확률 계산 시작 ===")
        print(f"비선호하는 Basic Pokemon: {', '.join(non_preferred_basics)}")
        print(f"시뮬레이션 횟수: {num_simulations:,}회")
        print("조건: Basic Pokemon은 있지만 모두 비선호하는 카드인 경우")
        
        success_count = 0
        total_valid_games = 0
        checkpoint = max(1, num_simulations // 10)
        
        for i in range(num_simulations):
            if (i + 1) % checkpoint == 0 or i == 0:
                progress = ((i + 1) / num_simulations) * 100
                print(f"진행률: {progress:.1f}% ({i+1:,}/{num_simulations:,})")
            
            # 0턴(시작 5장)만 시뮬레이션
            game_result = self.sim_engine.simulate_single_game(max_turn=0, verbose=False)
            
            if game_result['success']:
                total_valid_games += 1
                
                turn_0_hand = game_result['turn_results'][0]['hand_before_effects']
                
                # Basic Pokemon들만 필터링
                basic_pokemons_in_hand = [card for card in turn_0_hand 
                                        if self._is_basic_pokemon(card)]
                
                # Basic이 있고, 모든 Basic이 비선호 목록에 포함된 경우
                if (len(basic_pokemons_in_hand) > 0 and 
                    all(basic in non_preferred_basics for basic in basic_pokemons_in_hand)):
                    success_count += 1
        
        if total_valid_games == 0:
            probability = 0.0
        else:
            probability = (success_count / total_valid_games) * 100
        
        result = {
            'calculation_type': 'non_preferred_opening',
            'description': f'비선호하는 Basic Pokemon({", ".join(non_preferred_basics)})으로만 시작해야 하는 확률',
            'non_preferred_basics': non_preferred_basics,
            'probability_percent': round(probability, 2),
            'success_count': success_count,
            'total_valid_games': total_valid_games,
            'simulation_count': num_simulations
        }
        
        print(f"\n=== 비선호하는 Opening 확률 계산 완료 ===")
        print(f"성공: {success_count:,}회 / 유효 게임: {total_valid_games:,}회")
        print(f"확률: {probability:.2f}%")
        
        return result

    def calculate_multi_card_probability(self, target_cards: List[str], max_turn: int, num_simulations: int = 10000) -> Dict[str, Any]:
        """
        N턴까지 지정된 카드들을 각각 1장 이상 드로우할 확률
        (기존 타입 3, 4, 5 통합)
        
        Args:
            target_cards: 대상 카드명 리스트 (1~3개)
            max_turn: 최대 턴 수 (1, 2, 3 등)
            num_simulations: 시뮬레이션 횟수
        
        Returns:
            Dict: 확률 계산 결과
        """
        print(f"=== 멀티카드 드로우 확률 계산 시작 ===")
        print(f"대상 카드: {', '.join(target_cards)}")
        print(f"최대 턴: {max_turn}턴")
        print(f"시뮬레이션 횟수: {num_simulations:,}회")
        print(f"조건: {max_turn}턴까지 각 카드를 1장 이상씩 드로우")
        
        success_count = 0
        total_valid_games = 0
        checkpoint = max(1, num_simulations // 10)
        
        for i in range(num_simulations):
            if (i + 1) % checkpoint == 0 or i == 0:
                progress = ((i + 1) / num_simulations) * 100
                print(f"진행률: {progress:.1f}% ({i+1:,}/{num_simulations:,})")
            
            game_result = self.sim_engine.simulate_single_game(max_turn=max_turn, verbose=False)
            
            if game_result['success']:
                total_valid_games += 1
                
                # 최종 손패에서 모든 대상 카드가 있는지 확인
                final_hand = game_result['final_hand']
                
                # 모든 카드가 1장 이상씩 있는지 확인
                all_cards_found = all(card in final_hand for card in target_cards)
                if all_cards_found:
                    success_count += 1
        
        if total_valid_games == 0:
            probability = 0.0
        else:
            probability = (success_count / total_valid_games) * 100
        
        result = {
            'calculation_type': 'multi_card',
            'description': f'{max_turn}턴까지 {", ".join(target_cards)} 각각 1장 이상 드로우 확률',
            'target_cards': target_cards,
            'max_turn': max_turn,
            'card_count': len(target_cards),
            'probability_percent': round(probability, 2),
            'success_count': success_count,
            'total_valid_games': total_valid_games,
            'simulation_count': num_simulations
        }
        
        print(f"\n=== 멀티카드 드로우 확률 계산 완료 ===")
        print(f"성공: {success_count:,}회 / 유효 게임: {total_valid_games:,}회")
        print(f"확률: {probability:.2f}%")
        
        return result

    def print_calculation_result(self, result: Dict[str, Any]):
        """확률 계산 결과를 보기 좋게 출력"""
        print("=" * 60)
        print(f"확률 계산 결과 ({result['calculation_type']})")
        print("=" * 60)
        print(f"설명: {result['description']}")
        
        if result['calculation_type'] == 'preferred_opening':
            print(f"선호하는 Basic: {', '.join(result['preferred_basics'])}")
        elif result['calculation_type'] == 'non_preferred_opening':
            print(f"비선호하는 Basic: {', '.join(result['non_preferred_basics'])}")
        elif result['calculation_type'] == 'multi_card':
            print(f"대상 카드: {', '.join(result['target_cards'])}")
            print(f"최대 턴: {result['max_turn']}턴")
        
        print(f"확률: {result['probability_percent']}%")
        print(f"성공: {result['success_count']:,}회 / 총 {result['total_valid_games']:,}회")
        print(f"시뮬레이션 횟수: {result['simulation_count']:,}회")
        print("=" * 60)
    
    def run_calculation(self, calculation_request: Dict[str, Any], simulation_count: int = 10000) -> Dict[str, Any]:
        """
        계산 요청에 따라 적절한 확률 계산 함수 호출
        
        Args:
            calculation_request: 계산 요청 정보
            simulation_count: 시뮬레이션 횟수
        
        Returns:
            Dict: 확률 계산 결과
        """
        print("=" * 60)
        print("확률 계산 실행 중...")
        print("=" * 60)
        
        calc_type = calculation_request.get('type')
        
        if calc_type == 'preferred_opening':
            preferred_basics = calculation_request.get('preferred_basics', [])
            if not preferred_basics:
                print("❌ 오류: 선호하는 Basic Pokemon 목록이 필요합니다.")
                return None
            result = self.calculate_preferred_opening_probability(preferred_basics, simulation_count)
            
        elif calc_type == 'non_preferred_opening':
            non_preferred_basics = calculation_request.get('non_preferred_basics', [])
            if not non_preferred_basics:
                print("❌ 오류: 비선호하는 Basic Pokemon 목록이 필요합니다.")
                return None
            result = self.calculate_non_preferred_opening_probability(non_preferred_basics, simulation_count)
            
        elif calc_type == 'multi_card':
            target_cards = calculation_request.get('target_cards', [])
            max_turn = calculation_request.get('turn', 2)
            if not target_cards:
                print("❌ 오류: 대상 카드 목록이 필요합니다.")
                return None
            if len(target_cards) > 3:
                print("❌ 오류: 대상 카드는 최대 3개까지만 지원합니다.")
                return None
            result = self.calculate_multi_card_probability(target_cards, max_turn, simulation_count)
            
        else:
            print(f"❌ 오류: '{calc_type}' 타입은 지원되지 않습니다.")
            print("지원되는 타입: 'preferred_opening', 'non_preferred_opening', 'multi_card'")
            return None
        
        if result:
            self.print_calculation_result(result)
        
        return result
