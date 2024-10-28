from threading import Thread

from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time

import json

from tokenizer import TokenCounter


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        """
        try: 
            with open("word_frequencies.json", "r") as f:
                total_word_frequencies = TokenCounter()
                total_word_frequencies.addTokensFromDict(json.load(f))
        except FileNotFoundError:
            with open("word_frequencies.json", "w") as f:
                total_word_frequencies = TokenCounter()
        """
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = scraper.scraper(tbd_url, resp)
            word_count = scraper.get_word_count(tbd_url, resp)
            """
            word_frequencies = scraper.get_word_frequencies(tbd_url, resp)
            total_word_frequencies.addTokensFromTokenCounter(word_frequencies)
            """
            with open("word_counts.txt", "a") as f:
                f.write(f"{word_count}: {tbd_url}\n")
            """ 
            with open("word_frequencies.json", "r") as f:
                f.dump(total_word_frequencies._counts)
            """   
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
