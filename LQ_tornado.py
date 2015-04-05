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
import os.path

define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # greeting = self.get_argument('name', default='Hello ')
        # self.write(greeting + ', friendly user!')
        self.redirect('/dashboard')


class DashboardHandler(tornado.web.RequestHandler):
    def get(self):
        hosts_info = [['B1', '10.0.25.1', 2, 3],
                      ['B2', '10.0.25.2', 2, 3],
                      ['B3', '10.0.25.3', 2, 3],
                      ]
        self.render('dashboard.html', hosts_info=hosts_info)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/dashboard', DashboardHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        debug=True
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
