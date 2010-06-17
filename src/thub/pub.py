#!/usr/bin/python

import socket
import urlparse
import urllib
import hashlib
import random
import logging

PublisherRequired = ['hub.mode', 'hub.url']

def validPubRequest(**kwargs):
    for k in PublisherRequired:
        if not k in kwargs:
            return False
    return True

class Publish:
    def __init__(self, storage, hub,  **kwargs):
        if not validPubRequest(**kwargs):
            raise        

        self.args = {}
        for i in PublisherRequired:
            self.args[i] = kwargs[i]

        self.storage = storage
        self.hub = hub
        self.topic = self.args['hub.url']
        self.subscribers = self.storage.reverseLookup('hub.topic', self.args['hub.url'])
        
        self.domains = {}       # TODO: use X-Hub-On-Behalf-Of
        for i in self.subscribers:
            p = urlparse.urlparse(i)
            if p[1] in self.domains:
                self.domains[p[1]] += 1
            else:
                self.domains[p[1]] = 1

        logging.info('pub: subscribers>>%s', self.subscribers)


    def new_contents(self, body):
        '''save modified date'''
        # TODO: check modification, generate atom:id
        return body

    def content_fetch_headers(self):
        '''make best practice headers'''
        
        headers = {}
        headers['User-Agent'] = 'tornado-hub' + ' (+%s; %d subscribers)' % (self.hub, len(self.subscribers))
        
        for i in self.domains:
            headers['User-Agent'] += ' (%s; %d subscribers)' % (i, self.domains[i])
                     
        return headers

    def content_distribute_headers(self):
        '''support atom only now'''
        return {'Content-Type': 'application/atom+xml'}


    def get_subscribers(self):
        return []
    
def main():
    import storage
    
    args = dict({'hub.mode': 'publish',
                 'hub.url': 'http://example.com'})
#     t =  urlparse.urlparse('http://example.com')
#     print t[1]
    
    obj = Publish(storage.Storage(), 'http://sui2.is-a-geek.net', **args)
    print obj.content_fetch_headers()

#    print gethubname()
#    print 'hgoe'
#    print socket.gethostname()
#    pass

if __name__ == "__main__":
    main()

