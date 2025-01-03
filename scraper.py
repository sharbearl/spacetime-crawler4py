import re
from tokenizer import TokenCounter, tokenize
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def get_word_count(url, resp):
    # same kinda thing going on
    if resp.status != 200:
        return 0
    content = BeautifulSoup(resp.raw_response.content, "lxml")
    if is_valid(url) and is_worth_scraping(url, resp):
        return len(content.getText().split())
    return 0

def get_word_frequencies(url, resp):
    if resp.status != 200:
        return TokenCounter()
    content = BeautifulSoup(resp.raw_response.content, "lxml")
    if is_valid(url) and is_worth_scraping(url, resp):
        ret = TokenCounter()
        ret.addTokensFromList(tokenize(content.getText()))
        return ret
        
    return TokenCounter()


def is_worth_scraping(url, resp):
    if resp.status != 200:
        print("Status code:", resp.status,"| Error Message:", resp.error)
        return False
    content = BeautifulSoup(resp.raw_response.content, "lxml")
    # New specification!
    if len(content.getText().split()) <= 200:
        print("Low information page:", url)
        return False
    return True

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    if not is_worth_scraping(url, resp):
        return list()
    content = BeautifulSoup(resp.raw_response.content, "lxml")
    atags = content.select('a[href]')
    # I wanna use a list comprehension so bad but I shouldn't
    # (I did it anyway)
    return [atag['href'] for atag in atags]


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        # print("is_valid URL IS:",url)
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        regMatch = not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|jpg|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|ppsx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
        if not regMatch:
            return False
        validPaths = set(["ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu", "today.uci.edu/department/information_computer_sciences"])
        # bannedQueries = set(["eventDisplay=day&eventDate=2024"])
        datePattern = r"\b\d{4}-\d{2}\b"
        matchQuery = re.search(datePattern, parsed.query)
        matchPath = re.search(datePattern, parsed.path)
        if matchQuery or matchPath:
            return False
        if "filter" in parsed.query or "ical" in parsed.query or "download" in parsed.query or "login" in parsed.query:
            return False
        if "share=" in parsed.query:
            return False
        if "/uploads" in parsed.path:
            return False
        if len(parsed.fragment) > 0:
            return False
        if parsed.hostname == "" or parsed.hostname == None:
            return False
        isValidPath = False
        for path in validPaths:
            if ("." + path) in parsed.hostname.lower():
                isValidPath = True
                break
            if ("/" + path ) in parsed.hostname.lower():
                isValidPath = True
                break
        if not isValidPath:
            return False
        # obeying informatics robots.txt
        if "informatics.uci.edu" in parsed.hostname.lower():
            allowedDomains = {
                "/wp-admin/admin-ajax.php",
                "/research/labs-centers/",
                "/research/areas-of-expertise/",
                "/research/example-research-projects/",
                "/research/phd-research/",
                "/research/past-dissertations/",
                "/research/masters-research/",
                "/research/undergraduate-research/",
                "/research/gifts-grants/"
            }
            for allowedDomain in allowedDomains:
                if parsed.path.startswith(allowedDomain):
                    return True
            if parsed.path.startswith('/wp-admin') or parsed.path.startswith('/research'):
                return False
            return True # other pages should be fine?
        # nothing specificed for:
        # ics.uci.edu
        # cs.uci.edu
        if 'ics.uci.edu' in parsed.hostname or 'cs.uci.edu' in parsed.hostname:
            return True
        # obeying robots.txt for stat.uci.edu
        if 'stat.uci.edu' in parsed.hostname:
            if parsed.path.startswith("/web-admin/admin-ajax.php"):
                return True
            return not parsed.path.startswith("/wp-admin")
        if 'today.uci.edu' in parsed.hostname:
            return not parsed.path.startswith("/iseb")

        return False
        

    except TypeError:
        print ("TypeError for ", parsed)
        raise
