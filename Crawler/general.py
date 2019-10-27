import os
# each website you crawl is a seperate project(folder)

def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating project' + directory)
        os.makedirs(directory)

# create queue and crawled files(if not created)
def create_data_files(project_name, base_url):
    queue = os.path.join(project_name, 'queue.txt')
    crawled = os.path.join(project_name, 'crawled.txt')
    if not os.path.isfile(queue):
        write_file(queue, base_url) # file path/name data in the file 
    if not os.path.isfile(crawled):
        write_file(crawled, '') # empty waiting to move url from queue

# create a new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close() # free memory space

# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file: # append
        file.write(data + '\n')

# Delete the contents of a file
def delete_file_contents(path):
    with open(path, 'w'):
        pass # do nothing

#  Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

# Iterate through a set, each item will be a new line in the file
def set_to_file(links, file):
    delete_file_contents(file) # old data 
    for link in sorted(links):
        append_to_file(file, link)


# create_data_files("thenewboston", 'https://thenewboston.com/')
    