import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'thenewboston' # constant capitalized
HOMEPAGE = 'https://thenewboston.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRWALED_FILE = PROJECT_NAME + '/crwaled.txt'
NUMBER_OF_THREADS = 8 # operating system specifies
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME) # first spider


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True # die whenever the main exits
        t.start()

# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join() # threads don't bump into each other
    crawl()
    
# check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

create_workers()
crawl()

