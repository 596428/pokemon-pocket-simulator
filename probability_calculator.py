# probability_calculator.py - 확률 계산 전용 모듈 (v2.1 - 수학적 계산 추가)
from typing import Dict, List, Any
import math

class ProbabilityCalculator:
    """Pokemon Pocket 시뮬레이터용 확률 계산기 v2.1"""
    
    def __init__(self, simulation_engine):
        """
        확률 계산기 초기화
        
        Args:
            simulation_engine: SimulationEngine 인스턴스
        """
        self.sim_engine = simulation_engine
        self.deck_input = simulation_engine.deck_input
        self.total_cards = 20
        self.opening_hand_size = 5
        
        # Basic Pokemon 카드들과 장수 계산
        self.basic_pokemon_cards = {}
        self.total_basic_count = 0
        
        for card_name, card_info in self.deck_input.items():
            if card_info['type'] == 'Basic Pokemon':
                count = card_info['count']
                self.basic_pokemon_cards[card_name] = count
                self.total_basic_count += count
    
    def _is_basic_pokemon(self, card_name: str) -> bool:
        """카드가 Basic Pokemon인지 확인"""
        if card_name in self.deck_input:
            return self.deck_input[card_name]['type'] == 'Basic Pokemon'
        return False
    
    def _combination(self, n: int, k: int) -> int:
        """조합 C(n,k) 계산"""
        if k > n or k < 0:
            return 0
        return math.comb(n, k)
    
    def _hypergeometric_probability(self, N: int, K: int, n: int, k: int) -> float:
        """
        하이퍼지오메트릭 확률 계산
        
        Args:
            N: 전체 모집단 크기 (덱 크기)
            K: 성공 요소의 총 개수 (선호하는 카드 총 장수)
            n: 표본 크기 (뽑는 카드 수)
            k: 원하는 성공 횟수
        
        Returns:
            확률 (0~1)
        """
        numerator = self._combination(K, k) * self._combination(N - K, n - k)
        denominator = self._combination(N, n)
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def _probability_basic_at_least_one(self) -> float:
        """Basic Pokemon이 최소 1장 나올 확률 (재드로우 조건)"""
        # P(Basic ≥ 1) = 1 - P(Basic = 0)
        prob_zero_basic = self._hypergeometric_probability(
            N=self.total_cards,
            K=self.total_basic_count, 
            n=self.opening_hand_size,
            k=0
        )
        return 1.0 - prob_zero_basic
    
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

    def calculate_preferred_opening_mathematical(self, preferred_basics: List[str]) -> Dict[str, Any]:
        """
        선호하는 Basic Pokemon으로 시작할 수 있는 확률 (수학적 계산)
        
        Args:
            preferred_basics: 선호하는 Basic Pokemon 카드명 리스트
        
        Returns:
            계산 결과
        """
        print(f"=== 수학적 계산: 선호하는 Opening 확률 ===")
        print(f"선호하는 Basic Pokemon: {', '.join(preferred_basics)}")
        
        # 선호하는 Basic Pokemon의 총 장수 계산
        preferred_count = 0
        for card_name in preferred_basics:
            if card_name in self.basic_pokemon_cards:
                preferred_count += self.basic_pokemon_cards[card_name]
                print(f"  {card_name}: {self.basic_pokemon_cards[card_name]}장")
            else:
                print(f"  경고: {card_name}은 덱에 없거나 Basic Pokemon이 아닙니다.")
        
        print(f"선호하는 Basic Pokemon 총합: {preferred_count}장")
        print(f"전체 Basic Pokemon: {self.total_basic_count}장")
        
        if preferred_count == 0:
            print("오류: 선호하는 Basic Pokemon이 덱에 없습니다.")
            return None
        
        # 조건부 확률 계산 (Basic이 최소 1장 있다는 조건 하에)
        prob_basic_at_least_one = self._probability_basic_at_least_one()
        
        # P(선호 Basic ≥ 1) = 1 - P(선호 Basic = 0)
        prob_preferred_at_least_one = 1.0 - self._hypergeometric_probability(
            N=self.total_cards,
            K=preferred_count,
            n=self.opening_hand_size,
            k=0
        )
        
        # 조건부 확률: P(선호 Basic ≥ 1 | Basic ≥ 1)
        if prob_basic_at_least_one == 0:
            conditional_probability = 0.0
        else:
            conditional_probability = prob_preferred_at_least_one / prob_basic_at_least_one
        
        probability_percent = conditional_probability * 100
        
        print(f"\n=== 수학적 계산 결과 ===")
        print(f"P(Basic ≥ 1장): {prob_basic_at_least_one:.6f}")
        print(f"P(선호 Basic ≥ 1장): {prob_preferred_at_least_one:.6f}")
        print(f"P(선호 Basic ≥ 1장 | Basic ≥ 1장): {conditional_probability:.6f}")
        print(f"최종 확률: {probability_percent:.2f}%")
        
        return {
            'calculation_type': 'preferred_opening_mathematical',
            'description': f'수학적 계산: 선호하는 Basic Pokemon({", ".join(preferred_basics)})으로 시작할 수 있는 확률',
            'preferred_basics': preferred_basics,
            'preferred_count': preferred_count,
            'total_basic_count': self.total_basic_count,
            'probability_percent': round(probability_percent, 2),
            'raw_probability': conditional_probability,
            'prob_basic_at_least_one': prob_basic_at_least_one,
            'prob_preferred_at_least_one': prob_preferred_at_least_one,
            'calculation_method': 'Hypergeometric Distribution (수학적 정확값)',
            'execution_time': '< 0.001초'
        }

    def calculate_non_preferred_opening_mathematical(self, non_preferred_basics: List[str]) -> Dict[str, Any]:
        """
        비선호하는 Basic Pokemon으로만 시작해야 하는 확률 (수학적 계산)
        
        Args:
            non_preferred_basics: 비선호하는 Basic Pokemon 카드명 리스트
        
        Returns:
            계산 결과
        """
        print(f"=== 수학적 계산: 비선호하는 Opening 확률 ===")
        print(f"비선호하는 Basic Pokemon: {', '.join(non_preferred_basics)}")
        
        # 덱에 실제로 존재하는 비선호 Basic Pokemon만 계산
        actual_non_preferred_count = 0
        actual_non_preferred_cards = []
        for card_name in non_preferred_basics:
            if card_name in self.basic_pokemon_cards:
                count = self.basic_pokemon_cards[card_name]
                actual_non_preferred_count += count
                actual_non_preferred_cards.append(card_name)
                print(f"  {card_name}: {count}장 (덱에 존재)")
            else:
                print(f"  {card_name}: 0장 (덱에 없음 - 계산에서 제외)")
        
        # 선호하는 Basic Pokemon 계산 (전체 - 실제 비선호)
        preferred_count = self.total_basic_count - actual_non_preferred_count
        
        print(f"\n=== 덱 내 Basic Pokemon 분포 ===")
        print(f"실제 비선호하는 Basic Pokemon: {actual_non_preferred_count}장")
        print(f"선호하는 Basic Pokemon: {preferred_count}장")
        print(f"전체 Basic Pokemon: {self.total_basic_count}장")
        
        if actual_non_preferred_count == 0:
            print("오류: 덱에 비선호하는 Basic Pokemon이 없습니다.")
            return {
                'calculation_type': 'non_preferred_opening_mathematical',
                'description': f'수학적 계산: 비선호하는 Basic Pokemon({", ".join(non_preferred_basics)})으로만 시작해야 하는 확률',
                'non_preferred_basics': non_preferred_basics,
                'actual_non_preferred_cards': actual_non_preferred_cards,
                'non_preferred_count': actual_non_preferred_count,
                'preferred_count': preferred_count,
                'total_basic_count': self.total_basic_count,
                'probability_percent': 0.0,
                'raw_probability': 0.0,
                'calculation_method': 'Hypergeometric Distribution (수학적 정확값)',
                'execution_time': '< 0.001초',
                'note': '덱에 비선호 Basic Pokemon이 없어 확률은 0%'
            }
        
        if preferred_count == 0:
            # 모든 Basic이 비선호인 경우
            conditional_probability = 1.0
        else:
            # 상호 배타적 관계 활용: P(비선호만) = 1 - P(선호 ≥ 1)
            prob_basic_at_least_one = self._probability_basic_at_least_one()
            
            # P(선호 Basic ≥ 1) = 1 - P(선호 Basic = 0)
            prob_preferred_at_least_one = 1.0 - self._hypergeometric_probability(
                N=self.total_cards,
                K=preferred_count,
                n=self.opening_hand_size,
                k=0
            )
            
            # P(선호 Basic ≥ 1 | Basic ≥ 1)
            prob_preferred_given_basic = prob_preferred_at_least_one / prob_basic_at_least_one
            
            # 상호 배타적: P(비선호만 | Basic ≥ 1) = 1 - P(선호 ≥ 1 | Basic ≥ 1)
            conditional_probability = 1.0 - prob_preferred_given_basic
        
        probability_percent = conditional_probability * 100
        
        print(f"\n=== 수학적 계산 결과 ===")
        if preferred_count > 0:
            prob_basic_at_least_one = self._probability_basic_at_least_one()
            prob_preferred_at_least_one = 1.0 - self._hypergeometric_probability(
                N=self.total_cards, K=preferred_count, n=self.opening_hand_size, k=0)
            prob_preferred_given_basic = prob_preferred_at_least_one / prob_basic_at_least_one
            
            print(f"P(Basic ≥ 1장): {prob_basic_at_least_one:.6f}")
            print(f"P(선호 Basic ≥ 1장 | Basic ≥ 1장): {prob_preferred_given_basic:.6f}")
            print(f"P(비선호만 | Basic ≥ 1장): {conditional_probability:.6f} (= 1 - {prob_preferred_given_basic:.6f})")
        print(f"최종 확률: {probability_percent:.2f}%")
        
        return {
            'calculation_type': 'non_preferred_opening_mathematical',
            'description': f'수학적 계산: 비선호하는 Basic Pokemon({", ".join(non_preferred_basics)})으로만 시작해야 하는 확률',
            'non_preferred_basics': non_preferred_basics,
            'actual_non_preferred_cards': actual_non_preferred_cards,
            'non_preferred_count': actual_non_preferred_count,
            'preferred_count': preferred_count,
            'total_basic_count': self.total_basic_count,
            'probability_percent': round(probability_percent, 2),
            'raw_probability': conditional_probability,
            'calculation_method': 'Hypergeometric Distribution (수학적 정확값)',
            'execution_time': '< 0.001초',
            'complementary_to_preferred': True
        }

    def print_calculation_result(self, result: Dict[str, Any]):
        """확률 계산 결과를 보기 좋게 출력"""
        print("=" * 60)
        print(f"확률 계산 결과 ({result['calculation_type']})")
        print("=" * 60)
        print(f"설명: {result['description']}")
        
        if 'preferred_opening' in result['calculation_type']:
            if 'preferred_basics' in result:
                print(f"선호하는 Basic: {', '.join(result['preferred_basics'])}")
            if 'calculation_method' in result:
                print(f"계산 방법: {result['calculation_method']}")
                print(f"실행 시간: {result.get('execution_time', '정보 없음')}")
                
        elif 'non_preferred_opening' in result['calculation_type']:
            if 'non_preferred_basics' in result:
                print(f"비선호하는 Basic: {', '.join(result['non_preferred_basics'])}")
            if 'calculation_method' in result:
                print(f"계산 방법: {result['calculation_method']}")
                print(f"실행 시간: {result.get('execution_time', '정보 없음')}")
                
        elif result['calculation_type'] == 'multi_card':
            print(f"대상 카드: {', '.join(result['target_cards'])}")
            print(f"최대 턴: {result['max_turn']}턴")
        
        print(f"확률: {result['probability_percent']}%")
        
        # 시뮬레이션 결과인 경우
        if 'success_count' in result and 'total_valid_games' in result:
            print(f"성공: {result['success_count']:,}회 / 총 {result['total_valid_games']:,}회")
            print(f"시뮬레이션 횟수: {result['simulation_count']:,}회")
        
        print("=" * 60)
    
    def run_calculation(self, calculation_request: Dict[str, Any], simulation_count: int = 10000, use_mathematical: bool = True) -> Dict[str, Any]:
        """
        계산 요청에 따라 적절한 확률 계산 함수 호출
        
        Args:
            calculation_request: 계산 요청 정보
            simulation_count: 시뮬레이션 횟수 (시뮬레이션 사용 시)
            use_mathematical: True면 수학적 계산, False면 시뮬레이션 사용
        
        Returns:
            Dict: 확률 계산 결과
        """
        print("=" * 60)
        if use_mathematical:
            print("수학적 정확 계산 실행 중...")
        else:
            print("시뮬레이션 기반 확률 계산 실행 중...")
        print("=" * 60)
        
        calc_type = calculation_request.get('type')
        
        if calc_type == 'preferred_opening':
            preferred_basics = calculation_request.get('preferred_basics', [])
            if not preferred_basics:
                print("❌ 오류: 선호하는 Basic Pokemon 목록이 필요합니다.")
                return None
            
            if use_mathematical:
                result = self.calculate_preferred_opening_mathematical(preferred_basics)
            else:
                result = self.calculate_preferred_opening_probability(preferred_basics, simulation_count)
            
        elif calc_type == 'non_preferred_opening':
            non_preferred_basics = calculation_request.get('non_preferred_basics', [])
            if not non_preferred_basics:
                print("❌ 오류: 비선호하는 Basic Pokemon 목록이 필요합니다.")
                return None
            
            if use_mathematical:
                result = self.calculate_non_preferred_opening_mathematical(non_preferred_basics)
            else:
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
                
            if use_mathematical:
                print("⚠️ 멀티카드 드로우는 카드 효과가 복잡하여 시뮬레이션을 사용합니다.")
            
            # 멀티카드는 항상 시뮬레이션 사용 (카드 효과 때문)
            result = self.calculate_multi_card_probability(target_cards, max_turn, simulation_count)
            
        else:
            print(f"❌ 오류: '{calc_type}' 타입은 지원되지 않습니다.")
            print("지원되는 타입: 'preferred_opening', 'non_preferred_opening', 'multi_card'")
            return None
        
        if result:
            self.print_calculation_result(result)
        
        return result
