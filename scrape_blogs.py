#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import time
import sys

try:
    # get page
    p = "https://www.shadecoder.com/blogs"
    print(f"Fetching {p}...")
    r = requests.get(p, timeout=10)
    s = BeautifulSoup(r.content, 'html.parser')
except Exception as e:
    print(f"ERROR: Failed to fetch blogs page")
    print(f"Details: {str(e)}")
    print("\nMake sure:")
    print("- You have an internet connection")
    print("- shadecoder.com is accessible")
    print("- The website is not blocked")
    input("\nPress Enter to exit...")
    sys.exit(1)

# find urls
urls = []
for a in s.find_all('a'):
    href = a.get('href')
    if href and './blogs/' in href:
        url = "https://www.shadecoder.com" + href.replace('./', '/')
        urls.append(url)

# remove dups
final = []
for link in urls:
    if link not in final:
        final.append(link)

print(f"Got {len(final)} urls")
results = []

for idx in range(len(final)):
    u = final[idx]
    print(f"[{idx+1}/{len(final)}]")

    try: 
        resp = requests.get(u, timeout=10)
        page = BeautifulSoup(resp.content, 'html.parser')
    except:
        continue

    # title 
    t = page.find('h1')
    title = ""
    if t:
        title = t.get_text(strip=True)

    
    if title == "":
        h2 = page.find('h2')
        if h2:
            title = h2.get_text(strip=True)

    if title == "":
        title = "notitle"

    
    # content 
    art = page.find('article')
    cont = ""
    if art : 
        cont = art.get_text(separator=' ', strip=True)
    else:
        m = page.find('main')
        if m : 
            cont = m.get_text(separator=' ', strip=True)
        else : 
            b = page.body 
            if b : 
                cont = b.get_text(separator=' ', strip=True)
    
    # desc 
    meta = page.find('meta', attrs={'name': 'description'})
    desc = ""
    if meta : 
        d = meta.get('content')
        if d:
            desc = d

    # headings 
    heads = []
    for h in page.find_all(['h1', 'h2', 'h3', 'h4']):
        lv = h.name
        tx = h.get_text(strip=True)
        heads.append({'level' : lv, "text" : tx})

    # toc
    toc_str = ""
    for hd in heads : 
        lnum = int(hd['level'][1])
        ind = "  " * (lnum - 1)
        toc_str = toc_str + f"{ind}- {hd['text']}\n"

    # get code blocks from page 
    codes = []
    code_blocks = page.find_all('code')
    for code_block in code_blocks:
        code_text = code_block.get_text()
        # only grab code if its not tiny 
        if len(code_text) > 20:
            code_obj = {
                'type' : 'code',
                'content' : code_text[:500]
            }
            codes.append(code_obj)

    # also grab pre blocks
    pre_blocks = page.find_all('pre')
    for pre_block in pre_blocks:
        pre_text = pre_block.get_text()
        if len(pre_text) > 20:
            pre_obj ={
                'type' : 'pre',
                'content' : pre_text[:1000]
            }
            codes.append(pre_obj)

    # scrape all external links 
    links = []
    all_links = page.find_all('a', href=True)
    for link in all_links:
        link_href = link['href']
        link_text = link.get_text(strip = True)
        # make sure it's a real external link
        if link_href.startswith('http'):
            link_entry ={
                'url' : link_href,
                'text' : link_text[:100]
            }
            links.append(link_entry)

    # check for keywords in content
    keywords_to_check = ['interview', 'coding', 'leetcode', 'hackerrank', 'assessment', 'python', 'java', 'javascript', 'sql', 'algorithm', 'graph', 'dp', 'dynamic programming', 'string', 'array', 'detection', 'cheating', 'proctoring', 'aws', 'google', 'amazom', 'meta', 'faang']
    topics = []
    content_lower = cont.lower()
    for keyword in keywords_to_check:
        keyword_lower = keyword.lower()
        if keyword_lower in content_lower :
            # don't add duplicates 
            if keyword not in topics :
                topics.append(keyword)

    # calculate how many words 
    word_count = len(cont.split())

    # create the data dict
    entry = {}
    entry['url'] = u
    entry['title'] = title
    entry['description'] = desc
    entry['preview'] = cont[:500]
    entry['content'] = cont[:5000]
    entry['headings'] = heads
    entry['toc'] = toc_str
    entry['codes'] = codes
    entry['links'] = links
    entry['topics'] = topics
    entry['words'] = word_count

    # save and wait a bit so we don't hammer the server 
    results.append(entry)
    time.sleep(0.5)

