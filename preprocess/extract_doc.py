import os
import json
import re
from collections import defaultdict, OrderedDict
from threading import Thread
from time import sleep

def Print(num):
    fold = {}
    title = ''
    cnt = 0
    numTitle = 0
    file = open(f"enwiki-latest-pages-articles_{num}.xml",'r',encoding="utf-8") 
    for line in file:
        # Find a new title
        if line.find('<title>') > 0 and line.find('</title>') > 0: 
            numTitle = numTitle + 1
            title = line[line.find('<title>')+7:line.find('</title>')]
            locals()[f'item_{numTitle}'] = defaultdict(list)
            # Save item
            fold[title] = locals()[f'item_{numTitle}']
            cnt = 0

        # Find redirect
        if line.find('<redirect title') > 0 and title != '':
            redirectTitle = re.findall(r'["](.*?)["]', line)
            for i in redirectTitle:
                locals()[f'item_{numTitle}']['redirects'].append(i)
        
        # Start add keywords to item (using at most 30 lines)
        if title != '':
            if cnt < 30:
                keywords = re.findall(r'[[[](.*?)[]]]', line)
                # fliter
                for i in keywords:
                    i = i[1:]
                    if i.find(':')>0 or i.find('.')>0 or i.find('[')>0 or i.find(',')>0:
                        continue
                    else:
                        if i.find('|')>0:
                            i = i[:i.find('|')]
                        locals()[f'item_{numTitle}']['keywords'].append(i)
                cnt = cnt+1
    file.close()

    # Open the next file to add keywords
    if cnt < 30 and num + 1 <= 622:
        file = open(f"enwiki-latest-pages-articles_{num + 1}.xml",'r',encoding="utf-8") 
        for line in file:
            if line.find('<title>') > 0 and line.find('</title>') > 0: 
                break

            # Find redirect
            if line.find('<redirect title') > 0:
                redirectTitle = re.findall(r'["](.*?)["]', line)
                for i in redirectTitle:
                    locals()[f'item_{numTitle}']['redirects'].append(i)

            if cnt < 30:
                keywords = re.findall(r'[[[](.*?)[]]]', line)
                # fliter
                for i in keywords:
                    i = i[1:]
                    if i.find(':')>0 or i.find('.')>0 or i.find('[')>0 or i.find(',')>0:
                        continue
                    else:
                        if i.find('|')>0:
                            i = i[:i.find('|')]
                        locals()[f'item_{numTitle}']['keywords'].append(i)
                cnt = cnt+1
        file.close()

    # Save json
    json_str = json.dumps(fold, indent=4)
    with open(f'output_data_{num}.json', 'w',encoding="utf-8") as json_file:
        json_file.write(json_str)



def T(index):
    numTurn = 0
    while(index + numTurn * 8 <=622):
        Print(index + numTurn * 8)
        print(index + numTurn * 8)
        numTurn = numTurn + 1

if __name__ == "__main__":
    
    threads = []
    for x in range(8):
        thread = Thread(target=T, args=(x+1,))   
        thread.start()   
        threads.append(thread)

    for thread in threads:
        thread.join()   
    '''
    Print(56)
    '''