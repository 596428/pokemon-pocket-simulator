# -*- coding: utf-8 -*-
# Munpia Individual Novel ID Finder - 실제 작품 ID 찾기

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random

class MunpiaNovelIdFinder:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Referer': 'https://www.munpia.com/'
        })
        
        try:
            self.session.get("https://www.munpia.com/", timeout=10)
            time.sleep(1)
        except:
            pass
    
    def extract_novel_ids_from_html(self, html_content):
        """HTML에서 작품 ID 추출"""
        
        novel_ids = []
        
        # 패턴 1: novel.munpia.com/숫자
        pattern1 = re.findall(r'novel\.munpia\.com/(\d+)', html_content)
        novel_ids.extend(pattern1)
        
        # 패턴 2: /novel/숫자
        pattern2 = re.findall(r'/novel/(\d+)', html_content)
        novel_ids.extend(pattern2)
        
        # 패턴 3: novelId=숫자
        pattern3 = re.findall(r'novelId=(\d+)', html_content)
        novel_ids.extend(pattern3)
        
        # 패턴 4: JavaScript나 AJAX 호출에서
        pattern4 = re.findall(r'id["\']?\s*[:=]\s*["\']?(\d{4,7})["\']?', html_content)
        novel_ids.extend(pattern4)
        
        # 중복 제거 및 정리
        unique_ids = list(set(novel_ids))
        
        # 숫자가 너무 크거나 작으면 제외 (일반적으로 작품 ID는 4-7자리)
        valid_ids = [id for id in unique_ids if 1000 <= int(id) <= 9999999]
        
        return valid_ids
    
    def find_novel_ids_from_multiple_pages(self):
        """여러 페이지에서 작품 ID 수집"""
        
        print("문피아 개별 작품 ID 수집")
        print("=" * 50)
        
        # 다양한 페이지에서 ID 수집
        pages_to_check = [
            "https://www.munpia.com/ranking/novel",
            "https://www.munpia.com/",
            "https://www.munpia.com/page/j/view/w/best/today",
            "https://www.munpia.com/page/j/view/w/best/week",
            "https://www.munpia.com/page/j/view/w/genre/13",  # 판타지
            "https://www.munpia.com/page/j/view/w/genre/21",  # 무협
            "https://www.munpia.com/page/j/view/w/genre/23"   # 로맨스
        ]
        
        all_novel_ids = []
        
        for page_url in pages_to_check:
            print(f"\n페이지 분석: {page_url}")
            
            try:
                time.sleep(random.uniform(1, 3))
                response = self.session.get(page_url, timeout=15)
                
                if response.status_code == 200:
                    novel_ids = self.extract_novel_ids_from_html(response.text)
                    print(f"  발견된 ID: {len(novel_ids)}개")
                    all_novel_ids.extend(novel_ids)
                    
                    if novel_ids:
                        print(f"  샘플: {novel_ids[:5]}")
                else:
                    print(f"  HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  오류: {e}")
        
        # 중복 제거
        unique_novel_ids = list(set(all_novel_ids))
        print(f"\n총 고유 작품 ID: {len(unique_novel_ids)}개")
        
        return unique_novel_ids[:50]  # 상위 50개만 반환
    
    def analyze_novel_with_id(self, novel_id):
        """작품 ID로 개별 작품 분석"""
        
        novel_url = f"https://novel.munpia.com/{novel_id}"
        print(f"\n[ID {novel_id}] 분석: {novel_url}")
        
        try:
            time.sleep(random.uniform(2, 4))
            response = self.session.get(novel_url, timeout=15)
            
            if response.status_code != 200:
                print(f"  접근 실패: HTTP {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            novel_data = {
                'novel_id': novel_id,
                'url': novel_url,
                'title': None,
                'author': None,
                'genre': None,
                'views': None,
                'rating': None,
                'synopsis': None,
                'upload_date': None,
                'episode_count': None,
                'status': None,
                'tags': [],
                'favorites': None
            }
            
            # 제목 찾기 (개선된 방법)
            title_selectors = [
                'h1.title', '.novel-title', '.work-title', 
                'h1', 'title', '.subject', '.name'
            ]
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get_text().strip()
                    if title and len(title) > 2 and '문피아' not in title and '에러' not in title:
                        novel_data['title'] = title
                        print(f"  제목: {title}")
                        break
            
            # 만약 제목을 찾지 못했다면 페이지 타이틀에서
            if not novel_data['title']:
                page_title = soup.find('title')
                if page_title:
                    title = page_title.get_text().strip()
                    if '문피아' in title:
                        title = title.replace('- 웹소설 문피아', '').strip()
                    if len(title) > 2:
                        novel_data['title'] = title
                        print(f"  제목(타이틀): {title}")
            
            # 전체 페이지 텍스트에서 정보 추출
            page_text = soup.get_text()
            
            # 작가 찾기
            author_patterns = [
                r'작가\s*[:：]\s*([가-힣a-zA-Z0-9_\s]{2,20})',
                r'글\s*[:：]\s*([가-힣a-zA-Z0-9_\s]{2,20})',
                r'저자\s*[:：]\s*([가-힣a-zA-Z0-9_\s]{2,20})'
            ]
            
            for pattern in author_patterns:
                match = re.search(pattern, page_text)
                if match:
                    author = match.group(1).strip()
                    if len(author) > 1 and len(author) < 20:
                        novel_data['author'] = author
                        print(f"  작가: {author}")
                        break
            
            # 장르 찾기
            genre_keywords = ['판타지', '무협', '로맨스', 'BL', 'GL', '현대', '역사', '추리', 'SF', '오컬트']
            for genre in genre_keywords:
                if genre in page_text:
                    novel_data['genre'] = genre
                    print(f"  장르: {genre}")
                    break
            
            # 조회수 찾기 (개선된 패턴)
            view_patterns = [
                r'조회수?\s*[:：]?\s*([\d,]+(?:만|천)?)',
                r'조회\s*([\d,]+(?:만|천)?)',
                r'view\s*[:：]?\s*([\d,]+(?:만|천)?)',
                r'([\d,]+(?:만|천)?)\s*회\s*조회',
                r'Total\s*View\s*[:：]?\s*([\d,]+)',
                r'총\s*조회\s*[:：]?\s*([\d,]+)'
            ]
            
            for pattern in view_patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    views = match.group(1)
                    novel_data['views'] = views
                    print(f"  조회수: {views}")
                    break
            
            # 별점 찾기
            rating_patterns = [
                r'별점\s*[:：]?\s*(\d+\.?\d*)',
                r'평점\s*[:：]?\s*(\d+\.?\d*)',
                r'★\s*(\d+\.?\d*)',
                r'rating\s*[:：]?\s*(\d+\.?\d*)',
                r'(\d+\.?\d*)\s*/\s*(?:10|5)',
                r'(\d+\.?\d*)\s*점'
            ]
            
            for pattern in rating_patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    rating = float(match.group(1))
                    if 0 <= rating <= 10:
                        novel_data['rating'] = match.group(1)
                        print(f"  별점: {match.group(1)}")
                        break
            
            # 시놉시스 찾기 (개선된 방법)
            synopsis_selectors = [
                '.synopsis', '.summary', '.description', '.intro',
                '.content', '.story', '.plot', '[class*="synopsis"]'
            ]
            
            for selector in synopsis_selectors:
                synopsis_elem = soup.select_one(selector)
                if synopsis_elem:
                    synopsis = synopsis_elem.get_text().strip()
                    if synopsis and len(synopsis) > 50:
                        novel_data['synopsis'] = synopsis[:300]
                        print(f"  시놉시스: {synopsis[:50]}...")
                        break
            
            # 메타 태그에서 시놉시스
            if not novel_data['synopsis']:
                meta_desc = soup.find('meta', {'name': 'description'})
                if meta_desc:
                    content = meta_desc.get('content', '').strip()
                    if len(content) > 30 and '문피아' not in content:
                        novel_data['synopsis'] = content
                        print(f"  메타 시놉시스: {content[:50]}...")
            
            # 업로드 날짜
            date_patterns = [
                r'업데이트\s*[:：]?\s*(\d{4}[-./]\d{1,2}[-./]\d{1,2})',
                r'등록\s*[:：]?\s*(\d{4}[-./]\d{1,2}[-./]\d{1,2})',
                r'(\d{4}\.\d{1,2}\.\d{1,2})',
                r'(\d{4}-\d{1,2}-\d{1,2})'
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, page_text)
                if match:
                    date = match.group(1)
                    novel_data['upload_date'] = date
                    print(f"  업로드: {date}")
                    break
            
            # 회차/에피소드 수
            episode_patterns = [
                r'총\s*(\d+)\s*화',
                r'총\s*(\d+)\s*회',
                r'(\d+)\s*화\s*완결',
                r'전체\s*(\d+)\s*화'
            ]
            
            for pattern in episode_patterns:
                match = re.search(pattern, page_text)
                if match:
                    episodes = match.group(1)
                    novel_data['episode_count'] = episodes
                    print(f"  회차수: {episodes}화")
                    break
            
            # 좋아요/찜하기 수
            favorite_patterns = [
                r'좋아요\s*[:：]?\s*([\d,]+)',
                r'찜\s*[:：]?\s*([\d,]+)',
                r'관심\s*[:：]?\s*([\d,]+)'
            ]
            
            for pattern in favorite_patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    favorites = match.group(1)
                    novel_data['favorites'] = favorites
                    print(f"  좋아요: {favorites}")
                    break
            
            # 연재 상태
            status_patterns = [
                r'(완결)', r'(연재중)', r'(휴재)', r'(중단)', r'(완료)'
            ]
            
            for pattern in status_patterns:
                match = re.search(pattern, page_text)
                if match:
                    status = match.group(1)
                    novel_data['status'] = status
                    print(f"  상태: {status}")
                    break
            
            return novel_data
            
        except Exception as e:
            print(f"  분석 오류: {e}")
            return None
    
    def comprehensive_novel_analysis(self):
        """종합적인 작품 분석"""
        
        print("문피아 개별 작품 종합 분석 v2.0")
        print("=" * 60)
        
        # 1. 작품 ID들 수집
        novel_ids = self.find_novel_ids_from_multiple_pages()
        
        if not novel_ids:
            print("분석할 작품 ID를 찾을 수 없습니다.")
            return None
        
        print(f"\n총 {len(novel_ids)}개 작품 ID로 상세 분석 시작")
        
        # 2. 개별 작품들 분석
        results = []
        successful_extractions = {
            'title': 0, 'author': 0, 'genre': 0, 'views': 0,
            'rating': 0, 'synopsis': 0, 'upload_date': 0,
            'episode_count': 0, 'status': 0, 'favorites': 0
        }
        
        for i, novel_id in enumerate(novel_ids[:15]):  # 처음 15개만 테스트
            print(f"\n--- 작품 {i+1}/{min(15, len(novel_ids))} ---")
            
            novel_data = self.analyze_novel_with_id(novel_id)
            if novel_data:
                results.append(novel_data)
                
                # 성공률 계산
                for key in successful_extractions:
                    if novel_data.get(key):
                        successful_extractions[key] += 1
        
        # 3. 결과 분석 및 저장
        total_analyzed = len(results)
        if total_analyzed > 0:
            print(f"\n=== 최종 종합 결과 ===")
            print(f"성공적으로 분석된 작품: {total_analyzed}개")
            
            print(f"\n데이터별 추출 성공률:")
            korean_names = {
                'title': '제목', 'author': '작가', 'genre': '장르', 
                'views': '조회수', 'rating': '별점', 'synopsis': '시놉시스',
                'upload_date': '업로드날짜', 'episode_count': '회차수', 
                'status': '연재상태', 'favorites': '좋아요수'
            }
            
            for key, count in successful_extractions.items():
                success_rate = (count / total_analyzed) * 100
                status = "SUCCESS" if success_rate >= 70 else "PARTIAL" if success_rate >= 30 else "FAILED"
                korean_name = korean_names.get(key, key)
                print(f"{status:8} {korean_name:10}: {success_rate:5.1f}% ({count:2}/{total_analyzed:2})")
        
        # 결과 저장
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'munpia_comprehensive_analysis_{timestamp}.json'
        
        final_results = {
            'timestamp': timestamp,
            'total_novel_ids_found': len(novel_ids),
            'analyzed_count': total_analyzed,
            'success_rates': {key: (count/total_analyzed*100) if total_analyzed > 0 else 0 
                            for key, count in successful_extractions.items()},
            'novels': results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(final_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n상세 결과가 {filename}에 저장되었습니다.")
        
        return final_results

def main():
    print("문피아 개별 작품 ID 기반 종합 분석")
    print("목표: 실제 작품 페이지에서 모든 상세 정보 추출")
    print("=" * 80)
    
    finder = MunpiaNovelIdFinder()
    results = finder.comprehensive_novel_analysis()
    
    if results:
        avg_success = sum(results['success_rates'].values()) / len(results['success_rates'])
        print(f"\n전체 평균 추출 성공률: {avg_success:.1f}%")
        
        if avg_success >= 60:
            print("🎉 문피아 상세 정보 추출 성공! 네이버와 경쟁 가능한 수준입니다.")
        elif avg_success >= 40:
            print("🟡 부분적 성공. 대부분의 정보는 추출 가능합니다.")
        else:
            print("🔴 추가 개선이 필요합니다.")

if __name__ == "__main__":
    main()
