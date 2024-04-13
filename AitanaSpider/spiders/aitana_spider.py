from typing import Any
import scrapy
import os
from bs4 import BeautifulSoup
import json
import re

CHUNK_MIN_WORDS = 90
K_MAX_PAGES = 700
WORDS_IN_CHUNK = 200

priority_words = ['masteres', 'grados']
exclude_words = ['sitemap', 'ua.es/va/', 'ua.es/en/']
obligatory_words = ['web.ua.es', 'cfp.ua.es', 'es/masteres', 'es/grados', '/es/oia']

chunk_mode = False


class AitanaSpider(scrapy.Spider):
    name = 'aitana_spider'

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.max_pages = K_MAX_PAGES
        self.visited_urls = set()
        self.savedPageCount = 0
        self.chunkCount = 0

    def start_requests(self, urls=None):
        if urls is None:
            urls = ["https://web.ua.es/es/grados-oficiales.html",
                    "https://web.ua.es/es/masteres-oficiales.html",
                    "https://web.ua.es/es/oia",
                    "https://www.ua.es"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # Mark the current page as visited
        self.visited_urls.add(response.url)

        if 'text/html' not in response.headers.get('Content-Type').decode():
            #self.log(f'Skipped {response.url} because it does contain text/html Content-Type')
            return

        # Path to the output txt file
        save_path_json = 'rag-faiss/page_contents.json'

        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('title')
        if title_tag:
            page_name = title_tag.text.strip()
        else:
            page_name = 'Unknown'

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

        if word_count >= CHUNK_MIN_WORDS:
            self.savedPageCount += 1

            if chunk_mode:
                chunks = self.split_text_by_words(text, WORDS_IN_CHUNK)
            else:
                chunks = [text]

            for chunk in chunks:
                if len(chunk) < CHUNK_MIN_WORDS:
                    continue

                data = {
                    "index_chunk": self.chunkCount,
                    "index_page": self.savedPageCount,
                    "page_name": page_name.strip(),
                    "url": response.url,
                    "content": chunk.strip()
                }

                self.chunkCount += 1
                if not os.path.isfile(save_path_json):
                    with open(save_path_json, 'w', encoding='utf-8') as f:
                        json.dump([data], f, ensure_ascii=False, indent=4)
                else:
                    with open(save_path_json, 'r', encoding='utf-8') as f:
                        content = json.load(f)

                    content.append(data)

                    with open(save_path_json, 'w', encoding='utf-8') as f:
                        json.dump(content, f, ensure_ascii=False, indent=4)

            self.log(f'Added content of {response.url} to {save_path_json}, page count: {self.savedPageCount}, '
                     f'chunk count: {self.chunkCount}')
        else:
            self.log(f'Skipped {response.url} because it does not contain enough text')

        # Check if the number of visited pages has reached the maximum
        if self.savedPageCount >= self.max_pages:
            self.log(f'Number of visited pages reached maximum ({self.max_pages}). Stopping crawler.')
            raise scrapy.exceptions.CloseSpider('Maximum pages reached')

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

    def split_text_by_words(self, text: str, max_words=200):
        sentences = re.split(r'(?<=[.!?]) +', text)
        chunks = []
        current_chunk = []
        current_count = 0

        for sentence in sentences:
            words = sentence.split()
            if current_count + len(words) <= max_words:
                current_chunk.append(sentence)
                current_count += len(words)
            else:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_count = len(words)

        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(' '.join(current_chunk))

        # Check if the last chunk has less than 100 words
        # and combine it with the penultimate one if possible
        if len(chunks) > 1 and len(chunks[-1].split()) < max_words / 2:
            chunks[-2] += ' ' + chunks[-1]
            chunks.pop()

        return chunks
