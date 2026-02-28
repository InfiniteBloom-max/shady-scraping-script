# scrape_blogs.py 

A web scrapper that extracts blog posts from an intresting site I found shadecoder.com and generates a structured json file names as knowlegdge.json for later use.

Why read all the blogs when you can get a custom knowledge base ? 

Saves time and effort on reading 100+ blogs !

## what it does 

This script crawls the blog listing page, extracts all blog URLS (which we don't know before) , and then srpas each blog post page to collect these : 

- **Article metadata** : title , URL , word count , description 
- **Structure** : headings , table of contents
- **Content** : code blocks (from `<code>` and `<pre>` tags), text preview , full content 
- **Links** " external links found in articles
- **Topic** : keywords matching a predefined list (interview , coding , algorithm, ect.)

## Output files

The script generates three files:

1. **advanced_knowledge_base.json** - Complete structured data fro all articles
2. **topics_index.json** - Index mapping topics to article titles for quick lookup
3. **advanced_knowledge_base.md** - Formatted markdown file with all articles and their details 

## Requirements

- requests
- beautifulsoup4

To install the required packages, run the following command in your terminal:
```
pip install requests beautifulsoup4
```

## Usage 

You can simply run the script and look the magic happen!

```
python scrape_blogs.py
```

The script will :
1. Fetch all the blogs available on the site.
2. Extract unique blog URLs.
3. Crawl each blog (with 0.5s delay between requests to be respectful)
4. Parse, titles , content , headings , code samples , links
5. Detect relevant topics from keyword matching
6. Generate output files

The release is there as an EXE file to ease the process just have internet connection and run it.
(makesure to install and try it on windows its easy that way)


## Output format


### advanced_knowledge_base.json

Each article object contains : 
```json
{
    "url": "https://www.sbadecoder.com/blogs/...",
    "title" : "Article Title",
    "description" : "Meta description",
    "preview" : "First 500 chars of content",
    "content" : "First 5000 chars of content",
    "headings" : [{"level" : "h1" , "text" : "Heading"}, ...],
    "toc" : "Markdown table of contents",
    "codes" : [{"type" : "code|pre" , "content" : "code snippet"}, ...],
    "links" : [{"url" : "http://..." , "text" : "Link text"}, ...],
    "topic" : ["python" , "algorithm", ...],
    "words" : 1500
}

```
### topics_index.json

```json
{
    "python" : ["Article 1", "Article 2"],
    "algorithm" : ["Article 3"],
    ...
}
```


## Keyword detection 

The script automatically detects these topics from article content: 

interview , coding , leetcode , hackerrank , assesment , python , java, 
javascript , sql , algorithm , graph , dp , dynamic programming , string, array , detection , cheating , proctoring, aws, google , amazon , meta , faang

## Notes

- Requests incude a 10-second timeout 
- Duplicate URLs are removed from the crawl
- code snippets are limited to 500 chars (for `<code>`) or 1000 chars (for `<prev`)
- Failed requests are skipped silently 
- A 0.5 second delay is added between requests to avoid overwheliming the server ( and not being blacklisted if there is such a thing)
- Content preview is capped at 500 chars , full content at 5000 chars


## AI Use 
The whole project didnt use AI but used to generate the keywords from the content 
The keywords are generated using a simple keyword extraction algorithm that looks for common words and phrases in the content. It's not perfect but it's a good starting point.
Used to fix bugs in the code 
AI wasn't used for coding or any other task

## Path from here 
Hope to improve the project to support custom URL and custom keywords giving more accessibiliy to generate knowledge bases for any site !