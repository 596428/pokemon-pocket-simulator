#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Pokemon Pocket Simulator v3.0 - 드로우카드 시스템 (간소화 버전)'''

from typing import List, Dict, Any
from v3_game_state import GameStateV3
from v3_evolution_system import auto_evolve_all
from card_effects import CardEffects


def use_draw_cards_v3(game_state: GameStateV3,
                     draw_order: List[str],
                     target_cards: List[str] = None,
                     verbose: bool = False) -> Dict[str, Any]:
    '''v3.0 드로우카드 사용 함수 - Iono 특별 처리 포함'''
    
    result = {
        'cards_used': [],
        'evolution_logs': [],
        'supporter_used': False,
        'total_evolutions': 0
    }
    
    supporter_used = False
    
    if verbose:
        turn_num = game_state.turn
        hand_names = [card.name for card in game_state.hand]
        print(f'=== 턴 {turn_num} 드로우카드 사용 시작 ===')
        print(f'Hand: {hand_names}')
        
    # 드로우카드들 사용
    for card_name in draw_order:
        cards_in_hand = [card for card in game_state.hand if card.name == card_name]
        
        for card in cards_in_hand:
            # Supporter 제한 체크
            if card.card_type == 'Supporter' and supporter_used:
                if verbose:
                    print(f'  {card_name} (Supporter) 건너뜀 - 이미 Supporter 사용함')
                continue
            
            if verbose:
                print(f'  {card_name} 사용 시도...')
            
            # === v3.0 핵심: Iono 특별 처리 ===
            if card_name == 'Iono':
                # Iono 사용 여부 판단
                should_use = False
                if target_cards:
                    decision = CardEffects.should_use_iono(game_state, target_cards)
                    should_use = decision['should_use']
                    if verbose and not should_use:
                        reason = decision.get('reason', '알 수 없음')
                        print(f'    Iono 사용 안 함: {reason}')
                
                if not should_use:
                    continue
                
                # Iono 사용 전 진화 체크 (v3.0 핵심!)
                if verbose:
                    print('  *** Iono 사용 전 진화 체크 ***')
                
                evolution_log = auto_evolve_all(game_state)
                result['evolution_logs'].append({
                    'timing': 'before_iono',
                    'turn': game_state.turn,
                    'log': evolution_log
                })
                result['total_evolutions'] += evolution_log['total_evolutions']
                
                if verbose and evolution_log['total_evolutions'] > 0:
                    details = evolution_log.get('evolution_details', [])
                    print(f'  진화 완료: {details}')
            
            # 카드 효과 실행
            effect_result = CardEffects.use_card_effect(card_name, game_state)
            
            if verbose:
                description = effect_result.get('description', '효과 실행')
                print(f'    결과: {description}')
            
            # 사용된 카드 처리
            game_state.hand.remove(card)
            result['cards_used'].append(card_name)
            
            # Supporter 사용 체크
            if card.card_type == 'Supporter':
                supporter_used = True
                result['supporter_used'] = True
                if verbose:
                    print('    Supporter 사용됨 - 이번 턴 추가 Supporter 사용 불가')
    
    # === v3.0 핵심: 턴 마지막 진화 체크 ===
    if verbose:
        print('  *** 턴 마지막 진화 체크 ***')
    
    final_evolution_log = auto_evolve_all(game_state)
    result['evolution_logs'].append({
        'timing': 'end_of_turn',
        'turn': game_state.turn,
        'log': final_evolution_log
    })
    result['total_evolutions'] += final_evolution_log['total_evolutions']
    
    if verbose and final_evolution_log['total_evolutions'] > 0:
        details = final_evolution_log.get('evolution_details', [])
        print(f'  진화 완료: {details}')
    
    if verbose:
        turn_num = game_state.turn
        cards_used = result['cards_used']
        total_evolutions = result['total_evolutions']
        print(f'=== 턴 {turn_num} 드로우카드 사용 완료 ===')
        print(f'사용된 카드: {cards_used}')
        print(f'총 진화 횟수: {total_evolutions}')
        
    return result
