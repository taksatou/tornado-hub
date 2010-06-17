#!/usr/bin/python

import logging
import tornado.escape
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.options
import tornado.web
import urllib
import time

import thub.sub
import thub.pub
from thub.storage import Storage
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        self.storage = Storage()
        handlers = [(r"/", MainHandler)]
        settings = {}
 
        tornado.web.Application.__init__(self, handlers, **settings)

def url2dict(str):
    decoded = urllib.unquote(str)
    r = {}
    for i in decoded.split('&'):
        kv = i.split('=')
        r[kv[0]] = kv[1]
    return r
    
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("this is my hub")

    def on_subscribe(self, response):
        if self.sub.verify_response(response.body):
            self.sub.commit_state()
        else:
            raise NotImplemented, 'asyc subscription retry is not implemented'

    def on_publish(self, response):        
        contents = self.pub.new_contents(response.body)
        headers = self.pub.content_distribute_headers()

        for i in self.pub.subscribers:
            http = tornado.httpclient.AsyncHTTPClient()
            kwargs = {'headers': headers,
                      'method': 'POST',
                      'body': contents}
            http.fetch(request=i, callback=self.async_callback(self.on_distribution), **kwargs)


    def on_distribution(self, response):
        '''retry is not implemented'''
        logging.info('successed distribution')
        
    
    @tornado.web.asynchronous
    def post(self):
        if self.request.headers.get('Content-Type') != 'application/x-www-form-urlencoded':
            raise tornado.web.HTTPError(415)

        body = url2dict(self.request.body)
        print body
        if 'hub.mode' not in body:
            raise tornado.web.HTTPError(400)
        else:
            mode = body['hub.mode']
            
        if mode == 'subscribe' or mode == 'unsubscribe':
            self.sub = thub.sub.Subscribe(storage=self.application.storage, **body)
                
            if not self.sub.diff_state():
                self.set_status(204)
                self.finish()
                return
            else:
                (verify_mode, callback, kwargs) = self.sub.get_verification_info()
                if verify_mode == 'async':
                    self.set_status(202)
                    self.finish()
                    http = tornado.httpclient.AsyncHTTPClient()
                    http.fetch(request=callback, callback=self.async_callback(self.on_subscribe), **kwargs)
                    return
                elif verify_mode == 'sync':
                    http = tornado.httpclient.HTTPClient()
                    response = http.fetch(request=callback, **kwargs)
                    logging.info(response.body)
                    if self.sub.verify_response(response.body):
                        self.sub.commit_state()
                        self.set_status(202)
                        self.finish()
                        return
                    else:
                        raise tornado.web.HTTPError(400)
                
        elif mode == 'publish':
            self.pub = thub.pub.Publish(storage=self.application.storage,
                                        hub='http://sui2.is-a-geek.net:8888', **body)
            self.set_status(204)
            self.finish()
             
            headers = self.pub.content_fetch_headers()
            http = tornado.httpclient.AsyncHTTPClient()
            http.fetch(request=self.pub.topic,
                       callback=self.async_callback(self.on_publish), headers=headers)

            return
        else:
            raise tornado.web.HTTPError(400)

        self.finish()


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
