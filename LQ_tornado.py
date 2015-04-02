# -*-coding:utf-8 -*-
__author__ = 'longqi'
'''
sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8000
'''
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('name', default='Hello ')
        self.write(greeting + ', friendly user!')


class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        greeting = self.get_argument('name', default='Hello ')
        text = self.get_argument('text', default='...')

        import textwrap
        self.write(greeting + ', friendly user!'+textwrap.fill(text=text, width=20))

if __name__ == "__main__":
    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/wrap", WrapHandler)
        ]
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
