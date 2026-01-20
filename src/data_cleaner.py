import logging
import os
from typing import Dict, Optional, List
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)

class FacultyCleaner:
    def __init__(self, base_url: str = "https://www.daiict.ac.in"):
        self.base_url = base_url

    def clean_text(self, text: Optional[str]) -> str:
        if not text:
            return ""
        text = text.replace('\xa0', ' ')
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def decode_email(self, email_text: str) -> str:
        if not email_text:
            return ""
        email = email_text.replace('[at]', '@').replace('[dot]', '.')
        return email.strip()

    def get_section_content(self, soup: BeautifulSoup, section_title: str, fallback_class: str = None) -> str:
        header = soup.find('h2', string=lambda t: t and section_title.lower() in t.lower())
        if header:
            content_div = header.find_next(['div', 'p'])
            if content_div:
                text = self.clean_text(content_div.get_text())
                if text:
                    return text

        if fallback_class:
            field = soup.find(class_=fallback_class)
            if field:
                return self.clean_text(field.get_text())
                
        return ""

    def extract_faculty_data(self, html: str, file_name: str) -> Dict[str, str]:
        soup = BeautifulSoup(html, 'lxml')
        
        data = {
            "name": self.clean_text(self._get_field(soup, "field--name-field-faculty-names")),
            "image_url": self._get_image_url(soup),
            "education": self.clean_text(self._get_field(soup, "field--name-field-faculty-name")),
            "contact_no": self.clean_text(self._get_field(soup, "field--name-field-contact-no")),
            "address": self.clean_text(self._get_field(soup, "field--name-field-address")),
            "email": self.decode_email(self._get_field(soup, "field--name-field-email")),
            "biography": self.get_section_content(soup, "Biography", "field--name-field-biography"),
            "specialization": self.get_section_content(soup, "Specialization", "field--name-field-specialization"),
            "teaching": self.get_section_content(soup, "Teaching", "field--name-field-teaching"),
            "publications": self.get_section_content(soup, "Publications", "field--name-field-publication"),
            "raw_source_file": file_name
        }
        
        if not data["biography"] and data["specialization"]:
            spec_text = data["specialization"]
            if len(spec_text) > 50 and any(start in spec_text.lower() for start in ['dr.', 'mr.', 'ms.', 'prof.', 'i am', 'he is', 'she is', data['name'].split()[0].lower()]):
                data["biography"] = spec_text
                data["specialization"] = ""
        
        if not data["name"]:
            h1 = soup.find('h1')
            if h1:
                data["name"] = self.clean_text(h1.get_text())
                
        return data

    def _get_field(self, soup: BeautifulSoup, class_name: str) -> str:
        field = soup.find(class_=class_name)
        if not field:
            return ""
        item = field.find(class_="field__item")
        if item:
            return item.get_text()
        return field.get_text()

    def _get_image_url(self, soup: BeautifulSoup) -> str:
        image_field = soup.find(class_="field--name-field-faculty-image")
        if not image_field:
            return ""
        img = image_field.find('img')
        if not img or not img.get('src'):
            return ""
        
        src = img['src']
        if src.startswith('http'):
            return src
        return f"{self.base_url}{src}"

def main():
    import json
    try:
        from .config import RAW_DATA_DIR
    except ImportError:
        from config import RAW_DATA_DIR
    
    cleaner = FacultyCleaner()
    all_data = []
    
    files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.html')]
    logger.info(f"Cleaning {len(files)} files...")
    
    for file_name in files:
        file_path = os.path.join(RAW_DATA_DIR, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
            data = cleaner.extract_faculty_data(html, file_name)
            all_data.append(data)
            
    logger.info(f"Successfully cleaned {len(all_data)} profiles")
    return all_data

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
