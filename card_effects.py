#!/usr/bin/env python3
"""
Pokemon Pocket Simulator - 카드 효과 모듈

카드별 효과를 구현하고 관리하는 모듈입니다.
새로운 카드 효과를 추가할 때는 이 파일에서 작업하면 됩니다.
"""

import random
from typing import Dict, Any, List

# 드로우 효과가 있는 카드들 정의
DRAW_CARDS = {
    "Poke Ball": "random_basic_pokemon",
    "Professor's Research": "draw_2", 
    "Galdion": "random_type_null_silvally",
    "Pokemon Communication": "pokemon_exchange"
}

class CardEffects:
    """카드 효과를 구현하는 클래스"""
    
    @staticmethod
    def poke_ball(game_state) -> bool:
        """
        Poke Ball 효과: 덱에서 랜덤한 Basic Pokemon을 손으로 가져오기
        
        Args:
            game_state: 현재 게임 상태
            
        Returns:
            bool: 효과 성공 여부
        """
        basic_pokemons_in_deck = [card for card in game_state.deck if card.card_type == "Basic Pokemon"]
        
        if not basic_pokemons_in_deck:
            random.shuffle(game_state.deck)
            return False
        
        selected_card = random.choice(basic_pokemons_in_deck)
        game_state.deck.remove(selected_card)
        game_state.hand.append(selected_card)
        random.shuffle(game_state.deck)
        
        return True
    
    @staticmethod
    def professors_research(game_state) -> int:
        """
        Professor's Research 효과: 2장 드로우
        
        Args:
            game_state: 현재 게임 상태
            
        Returns:
            int: 실제로 드로우한 카드 수
        """
        drawn_cards = game_state.draw_cards(2)
        return len(drawn_cards)
    
    @staticmethod
    def galdion(game_state) -> bool:
        """
        Galdion 효과: 덱에서 랜덤한 'Type:Null' 또는 'Silvally'를 손으로 가져오기
        
        Args:
            game_state: 현재 게임 상태
            
        Returns:
            bool: 효과 성공 여부
        """
        target_cards = [card for card in game_state.deck if card.name in ["Type:Null", "Silvally"]]
        
        if not target_cards:
            random.shuffle(game_state.deck)
            return False
        
        selected_card = random.choice(target_cards)
        game_state.deck.remove(selected_card)
        game_state.hand.append(selected_card)
        random.shuffle(game_state.deck)
        
        return True
    
    @staticmethod
    def pokemon_communication(game_state, sacrifice_pokemon_name: str = None) -> Dict[str, Any]:
        """
        Pokemon Communication 효과: 손패의 Pokemon을 덱의 랜덤한 Pokemon과 교환
        
        Args:
            game_state: 현재 게임 상태
            sacrifice_pokemon_name: 교환할 손패의 Pokemon 이름 (None이면 자동 선택)
            
        Returns:
            Dict: 효과 실행 결과
        """
        # 손패에서 Pokemon 카드들 찾기
        hand_pokemons = [card for card in game_state.hand if card.card_type in ["Basic Pokemon", "Stage1 Pokemon", "Stage2 Pokemon"]]
        
        if not hand_pokemons:
            return {"success": False, "description": "손패에 Pokemon이 없습니다", "card_obtained": None}
        
        # 덱에서 Pokemon 카드들 찾기
        deck_pokemons = [card for card in game_state.deck if card.card_type in ["Basic Pokemon", "Stage1 Pokemon", "Stage2 Pokemon"]]
        
        if not deck_pokemons:
            random.shuffle(game_state.deck)
            return {"success": False, "description": "덱에 Pokemon이 없습니다", "card_obtained": None}
        
        # 교환할 손패 Pokemon 선택
        if sacrifice_pokemon_name:
            # 지정된 Pokemon 찾기
            sacrifice_card = next((card for card in hand_pokemons if card.name == sacrifice_pokemon_name), None)
            if not sacrifice_card:
                return {"success": False, "description": f"손패에 {sacrifice_pokemon_name}이 없습니다", "card_obtained": None}
        else:
            # 자동 선택 (첫 번째 Pokemon)
            sacrifice_card = hand_pokemons[0]
        
        # 덱에서 랜덤한 Pokemon 선택
        obtained_card = random.choice(deck_pokemons)
        
        # 카드 교환 실행
        game_state.hand.remove(sacrifice_card)
        game_state.deck.remove(obtained_card)
        game_state.hand.append(obtained_card)
        game_state.deck.append(sacrifice_card)
        
        # 덱 셔플
        random.shuffle(game_state.deck)
        
        return {
            "success": True, 
            "description": f"{sacrifice_card.name} → {obtained_card.name} 교환 완료",
            "card_sacrificed": sacrifice_card.name,
            "card_obtained": obtained_card.name
        }
    
    @staticmethod
    def should_use_pokemon_communication(game_state, target_cards: List[str], max_turn: int) -> Dict[str, Any]:
        """
        Pokemon Communication 사용 여부를 판단하는 함수
        
        Args:
            game_state: 현재 게임 상태
            target_cards: 목표 카드들
            max_turn: 최대 턴 수
            
        Returns:
            Dict: 사용 여부 및 선택할 Pokemon 정보
        """
        # 1. 발동 조건 체크
        if game_state.turn != max_turn:
            return {"should_use": False, "reason": "마지막 턴이 아님"}
        
        # 2. target_cards 완성 여부 체크
        current_hand_names = [card.name for card in game_state.hand]
        missing_cards = [card for card in target_cards if card not in current_hand_names]
        
        if not missing_cards:
            return {"should_use": False, "reason": "이미 target_cards 완성됨"}
        
        # 3. 손패에 Pokemon 존재 여부 체크
        hand_pokemons = [card for card in game_state.hand if card.card_type in ["Basic Pokemon", "Stage1 Pokemon", "Stage2 Pokemon"]]
        
        if not hand_pokemons:
            return {"should_use": False, "reason": "손패에 Pokemon이 없음"}
        
        # 4. 덱에 필요한 Pokemon 존재 여부 체크
        deck_pokemons = [card for card in game_state.deck if card.card_type in ["Basic Pokemon", "Stage1 Pokemon", "Stage2 Pokemon"]]
        needed_pokemons_in_deck = [card for card in deck_pokemons if card.name in missing_cards]
        
        if not needed_pokemons_in_deck:
            return {"should_use": False, "reason": "덱에 필요한 Pokemon이 없음"}
        
        # 5. 교환할 Pokemon 선택 (우선순위: target에 없는 > target에 있지만 중복)
        hand_pokemon_names = [card.name for card in hand_pokemons]
        
        # 1순위: target_cards에 없는 Pokemon
        non_target_pokemons = [name for name in hand_pokemon_names if name not in target_cards]
        if non_target_pokemons:
            chosen_pokemon = non_target_pokemons[0]
            return {
                "should_use": True, 
                "chosen_pokemon": chosen_pokemon,
                "reason": f"덱에 필요한 Pokemon {len(needed_pokemons_in_deck)}장 존재, {chosen_pokemon} 교환 예정"
            }
        
        # 2순위: target에 있지만 손패에 중복으로 있는 Pokemon
        duplicates = [name for name in hand_pokemon_names if name in target_cards and current_hand_names.count(name) > 1]
        if duplicates:
            chosen_pokemon = duplicates[0]
            return {
                "should_use": True, 
                "chosen_pokemon": chosen_pokemon,
                "reason": f"덱에 필요한 Pokemon {len(needed_pokemons_in_deck)}장 존재, 중복 {chosen_pokemon} 교환 예정"
            }
        
        # 3순위: 사용하지 않는 것이 좋음 (유일한 target Pokemon만 있는 경우)
        return {"should_use": False, "reason": "교환할 Pokemon이 모두 중요한 target 카드"}
    
    @staticmethod
    def use_card_effect(card_name: str, game_state) -> Dict[str, Any]:
        """
        카드 효과를 실행하는 메인 함수
        
        Args:
            card_name: 사용할 카드 이름
            game_state: 현재 게임 상태
            
        Returns:
            Dict: 효과 실행 결과
        """
        result = {
            "card_name": card_name,
            "success": False,
            "description": ""
        }
        
        if card_name == "Poke Ball":
            success = CardEffects.poke_ball(game_state)
            result["success"] = success
            result["description"] = "Basic Pokemon을 덱에서 손으로" if success else "덱에 Basic Pokemon이 없음"
        
        elif card_name == "Professor's Research":
            drawn_count = CardEffects.professors_research(game_state)
            result["success"] = drawn_count > 0
            result["description"] = f"{drawn_count}장 드로우"
        
        elif card_name == "Galdion":
            success = CardEffects.galdion(game_state)
            result["success"] = success
            result["description"] = "Type:Null 또는 Silvally를 덱에서 손으로" if success else "덱에 대상 카드가 없음"
        
        elif card_name == "Pokemon Communication":
            # Pokemon Communication은 특별한 로직이 필요하므로 기본 효과만 실행
            # 실제 사용 여부는 should_use_pokemon_communication에서 판단
            pc_result = CardEffects.pokemon_communication(game_state)
            result["success"] = pc_result["success"]
            result["description"] = pc_result["description"]
            if "card_sacrificed" in pc_result:
                result["card_sacrificed"] = pc_result["card_sacrificed"]
            if "card_obtained" in pc_result:
                result["card_obtained"] = pc_result["card_obtained"]
        
        else:
            result["description"] = f"알 수 없는 카드: {card_name}"
        
        return result

