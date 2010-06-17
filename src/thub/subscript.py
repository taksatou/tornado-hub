#!/usr/bin/env python

import logging
import storage
import pika
import asyncore

class Subscript():
    __storage = None
    __topics = []
    
    def __init__(self, storage=storage.SimpleStorage()):
        logging.info("sub initting")
        self.__storage = storage
        self.__topics = self.__storage.getTopics()
        # TODO
        # register all subscribers

    def update(self, topic, callback, mode):
        if mode == 'subscribe':
            return self.__addSubscriber(topic, callback)                
        elif mode == 'unsubscribe':
            return self.__deleteSubscriber(topic, callback)
        else:
            return False
            
    def __addSubscriber(self, topic, callback):
        # TODO: use pika
        try:
            new_topic = self.__storage.setSubscriber(topic, callback)
            if new_topic:
                self.__topics += [topic]
            return True
        except:
            print 'sub add error'
            raise

    def __deleteSubscriber(self, topic, callback):
        try:
            subscribers = self.__storage.deleteSubscriber(topic, callback)
            if not subscribers:
                self.__topics = filter(lambda x: x != topic, self.__topics)
            return True
        except:
            print 'sub delete error'
            raise

    def dumpSubscribers(self, *topics):
        if not topics:
            topics = self.__storage.getTopics()

        for i in topics:
            print '--- <%s> subscribers:' % i
            print self.__storage.getSubscribers(i)

    def dumpTopics(self):
        print '--- topics'
        print self.__topics
        

def main():
    logging.error("sub")
    obj = Subscript()
    obj.update("foo", "callback", 'subscribe')
    obj.update("foo", "callback1", 'subscribe')
    obj.update("foo", "callback1", 'subscribe')
    obj.update("foo", "callback1", 'subscribe')
    obj.update("foo", "callback1", 'subscribe')
    obj.update("bar", "callback1", 'subscribe')
    obj.dumpSubscribers()
    obj.dumpTopics()
    print '======='
    obj.update("foo", "callback1", 'unsubscribe')
    obj.update("bar", "callback1", 'unsubscribe')
    obj.update("bar", "callback1", 'unsubscribe')
    obj.update("bar", "callback1", 'unsubscribe')
    obj.update("barbas", "callback1", 'unsubscribe')
    obj.update("barbas", "callba", 'unsubscribe')
    obj.dumpSubscribers()
    obj.dumpTopics()



if __name__ == "__main__":
    main()
