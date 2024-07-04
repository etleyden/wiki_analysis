import json
import mwparserfromhell as mwp
import re
# find the n most frequent elements in an array
from collections import Counter
import heapq

with open("config.json", "r") as config_file:
    conf = json.load(config_file)
    print(conf)

PAGE = re.compile(r"<page>[\s\S]+?<\/page>")
TITLE = re.compile(r"<title>(.*)<\/title>")
PAGE_TEXT = re.compile(r"<text[\s\S]*?>([\s|\S]*)?<\/text>")
DOUBLE_BRACKETS = re.compile(r"{\s?{[\S|\s]*}\s?}") # matches any {{[useless wikicode]}} that may be leftover
HTML_TAGS = re.compile(r"<\/?[a-z]+(\s[a-z]*=\"?[a-zA-Z0-9]*\"?)*\s?\/?>")
NLTK_STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 
'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 
'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 
'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 
'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 
's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 
'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
 "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 
'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

# reads `chunk_size` megabytes from the wikidump given by `wiki_fname`. 
# if `outfile` is specified, the processed chunks are written to a file.
# returns the chunks TODO: write pages to shared memory so a separate process can parse them into page objects
def read_chunks(wiki_fname: str, chunk_size: int, outfile: None):
    with open(wiki_fname) as raw_wiki_data:
        chunk = ""
        chunk += raw_wiki_data.read(chunk_size * 1024 * 1024) 
        res = PAGE.finditer(chunk, re.MULTILINE)

        last_match = 0
        for match in res:
            page = chunk[match.start():match.end()]

            print(page) # ADD THIS TO THE MESSAGE QUEUE

            if outfile:
                with open(outfile, "w") as of:
                    of.write(page)

            last_match = match.end()
        
        chunk = chunk[match.end():]

class Page():
    def __init__(self, title: str, links: list[str], top_words: list[str]):
        self.title = title
        self.links = links
        self.top_words = top_words

# parses the XML dump text for ONE page (matches <page>(.*)</page>)
# returns a Page object
def parse_text(text: str) -> Page:
    
    # get the title TODO: this could probably be one line
    title = TITLE.search(text)
    if title:
        title = title.group(1)

    # clean the text for some statistical analysis about word frequencies
    # grab everything in the <text></text> tags
    page_text = PAGE_TEXT.search(text)
    if page_text:
        # shave off most of the wikicode
        page_text = mwp.parse(page_text.group(1))
        page_text = page_text.strip_code()
        # remove all {{wikicode}}
        page_text = DOUBLE_BRACKETS.sub("", page_text)
        # remove all <ref>, <sub>, etc
        page_text = HTML_TAGS.sub("", page_text)
        # remove all punctuation and make everything lowercase. Split into an array
        page_text = re.sub(r'[^\w\s]','',page_text).lower().split()

        # remove stopwords
        set_stopwords = set(NLTK_STOPWORDS)
        page_text = [x for x in page_text if x not in set_stopwords]
        # Count the N most frequent elements (n=10)
        count = Counter(page_text)
        most_common = heapq.nlargest(10, count.items(), key=lambda x:x[1])
        most_common = [item for item, freq in most_common]
        print(most_common)

# takes a title of a wikipedia page and computes the URL ending
# returns the URL as a string
def get_url_ending(title: str) -> str:
    # turn spaces into underscores

    pass

if __name__ == "__main__":
    #read_chunks(conf["wikidump"], conf["chunk_size"], conf["output"])
    with open(conf["output"]) as test_f:
        test_str = test_f.read()
        parse_text(test_str)