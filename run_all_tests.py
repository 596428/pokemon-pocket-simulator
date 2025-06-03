#!/usr/bin/env python3
"""전체 테스트 스위트 자동 실행"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_simulator import PokemonPocketSimulator, load_deck_from_file, load_test_cases_from_file

def run_all_tests():
    print("=== Pokemon Pocket 시뮬레이터 - 전체 테스트 실행 ===")
    print()
    
    # 시뮬레이터 인스턴스 생성
    simulator = PokemonPocketSimulator()
    
    # 파일에서 덱 정보 읽기
    deck, draw_order = load_deck_from_file()
    if deck is None or draw_order is None:
        print("❌ 덱 파일 읽기 실패")
        return
    
    # 파일에서 테스트 케이스 읽기
    test_cases, file_draw_order, simulation_count = load_test_cases_from_file()
    if test_cases is None:
        print("❌ 테스트 케이스 파일 읽기 실패")
        return
    
    # 파일에서 읽은 드로우 순서가 있으면 그것을 우선 사용
    if file_draw_order:
        draw_order = file_draw_order
    
    print(f"📁 덡 정보: {len(deck)}종류 카드, 총 20장")
    print(f"📁 테스트 케이스: {len(test_cases)}개")
    print(f"🎯 시뮬레이션 횟수: {simulation_count:,}회")
    print(f"🔄 드로우 순서: {' → '.join(draw_order)}")
    print()
    
    # 시뮬레이션 설정
    setup_success = simulator.setup_simulation(deck, draw_order)
    if not setup_success:
        print("❌ 시뮬레이션 설정 실패")
        return
    
    # 덱 요약 정보만 출력
    total_cards = sum(info['count'] for info in deck.values())
    basic_count = sum(info['count'] for info in deck.values() if info['type'] == 'Basic Pokemon')
    draw_card_names = ['Poke Ball', "Professor's Research", 'Galdion']
    draw_card_count = len([c for c in deck.keys() if c in draw_card_names])
    print("📋 덡 요약:")
    print(f"   - 총 카드: {total_cards}장 ({len(deck)}종류)")
    print(f"   - Basic Pokemon: {basic_count}장")
    print(f"   - 드로우 카드: {draw_card_count}종류")
    print()
    
    # 모든 테스트 케이스 실행
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"🧪 테스트 {i}/{len(test_cases)}: {test_case['name']}")
        print("-" * 60)
        
        result = simulator.run_calculation(test_case["request"], simulation_count)
        if result:
            results.append((i, test_case['name'], result))
            prob_percent = result.get('probability_percent', 0.0)
            prob_decimal = prob_percent / 100.0
            print(f"✅ 확률: {prob_decimal:.4f} ({prob_percent:.2f}%)")
        else:
            print(f"❌ 테스트 {i} 실패")
        print()
    
    # 전체 결과 요약
    print("=" * 80)
    print("📊 전체 테스트 결과 요약")
    print("=" * 80)
    
    for test_num, test_name, result in results:
        prob_percent = result.get('probability_percent', 0.0)
        print(f"테스트 {test_num}: {prob_percent:.2f}%")
        print(f"         {test_name}")
        print(f"         성공: {result.get('success_count', 'N/A')}회 / 총 {result.get('total_simulations', simulation_count)}회")
        print()
    
    print(f"✅ 전체 테스트 완료: {len(results)}/{len(test_cases)}개 성공")

if __name__ == "__main__":
    run_all_tests()
