import Queue
import grequests

from utilities import get_data, scrape

class Scraper:

    def __init__(self, base_url, pool):
        self.base_url = base_url
        self.results = []
        self.visited = set([])
        self.queue = Queue.Queue()
        self.pool = pool
    
    def set_base_url(self, base_url):
        self.base_url = base_url
        
    def scrape(self, starting_path, body_config, nav_config, data_config):
        self.queue.put(starting_path)
        self.visited.add(starting_path)

        while not self.queue.empty():
            links = []
            while not self.queue.empty() and len(links) < self.pool:
                links.append(self.base_url+self.queue.get())
            
            async_reqs = (grequests.get(link) for link in links)
            async_resps = grequests.map(async_reqs)

            for resp in async_resps:
                self.results += scrape(resp, self.queue, self.visited, body_config, nav_config, data_config)
        
        return self.results
