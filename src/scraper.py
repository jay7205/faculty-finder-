import requests
from bs4 import BeautifulSoup
import time
import os
from typing import List, Dict, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

try:
    from .config import HEADERS, REQUEST_DELAY, MAX_RETRIES, TIMEOUT, RAW_DATA_DIR, FACULTY_URLS
except ImportError:
    from config import HEADERS, REQUEST_DELAY, MAX_RETRIES, TIMEOUT, RAW_DATA_DIR, FACULTY_URLS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FacultyScraper:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    @retry(stop=stop_after_attempt(MAX_RETRIES), wait=wait_exponential(multiplier=1, min=4, max=10))
    def fetch_page(self, url: str) -> Optional[str]:
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            time.sleep(REQUEST_DELAY)
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            raise
    
    def extract_profile_links(self, html: str, base_url: str) -> List[str]:
        soup = BeautifulSoup(html, 'lxml')
        
        valid_patterns = [
            '/faculty/',
            '/adjunct-faculty/',
            '/adjunct-faculty-international/',
            '/distinguished-professor/',
            '/professor-practice/'
        ]
        
        profile_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            has_valid_pattern = any(pattern in href for pattern in valid_patterns)
            
            if has_valid_pattern and href.count('/') >= 2:
                if href.startswith('http'):
                    full_url = href
                elif href.startswith('/'):
                    full_url = f"https://www.daiict.ac.in{href}"
                else:
                    full_url = f"{base_url}/{href}"
                
                has_daiict_pattern = any(f'daiict.ac.in{pattern}' in full_url for pattern in valid_patterns)
                
                if full_url not in profile_links and has_daiict_pattern:
                    profile_links.append(full_url)
        
        logger.info(f"Found {len(profile_links)} profile links")
        return profile_links
    
    def scrape_faculty_directory(self, directory_url: str) -> List[str]:
        html = self.fetch_page(directory_url)
        if html:
            return self.extract_profile_links(html, directory_url)
        return []
    
    def fetch_profile_html(self, profile_url: str) -> Optional[str]:
        return self.fetch_page(profile_url)
    
    def save_raw_html(self, html: str, slug: str) -> None:
        filename = os.path.join(RAW_DATA_DIR, f"{slug}.html")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        logger.info(f"Saved raw HTML: {filename}")
    
    def scrape_all_directories(self) -> Dict[str, List[str]]:
        all_profiles = {}
        
        for url in FACULTY_URLS:
            faculty_type = url.split('/')[-1]
            logger.info(f"\n{'='*60}")
            logger.info(f"Scraping directory: {faculty_type}")
            logger.info(f"{'='*60}")
            
            profile_links = self.scrape_faculty_directory(url)
            all_profiles[faculty_type] = profile_links
            
            logger.info(f"Total profiles found in {faculty_type}: {len(profile_links)}")
        
        return all_profiles
    
    def scrape_profile_details(self, profile_url: str) -> Optional[str]:
        slug = profile_url.rstrip('/').split('/')[-1]
        
        html = self.fetch_profile_html(profile_url)
        if html:
            self.save_raw_html(html, slug)
            return html
        return None


def main():
    scraper = FacultyScraper()
    
    logger.info("Starting Faculty Scraper...")
    all_profiles = scraper.scrape_all_directories()
    
    logger.info(f"\n{'='*60}")
    logger.info("SUMMARY")
    logger.info(f"{'='*60}")
    for faculty_type, profiles in all_profiles.items():
        logger.info(f"{faculty_type}: {len(profiles)} profiles")
    
    total_profiles = sum(len(profiles) for profiles in all_profiles.values())
    logger.info(f"\nTotal unique profiles to scrape: {total_profiles}")
    
    logger.info("\nStarting detailed profile scraping...")
    scraped_count = 0
    for faculty_type, profiles in all_profiles.items():
        for profile_url in profiles:
            scraper.scrape_profile_details(profile_url)
            scraped_count += 1
            logger.info(f"Progress: {scraped_count}/{total_profiles}")
    
    logger.info("\nScraping completed!")


if __name__ == "__main__":
    main()
