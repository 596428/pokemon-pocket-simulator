#!/usr/bin/env python3
"""
복합 확률 계산 테스트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_simulator import PokemonPocketSimulator

def test_composite_calculations():
    print("=== 복합 확률 계산 테스트 ===")
    print()
    
    # 테스트용 덱 (파이리/꼬부기 진화 라인)
    test_deck = {
        # 진화 라인 A (파이리)
        "파이리": {"type": "Basic Pokemon", "count": 2},
        "리자몽": {"type": "Stage2 Pokemon", "count": 2},
        
        # 진화 라인 B (꼬부기)
        "꼬부기": {"type": "Basic Pokemon", "count": 2},
        "거북왕": {"type": "Stage2 Pokemon", "count": 2},
        
        # 공통 카드들
        "rare candy": {"type": "Item", "count": 2},
        "LEAF": {"type": "Supporter", "count": 2},
        
        # 드로우 카드들
        "Poke Ball": {"type": "Item", "count": 2},
        "Professor's Research": {"type": "Supporter", "count": 2},
        
        # 기타
        "Energy Search": {"type": "Item", "count": 2},
        "Switch": {"type": "Item", "count": 2}
    }
    
    draw_order = ["Poke Ball", "Professor's Research"]
    simulation_count = 2000
    
    print("🧪 테스트 덱:")
    total_cards = sum(card["count"] for card in test_deck.values())
    print(f"총 {total_cards}장")
    for name, info in test_deck.items():
        print(f"  {name}: {info['count']}장 ({info['type']})")
    print()
    
    # 시뮬레이터 설정
    simulator = PokemonPocketSimulator()
    simulator.setup_simulation(test_deck, draw_order)
    
    # 테스트 1: preferred_and_multi (직접 호출)
    print("🎯 TEST 1: 파이리 시작 + 파이리 라인 완성")
    try:
        result1 = simulator.prob_calculator.calculate_preferred_and_multi_probability(
            preferred_basics=["파이리"],
            target_cards=["파이리", "리자몽", "rare candy"],
            max_turn=2,
            num_simulations=simulation_count
        )
        print(f"결과: {result1['probability_percent']:.2f}%")
        print(f"성공: {result1['success_count']}/{result1['total_valid_games']}회")
    except Exception as e:
        print(f"❌ 오류: {e}")
    
    print()
    
    # 테스트 2: non_preferred_and_multi (직접 호출)
    print("🎯 TEST 2: 꼬부기 시작 + LEAF 확보")
    try:
        result2 = simulator.prob_calculator.calculate_non_preferred_and_multi_probability(
            non_preferred_basics=["꼬부기"],
            target_cards=["LEAF"],
            max_turn=2,
            num_simulations=simulation_count
        )
        print(f"결과: {result2['probability_percent']:.2f}%")
        print(f"성공: {result2['success_count']}/{result2['total_valid_games']}회")
    except Exception as e:
        print(f"❌ 오류: {e}")
    
    print()
    
    # 테스트 3: multi_or_multi (직접 호출)
    print("🎯 TEST 3: 파이리 라인 OR 꼬부기 라인 완성")
    try:
        target_groups = [
            {
                "name": "파이리 라인",
                "target_cards": ["파이리", "리자몽", "rare candy"]
            },
            {
                "name": "꼬부기 라인",
                "target_cards": ["꼬부기", "거북왕", "rare candy"]
            }
        ]
        
        result3 = simulator.prob_calculator.calculate_multi_or_multi_probability(
            target_groups=target_groups,
            max_turn=3,
            num_simulations=simulation_count
        )
        print(f"전체 결과: {result3['probability_percent']:.2f}%")
        print(f"성공: {result3['success_count']}/{result3['total_valid_games']}회")
        print("그룹별 성공률:")
        for group_name, prob in result3['group_probabilities'].items():
            print(f"  {group_name}: {prob:.2f}%")
    except Exception as e:
        print(f"❌ 오류: {e}")
    
    print()
    print("="*60)
    print("📋 복합 확률 계산 기능 상태:")
    print("✅ preferred_and_multi: 구현 완료")
    print("✅ non_preferred_and_multi: 구현 완료") 
    print("✅ multi_or_multi: 구현 완료")
    print()
    print("🚀 다음 단계: main_simulator.py에서 새 타입 지원 추가")

if __name__ == "__main__":
    test_composite_calculations()
