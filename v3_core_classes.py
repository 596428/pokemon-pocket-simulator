#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pokemon Pocket Simulator v3.0 - 핵심 클래스들
파일명: v3_core_classes.py
생성일: 2025-06-12
목적: v3.0의 핵심 클래스 PokemonSlot과 Field 정의

주요 클래스:
- Card: 기본 카드 클래스 (기존 호환성 유지)
- PokemonSlot: 진화 스택과 Tool 부착을 관리하는 슬롯
- Field: Active Spot과 Bench를 관리하는 필드
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Card:
    """기본 카드 클래스 (기존 구조 유지)
    
    v2.02와의 호환성을 위해 최소한의 구조로 유지
    """
    name: str
    card_type: str
    
    def __str__(self) -> str:
        return f"{self.name} ({self.card_type})"


class PokemonSlot:
    """v3.0 신규: 포켓몬 슬롯 클래스
    
    진화 스택과 Tool 부착을 관리하는 클래스
    - evolution_stack: [Basic, Stage1, Stage2] 순서로 진화 스택
    - attached_tool: 부착된 Tool 카드 (최상위에만 적용)
    - can_evolve: 해당 턴 진화 가능 여부
    
    v3 가이드 참조:
    - 진화 스택: 하위 카드는 deactive 상태로 field에 유지
    - Tool 유지: 진화 시 Tool은 최상위 카드에 계속 부착
    - 진화 제한: 나온 턴에는 진화 불가
    """
    
    def __init__(self):
        self.evolution_stack: List[Card] = []
        self.attached_tool: Optional[Card] = None
        self.can_evolve: bool = True
        
    def get_top_pokemon(self) -> Optional[Card]:
        """최상위(활성) 포켓몬 반환"""
        return self.evolution_stack[-1] if self.evolution_stack else None
        
    def get_bottom_pokemon(self) -> Optional[Card]:
        """최하위(Basic) 포켓몬 반환"""
        return self.evolution_stack[0] if self.evolution_stack else None
        
    def add_evolution(self, card: Card) -> bool:
        """진화 카드 추가
        
        Args:
            card: 추가할 진화 카드
            
        Returns:
            bool: 진화 성공 여부
        """
        if not self.can_evolve:
            return False
        self.evolution_stack.append(card)
        return True
        
    def can_evolve_to(self, evolution_card: Card) -> bool:
        """특정 카드로 진화 가능한지 체크
        
        Args:
            evolution_card: 진화하려는 카드
            
        Returns:
            bool: 진화 가능 여부
            
        TODO: 실제 진화 조건 체크 로직 구현 필요
        - Basic → Stage1 조건 체크
        - Stage1 → Stage2 조건 체크
        - rare candy: Basic → Stage2 조건 체크
        """
        if not self.can_evolve or not self.evolution_stack:
            return False
        # TODO: 실제 진화 조건 체크 로직 구현 필요
        return True
        
    def attach_tool(self, tool_card: Card) -> bool:
        """Tool 카드 부착
        
        Args:
            tool_card: 부착할 Tool 카드
            
        Returns:
            bool: 부착 성공 여부
        """
        if self.attached_tool is None and self.get_top_pokemon():
            self.attached_tool = tool_card
            return True
        return False
        
    def is_empty(self) -> bool:
        """빈 슬롯인지 확인"""
        return len(self.evolution_stack) == 0
        
    def get_evolution_stage(self) -> int:
        """현재 진화 단계 반환 (0=빈슬롯, 1=Basic, 2=Stage1, 3=Stage2)"""
        return len(self.evolution_stack)
        
    def __str__(self) -> str:
        if self.is_empty():
            return "[빈 슬롯]"
        
        pokemon_info = " -> ".join(card.name for card in self.evolution_stack)
        tool_info = f" (Tool: {self.attached_tool.name})" if self.attached_tool else ""
        evolve_info = " [진화가능]" if self.can_evolve else " [진화불가]"
        
        return f"{pokemon_info}{tool_info}{evolve_info}"


