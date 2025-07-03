# -*- coding: utf-8 -*-
# Munpia Fixed Crawler - 실제 페이지 구조 기반 정확한 추출

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time
import random

class MunpiaFixedCrawler:
    """문피아 수정된 크롤러 - 실제 구조 기반"""
    
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
    
    def safe_request(self, url, retries=3):
        """안전한 요청 처리"""
        for attempt in range(retries):
            try:
                time.sleep(random.uniform(1, 3))
                response = self.session.get(url, timeout=15)
                if response.status_code == 200:
                    return response
                else:
                    print(f"   HTTP {response.status_code}: {url}")
            except Exception as e:
                print(f"   요청 실패 ({attempt+1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(random.uniform(2, 5))
        return None
    
    def extract_munpia_novels(self):
        """문피아 소설 데이터 추출 - 실제 구조 기반"""
        
        print("문피아 소설 데이터 추출 시작")
        print("=" * 60)
        
        # 테스트할 문피아 페이지들
        test_pages = [
            {
                'name': '메인 랭킹 페이지', 
                'url': 'https://www.munpia.com/ranking/novel',
                'type': 'ranking'
            },
            {
                'name': '베스트 페이지', 
                'url': 'https://www.munpia.com/page/j/view/w/best/today',
                'type': 'best'
            },
            {
                'name': '메인 페이지', 
                'url': 'https://www.munpia.com/',
                'type': 'main'
            }
        ]
        
        all_results = {}
        
        for page_info in test_pages:
            print(f"\n[분석] {page_info['name']}")
            
            response = self.safe_request(page_info['url'])
            if not response:
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            novels = self.extract_novels_from_soup(soup, page_info)
            
            if novels:
                all_results[page_info['name']] = {
                    'url': page_info['url'],
                    'type': page_info['type'],
                    'novels': novels,
                    'count': len(novels)
                }
                print(f"   성공: {len(novels)}개 작품 추출")
                
                # 샘플 출력
                for i, novel in enumerate(novels[:3]):
                    print(f"   작품 {i+1}: {novel.get('제목', 'Unknown')}")
                    print(f"      작가: {novel.get('작가', 'Unknown')}")
                    print(f"      장르: {novel.get('장르', 'Unknown')}")
            else:
                print(f"   실패: 작품 추출 불가")
        
        return all_results
    
    def extract_novels_from_soup(self, soup, page_info):
        """BeautifulSoup 객체에서 소설 데이터 추출"""
        
        novels = []
        
        # 실제 문피아 구조 기반 추출
        # 방법 1: title heavy 클래스 기반 추출
        titles = soup.find_all('span', class_='title heavy')
        print(f"      찾은 제목 수: {len(titles)}")
        
        for i, title_elem in enumerate(titles):
            novel_data = {
                'rank': i + 1,
                'has_data': False,
                '제목': None,
                '작가': None,
                '장르': None,
                '조회수': None,
                '업로드시간': None,
                '회차별분량': None,
                '별점': None,
                '시놉시스': None
            }
            
            try:
                # 제목 추출
                title = title_elem.get_text().strip()
                if title and len(title) > 1:
                    novel_data['제목'] = title
                    novel_data['has_data'] = True
                
                # 같은 부모에서 작가와 장르 찾기
                parent = title_elem.parent
                if parent:
                    # 작가 찾기
                    author_elem = parent.find('span', class_='author')
                    if author_elem:
                        author = author_elem.get_text().strip()
                        if author:
                            novel_data['작가'] = author
                            novel_data['has_data'] = True
                    
                    # 장르 찾기
                    genre_elem = parent.find('span', class_='genre')
                    if genre_elem:
                        genre = genre_elem.get_text().strip()
                        if genre:
                            novel_data['장르'] = genre
                            novel_data['has_data'] = True
                    
                    # 추가 정보 찾기 (조회수, 별점 등)
                    self.extract_additional_info(parent, novel_data)
                
                if novel_data['has_data']:
                    novels.append(novel_data)
                    
            except Exception as e:
                print(f"      작품 {i+1} 추출 오류: {e}")
        
        # 방법 2: item 클래스 기반 추출 (보완)
        if len(novels) < 5:  # 충분히 추출되지 않았다면
            items = soup.find_all(class_='item')
            print(f"      아이템 방식으로 추가 추출 시도: {len(items)}개")
            
            for i, item in enumerate(items[:20]):  # 상위 20개만
                additional_novel = self.extract_from_item(item, len(novels) + i + 1)
                if additional_novel and additional_novel.get('has_data'):
                    novels.append(additional_novel)
        
        return novels
    
    def extract_additional_info(self, element, novel_data):
        """추가 정보 추출 (조회수, 별점, 날짜 등)"""
        
        try:
            full_text = element.get_text()
            
            # 조회수 패턴
            view_patterns = [
                r'조회수?\s*[:：]?\s*([\d,]+(?:만|천)?)',
                r'조회\s*([\d,]+(?:만|천)?)',
                r'([\d,]+(?:만|천)?)\s*조회',
                r'view\s*([\d,]+(?:만|천)?)'
            ]
            
            for pattern in view_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    novel_data['조회수'] = match.group(1)
                    break
            
            # 별점 패턴
            rating_patterns = [
                r'별점\s*[:：]?\s*(\d+\.?\d*)',
                r'평점\s*[:：]?\s*(\d+\.?\d*)',
                r'★\s*(\d+\.?\d*)',
                r'(\d+\.?\d*)\s*점'
            ]
            
            for pattern in rating_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    rating = float(match.group(1))
                    if 0 <= rating <= 10:
                        novel_data['별점'] = match.group(1)
                        break
            
            # 날짜 패턴
            date_patterns = [
                r'(\d{4}[-./]\d{1,2}[-./]\d{1,2})',
                r'(\d{4}년\s*\d{1,2}월\s*\d{1,2}일)',
                r'(\d{2}\.\d{2}\.\d{2})'
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, full_text)
                if match:
                    novel_data['업로드시간'] = match.group(1)
                    break
            
            # 회차 정보
            episode_patterns = [
                r'총\s*(\d+)\s*화',
                r'(\d+)\s*화',
                r'총\s*(\d+)\s*회',
                r'(\d+)\s*회'
            ]
            
            for pattern in episode_patterns:
                match = re.search(pattern, full_text)
                if match:
                    novel_data['회차별분량'] = f"{match.group(1)}화"
                    break
            
        except Exception as e:
            pass
    
    def extract_from_item(self, item, rank):
        """item 클래스에서 정보 추출"""
        
        novel_data = {
            'rank': rank,
            'has_data': False,
            '제목': None,
            '작가': None,
            '장르': None,
            '조회수': None,
            '업로드시간': None,
            '회차별분량': None,
            '별점': None,
            '시놉시스': None
        }
        
        try:
            # 제목 찾기
            title_selectors = [
                '.title', '.title.heavy', 'a[href*="novel"]', 'strong', 'h3', 'h4'
            ]
            
            for selector in title_selectors:
                title_elem = item.select_one(selector)
                if title_elem:
                    title = title_elem.get_text().strip()
                    if title and len(title) > 2 and not title.isdigit():
                        novel_data['제목'] = title
                        novel_data['has_data'] = True
                        break
            
            # 작가 찾기
            author_elem = item.select_one('.author')
            if author_elem:
                author = author_elem.get_text().strip()
                if author:
                    novel_data['작가'] = author
                    novel_data['has_data'] = True
            
            # 장르 찾기
            genre_elem = item.select_one('.genre')
            if genre_elem:
                genre = genre_elem.get_text().strip()
                if genre:
                    novel_data['장르'] = genre
                    novel_data['has_data'] = True
            
            # 추가 정보 추출
            self.extract_additional_info(item, novel_data)
            
        except Exception as e:
            pass
        
        return novel_data
    
    def generate_analysis_report(self, results):
        """분석 리포트 생성"""
        
        print(f"\n문피아 크롤링 최종 결과")
        print("=" * 50)
        
        total_novels = sum(page_data.get('count', 0) for page_data in results.values())
        print(f"총 추출된 작품 수: {total_novels}개")
        
        if total_novels == 0:
            print("추출된 작품이 없습니다.")
            return
        
        # 모든 소설 데이터 통합
        all_novels = []
        for page_data in results.values():
            all_novels.extend(page_data.get('novels', []))
        
        # 데이터별 성공률 분석
        data_items = ['제목', '작가', '장르', '조회수', '업로드시간', '회차별분량', '별점', '시놉시스']
        
        print(f"\n데이터별 추출 성공률:")
        for item in data_items:
            successful = [novel for novel in all_novels if novel.get(item)]
            success_rate = (len(successful) / len(all_novels)) * 100 if all_novels else 0
            
            if success_rate >= 70:
                status = "SUCCESS"
            elif success_rate >= 30:
                status = "PARTIAL"
            else:
                status = "FAILED"
            
            print(f"{status:8} {item:10}: {success_rate:5.1f}% ({len(successful):2}/{len(all_novels):2})")
            
            if successful:
                sample = successful[0][item]
                print(f"           예시: {sample}")
        
        # 우수 추출 사례
        print(f"\n추출 성공 사례:")
        complete_novels = [n for n in all_novels if sum(1 for v in n.values() if v) >= 4]
        
        for i, novel in enumerate(complete_novels[:5]):
            print(f"\n작품 {i+1}:")
            for key, value in novel.items():
                if value and key != 'rank' and key != 'has_data':
                    print(f"  {key}: {value}")
        
        return {
            'total_novels': total_novels,
            'success_rates': {
                item: (len([n for n in all_novels if n.get(item)]) / len(all_novels) * 100) if all_novels else 0
                for item in data_items
            },
            'sample_novels': complete_novels[:10]
        }

def main():
    """메인 실행 함수"""
    
    print("문피아 수정된 크롤링 시스템 v3.0")
    print("목표: 제목, 작가, 장르, 조회수, 업로드시간, 회차별분량, 별점, 시놉시스")
    print("=" * 80)
    
    crawler = MunpiaFixedCrawler()
    
    # 소설 데이터 추출
    results = crawler.extract_munpia_novels()
    
    if results:
        # 분석 리포트 생성
        analysis = crawler.generate_analysis_report(results)
        
        # 결과 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'munpia_fixed_results_{timestamp}.json'
        
        final_results = {
            'timestamp': timestamp,
            'extraction_results': results,
            'analysis': analysis
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(final_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n상세 결과가 {filename}에 저장되었습니다.")
        
        # 네이버와 비교
        if analysis['total_novels'] > 0:
            avg_success = sum(analysis['success_rates'].values()) / len(analysis['success_rates'])
            print(f"\n평균 추출 성공률: {avg_success:.1f}%")
            
            if avg_success >= 60:
                print("문피아 크롤링 성공! 네이버와 경쟁 가능한 수준입니다.")
            elif avg_success >= 30:
                print("문피아 크롤링 부분 성공. 추가 개선이 필요합니다.")
            else:
                print("문피아 크롤링 개선 필요. 구조 재분석이 요구됩니다.")
    
    else:
        print("크롤링 결과가 없습니다.")

if __name__ == "__main__":
    main()
