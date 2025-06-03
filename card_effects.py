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
    "Galdion": "random_type_null_silvally"
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
