from typing import Any
import scrapy
import os
from bs4 import BeautifulSoup
import json

K_MIN_WORDS = 90
K_MAX_PAGES = 100

class AitanaSpider(scrapy.Spider):
    name = 'aitana_spider'

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.max_pages = K_MAX_PAGES
        self.visited_urls = set()
        self.savedPageCount = 0

    def start_requests(self, urls=None):
        if urls is None:
            urls = ["https://web.ua.es/es/grados-oficiales.html",
                    "https://web.ua.es/es/masteres-oficiales.html",
                    "https://www.ua.es"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        if 'text/html' not in response.headers.get('Content-Type').decode():
            #self.log(f'Skipped {response.url} because it does contain text/html Content-Type')
            return

        # Adjusting to use a single .txt file and include page title
        url_parts = response.url.split("/")
        page_name = url_parts[-1]

        if response.url == 'https://www.ua.es':
            page_name = 'index'
        else:
            print(page_name)
            # Si la URL termina con ".html" se elimina la extensión
            if page_name.endswith('.html'):
                page_name = os.path.splitext(page_name)[0]
            else:
                # En caso contrario se obtiene el índece anterior
                page_name = url_parts[-2]

        # Path to the output txt file
        save_path = 'rag-faiss/page_contents.txt'
        save_path_json = 'rag-faiss/page_contents.json'
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        soup = BeautifulSoup(response.text, 'html.parser')

        for script_or_style in soup(['script', 'style', 'iframe']):
            script_or_style.decompose()

        main_content = soup.find('main')
        if not main_content:
            self.log(f'No main content found for {response.url}. Skipping.')
            return

        for link in main_content.find_all('a'):
            link.decompose()

        text = main_content.get_text(separator='\n', strip=True) if main_content else ''
        word_count = len(text.split())

        if len(text) > 0 and word_count >= K_MIN_WORDS:
            # Saving the page name and content with a delimiter
            with open(save_path, 'a', encoding='utf-8') as f:
                f.write(f"Page Name: {page_name} url: {response.url} | Content:\n{text}\n\n")
                f.write(f"=============================================================\n\n")

            data = {
                "index": self.savedPageCount,
                "page_name": page_name,
                "url": response.url,
                "content": text
            }

            if not os.path.isfile(save_path_json):
                with open(save_path_json, 'w', encoding='utf-8') as f:
                    json.dump([data], f, ensure_ascii=False, indent=4)
            else:
                with open(save_path_json, 'r', encoding='utf-8') as f:
                    content = json.load(f)

                content.append(data)
                self.savedPageCount += 1

                with open(save_path_json, 'w', encoding='utf-8') as f:
                    json.dump(content, f, ensure_ascii=False, indent=4)

                self.log(f'Added content of {response.url} to {save_path_json}')
        else:
            self.log(f'Skipped {response.url} because it does not contain enough text')
        # Mark the current page as visited
        self.visited_urls.add(response.url)

        # Check if the number of visited pages has reached the maximum
        if self.savedPageCount >= self.max_pages:
            self.log(f'Number of visited pages reached maximum ({self.max_pages}). Stopping crawler.')
            raise scrapy.exceptions.CloseSpider('Maximum pages reached')

        priority_words = ['masteres', 'grados']
        exclude_words = ['sitemap', 'ua.es/va/', 'ua.es/en/']
        obligatory_words = ['web.ua.es', 'cfp.ua.es', 'es/masteres', 'es/grados']

        all_links = response.css('a::attr(href)').getall()
        sorted_links = sorted(all_links, key=lambda link: any(word in link for word in priority_words), reverse=True)

        # Search for and follow links on the current page
        for next_page in sorted_links:
            # Ignore links that do not contain .ua.es
            if not any(domain in next_page for domain in obligatory_words):
                continue

            if any(exclude_word in next_page for exclude_word in exclude_words):
                #self.log(f'Skipped {next_page} because it does contain exclude_words')
                continue

            next_url = response.urljoin(next_page)
            if next_url not in self.visited_urls:
                yield scrapy.Request(url=next_url, callback=self.parse)
