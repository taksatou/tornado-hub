#!/usr/bin/python

import urllib
import hashlib
import random
import logging

SubscriberRequired = ['hub.callback', 'hub.mode', 'hub.topic', 'hub.verify']
SubscriberOptional = ['hub.lease_seconds', 'hub.secret', 'hub.verify_token']
VerifyRequired = ['hub.mode', 'hub.topic', 'hub.challenge']
VerifyOptional = ['hub.lease_seconds', 'hub.verify_token']

def validSubRequest(**args):
    for k in SubscriberRequired:
        if not k in args:
            return False
    return True

def validUnsubRequest(*args):
    for k in SubscriberRequired:
        if not k in args[i]:
            return False
    return True

class Subscribe:
    def __init__(self, storage, **kwargs):
        '''load subscriber's info'''
        if not validSubRequest(**kwargs):
            raise

        self.args = {}
        for i in SubscriberRequired:
            self.args[i] = kwargs[i]
            
        for i in SubscriberOptional:
            if i in kwargs:
                self.args[i] = kwargs[i]

        self.storage = storage

    def diff_state(self):
        '''whether the operation will change the state'''
        return True

    def commit_state(self):
        '''commit the change'''
        logging.info('new subscriber>> callback: %s, topic: %s', self.args['hub.callback'], self.args['hub.topic'])
        pass

    def get_verification_info(self):
        h = hashlib.md5()
        h.update(str(random.random()))
        self.challenge = h.hexdigest()
        params = {'hub.mode': self.args['hub.mode'],
                  'hub.topic': self.args['hub.topic'],
                  'hub.challenge': self.challenge}

        url = self.args['hub.callback'] + '?' + urllib.urlencode(params)
        return (self.args['hub.verify'], url, {})

    def verify_response(self, response):
        if response == self.challenge:
            return True
        else:
            return False
        
    
    def do(self):

#             if self.sub.verify == 'sync':
#                 http = tornado.httpclient.AsyncHTTPClient()
#                 self.sub.do_sync()
                
#             elif self.sub.verify == 'async':
#                 self.sub.do_sync()
#                 logging.warn('async mode in not implemented')
#                 raise tornado.web.HTTPError(401)
#             else:
#                 logging.warn('fialed subscribe')
#                 raise tornado.web.HTTPError(400)


        
        pass

class Unsubscribe:
    def __init__(self):
        pass

    def do(self):
        pass
   

    
def main():
    pass

if __name__ == "__main__":
    main()

