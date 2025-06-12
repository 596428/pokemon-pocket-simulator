#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pokemon Pocket Simulator v3.0 - 핵심 클래스 테스트
파일명: test_v3_core.py
생성일: 2025-06-12
목적: v3_core_classes.py의 클래스들을 테스트

테스트 대상:
- PokemonSlot 클래스 기본 기능
- Field 클래스 기본 기능
- 진화 시스템 기초 동작
- Tool 부착 시스템
"""

from v3_core_classes import Card, PokemonSlot, Field, create_pokemon_card, create_tool_card


def test_pokemon_slot():
    """PokemonSlot 클래스 테스트"""
    print("=== PokemonSlot 테스트 ===")
    
    # 카드 생성
    pikachu = create_pokemon_card("피카츄", "Basic Pokemon")
    raichu = create_pokemon_card("라이츄", "Stage1 Pokemon")
    thunder_tool = create_tool_card("번개 도구")
    
    # 슬롯 생성 및 기본 상태 테스트
    slot = PokemonSlot()
    print(f"1. 빈 슬롯 생성: {slot}")
    assert slot.is_empty() == True, "빈 슬롯 체크 실패"
    assert slot.get_evolution_stage() == 0, "진화 단계 체크 실패"
    
    # Basic 포켓몬 배치
    success = slot.add_evolution(pikachu)
    print(f"2. 피카츄 배치 성공: {success}")
    assert success == True, "피카츄 배치 실패"
    assert slot.get_top_pokemon().name == "피카츄", "최상위 포켓몬 체크 실패"
    assert slot.get_bottom_pokemon().name == "피카츄", "최하위 포켓몬 체크 실패"
    assert slot.get_evolution_stage() == 1, "진화 단계 체크 실패"
    print(f"   슬롯 상태: {slot}")
    
    # Tool 부착
    tool_success = slot.attach_tool(thunder_tool)
    print(f"3. 도구 부착 성공: {tool_success}")
    assert tool_success == True, "도구 부착 실패"
    print(f"   슬롯 상태: {slot}")
    
    # 중복 Tool 부착 시도 (실패해야 함)
    duplicate_tool = create_tool_card("다른 도구")
    duplicate_success = slot.attach_tool(duplicate_tool)
    print(f"4. 중복 도구 부착 시도: {duplicate_success} (실패해야 정상)")
    assert duplicate_success == False, "중복 도구 부착이 성공함 (오류)"
    
    # 진화
    evolve_success = slot.add_evolution(raichu)
    print(f"5. 라이츄 진화 성공: {evolve_success}")
    assert evolve_success == True, "진화 실패"
    assert slot.get_top_pokemon().name == "라이츄", "진화 후 최상위 포켓몬 체크 실패"
    assert slot.get_bottom_pokemon().name == "피카츄", "진화 후 최하위 포켓몬 체크 실패"
    assert slot.get_evolution_stage() == 2, "진화 후 단계 체크 실패"
    print(f"   최종 슬롯 상태: {slot}")
    
    # 진화 불가 상태 테스트
    slot.can_evolve = False
    fake_evolution = create_pokemon_card("가짜진화", "Stage2 Pokemon")
    blocked_evolution = slot.add_evolution(fake_evolution)
    print(f"6. 진화 불가 상태에서 진화 시도: {blocked_evolution} (실패해야 정상)")
    assert blocked_evolution == False, "진화 불가 상태에서 진화가 성공함 (오류)"
    
    print("✅ PokemonSlot 모든 테스트 통과!\n")


def test_field():
    """Field 클래스 테스트"""
    print("=== Field 테스트 ===")
    
    # 카드들 생성
    pikachu = create_pokemon_card("피카츄")
    magnemite = create_pokemon_card("코일")
    voltorb = create_pokemon_card("찌리리공")
    electrode = create_pokemon_card("붐볼")
    
    # Field 생성
    field = Field()
    print("1. 초기 Field 상태:")
    print(field)
    assert field.has_active_pokemon() == False, "초기 Active 상태 체크 실패"
    assert field.get_bench_pokemon_count() == 0, "초기 벤치 포켓몬 수 체크 실패"
    assert len(field.get_available_bench_slots()) == 3, "초기 가용 벤치 슬롯 수 체크 실패"
    
    # Active에 포켓몬 배치
    active_success = field.place_pokemon_active(pikachu)
    print(f"\n2. Active에 피카츄 배치: {active_success}")
    assert active_success == True, "Active 배치 실패"
    assert field.has_active_pokemon() == True, "Active 포켓몬 존재 체크 실패"
    
    # 중복 Active 배치 시도 (실패해야 함)
    duplicate_active = field.place_pokemon_active(magnemite)
    print(f"3. 중복 Active 배치 시도: {duplicate_active} (실패해야 정상)")
    assert duplicate_active == False, "중복 Active 배치가 성공함 (오류)"
    
    # 벤치에 포켓몬들 배치
    bench1_success = field.place_pokemon_bench(magnemite)
    bench2_success = field.place_pokemon_bench(voltorb)
    print(f"4. 벤치에 코일 배치: {bench1_success}")
    print(f"5. 벤치에 찌리리공 배치: {bench2_success}")
    assert bench1_success == True, "벤치 배치 실패"
    assert bench2_success == True, "벤치 배치 실패"
    assert field.get_bench_pokemon_count() == 2, "벤치 포켓몬 수 체크 실패"
    
    print("\n6. 배치 후 Field 상태:")
    print(field)
    
    # 사용 가능한 벤치 슬롯 확인
    available = field.get_available_bench_slots()
    print(f"\n7. 사용 가능한 벤치 슬롯: {available}")
    assert available == [2], "가용 벤치 슬롯 체크 실패"
    
    # 세 번째 포켓몬 배치
    bench3_success = field.place_pokemon_bench(electrode)
    print(f"8. 벤치에 붐볼 배치: {bench3_success}")
    assert bench3_success == True, "세 번째 벤치 배치 실패"
    
    # 벤치가 꽉 찬 상태에서 추가 배치 시도 (실패해야 함)
    extra_pokemon = create_pokemon_card("추가포켓몬")
    full_bench_try = field.place_pokemon_bench(extra_pokemon)
    print(f"9. 벤치 가득한 상태에서 추가 배치: {full_bench_try} (실패해야 정상)")
    assert full_bench_try == False, "벤치 가득한 상태에서 배치가 성공함 (오류)"
    
    # 모든 포켓몬 슬롯 가져오기
    all_slots = field.get_all_pokemon_slots()
    print(f"10. 전체 포켓몬 슬롯 수: {len(all_slots)} (4개여야 함)")
    assert len(all_slots) == 4, "전체 포켓몬 슬롯 수 체크 실패"
    
    # 벤치 크기 변경 테스트
    print(f"\n11. 벤치 크기를 2로 줄이기:")
    discarded = field.resize_bench(2)
    print(f"    버려진 카드들: {[card.name for card in discarded]}")
    print(f"    새로운 벤치 크기: {len(field.bench)}")
    assert len(field.bench) == 2, "벤치 크기 변경 실패"
    assert len(discarded) == 1, "버려진 카드 수 체크 실패"
    assert discarded[0].name == "붐볼", "버려진 카드 확인 실패"
    
    print(f"\n12. 최종 Field 상태:")
    print(field)
    
    # 새 턴 마킹 테스트
    field.mark_new_turn()
    print(f"13. 새 턴 마킹 후 Active 진화 가능: {field.active.can_evolve}")
    assert field.active.can_evolve == True, "새 턴 진화 가능 상태 체크 실패"
    
    print("✅ Field 모든 테스트 통과!\n")


def test_integration():
    """통합 테스트 - 실제 게임 시나리오"""
    print("=== 통합 테스트: 게임 시나리오 ===")
    
    # 게임 시나리오: 피카츄로 시작해서 라이츄로 진화
    pikachu = create_pokemon_card("피카츄")
    raichu = create_pokemon_card("라이츄", "Stage1 Pokemon")
    thunder_tool = create_tool_card("번개석")
    
    field = Field()
    
    # 1턴: 피카츄를 Active에 배치
    print("1턴: 피카츄를 Active에 배치")
    success = field.place_pokemon_active(pikachu)
    assert success == True, "Active 배치 실패"
    
    # 새로 배치된 포켓몬은 진화 불가
    field.mark_newly_placed(field.active)
    print(f"   진화 가능 상태: {field.active.can_evolve} (False여야 함)")
    assert field.active.can_evolve == False, "새로 배치된 포켓몬 진화 제한 실패"
    
    # 2턴: 새 턴 시작 (진화 가능하게 됨)
    print("\n2턴: 새 턴 시작")
    field.mark_new_turn()
    print(f"   진화 가능 상태: {field.active.can_evolve} (True여야 함)")
    assert field.active.can_evolve == True, "새 턴 진화 가능 상태 변경 실패"
    
    # Tool 부착
    tool_success = field.active.attach_tool(thunder_tool)
    print(f"   번개석 부착: {tool_success}")
    assert tool_success == True, "Tool 부착 실패"
    
    # 라이츄로 진화
    evolve_success = field.active.add_evolution(raichu)
    print(f"   라이츄로 진화: {evolve_success}")
    assert evolve_success == True, "진화 실패"
    
    print(f"\n최종 상태:")
    print(field)
    
    # Tool이 진화 후에도 유지되는지 확인
    assert field.active.attached_tool.name == "번개석", "진화 후 Tool 유지 실패"
    assert field.active.get_top_pokemon().name == "라이츄", "진화 후 최상위 포켓몬 체크 실패"
    assert field.active.get_bottom_pokemon().name == "피카츄", "진화 후 최하위 포켓몬 체크 실패"
    
    print("✅ 통합 테스트 통과!")


def main():
    """메인 테스트 함수"""
    print("Pokemon Pocket Simulator v3.0 - 핵심 클래스 테스트")
    print("=" * 60)
    
    try:
        test_pokemon_slot()
        test_field() 
        test_integration()
        
        print("\n🎉 모든 테스트가 성공적으로 완료되었습니다!")
        print("v3.0 핵심 클래스들(PokemonSlot, Field)이 정상적으로 작동합니다.")
        print("\n다음 단계: GameState 확장 구현 (v3_game_state.py)")
        
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