# ===================== 새로운 카드 효과 추가 가이드 =====================
"""
새로운 카드 효과를 추가하려면:

1. DRAW_CARDS 딕셔너리에 카드 추가:
   "새카드명": "효과설명"

2. CardEffects 클래스에 새 메서드 추가:
   @staticmethod
   def 새카드명_소문자(game_state) -> bool/int:
       # 효과 구현
       return result

3. use_card_effect 메서드에 elif 블록 추가:
   elif card_name == "새카드명":
       result = CardEffects.새카드명_소문자(game_state)
       result["success"] = ...
       result["description"] = ...

예시:
- Red Card: 상대방 손패 1장 버리기 (시뮬레이터에서는 구현 안함)
- Potion: HP 회복 (시뮬레이터에서는 구현 안함)
- Ultra Ball: Basic Pokemon 또는 Stage1 Pokemon 서치
- Pokemon Communication: 손패 Pokemon을 덱 Pokemon과 교환 (v2.01에서 추가됨)

Pokemon Communication 특별 기능:
- should_use_pokemon_communication(): 복잡한 발동 조건 판단
- 마지막 턴에서만 사용, target_cards 미완성 시만 발동
- 연쇄 사용 로직 지원 (main_simulator.py에서 처리)
"""

def get_draw_cards_list() -> List[str]:
    """드로우 카드 목록 반환"""
    return list(DRAW_CARDS.keys())

def is_draw_card(card_name: str) -> bool:
    """해당 카드가 드로우 카드인지 확인"""
    return card_name in DRAW_CARDS

def get_card_effect_description(card_name: str) -> str:
    """카드 효과 설명 반환"""
    return DRAW_CARDS.get(card_name, "효과 없음")
