#!/usr/bin/env python

import logging

class Storage():
    __storage = {}
    
    def __init__(self):
        logging.info("simple storage initting")

    def set(self, key, val):
        self.__storage[key] = val;
        return True

    def get(self, key):
        if key in self.__storage:
            return self.__storage[key]
        return None

    def reverseLookup(self, key, arg):
        ret = []
        for i in self.__storage:
            if key in self.__storage[i]:
                if self.__storage[i][key] == arg:
                    ret.append(i)

        return ret            

        
    def delete(self, key):
        if key in self.__storage:
            del self.__storage[key]
            return True
        return False
    
#     def getSubscribers(self, topic):
#         if self.__storage.get(topic):
#             return self.__storage[topic]
#         else:
#             None

#     def getTopics(self):
#         return self.__storage.keys()


#     def setSubscriber(self, topic, subscriber):
#         # TODO: validation
#         if topic in self.__storage:
#             if subscriber not in self.__storage[topic]:
#                 self.__storage[topic] += [subscriber]
#             return None
#         else:
#             self.__storage[topic] = [subscriber]
#             return topic

#     def deleteSubscriber(self, topic, subscriber):
#         if topic in self.__storage:
#             self.__storage[topic] = filter(lambda x: x != subscriber, self.__storage[topic])
#             return self.__storage[topic]
#         else:
#             return []
    
# #         if len(self.__storage[topic]):
# #             return True
# #         else:
# #             del self.__storage[topic]
# #             return False

#     def deleteAll(self):
#         self.__storage = {}
#         return True

    
def main():
    pass
#     print "storage"
#     logging.info("storage")
#     obj = SimpleStorage()
#     obj.setSubscriber(topic="foo", subscriber="bar")
#     obj.setSubscriber(topic="foo", subscriber="baz")
#     obj.setSubscriber(topic="foo", subscriber="fizz")
#     print obj.getSubscribers('foo')
#     obj.deleteSubscriber('foo', 'baz')
#     print obj.getSubscribers('foo')
#     obj.deleteSubscriber('foo', 'bazbaz')
#     print obj.getSubscribers('foo')
    
if __name__ == "__main__":
    main()