# how many did we get in total
num_results = len(results)
print("got results: " + str(num_results))

# dump everything to json file
result_json = json.dumps(results, indent=2)
# print(results_json[:100]) # debug print 
knowledge_file = open('advanced_knowledge.json', 'w')
knowledge_file.write(result_json)
knowledge_file.close()

# will get the text backup later but for now just json 
# build a map of topics to article titles 
topic_map = {}
for res in results:
    article_topics = res['topics']
    for topic in article_topics:
        if topic in topic_map:
            # we already have this topic add the title to the list 
            topic_map[topic].append(res['title'])
        else :
            # first time seeing this topic, create list
            topic_map[topic] = [res['title']]


# now save the topic map as json 
topic_json = json.dumps(topic_map, indent=2)
topic_file = open('topic_index.json', 'w')
topic_file.write(topic_json)
topic_file.close()
print("topics done")

# write markdown file with all the info 
# open file for writing 
md_output = open('advanced_knowledge.md', 'w')

# write header
md_output.write("# Knowledge Base\n\n")
total_blogs = len(results)
md_output.write("Blogs: " + str(total_blogs) + "\n\n")

# go through each result and write it 
counter = 1 
for result in results : 
    result_title = result['title']
    result_url = result['url']
    result_words = result['words']
    result_desc = result['description']
    result_toc = result['toc']
    result_codes = result['codes']
    result_links = result['links']
    result_preview = result['preview']
    result_topic = result['topics']


    # write title and url
    md_output.write("## " + str(counter) + ". " + result_title + "\n\n")
    md_output.write("URL : " + result_url + "\n\n")
    md_output.write("Words: " + str(result_words) + "\n\n")
    
    # write topics if we found any
    if len(result_topic) > 0:
        topics_list = ""
        for topic in result_topic :
            topics_list += topic + ", "
        topics_list = topics_list.rstrip(", ")
        md_output.write("Topics: " + topics_list + "\n\n")

    # add the table of contents section 
    toc_check = result_toc and len(result_toc) > 0
    if toc_check:
        md_output.write("Table of Contents:\n")
        md_output.write("```\n")
        md_output.write(result_toc)
        md_output.write("\n```\n\n")

    
    # check if there are code samples and add them 
    if result_codes:
        if len(result_codes) > 0:
            how_many_codes = len(result_codes)
            md_output.write("Code Samples Found: " + str(how_many_codes) + "\n\n")
            for each_code_sample in result_codes:
                code_content_text = each_code_sample['content']
                truncated_code = code_content_text[:200]
                md_output.write("```\n")
                md_output.write(truncated_code)
                md_output.write("\n```\n\n")

    # add external links if the article has any
    if result_links:
                if len(result_links) > 0:
                    md_output.write("External Links:\n")
                    for each_link in result_links:
                        current_link_url = each_link['url']
                        current_link_text = each_link['text']
                        md_output.write("- ")
                        md_output.write(current_link_text)
                        md_output.write(" (")
                        md_output.write(current_link_url)
                        md_output.write(")\n")
                    md_output.write("\n")

    # put preview section before divider
    md_output.write("Preview:\n")
    md_output.write(result_preview)
    md_output.write("\n\n")
    # horizontal line to seperate entries
    md_output.write("---\n\n")

    # increment for next iteration 
    counter = counter + 1 

# close the file when done with the loop 
md_output.close()
print("\n" + "="*50)
print("FINISHED SUCCESSFULLY!")
print("="*50)
print(f"\nGenerated files:")
print(f"  - advanced_knowledge.json ({num_results} blogs)")
print(f"  - topic_index.json ({len(topic_map)} topics)")
print(f"  - advanced_knowledge.md")
print("\nAll files saved to current directory.")
input("\nPress Enter to exit...")
sys.exit(0)