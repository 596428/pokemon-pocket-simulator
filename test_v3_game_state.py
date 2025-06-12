#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pokemon Pocket Simulator v3.0 - GameState 테스트
파일명: test_v3_game_state.py
생성일: 2025-06-12
목적: v3_game_state.py의 GameStateV3 클래스를 테스트

테스트 대상:
- GameStateV3 초기화 및 기본 기능
- 4개 공간 시스템 (Deck, Hand, Field, Discard Pile)
- 포켓몬 배치 시스템
- 진화 불가 마킹 시스템
- 턴 진행 시스템
"""

from v3_game_state import GameStateV3, create_test_deck, create_test_evolution_lines
from v3_core_classes import Card


def test_game_state_initialization():
    """GameStateV3 초기화 테스트"""
    print("=== GameStateV3 초기화 테스트 ===")
    
    # 테스트 덱과 설정 생성
    deck_input = create_test_deck()
    evolution_lines = create_test_evolution_lines()
    preferred_basics = ["피카츄", "코일"]
    
    # GameState 생성
    game_state = GameStateV3(
        deck_input=deck_input,
        preferred_basics=preferred_basics,
        evolution_lines=evolution_lines
    )
    
    print(f"1. 덱 크기: {len(game_state.deck)} (20장이어야 함)")
    assert len(game_state.deck) == 20, "덱 크기가 잘못됨"
    
    print(f"2. Hand 크기: {len(game_state.hand)} (0장이어야 함)")
    assert len(game_state.hand) == 0, "초기 Hand가 비어있지 않음"
    
    print(f"3. Field 상태: Active={game_state.field.has_active_pokemon()}, Bench={game_state.field.get_bench_pokemon_count()}")
    assert game_state.field.has_active_pokemon() == False, "초기 Active가 비어있지 않음"
    assert game_state.field.get_bench_pokemon_count() == 0, "초기 Bench가 비어있지 않음"
    
    print(f"4. Discard Pile 크기: {len(game_state.discard_pile)} (0장이어야 함)")
    assert len(game_state.discard_pile) == 0, "초기 Discard Pile이 비어있지 않음"
    
    print(f"5. 선호 Basic Pokemon: {game_state.preferred_basics}")
    assert game_state.preferred_basics == ["피카츄", "코일"], "선호 Basic Pokemon 설정 오류"
    
    print(f"6. 진화 라인 수: {len(game_state.evolution_lines)} (2개여야 함)")
    assert len(game_state.evolution_lines) == 2, "진화 라인 수가 잘못됨"
    
    print(f"7. 초기 턴: {game_state.turn} (0이어야 함)")
    assert game_state.turn == 0, "초기 턴이 0이 아님"
    
    print("✅ GameStateV3 초기화 테스트 통과!\n")
    return game_state


def test_initial_draw():
    """초기 드로우 테스트"""
    print("=== 초기 드로우 테스트 ===")
    
    # Basic Pokemon이 충분한 덱으로 테스트
    deck_input = create_test_deck()
    game_state = GameStateV3(deck_input=deck_input)
    
    # 초기 드로우 실행
    success = game_state.initial_draw()
    print(f"1. 초기 드로우 성공: {success}")
    assert success == True, "초기 드로우 실패"
    
    print(f"2. Hand 크기: {len(game_state.hand)} (5장이어야 함)")
    assert len(game_state.hand) == 5, "초기 드로우 카드 수가 잘못됨"
    
    # Basic Pokemon이 있는지 확인
    basic_pokemon = game_state.get_basic_pokemon_in_hand()
    print(f"3. Hand의 Basic Pokemon: {[card.name for card in basic_pokemon]}")
    assert len(basic_pokemon) > 0, "Hand에 Basic Pokemon이 없음"
    
    print(f"4. 덱 남은 카드: {len(game_state.deck)} (15장이어야 함)")
    assert len(game_state.deck) == 15, "드로우 후 덱 크기가 잘못됨"
    
    print("✅ 초기 드로우 테스트 통과!\n")
    return game_state


def test_pokemon_placement():
    """포켓몬 배치 테스트"""
    print("=== 포켓몬 배치 테스트 ===")
    
    # 특정 카드가 Hand에 있도록 설정
    deck_input = create_test_deck()
    game_state = GameStateV3(deck_input=deck_input)
    
    # 수동으로 Hand에 카드 추가 (테스트용)
    pikachu = Card("피카츄", "Basic Pokemon")
    magnemite = Card("코일", "Basic Pokemon")
    voltorb = Card("찌리리공", "Basic Pokemon")
    
    game_state.hand = [pikachu, magnemite, voltorb]
    print(f"1. 테스트용 Hand 설정: {[card.name for card in game_state.hand]}")
    
    # Active에 피카츄 배치
    active_success = game_state.place_pokemon_active("피카츄")
    print(f"2. Active에 피카츄 배치: {active_success}")
    assert active_success == True, "Active 배치 실패"
    assert game_state.field.has_active_pokemon() == True, "Active 포켓몬 확인 실패"
    assert len(game_state.newly_placed_pokemon) == 1, "newly_placed_pokemon 기록 실패"
    
    # Hand에서 피카츄가 제거되었는지 확인
    hand_names = [card.name for card in game_state.hand]
    print(f"3. 배치 후 Hand: {hand_names}")
    assert "피카츄" not in hand_names, "배치 후 Hand에서 카드가 제거되지 않음"
    assert len(game_state.hand) == 2, "Hand 크기가 잘못됨"
    
    # 벤치에 코일 배치
    bench_success = game_state.place_pokemon_bench("코일")
    print(f"4. 벤치에 코일 배치: {bench_success}")
    assert bench_success == True, "벤치 배치 실패"
    assert game_state.field.get_bench_pokemon_count() == 1, "벤치 포켓몬 수 확인 실패"
    assert len(game_state.newly_placed_pokemon) == 2, "newly_placed_pokemon 기록 실패"
    
    # 존재하지 않는 카드 배치 시도
    invalid_placement = game_state.place_pokemon_active("존재하지않는카드")
    print(f"5. 존재하지 않는 카드 배치 시도: {invalid_placement} (실패해야 함)")
    assert invalid_placement == False, "존재하지 않는 카드 배치가 성공함"
    
    # Active 중복 배치 시도
    duplicate_active = game_state.place_pokemon_active("찌리리공")
    print(f"6. Active 중복 배치 시도: {duplicate_active} (실패해야 함)")
    assert duplicate_active == False, "Active 중복 배치가 성공함"
    
    print(f"\n7. 최종 Field 상태:")
    print(game_state.field)
    
    print("✅ 포켓몬 배치 테스트 통과!\n")
    return game_state


def test_turn_progression():
    """턴 진행 테스트"""
    print("=== 턴 진행 테스트 ===")
    
    # 이전 테스트에서 포켓몬이 배치된 상태에서 시작
    game_state = test_pokemon_placement()
    
    print(f"1. 턴 진행 전 상태:")
    print(f"   현재 턴: {game_state.turn}")
    print(f"   Hand 크기: {len(game_state.hand)}")
    print(f"   newly_placed_pokemon: {len(game_state.newly_placed_pokemon)}")
    print(f"   Active 진화 가능: {game_state.field.active.can_evolve}")
    
    # 새 턴 시작
    initial_hand_size = len(game_state.hand)
    game_state.start_turn()
    
    print(f"\n2. 턴 진행 후 상태:")
    print(f"   현재 턴: {game_state.turn} (1이어야 함)")
    assert game_state.turn == 1, "턴 증가 실패"
    
    print(f"   Hand 크기: {len(game_state.hand)} ({initial_hand_size + 1}장이어야 함)")
    assert len(game_state.hand) == initial_hand_size + 1, "드로우 실패"
    
    print(f"   newly_placed_pokemon: {len(game_state.newly_placed_pokemon)} (0이어야 함)")
    assert len(game_state.newly_placed_pokemon) == 0, "newly_placed_pokemon 초기화 실패"
    
    print(f"   Active 진화 가능: {game_state.field.active.can_evolve} (True여야 함)")
    assert game_state.field.active.can_evolve == True, "진화 가능 상태 변경 실패"
    
    print("✅ 턴 진행 테스트 통과!\n")
    return game_state


def test_evolution_line_system():
    """진화 라인 시스템 테스트"""
    print("=== 진화 라인 시스템 테스트 ===")
    
    evolution_lines = create_test_evolution_lines()
    game_state = GameStateV3(
        deck_input=create_test_deck(),
        evolution_lines=evolution_lines
    )
    
    # 진화 라인 찾기 테스트
    pikachu_line = game_state.find_evolution_line("피카츄")
    print(f"1. 피카츄 진화 라인: {pikachu_line}")
    assert pikachu_line is not None, "피카츄 진화 라인을 찾을 수 없음"
    assert pikachu_line["basic"] == "피카츄", "피카츄 진화 라인 basic 오류"
    assert pikachu_line["stage1"] == "라이츄", "피카츄 진화 라인 stage1 오류"
    
    raichu_line = game_state.find_evolution_line("라이츄")
    print(f"2. 라이츄로 진화 라인 찾기: {raichu_line}")
    assert raichu_line is not None, "라이츄로 진화 라인을 찾을 수 없음"
    assert raichu_line["basic"] == "피카츄", "라이츄 진화 라인 오류"
    
    unknown_line = game_state.find_evolution_line("존재하지않는포켓몬")
    print(f"3. 존재하지 않는 포켓몬: {unknown_line} (None이어야 함)")
    assert unknown_line is None, "존재하지 않는 포켓몬으로 진화 라인이 찾아짐"
    
    print("✅ 진화 라인 시스템 테스트 통과!\n")


def test_discard_pile_system():
    """Discard Pile 시스템 테스트"""
    print("=== Discard Pile 시스템 테스트 ===")
    
    game_state = GameStateV3(deck_input=create_test_deck())
    
    # 테스트용 카드들 생성
    used_cards = [
        Card("사용된카드1", "Item"),
        Card("사용된카드2", "Supporter"),
        Card("사용된카드3", "Basic Energy")
    ]
    
    print(f"1. Discard Pile 초기 상태: {len(game_state.discard_pile)}장 (0장이어야 함)")
    assert len(game_state.discard_pile) == 0, "Discard Pile 초기 상태 오류"
    
    # 카드들을 Discard Pile로 이동
    game_state.move_to_discard_pile(used_cards)
    
    print(f"2. Discard Pile 카드 추가 후: {len(game_state.discard_pile)}장 (3장이어야 함)")
    assert len(game_state.discard_pile) == 3, "Discard Pile 카드 추가 실패"
    
    discard_names = [card.name for card in game_state.discard_pile]
    print(f"3. Discard Pile 내용: {discard_names}")
    assert "사용된카드1" in discard_names, "카드가 Discard Pile에 없음"
    assert "사용된카드2" in discard_names, "카드가 Discard Pile에 없음"
    assert "사용된카드3" in discard_names, "카드가 Discard Pile에 없음"
    
    print("✅ Discard Pile 시스템 테스트 통과!\n")


def test_integration_scenario():
    """통합 테스트 - 실제 게임 시나리오"""
    print("=== 통합 테스트: 게임 시나리오 ===")
    
    # 게임 시나리오: 게임 시작부터 포켓몬 배치까지
    deck_input = create_test_deck()
    evolution_lines = create_test_evolution_lines()
    preferred_basics = ["피카츄"]
    
    game_state = GameStateV3(
        deck_input=deck_input,
        preferred_basics=preferred_basics,
        evolution_lines=evolution_lines
    )
    
    print("1. 게임 시작 - 초기 드로우")
    success = game_state.initial_draw()
    assert success == True, "게임 시작 실패"
    print(f"   Hand: {[card.name for card in game_state.hand]}")
    
    print("\n2. Active Spot 배치 (선호 포켓몬 우선)")
    preferred_in_hand = game_state.get_preferred_basics_in_hand()
    print(f"   Hand의 선호 Basic Pokemon: {[card.name for card in preferred_in_hand]}")
    
    if preferred_in_hand:
        active_placed = game_state.place_pokemon_active(preferred_in_hand[0].name)
        print(f"   {preferred_in_hand[0].name}를 Active에 배치: {active_placed}")
    else:
        # 선호 포켓몬이 없으면 다른 Basic Pokemon 배치
        basic_pokemon = game_state.get_basic_pokemon_in_hand()
        if basic_pokemon:
            active_placed = game_state.place_pokemon_active(basic_pokemon[0].name)
            print(f"   {basic_pokemon[0].name}를 Active에 배치: {active_placed}")
    
    print("\n3. 벤치 배치")
    remaining_basics = game_state.get_basic_pokemon_in_hand()
    for i, pokemon in enumerate(remaining_basics[:2]):  # 최대 2마리만 배치
        bench_placed = game_state.place_pokemon_bench(pokemon.name)
        print(f"   {pokemon.name}를 벤치에 배치: {bench_placed}")
    
    print(f"\n4. 1턴 종료 후 상태:")
    print(game_state)
    
    print(f"\n5. 2턴 시작")
    game_state.start_turn()
    print(f"   턴: {game_state.turn}")
    print(f"   Hand 크기: {len(game_state.hand)}")
    print(f"   모든 포켓몬 진화 가능: {game_state.field.active.can_evolve}")
    
    # 사용된 카드를 Discard Pile로 (예: 아이템 사용)
    if len(game_state.hand) > 0:
        item_cards = [card for card in game_state.hand if card.card_type == "Item"]
        if item_cards:
            game_state.hand.remove(item_cards[0])
            game_state.move_to_discard_pile([item_cards[0]])
            print(f"   {item_cards[0].name} 사용 → Discard Pile")
    
    print(f"\n6. 최종 상태:")
    print(game_state)
    
    print("✅ 통합 테스트 통과!")


def main():
    """메인 테스트 함수"""
    print("Pokemon Pocket Simulator v3.0 - GameState 테스트")
    print("=" * 60)
    
    try:
        test_game_state_initialization()
        test_initial_draw()
        test_pokemon_placement() 
        test_turn_progression()
        test_evolution_line_system()
        test_discard_pile_system()
        test_integration_scenario()
        
        print("\n🎉 모든 테스트가 성공적으로 완료되었습니다!")
        print("v3.0 GameState 확장이 정상적으로 작동합니다.")
        print("\n다음 단계: auto_evolve_all() 함수 구현 (v3_evolution_system.py)")
        
    except AssertionError as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
