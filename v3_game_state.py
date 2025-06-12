#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pokemon Pocket Simulator v3.0 - GameState 확장
파일명: v3_game_state.py
생성일: 2025-06-12
목적: 기존 GameState를 v3.0 규칙에 맞게 확장

주요 변경사항:
- 4개 공간 시스템: Deck, Hand, Field, Discard Pile
- 진화 불가 마킹 시스템: newly_placed_pokemon
- 진화 라인 설정: evolution_lines
- 선호 Basic Pokemon 설정: preferred_basics

v3 가이드 참조:
- 데이터 공간: Deck ↔ Hand (2개) → Deck, Hand, Field, Discard Pile (4개)
- 확률 기준 변경: "Hand에 카드 보유" → "실제 진화 완료"
"""

from typing import List, Dict, Any, Optional
import copy
from v3_core_classes import Card, Field, create_pokemon_card


class GameStateV3:
    """v3.0 확장된 GameState 클래스
    
    기존 v2.02 GameState의 기능을 유지하면서 v3.0 새 기능 추가:
    - Field: Active Spot + Bench 관리
    - discard_pile: 사용된 카드들의 최종 목적지
    - newly_placed_pokemon: 해당 턴에 배치되어 진화 불가인 포켓몬들
    - evolution_lines: 진화 라인 정의 (rare candy 등에 사용)
    - preferred_basics: 선호하는 Basic Pokemon (Active 배치 우선순위)
    """
    
    def __init__(self, deck_input: Dict[str, Dict[str, Any]], 
                 draw_order: Optional[List[str]] = None,
                 preferred_basics: Optional[List[str]] = None,
                 evolution_lines: Optional[List[Dict[str, str]]] = None):
        """GameState 초기화
        
        Args:
            deck_input: 덱 구성 정보 (기존 v2.02 형식 유지)
            draw_order: 드로우 순서 (시뮬레이션용)
            preferred_basics: 선호 Basic Pokemon 리스트
            evolution_lines: 진화 라인 정의 [{"basic": "피카츄", "stage1": "라이츄", "stage2": None}]
        """
        
        # === 기존 v2.02 호환 속성들 ===
        self.deck = self._create_deck_from_input(deck_input)
        self.hand: List[Card] = []
        self.turn = 0
        self.supporter_used = False
        self.draw_order = draw_order or []
        
        # === v3.0 신규 속성들 ===
        self.field = Field()                           # Field 공간 (Active + Bench)
        self.discard_pile: List[Card] = []             # Discard Pile 공간
        self.newly_placed_pokemon: List[Card] = []     # 진화 불가 마킹용
        
        # === 설정 정보 ===
        self.preferred_basics = preferred_basics or []
        self.evolution_lines = evolution_lines or []
        
    def _create_deck_from_input(self, deck_input: Dict[str, Dict[str, Any]]) -> List[Card]:
        """덱 입력으로부터 Card 리스트 생성 (v2.02 호환성 유지)
        
        Args:
            deck_input: {"카드명": {"카드타입": str, "count": int}} 형식
            
        Returns:
            List[Card]: 생성된 덱 카드들
        """
        deck = []
        for card_name, card_info in deck_input.items():
            card_type = card_info.get("카드타입", "Unknown")
            count = card_info.get("count", 1)
            
            for _ in range(count):
                deck.append(Card(card_name, card_type))
                
        return deck
        
    def reset_game(self):
        """게임 상태를 초기 상태로 리셋 (v2.02 호환)"""
        # 기존 속성 리셋
        self.hand = []
        self.turn = 0
        self.supporter_used = False
        
        # v3.0 신규 속성 리셋
        self.field = Field()
        self.discard_pile = []
        self.newly_placed_pokemon = []
        
        # 덱 리셋 (deep copy로 원본 보존)
        # Note: deck은 초기화 시점의 원본 덱을 참조해야 하므로 별도 처리 필요
        
    def draw_cards(self, count: int) -> List[Card]:
        """덱에서 카드 드로우 (v2.02 호환)
        
        Args:
            count: 드로우할 카드 수
            
        Returns:
            List[Card]: 드로우한 카드들
        """
        drawn_cards = []
        for _ in range(count):
            if self.deck:
                card = self.deck.pop(0)  # 덱 맨 위에서 드로우
                drawn_cards.append(card)
                self.hand.append(card)
        return drawn_cards
        
    def initial_draw(self) -> bool:
        """게임 시작 시 5장 드로우 + Basic Pokemon 체크 (v3.0 수정)
        
        v3 가이드에 따른 게임 시작 시퀀스:
        1. 5장 드로우
        2. Basic Pokemon 있는지 체크
        3. 없으면 다시 셔플하고 5장 드로우 반복
        
        Returns:
            bool: 유효한 드로우 완료 여부
        """
        max_attempts = 10  # 무한 루프 방지
        attempts = 0
        
        while attempts < max_attempts:
            self.hand = []
            drawn_cards = self.draw_cards(5)
            
            # Basic Pokemon이 있는지 체크
            if self._has_basic_pokemon_in_hand():
                return True
                
            # Basic Pokemon이 없으면 덱에 다시 넣고 셔플
            self.deck.extend(self.hand)
            self.hand = []
            # TODO: 실제 셔플 로직 필요 (현재는 시뮬레이션이므로 draw_order 사용)
            attempts += 1
            
        return False  # 최대 시도 횟수 초과
        
    def _has_basic_pokemon_in_hand(self) -> bool:
        """Hand에 Basic Pokemon이 있는지 체크"""
        for card in self.hand:
            if card.card_type == "Basic Pokemon":
                return True
        return False
        
    def start_turn(self):
        """새 턴 시작 처리 (v3.0 확장)
        
        v3 가이드에 따른 턴 진행:
        1. 턴 카운터 증가
        2. 1장 드로우
        3. newly_placed_pokemon 초기화 (진화 가능하게 됨)
        4. Field의 모든 포켓몬을 진화 가능 상태로 변경
        """
        self.turn += 1
        self.supporter_used = False
        
        # 1장 드로우
        self.draw_cards(1)
        
        # 새 턴이므로 모든 포켓몬이 진화 가능해짐
        self.newly_placed_pokemon = []
        self.field.mark_new_turn()
        
    def place_pokemon_active(self, card_name: str) -> bool:
        """Active Spot에 포켓몬 배치 (v3.0 신규)
        
        Args:
            card_name: 배치할 포켓몬 카드명
            
        Returns:
            bool: 배치 성공 여부
        """
        # Hand에서 해당 카드 찾기
        card_to_place = None
        for card in self.hand:
            if card.name == card_name and card.card_type == "Basic Pokemon":
                card_to_place = card
                break
                
        if card_to_place is None:
            return False
            
        # Field에 배치 시도
        success = self.field.place_pokemon_active(card_to_place)
        if success:
            self.hand.remove(card_to_place)
            self.newly_placed_pokemon.append(card_to_place)
            self.field.mark_newly_placed(self.field.active)
            
        return success
        
    def place_pokemon_bench(self, card_name: str, slot_index: Optional[int] = None) -> bool:
        """벤치에 포켓몬 배치 (v3.0 신규)
        
        Args:
            card_name: 배치할 포켓몬 카드명
            slot_index: 배치할 벤치 슬롯 인덱스 (None이면 자동)
            
        Returns:
            bool: 배치 성공 여부
        """
        # Hand에서 해당 카드 찾기
        card_to_place = None
        for card in self.hand:
            if card.name == card_name and card.card_type == "Basic Pokemon":
                card_to_place = card
                break
                
        if card_to_place is None:
            return False
            
        # Field에 배치 시도
        success = self.field.place_pokemon_bench(card_to_place, slot_index)
        if success:
            self.hand.remove(card_to_place)
            self.newly_placed_pokemon.append(card_to_place)
            # 배치된 슬롯을 찾아서 진화 불가 마킹
            for slot in self.field.bench:
                if not slot.is_empty() and slot.get_top_pokemon().name == card_name:
                    self.field.mark_newly_placed(slot)
                    break
                    
        return success
        
    def move_to_discard_pile(self, cards: List[Card]):
        """카드들을 discard pile로 이동 (v3.0 신규)
        
        Args:
            cards: discard pile로 이동할 카드들
        """
        self.discard_pile.extend(cards)
        
    def get_basic_pokemon_in_hand(self) -> List[Card]:
        """Hand에 있는 Basic Pokemon들 반환"""
        return [card for card in self.hand if card.card_type == "Basic Pokemon"]
        
    def get_preferred_basics_in_hand(self) -> List[Card]:
        """Hand에 있는 선호 Basic Pokemon들 반환"""
        preferred_cards = []
        for card in self.hand:
            if card.card_type == "Basic Pokemon" and card.name in self.preferred_basics:
                preferred_cards.append(card)
        return preferred_cards
        
    def find_evolution_line(self, pokemon_name: str) -> Optional[Dict[str, str]]:
        """포켓몬 이름으로 해당하는 진화 라인 찾기
        
        Args:
            pokemon_name: 찾을 포켓몬 이름
            
        Returns:
            Optional[Dict]: 진화 라인 정보 또는 None
        """
        for evolution_line in self.evolution_lines:
            if (pokemon_name == evolution_line.get("basic") or 
                pokemon_name == evolution_line.get("stage1") or 
                pokemon_name == evolution_line.get("stage2")):
                return evolution_line
        return None
        
    def __str__(self) -> str:
        """GameState 현재 상태를 문자열로 표현"""
        result = [f"=== GameState (Turn {self.turn}) ==="]
        result.append(f"Deck: {len(self.deck)}장")
        result.append(f"Hand: {len(self.hand)}장 - {[card.name for card in self.hand]}")
        result.append(f"Discard Pile: {len(self.discard_pile)}장")
        result.append("")
        result.append(str(self.field))
        
        if self.newly_placed_pokemon:
            result.append(f"\n새로 배치된 포켓몬 (진화 불가): {[card.name for card in self.newly_placed_pokemon]}")
            
        return "\n".join(result)


# 모듈 레벨 유틸리티 함수들
def create_test_deck() -> Dict[str, Dict[str, Any]]:
    """테스트용 덱 생성"""
    return {
        "피카츄": {"카드타입": "Basic Pokemon", "count": 2},
        "라이츄": {"카드타입": "Stage1 Pokemon", "count": 2},
        "코일": {"카드타입": "Basic Pokemon", "count": 2},
        "레어드": {"카드타입": "Stage1 Pokemon", "count": 2},
        "Poke Ball": {"카드타입": "Item", "count": 2},
        "Professor's Research": {"카드타입": "Supporter", "count": 2},
        "rare candy": {"카드타입": "Item", "count": 2},
        "번개 에너지": {"카드타입": "Basic Energy", "count": 6}
    }


def create_test_evolution_lines() -> List[Dict[str, str]]:
    """테스트용 진화 라인 생성"""
    return [
        {
            "basic": "피카츄",
            "stage1": "라이츄", 
            "stage2": None
        },
        {
            "basic": "코일",
            "stage1": "레어드",
            "stage2": None
        }
    ]
