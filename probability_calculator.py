# probability_calculator.py - 확률 계산 전용 모듈
from typing import Dict, List, Any

class ProbabilityCalculator:
    """Pokemon Pocket 시뮬레이터용 확률 계산기"""
    
    def __init__(self, simulation_engine):
        """
        확률 계산기 초기화
        
        Args:
            simulation_engine: SimulationEngine 인스턴스
        """
        self.sim_engine = simulation_engine
    
    def calculate_type1_probability(self, target_basic_pokemon: str, num_simulations: int = 10000) -> Dict[str, Any]:
        """
        타입 1: 특정 Basic Pokemon이 시작 5장에 포함될 확률
        
        Args:
            target_basic_pokemon: 대상 Basic Pokemon 카드명
            num_simulations: 시뮬레이션 횟수
        
        Returns:
            Dict: 확률 계산 결과
        """
        print(f"=== 타입 1 확률 계산 시작 ===")
        print(f"대상 카드: {target_basic_pokemon}")
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
                
                # 0턴 손패에서 대상 카드가 있는지 확인
                turn_0_hand = game_result['turn_results'][0]['hand_before_effects']
                
                if target_basic_pokemon in turn_0_hand:
                    success_count += 1
        
        # 결과 계산
        if total_valid_games == 0:
            probability = 0.0
        else:
            probability = (success_count / total_valid_games) * 100
        
        result = {
            'calculation_type': 1,
            'description': f'특정 Basic Pokemon("{target_basic_pokemon}")이 시작 5장에 포함될 확률',
            'target_card': target_basic_pokemon,
            'probability_percent': round(probability, 2),
            'success_count': success_count,
            'total_valid_games': total_valid_games,
            'simulation_count': num_simulations
        }
        
        print(f"\n=== 타입 1 확률 계산 완료 ===")
        print(f"성공: {success_count:,}회 / 유효 게임: {total_valid_games:,}회")
        print(f"확률: {probability:.2f}%")
        
        return result
    
    def calculate_type2_probability(self, target_basic_pokemon: str, num_simulations: int = 10000) -> Dict[str, Any]:
        """
        타입 2: 시작 5장에서 Basic Pokemon이 정확히 1장이고, 그것이 특정 카드일 확률
        
        Args:
            target_basic_pokemon: 대상 Basic Pokemon 카드명
            num_simulations: 시뮬레이션 횟수
        
        Returns:
            Dict: 확률 계산 결과
        """
        print(f"=== 타입 2 확률 계산 시작 ===")
        print(f"대상 카드: {target_basic_pokemon}")
        print(f"시뮬레이션 횟수: {num_simulations:,}회")
        print("조건: Basic Pokemon이 정확히 1장이고, 그것이 특정 카드일 확률")
        
        success_count = 0
        total_valid_games = 0
        checkpoint = max(1, num_simulations // 10)
        
        for i in range(num_simulations):
            if (i + 1) % checkpoint == 0 or i == 0:
                progress = ((i + 1) / num_simulations) * 100
                print(f"진행률: {progress:.1f}% ({i+1:,}/{num_simulations:,})")
            
            game_result = self.sim_engine.simulate_single_game(max_turn=0, verbose=False)
            
            if game_result['success']:
                total_valid_games += 1
                
                turn_0_hand = game_result['turn_results'][0]['hand_before_effects']
                
                # Basic Pokemon들만 필터링
                basic_pokemons_in_hand = [card for card in turn_0_hand 
                                        if self._is_basic_pokemon(card)]
                
                # Basic Pokemon이 정확히 1장이고, 그것이 대상 카드인지 확인
                if (len(basic_pokemons_in_hand) == 1 and 
                    basic_pokemons_in_hand[0] == target_basic_pokemon):
                    success_count += 1
        
        if total_valid_games == 0:
            probability = 0.0
        else:
            probability = (success_count / total_valid_games) * 100
        
        result = {
            'calculation_type': 2,
            'description': f'시작 5장에서 Basic Pokemon이 정확히 1장이고, 그것이 "{target_basic_pokemon}"일 확률',
            'target_card': target_basic_pokemon,
            'probability_percent': round(probability, 2),
            'success_count': success_count,
            'total_valid_games': total_valid_games,
            'simulation_count': num_simulations
        }
        
        print(f"\n=== 타입 2 확률 계산 완료 ===")
        print(f"성공: {success_count:,}회 / 유효 게임: {total_valid_games:,}회")
        print(f"확률: {probability:.2f}%")
        
        return result
    
    def calculate_type3_probability(self, target_basic_pokemon: str, max_turn: int, num_simulations: int = 10000) -> Dict[str, Any]:
        """
        타입 3: 1턴 또는 2턴까지 특정 Basic Pokemon 드로우 확률
        
        Args:
            target_basic_pokemon: 대상 Basic Pokemon 카드명
            max_turn: 최대 턴 수 (1 또는 2)
            num_simulations: 시뮬레이션 횟수
        
        Returns:
            Dict: 확률 계산 결과
        """
        print(f"=== 타입 3 확률 계산 시작 ===")
        print(f"대상 카드: {target_basic_pokemon}")
        print(f"최대 턴: {max_turn}턴")
        print(f"시뮬레이션 횟수: {num_simulations:,}회")
        
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
                
                # 0턴부터 max_turn까지 모든 턴에서 대상 카드가 있는지 확인
                found_target = False
                for turn in range(max_turn + 1):
                    if turn in game_result['turn_results']:
                        hand_after_effects = game_result['turn_results'][turn]['hand_after_effects']
                        if target_basic_pokemon in hand_after_effects:
                            found_target = True
                            break
                
                if found_target:
                    success_count += 1
        
        if total_valid_games == 0:
            probability = 0.0
        else:
            probability = (success_count / total_valid_games) * 100
        
        result = {
            'calculation_type': 3,
            'description': f'{max_turn}턴까지 "{target_basic_pokemon}" 드로우 확률',
            'target_card': target_basic_pokemon,
            'max_turn': max_turn,
            'probability_percent': round(probability, 2),
            'success_count': success_count,
            'total_valid_games': total_valid_games,
            'simulation_count': num_simulations
        }
        
        print(f"\n=== 타입 3 확률 계산 완료 ===")
        print(f"성공: {success_count:,}회 / 유효 게임: {total_valid_games:,}회")
        print(f"확률: {probability:.2f}%")
        
        return result
    
    def calculate_type4_probability(self, target_basic_pokemon: str, target_stage1_pokemon: str, 
                                  num_simulations: int = 10000) -> Dict[str, Any]:
        """
        타입 4: 2턴까지 특정 Basic Pokemon + Stage1 Pokemon 각각 1장 이상 드로우 확률
        
        Args:
            target_basic_pokemon: 대상 Basic Pokemon 카드명
            target_stage1_pokemon: 대상 Stage1 Pokemon 카드명
            num_simulations: 시뮬레이션 횟수
        
        Returns:
            Dict: 확률 계산 결과
        """
        print(f"=== 타입 4 확률 계산 시작 ===")
        print(f"대상 Basic Pokemon: {target_basic_pokemon}")
        print(f"대상 Stage1 Pokemon: {target_stage1_pokemon}")
        print(f"시뮬레이션 횟수: {num_simulations:,}회")
        print("조건: 2턴까지 각각 1장 이상씩 드로우")
        
        success_count = 0
        total_valid_games = 0
        checkpoint = max(1, num_simulations // 10)
        
        for i in range(num_simulations):
            if (i + 1) % checkpoint == 0 or i == 0:
                progress = ((i + 1) / num_simulations) * 100
                print(f"진행률: {progress:.1f}% ({i+1:,}/{num_simulations:,})")
            
            game_result = self.sim_engine.simulate_single_game(max_turn=2, verbose=False)
            
            if game_result['success']:
                total_valid_games += 1
                
                # 2턴까지의 최종 손패에서 두 카드가 모두 있는지 확인
                final_hand = game_result['final_hand']
                
                has_basic = target_basic_pokemon in final_hand
                has_stage1 = target_stage1_pokemon in final_hand
                
                if has_basic and has_stage1:
                    success_count += 1
        
        if total_valid_games == 0:
            probability = 0.0
        else:
            probability = (success_count / total_valid_games) * 100
        
        result = {
            'calculation_type': 4,
            'description': f'2턴까지 "{target_basic_pokemon}" + "{target_stage1_pokemon}" 각각 1장 이상 드로우 확률',
            'target_basic': target_basic_pokemon,
            'target_stage1': target_stage1_pokemon,
            'probability_percent': round(probability, 2),
            'success_count': success_count,
            'total_valid_games': total_valid_games,
            'simulation_count': num_simulations
        }
        
        print(f"\n=== 타입 4 확률 계산 완료 ===")
        print(f"성공: {success_count:,}회 / 유효 게임: {total_valid_games:,}회")
        print(f"확률: {probability:.2f}%")
        
        return result
    
    def calculate_type5_probability(self, target_basic_pokemon: str, target_item: str, 
                                  target_stage2_pokemon: str, num_simulations: int = 10000) -> Dict[str, Any]:
        """
        타입 5: 2턴까지 특정 Basic Pokemon + Item + Stage2 Pokemon 각각 1장 이상 드로우 확률
        
        Args:
            target_basic_pokemon: 대상 Basic Pokemon 카드명
            target_item: 대상 Item 카드명
            target_stage2_pokemon: 대상 Stage2 Pokemon 카드명
            num_simulations: 시뮬레이션 횟수
        
        Returns:
            Dict: 확률 계산 결과
        """
        print(f"=== 타입 5 확률 계산 시작 ===")
        print(f"대상 Basic Pokemon: {target_basic_pokemon}")
        print(f"대상 Item: {target_item}")
        print(f"대상 Stage2 Pokemon: {target_stage2_pokemon}")
        print(f"시뮬레이션 횟수: {num_simulations:,}회")
        print("조건: 2턴까지 각각 1장 이상씩 드로우")
        
        success_count = 0
        total_valid_games = 0
        checkpoint = max(1, num_simulations // 10)
        
        for i in range(num_simulations):
            if (i + 1) % checkpoint == 0 or i == 0:
                progress = ((i + 1) / num_simulations) * 100
                print(f"진행률: {progress:.1f}% ({i+1:,}/{num_simulations:,})")
            
            game_result = self.sim_engine.simulate_single_game(max_turn=2, verbose=False)
            
            if game_result['success']:
                total_valid_games += 1
                
                # 2턴까지의 최종 손패에서 세 카드가 모두 있는지 확인
                final_hand = game_result['final_hand']
                
                has_basic = target_basic_pokemon in final_hand
                has_item = target_item in final_hand
                has_stage2 = target_stage2_pokemon in final_hand
                
                if has_basic and has_item and has_stage2:
                    success_count += 1
        
        if total_valid_games == 0:
            probability = 0.0
        else:
            probability = (success_count / total_valid_games) * 100
        
        result = {
            'calculation_type': 5,
            'description': f'2턴까지 "{target_basic_pokemon}" + "{target_item}" + "{target_stage2_pokemon}" 각각 1장 이상 드로우 확률',
            'target_basic': target_basic_pokemon,
            'target_item': target_item,
            'target_stage2': target_stage2_pokemon,
            'probability_percent': round(probability, 2),
            'success_count': success_count,
            'total_valid_games': total_valid_games,
            'simulation_count': num_simulations
        }
        
        print(f"\n=== 타입 5 확률 계산 완료 ===")
        print(f"성공: {success_count:,}회 / 유효 게임: {total_valid_games:,}회")
        print(f"확률: {probability:.2f}%")
        
        return result
    
    def _is_basic_pokemon(self, card_name: str) -> bool:
        """카드 이름으로 Basic Pokemon인지 확인하는 헬퍼 함수"""
        # 현재 덱에서 해당 카드의 타입을 확인
        deck_input = self.sim_engine.deck_input
        if card_name in deck_input:
            return deck_input[card_name]["type"] == "Basic Pokemon"
        return False
    
    def print_result(self, result: Dict[str, Any]):
        """
        확률 계산 결과를 깔끔하게 출력
        
        Args:
            result: calculate_typeX_probability 함수의 반환값
        """
        print(f"\n{'='*60}")
        print(f"확률 계산 결과 (타입 {result['calculation_type']})")
        print(f"{'='*60}")
        print(f"설명: {result['description']}")
        
        # 타입별로 다른 정보 출력
        if result['calculation_type'] in [1, 2, 3]:
            print(f"대상 카드: {result['target_card']}")
        elif result['calculation_type'] == 4:
            print(f"대상 Basic Pokemon: {result['target_basic']}")
            print(f"대상 Stage1 Pokemon: {result['target_stage1']}")
        elif result['calculation_type'] == 5:
            print(f"대상 Basic Pokemon: {result['target_basic']}")
            print(f"대상 Item: {result['target_item']}")
            print(f"대상 Stage2 Pokemon: {result['target_stage2']}")
        
        if result['calculation_type'] == 3:
            print(f"최대 턴: {result['max_turn']}턴")
            
        print(f"확률: {result['probability_percent']:.2f}%")
        print(f"성공: {result['success_count']:,}회 / 총 {result['total_valid_games']:,}회")
        print(f"시뮬레이션 횟수: {result['simulation_count']:,}회")
        print(f"{'='*60}")