class Field:
    """v3.0 신규: Field 클래스
    
    Active Spot과 Bench를 관리하는 클래스
    - active: Active Spot (1개, 반드시 존재해야 함)
    - bench: Bench Slots (기본 3개, 가변적)
    - bench_limit: 벤치 최대 크기
    
    v3 가이드 참조:
    - Active Spot: 반드시 1마리 존재 (비어있으면 패배)
    - Bench: 기본 3개, 카드 효과로 변경 가능
    - 벤치 초과 시: 플레이어 선택으로 초과분을 discard pile로
    - 배치 제한: 벤치 꽉 찬 상태에서는 새 배치 불가
    """
    
    def __init__(self, initial_bench_size: int = 3):
        self.active = PokemonSlot()
        self.bench = [PokemonSlot() for _ in range(initial_bench_size)]
        self.bench_limit = initial_bench_size
        
    def resize_bench(self, new_limit: int) -> List[Card]:
        """벤치 크기 변경 (카드 효과용)
        
        Args:
            new_limit: 새로운 벤치 크기 제한
            
        Returns:
            List[Card]: discard pile로 보내질 카드들
            
        Note:
            벤치가 줄어들 때 초과분은 플레이어 선택으로 discard
            현재는 뒤쪽 슬롯부터 자동으로 discard (TODO: 플레이어 선택 구현)
        """
        discarded_cards = []
        
        if new_limit < len(self.bench):
            # 벤치가 줄어드는 경우 - 초과분을 discard
            for i in range(new_limit, len(self.bench)):
                slot = self.bench[i]
                if not slot.is_empty():
                    # TODO: 플레이어 선택 로직 필요
                    discarded_cards.extend(slot.evolution_stack)
                    if slot.attached_tool:
                        discarded_cards.append(slot.attached_tool)
            
            self.bench = self.bench[:new_limit]
        else:
            # 벤치가 늘어나는 경우 - 새 슬롯 추가
            while len(self.bench) < new_limit:
                self.bench.append(PokemonSlot())
                
        self.bench_limit = new_limit
        return discarded_cards
        
    def get_available_bench_slots(self) -> List[int]:
        """비어있는 벤치 슬롯들의 인덱스 반환"""
        return [i for i, slot in enumerate(self.bench) if slot.is_empty()]
        
    def place_pokemon_active(self, card: Card) -> bool:
        """Active Spot에 포켓몬 배치
        
        Args:
            card: 배치할 Basic Pokemon 카드
            
        Returns:
            bool: 배치 성공 여부
        """
        if self.active.is_empty():
            return self.active.add_evolution(card)
        return False
        
    def place_pokemon_bench(self, card: Card, slot_index: Optional[int] = None) -> bool:
        """벤치에 포켓몬 배치
        
        Args:
            card: 배치할 Basic Pokemon 카드
            slot_index: 배치할 슬롯 인덱스 (None이면 자동 선택)
            
        Returns:
            bool: 배치 성공 여부
        """
        available_slots = self.get_available_bench_slots()
        
        if not available_slots:
            return False
            
        if slot_index is None:
            slot_index = available_slots[0]
        elif slot_index not in available_slots:
            return False
            
        return self.bench[slot_index].add_evolution(card)
        
    def get_all_pokemon_slots(self) -> List[PokemonSlot]:
        """모든 포켓몬 슬롯 반환 (Active + Bench)
        
        Returns:
            List[PokemonSlot]: 포켓몬이 있는 모든 슬롯들
        """
        slots = [self.active] if not self.active.is_empty() else []
        slots.extend([slot for slot in self.bench if not slot.is_empty()])
        return slots
        
    def mark_new_turn(self):
        """새 턴 시작 - 모든 포켓몬을 진화 가능 상태로 변경"""
        self.active.can_evolve = True
        for slot in self.bench:
            slot.can_evolve = True
            
    def mark_newly_placed(self, slot: PokemonSlot):
        """새로 배치된 포켓몬을 진화 불가 상태로 마킹
        
        Args:
            slot: 새로 배치된 포켓몬이 있는 슬롯
        """
        slot.can_evolve = False
        
    def has_active_pokemon(self) -> bool:
        """Active Spot에 포켓몬이 있는지 확인 (패배 조건 체크용)"""
        return not self.active.is_empty()
        
    def get_bench_pokemon_count(self) -> int:
        """벤치에 배치된 포켓몬 수 반환"""
        return sum(1 for slot in self.bench if not slot.is_empty())
        
    def __str__(self) -> str:
        result = ["=== Field 상태 ==="]
        result.append(f"Active: {self.active}")
        
        result.append("Bench:")
        for i, slot in enumerate(self.bench):
            result.append(f"  [{i}] {slot}")
            
        return "\n".join(result)


# 모듈 레벨에서 사용할 수 있는 유틸리티 함수들
def create_pokemon_card(name: str, stage: str = "Basic Pokemon") -> Card:
    """포켓몬 카드 생성 헬퍼 함수"""
    return Card(name, stage)


def create_tool_card(name: str) -> Card:
    """Tool 카드 생성 헬퍼 함수"""
    return Card(name, "Pokemon Tool")
