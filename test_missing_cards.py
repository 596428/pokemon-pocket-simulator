#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
덱에 없는 카드 처리 테스트 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_simulator import PokemonPocketSimulator, load_deck_from_file

def test_missing_cards():
    """덱에 없는 카드들이 각 계산 타입에서 어떻게 처리되는지 테스트"""
    
    print("=" * 80)
    print("덱에 없는 카드 처리 테스트")
    print("=" * 80)
    
    # 시뮬레이터 설정
    simulator = PokemonPocketSimulator()
    deck, draw_order = load_deck_from_file()
    
    if not simulator.setup_simulation(deck, draw_order):
        print("❌ 시뮬레이터 설정 실패")
        return
    
    print("📋 현재 덱의 Basic Pokemon:")
    for card_name, card_info in deck.items():
        if card_info['type'] == 'Basic Pokemon':
            print(f"  - {card_name}: {card_info['count']}장")
    
    print("\n" + "=" * 80)
    print("테스트 1: 선호 Basic에 덱에 없는 카드 포함")
    print("=" * 80)
    
    # 테스트 1: 선호 Basic에 덱에 없는 카드 (Pikachu) 포함
    test1_request = {
        "type": "preferred_opening",
        "preferred_basics": ["Type:Null", "Pikachu"]  # Pikachu는 덱에 없음
    }
    
    result1 = simulator.run_calculation(test1_request, simulation_count=1000)
    
    print("\n" + "=" * 80)
    print("테스트 2: 비선호 Basic에 덱에 없는 카드만")
    print("=" * 80)
    
    # 테스트 2: 비선호 Basic에 덱에 없는 카드들만
    test2_request = {
        "type": "non_preferred_opening", 
        "non_preferred_basics": ["Squirtle", "Pichu"]  # 둘 다 덱에 없음
    }
    
    result2 = simulator.run_calculation(test2_request, simulation_count=1000)
    
    print("\n" + "=" * 80)
    print("테스트 3: 멀티카드에 덱에 없는 카드 포함")
    print("=" * 80)
    
    # 테스트 3: 멀티카드에 덱에 없는 카드 포함
    test3_request = {
        "type": "multi_card",
        "target_cards": ["Type:Null", "Charizard"],  # Charizard는 덱에 없음
        "turn": 2
    }
    
    result3 = simulator.run_calculation(test3_request, simulation_count=1000)
    
    print("\n" + "=" * 80)
    print("테스트 4: 모든 카드가 덱에 없는 경우")
    print("=" * 80)
    
    # 테스트 4: 모든 카드가 덱에 없는 경우
    test4_request = {
        "type": "preferred_opening",
        "preferred_basics": ["Pikachu", "Charizard", "Mewtwo"]  # 모두 덱에 없음
    }
    
    result4 = simulator.run_calculation(test4_request, simulation_count=1000)
    
    print("\n" + "=" * 80)
    print("테스트 완료 - 요약")
    print("=" * 80)
    
    tests = [
        ("테스트 1 (선호, 일부 없음)", result1),
        ("테스트 2 (비선호, 모두 없음)", result2), 
        ("테스트 3 (멀티카드, 일부 없음)", result3),
        ("테스트 4 (선호, 모두 없음)", result4)
    ]
    
    for test_name, result in tests:
        if result:
            print(f"✅ {test_name}: {result['probability_percent']}%")
        else:
            print(f"❌ {test_name}: 계산 실패 또는 오류")

if __name__ == "__main__":
    test_missing_cards()
