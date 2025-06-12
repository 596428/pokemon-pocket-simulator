#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pokemon Pocket Simulator v3.0 - 진화 시스템
파일명: v3_evolution_system.py
생성일: 2025-06-12
목적: v3.0의 진화 시스템 구현 (auto_evolve_all 함수 및 관련 로직)

주요 기능:
- auto_evolve_all: 우선순위별 자동 진화 실행
- rare candy 진화: Basic → Stage2 직접 진화
- 일반 진화: Basic → Stage1 → Stage2 순차 진화
- 진화 조건 체크 및 제약사항 처리

v3 가이드 참조:
- 진화 체크 타이밍: 턴당 최대 2번 (Iono 사용 전 + 턴 마지막)
- rare candy 제약: 첫 턴 사용 불가, 해당 턴 배치된 포켓몬에 사용 불가
- 진화 우선순위: rare candy(선호) > rare candy(기타) > 일반(선호) > 일반(기타)
"""

from typing import List, Optional, Dict, Any
from v3_core_classes import Card, PokemonSlot
from v3_game_state import GameStateV3


def auto_evolve_all(game_state: GameStateV3) -> Dict[str, Any]:
    """현재 가능한 모든 진화를 우선순위에 따라 실행
    
    v3 가이드에 따른 진화 우선순위:
    1. rare candy + Stage2 (선호 라인)
    2. rare candy + Stage2 (기타 라인)
    3. 일반 진화 (선호 라인)
    4. 일반 진화 (기타 라인)
    
    Args:
        game_state: 현재 게임 상태
        
    Returns:
        Dict: 진화 실행 결과 정보
    """
    evolution_log = {
        "total_evolutions": 0,
        "rare_candy_evolutions": 0,
        "normal_evolutions": 0,
        "evolution_details": []
    }
    
    # 우선순위 1: rare candy + Stage2 (선호 라인)
    for evolution_line in game_state.evolution_lines:
        if _try_rare_candy_evolution(game_state, evolution_line, priority="preferred"):
            evolution_log["rare_candy_evolutions"] += 1
            evolution_log["total_evolutions"] += 1
            evolution_log["evolution_details"].append(f"rare candy 진화 (선호): {evolution_line['basic']} → {evolution_line.get('stage2', '?')}")
    
    # 우선순위 2: rare candy + Stage2 (기타 라인)
    if _try_rare_candy_evolution(game_state, None, priority="others"):
        evolution_log["rare_candy_evolutions"] += 1
        evolution_log["total_evolutions"] += 1
        evolution_log["evolution_details"].append("rare candy 진화 (기타)")
    
    # 우선순위 3: 일반 진화 (선호 라인)
    for evolution_line in game_state.evolution_lines:
        while _try_normal_evolution(game_state, evolution_line, priority="preferred"):
            evolution_log["normal_evolutions"] += 1
            evolution_log["total_evolutions"] += 1
            evolution_log["evolution_details"].append(f"일반 진화 (선호): {evolution_line['basic']} 라인")
    
    # 우선순위 4: 일반 진화 (기타 라인)
    while _try_normal_evolution(game_state, None, priority="others"):
        evolution_log["normal_evolutions"] += 1
        evolution_log["total_evolutions"] += 1
        evolution_log["evolution_details"].append("일반 진화 (기타)")
    
    return evolution_log


def _try_rare_candy_evolution(game_state: GameStateV3, 
                              evolution_line: Optional[Dict[str, str]] = None,
                              priority: str = "preferred") -> bool:
    """rare candy를 이용한 진화 시도
    
    rare candy 효과:
    - Basic Pokemon → Stage2 직접 진화 (Stage1 건너뛰기)
    - 첫 턴(turn 0) 사용 불가
    - 해당 턴에 배치된 포켓몬에 사용 불가
    
    Args:
        game_state: 게임 상태
        evolution_line: 특정 진화 라인 (None이면 모든 라인 검토)
        priority: "preferred" 또는 "others"
        
    Returns:
        bool: 진화 성공 여부
    """
    
    # 1. rare candy가 hand에 있는지 체크
    rare_candy_card = None
    for card in game_state.hand:
        if card.name == "rare candy":
            rare_candy_card = card
            break
    
    if rare_candy_card is None:
        return False
    
    # 2. 첫 턴(turn 0) 사용 불가
    if game_state.turn == 0:
        return False
    
    # 3. 진화 가능한 Basic Pokemon 찾기
    target_slot = None
    target_stage2_card = None
    
    # Active 슬롯 체크
    if _can_use_rare_candy_on_slot(game_state, game_state.field.active, evolution_line):
        stage2_card = _find_stage2_in_hand(game_state, game_state.field.active, evolution_line)
        if stage2_card:
            target_slot = game_state.field.active
            target_stage2_card = stage2_card
    
    # 벤치 슬롯들 체크
    if target_slot is None:
        for slot in game_state.field.bench:
            if _can_use_rare_candy_on_slot(game_state, slot, evolution_line):
                stage2_card = _find_stage2_in_hand(game_state, slot, evolution_line)
                if stage2_card:
                    target_slot = slot
                    target_stage2_card = stage2_card
                    break
    
    # 4. 진화 실행
    if target_slot and target_stage2_card:
        return _execute_rare_candy_evolution(game_state, target_slot, target_stage2_card, rare_candy_card)
    
    return False


def _try_normal_evolution(game_state: GameStateV3,
                          evolution_line: Optional[Dict[str, str]] = None,
                          priority: str = "preferred") -> bool:
    """일반 진화 시도
    
    일반 진화 규칙:
    - Basic → Stage1 → Stage2 순차 진화
    - 해당 턴에 배치된 포켓몬은 진화 불가
    - 항상 최고 단계까지 진화 시도
    
    Args:
        game_state: 게임 상태
        evolution_line: 특정 진화 라인 (None이면 모든 라인 검토)
        priority: "preferred" 또는 "others"
        
    Returns:
        bool: 진화 성공 여부
    """
    
    # Field의 모든 슬롯 체크 (Active + Bench)
    all_slots = [game_state.field.active] + game_state.field.bench
    
    for slot in all_slots:
        if slot.is_empty() or not slot.can_evolve:
            continue
            
        # 진화 가능한 카드가 hand에 있는지 체크
        evolution_card = _find_evolution_in_hand(game_state, slot, evolution_line)
        if evolution_card:
            # 진화 실행
            if _execute_normal_evolution(game_state, slot, evolution_card):
                return True
    
    return False


def _can_use_rare_candy_on_slot(game_state: GameStateV3, 
                                 slot: PokemonSlot,
                                 evolution_line: Optional[Dict[str, str]] = None) -> bool:
    """슬롯에 rare candy를 사용할 수 있는지 체크
    
    Args:
        game_state: 게임 상태
        slot: 체크할 슬롯
        evolution_line: 체크할 진화 라인
        
    Returns:
        bool: rare candy 사용 가능 여부
    """
    if slot.is_empty() or not slot.can_evolve:
        return False
    
    # Basic Pokemon인지 체크 (rare candy는 Basic에서만 사용 가능)
    top_pokemon = slot.get_top_pokemon()
    if top_pokemon.card_type != "Basic Pokemon":
        return False
    
    # 해당 턴에 배치된 포켓몬인지 체크
    for newly_placed in game_state.newly_placed_pokemon:
        if newly_placed.name == top_pokemon.name:
            return False
    
    return True


def _find_stage2_in_hand(game_state: GameStateV3,
                         slot: PokemonSlot,
                         evolution_line: Optional[Dict[str, str]] = None) -> Optional[Card]:
    """슬롯의 Basic Pokemon에 대응하는 Stage2 카드를 hand에서 찾기
    
    Args:
        game_state: 게임 상태
        slot: Basic Pokemon이 있는 슬롯
        evolution_line: 진화 라인 정보
        
    Returns:
        Optional[Card]: 찾은 Stage2 카드 또는 None
    """
    if slot.is_empty():
        return None
    
    basic_pokemon = slot.get_bottom_pokemon()
    
    # 지정된 진화 라인이 있으면 해당 라인에서만 찾기
    if evolution_line:
        if basic_pokemon.name != evolution_line.get("basic"):
            return None
        
        stage2_name = evolution_line.get("stage2")
        if stage2_name:
            for card in game_state.hand:
                if card.name == stage2_name and card.card_type == "Stage2 Pokemon":
                    return card
    else:
        # 진화 라인이 지정되지 않으면 모든 Stage2 카드 검토
        line = game_state.find_evolution_line(basic_pokemon.name)
        if line and line.get("stage2"):
            stage2_name = line["stage2"]
            for card in game_state.hand:
                if card.name == stage2_name and card.card_type == "Stage2 Pokemon":
                    return card
    
    return None


def _find_evolution_in_hand(game_state: GameStateV3,
                            slot: PokemonSlot,
                            evolution_line: Optional[Dict[str, str]] = None) -> Optional[Card]:
    """슬롯의 포켓몬에 대응하는 진화 카드를 hand에서 찾기
    
    Args:
        game_state: 게임 상태
        slot: 진화시킬 포켓몬이 있는 슬롯
        evolution_line: 진화 라인 정보
        
    Returns:
        Optional[Card]: 찾은 진화 카드 또는 None
    """
    if slot.is_empty():
        return None
    
    current_pokemon = slot.get_top_pokemon()
    current_stage = slot.get_evolution_stage()
    
    # 현재 포켓몬의 진화 라인 찾기
    if evolution_line:
        target_line = evolution_line
    else:
        target_line = game_state.find_evolution_line(current_pokemon.name)
    
    if not target_line:
        return None
    
    # 현재 단계에 따라 다음 단계 카드 찾기
    target_card_name = None
    target_card_type = None
    
    if current_stage == 1:  # Basic → Stage1
        target_card_name = target_line.get("stage1")
        target_card_type = "Stage1 Pokemon"
    elif current_stage == 2:  # Stage1 → Stage2
        target_card_name = target_line.get("stage2")
        target_card_type = "Stage2 Pokemon"
    
    if target_card_name and target_card_type:
        for card in game_state.hand:
            if card.name == target_card_name and card.card_type == target_card_type:
                return card
    
    return None


def _execute_rare_candy_evolution(game_state: GameStateV3,
                                   slot: PokemonSlot,
                                   stage2_card: Card,
                                   rare_candy_card: Card) -> bool:
    """rare candy 진화 실행
    
    Args:
        game_state: 게임 상태
        slot: 진화할 슬롯
        stage2_card: Stage2 카드
        rare_candy_card: rare candy 카드
        
    Returns:
        bool: 진화 실행 성공 여부
    """
    try:
        # 1. Stage2 카드를 슬롯에 추가 (Basic → Stage2 직접)
        success = slot.add_evolution(stage2_card)
        if not success:
            return False
        
        # 2. Hand에서 카드들 제거
        game_state.hand.remove(stage2_card)
        game_state.hand.remove(rare_candy_card)
        
        # 3. rare candy를 discard pile로
        game_state.move_to_discard_pile([rare_candy_card])
        
        return True
        
    except (ValueError, Exception):
        return False


def _execute_normal_evolution(game_state: GameStateV3,
                              slot: PokemonSlot,
                              evolution_card: Card) -> bool:
    """일반 진화 실행
    
    Args:
        game_state: 게임 상태
        slot: 진화할 슬롯
        evolution_card: 진화 카드
        
    Returns:
        bool: 진화 실행 성공 여부
    """
    try:
        # 1. 진화 카드를 슬롯에 추가
        success = slot.add_evolution(evolution_card)
        if not success:
            return False
        
        # 2. Hand에서 진화 카드 제거
        game_state.hand.remove(evolution_card)
        
        return True
        
    except (ValueError, Exception):
        return False


def check_evolution_success(game_state: GameStateV3, target_evolutions: List[str]) -> bool:
    """진화 완료 여부 체크 (v3.0 새로운 성공 조건)
    
    v3 가이드: "Hand에 카드 보유" → "실제 진화 완료"로 기준 변경
    
    Args:
        game_state: 게임 상태
        target_evolutions: 목표 진화 완료 카드들
        
    Returns:
        bool: 모든 목표 진화가 완료되었는지 여부
    """
    # Field에서 진화 완료된 포켓몬들 확인
    completed_evolutions = []
    
    # Active 포켓몬 체크
    if not game_state.field.active.is_empty():
        top_pokemon = game_state.field.active.get_top_pokemon()
        completed_evolutions.append(top_pokemon.name)
    
    # 벤치 포켓몬들 체크
    for slot in game_state.field.bench:
        if not slot.is_empty():
            top_pokemon = slot.get_top_pokemon()
            completed_evolutions.append(top_pokemon.name)
    
    # 모든 목표 진화가 완료되었는지 체크
    for target in target_evolutions:
        if target not in completed_evolutions:
            return False
    
    return True


def get_evolution_candidates(game_state: GameStateV3) -> Dict[str, List[str]]:
    """현재 진화 가능한 후보들 반환 (디버깅/분석용)
    
    Args:
        game_state: 게임 상태
        
    Returns:
        Dict: 진화 가능한 후보들 정보
    """
    candidates = {
        "rare_candy_candidates": [],
        "normal_evolution_candidates": [],
        "hand_evolution_cards": []
    }
    
    # Hand의 진화 카드들
    for card in game_state.hand:
        if card.card_type in ["Stage1 Pokemon", "Stage2 Pokemon"]:
            candidates["hand_evolution_cards"].append(f"{card.name} ({card.card_type})")
    
    # rare candy 후보들
    if "rare candy" in [card.name for card in game_state.hand] and game_state.turn > 0:
        all_slots = [game_state.field.active] + game_state.field.bench
        for i, slot in enumerate(all_slots):
            if _can_use_rare_candy_on_slot(game_state, slot):
                stage2_card = _find_stage2_in_hand(game_state, slot)
                if stage2_card:
                    slot_name = "Active" if i == 0 else f"Bench[{i-1}]"
                    candidates["rare_candy_candidates"].append(
                        f"{slot_name}: {slot.get_top_pokemon().name} → {stage2_card.name}"
                    )
    
    # 일반 진화 후보들
    all_slots = [game_state.field.active] + game_state.field.bench
    for i, slot in enumerate(all_slots):
        if not slot.is_empty() and slot.can_evolve:
            evolution_card = _find_evolution_in_hand(game_state, slot)
            if evolution_card:
                slot_name = "Active" if i == 0 else f"Bench[{i-1}]"
                candidates["normal_evolution_candidates"].append(
                    f"{slot_name}: {slot.get_top_pokemon().name} → {evolution_card.name}"
                )
    
    return candidates
