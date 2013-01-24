#!/usr/bin/python
# -*- coding: utf-8 -*-
import nltk   
import urllib2
import urllib
import json
import cStringIO

def google_links(query, n):
    """returns first n links from google.com"""
    def offset_search(offset):
        opts = urllib.urlencode({'q': query, 'start': offset})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&{0}'
        url = url.format(opts)
        search_results = urllib2.urlopen(url).read()
        results = json.loads(search_results)
        return [urllib2.unquote(x['url']) for x in results['responseData']['results']]
    return [subsub for sub in map(offset_search, range(0, n, 4)) for subsub in sub][:n]

def google_search(query, n):
    """returns n joined sites for a given query using google.com"""
    def read_link(link):
        req = urllib2.Request(link, headers={'User-Agent' : 'Kennedy Browser'})
        response = urllib2.urlopen(req)
        raw = response.read()
        escaped = nltk.clean_html(raw)
        return urllib2.unquote(escaped)
    links = google_links(query, n)
    fs = cStringIO.StringIO()
    for link in links:
        fs.write(read_link(link))
    return fs.getvalue()

