from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *


class Spider:

    # Class variables (shared among all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = '' # hard-drive
    queue = set()
    crawled = set() # ram

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name +'/qeueu.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod # don't need to pass self, because self is a referencec to this class)
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + 'now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crwaled ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)  # deal with set
            Spider.update_files()
        
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-type') == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
                # convert to human readable string
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string) # pass html
        except:
            print('Error: cannot crawl page')
            return set()
        return finder.page_links()
    
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url:
                continue # thenewboston.com 
            Spider.queue.add(url)
    
    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
    
    

    






