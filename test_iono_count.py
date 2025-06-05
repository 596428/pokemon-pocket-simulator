import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_simulator import PokemonPocketSimulator

def test_iono_count_comparison():
    print("=== Iono 장수별 효과 비교 테스트 ===")
    print("목표: Charizard EX + Dragonite + Master Ball 각각 1장씩 확보 (3턴까지)")
    print("시뮬레이션 횟수: 5000회")
    print()
    
    # 공통 덱 구성 (18장) - Target Cards + 드로우 카드 + 기타
    base_deck_18 = {
        # Target Cards (6장)
        "Charizard EX": {"type": "Basic Pokemon", "count": 2},
        "Dragonite": {"type": "Stage2 Pokemon", "count": 2},
        "Master Ball": {"type": "Item", "count": 2},
        
        # 드로우 카드들 (4장)
        "Poke Ball": {"type": "Item", "count": 2},
        "Professor's Research": {"type": "Supporter", "count": 2},
        
        # 기타 카드들 (8장)
        "Pikachu": {"type": "Basic Pokemon", "count": 2},
        "Squirtle": {"type": "Basic Pokemon", "count": 2},
        "Energy Search": {"type": "Item", "count": 2},
        "Switch": {"type": "Item", "count": 2}
    }
    
    # 계산 요청
    request = {
        "type": "multi_card",
        "target_cards": ["Charizard EX", "Dragonite", "Master Ball"],
        "turn": 3
    }
    
    simulation_count = 5000
    results = {}
    
    # TEST 1: Iono 0장 (Red Card 2장으로 대체)
    print("🔍 TEST 1: Iono 0장 (Red Card 2장)")
    deck_0_iono = base_deck_18.copy()
    deck_0_iono["Red Card"] = {"type": "Item", "count": 2}
    draw_order_0 = ["Poke Ball", "Professor's Research"]  # Iono 없음
    
    simulator_0 = PokemonPocketSimulator()
    simulator_0.setup_simulation(deck_0_iono, draw_order_0)
    result_0 = simulator_0.run_calculation(request, simulation_count)
    results[0] = result_0["probability_percent"]
    
    print(f"Iono 0장 결과: {results[0]:.2f}%")
    
    # TEST 2: Iono 1장 (Red Card 1장)
    print()
    print("🔍 TEST 2: Iono 1장 (Red Card 1장)")
    deck_1_iono = base_deck_18.copy()
    deck_1_iono["Iono"] = {"type": "Supporter", "count": 1}
    deck_1_iono["Red Card"] = {"type": "Item", "count": 1}
    draw_order_1 = ["Poke Ball", "Professor's Research", "Iono"]
    
    simulator_1 = PokemonPocketSimulator()
    simulator_1.setup_simulation(deck_1_iono, draw_order_1)
    result_1 = simulator_1.run_calculation(request, simulation_count)
    results[1] = result_1["probability_percent"]
    
    print(f"Iono 1장 결과: {results[1]:.2f}%")
    
    # TEST 3: Iono 2장 (Red Card 0장)
    print()
    print("🔍 TEST 3: Iono 2장 (Red Card 0장)")
    deck_2_iono = base_deck_18.copy()
    deck_2_iono["Iono"] = {"type": "Supporter", "count": 2}
    draw_order_2 = ["Poke Ball", "Professor's Research", "Iono"]
    
    simulator_2 = PokemonPocketSimulator()
    simulator_2.setup_simulation(deck_2_iono, draw_order_2)
    result_2 = simulator_2.run_calculation(request, simulation_count)
    results[2] = result_2["probability_percent"]
    
    print(f"Iono 2장 결과: {results[2]:.2f}%")
    
    # 결과 분석
    print()
    print("="*60)
    print("📊 Iono 장수별 성능 비교")
    print("="*60)
    
    print(f"Iono 0장:  {results[0]:6.2f}%")
    print(f"Iono 1장:  {results[1]:6.2f}% (차이: {results[1] - results[0]:+.2f}%)")
    print(f"Iono 2장:  {results[2]:6.2f}% (차이: {results[2] - results[0]:+.2f}%)")
    
    print()
    print("장수별 개선율:")
    if results[0] > 0:
        improvement_1 = ((results[1] - results[0]) / results[0]) * 100
        improvement_2 = ((results[2] - results[0]) / results[0]) * 100
        
        print(f"1장 vs 0장: {improvement_1:+.1f}%")
        print(f"2장 vs 0장: {improvement_2:+.1f}%")
        print(f"2장 vs 1장: {((results[2] - results[1]) / results[1]) * 100:+.1f}%")
    
    print()
    print("="*60)
    print("📈 분석 결론")
    print("="*60)
    
    # 최고 성능 찾기
    best_count = max(results, key=results.get)
    worst_count = min(results, key=results.get)
    
    print(f"최고 성능: Iono {best_count}장 ({results[best_count]:.2f}%)")
    print(f"최저 성능: Iono {worst_count}장 ({results[worst_count]:.2f}%)")
    
    # 트렌드 분석
    if results[2] > results[1] > results[0]:
        print("📈 결론: Iono가 많을수록 성능이 향상됩니다!")
        print("   → 손패 리셋 옵션이 많을수록 유리")
    elif results[1] > results[0] and results[1] > results[2]:
        print("⚖️  결론: Iono 1장이 최적입니다!")
        print("   → 너무 많으면 오히려 역효과")
    elif results[0] > results[1] > results[2]:
        print("📉 결론: Iono가 없는 게 더 좋습니다!")
        print("   → 이 덱 구성에서는 Iono가 비효율적")
    else:
        print("🔄 결론: 복잡한 패턴을 보입니다.")
        print("   → 상황에 따라 다른 효과")
    
    print()
    print("상세 데이터:")
    print(f"Iono 0장 - 성공: {result_0['success_count']}/{result_0['total_valid_games']}회")
    print(f"Iono 1장 - 성공: {result_1['success_count']}/{result_1['total_valid_games']}회") 
    print(f"Iono 2장 - 성공: {result_2['success_count']}/{result_2['total_valid_games']}회")

if __name__ == "__main__":
    test_iono_count_comparison()
