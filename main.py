# -*-coding:utf-8 -*-
__author__ = 'longqi'
'''
sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8000
'''
import os
import threading
import json
from pprint import pprint
import time
import copy

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from main.main_function import info_loop
from configuration import hosts_info
from configuration import threshold


define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # greeting = self.get_argument('name', default='Hello ')
        # self.write(greeting + ', friendly user!')
        self.redirect('/dashboard')


class DashboardHandler(tornado.web.RequestHandler):
    def get(self):
        # pprint(hosts_info)
        self.render('dashboard.html', hosts_info=hosts_info)


class UpdateDataHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        interval = self.get_argument('interval', default=5)

        # new dictionary
        response_to_send = copy.deepcopy(hosts_info)
        # ************
        for host in hosts_info:
            # print(host, type(hosts_info[host][2]), hosts_info[host][2])
            if time.time() - hosts_info[host][2].timestamp() < threshold:
                # if the difference between record time and time now is less than 5, then it's in normal condition
                hosts_info[host][3] = 0
            else:
                hosts_info[host][3] = -1
            # format the datetime to string for JSON sending
            response_to_send[host][2] = response_to_send[host][2].strftime('%Y-%m-%d %a %H:%M:%S')
            # print(response_to_send[host][2])

        # ************
        # print('Response to return')

        # pprint(response_to_send)

        self.write(json.dumps(response_to_send))


t1 = 1


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        global t1
        print('Test handler:', t1)
        # new dictionary
        t1 += 1
        response_to_send = {'newkey': t1}
        self.write(json.dumps(response_to_send))


if __name__ == '__main__':
    info_thread = threading.Thread(target=info_loop, args=())
    info_thread.start()

    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/dashboard', DashboardHandler),
            (r'/test/', TestHandler),
            (r'/updateData/', UpdateDataHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        debug=True
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
