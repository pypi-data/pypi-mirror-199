from urllib import parse

def buildUrl(url1:str,url2:str)->str:
    return parse.urljoin(url1, url2)