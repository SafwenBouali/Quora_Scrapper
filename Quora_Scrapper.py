import requests
from bs4 import BeautifulSoup
import urllib
import time
import datetime
import uuid
import random

__WaitTime = 6.0
__RequestQueue = []
__headers = """nothing to show here ... you need to find this yourself ;) """

def bypass_limitation(url):

    suffixe = "share=1"
    if ('?' in url):
        suffixe = '&' + suffixe
    else:
        suffixe = '?' + suffixe
    return suffixe        


def make_query_url(query, query_type='topic',bypass_limit=True):

    if (query==None or query==''):
        raise ValueError("bad query : empty or null.")
    if (query_type not in ['topic','question','answer']):
        raise ValueError(
            "query_type must be in"
            + "['topic','question','answer'].")
    url = ('https://www.quora.com/search?q='
            + urllib.quote_plus(query)
            + '&type='
            + query_type)
    if(bypass_limit):
        url = bypass_limitation(url)
    return url


def get_response_item_list(html):
    
    soup = BeautifulSoup(html,"html.parser")
    _list = soup.find(
        'div'
        ,class_ = 'QueryResultsList PagedList'
    ).findAll(class_='pagedlist_item')
    if (len(_list)==0):
        return None
    else:
        return _list


def send_request(url,headers=None):

    if (headers is None):
        headers = __headers
    #generate unique id
    requestID = str(uuid.uuid1())
    print  requestID + '%%%request enqued'
    #enqueue id
    __RequestQueue.append(requestID)
    #wait until id is 0 index
    while (__RequestQueue.index(requestID) != 0):
        time.sleep(random.random())
    #wait time for scrap detection
    print  requestID + '%%%scrap avoid sleep'
    temp_waitTime = (
        (__WaitTime*0.65)
        + random.random()*(__WaitTime*0.35)
    )
    time.sleep(temp_waitTime)
    print requestID + '%%%exec'
    #execute
    session = requests.Session()
    response = session.get(url, headers=headers,timeout=5)
#   response = requests.get(url, headers=headers,timeout=5)
    #dequeue
    __RequestQueue.remove(requestID)
    print requestID + '%%%dequeue'
            #return 
    soup = BeautifulSoup(
        response.content,
        "html.parser"
    )
    return response,soup
