import os
import json
import re
from collections import defaultdict, OrderedDict
from threading import Thread
from time import sleep


def Print(num, titles):
    fold = {}
    title = ''
    cnt = 0
    numTitle = 0
    file = open(f"enwiki-latest-pages-articles_{num}.xml",'r',encoding="utf-8") 
    for line in file:
        # Find a new title
        if line.find('<title>') > 0 and line.find('</title>') > 0: 
            title = "".join(filter(str.isalnum, line[line.find('<title>')+7:line.find('</title>')])).lower()
            if title in titles.keys():
                numTitle = numTitle + 1
                title = titles[title]
                locals()[f'item_{numTitle}'] = defaultdict(list)
                # Save item
                fold[title] = locals()[f'item_{numTitle}']
                locals()[f'item_{numTitle}']['keywords'].append(title)
                cnt = 0
            else:
                title = ''

        # Find redirect
        if line.find('<redirect title') > 0 and title != '':
            redirectTitle = re.findall(r'["](.*?)["]', line)
            for i in redirectTitle:
                i = "".join(filter(str.isalnum, i)).lower()
                if i in titles.keys():
                    locals()[f'item_{numTitle}']['redirects'].append(titles[i])
        
        # Start add keywords to item (using at most 50 lines)
        if title != '':
            if cnt < 50:
                keywords = re.findall(r'[[[](.*?)[]]]', line)
                # fliter
                for i in keywords:
                    i = i[1:]
                    if i.find('|')>0:
                        i = i[:i.find('|')]
                    i = "".join(filter(str.isalnum, i)).lower()
                    if i in titles.keys():
                        locals()[f'item_{numTitle}']['keywords'].append(titles[i])
                cnt = cnt+1
    file.close()

    # Open the next file to add keywords
    if cnt < 50 and num + 1 <= 622:
        file = open(f"enwiki-latest-pages-articles_{num + 1}.xml",'r',encoding="utf-8") 
        for line in file:
            if line.find('<title>') > 0 and line.find('</title>') > 0: 
                break

            # Find redirect
            if line.find('<redirect title') > 0 and title != '':
                redirectTitle = re.findall(r'["](.*?)["]', line)
                for i in redirectTitle:
                    i = "".join(filter(str.isalnum, i)).lower()
                    if i in titles.keys():
                        locals()[f'item_{numTitle}']['redirects'].append(titles[i])

            if title != '':
                if cnt < 50:
                    keywords = re.findall(r'[[[](.*?)[]]]', line)
                    # fliter
                    for i in keywords:
                        i = i[1:]
                        if i.find('|')>0:
                            i = i[:i.find('|')]
                        i = "".join(filter(str.isalnum, i)).lower()
                        if i in titles.keys():
                            locals()[f'item_{numTitle}']['keywords'].append(titles[i])
                    cnt = cnt+1
        file.close()

    # Save json
    json_str = json.dumps(fold, indent=4)
    with open(f'output_data_{num}.json', 'w',encoding="utf-8") as json_file:
        json_file.write(json_str)



def T(index,title):
    numTurn = 0
    while(index + numTurn * 8 <=622):
        Print(index + numTurn * 8, title)
        print(index + numTurn * 8)
        numTurn = numTurn + 1

if __name__ == "__main__":
    title = {}
    print("Load titles")
    
    with open("abstract.json",'r') as load_f:
        load_dict = json.load(load_f)
    
        for key in load_dict:
            title_key = "".join(filter(str.isalnum, key)).lower()
            title[title_key]=key

    print("Begin")
    threads = []
    for x in range(8):
        thread = Thread(target=T, args=(x+1,title))   
        thread.start()   
        threads.append(thread)

    for thread in threads:
        thread.join()   