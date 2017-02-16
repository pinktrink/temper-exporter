import argparse
import ipaddress
import wsgiref.simple_server

import prometheus_client

from . import wsgiext

def main():
    '''
    You are here.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--bind-address', type=ipaddress.ip_address, default='::', help='IPv6 or IPv4 address to listen on')
    parser.add_argument('--bind-port', type=int, default=9203, help='Port to listen on')
    parser.add_argument('--bind-v6only', type=int, choices=[0, 1], help='If 1, prevent IPv6 sockets from accepting IPv4 connections; if 0, allow; if unspecified, use OS default')
    parser.add_argument('--thread-count', type=int, help='Number of request-handling threads to spawn')
    args = parser.parse_args()

    server = wsgiext.Server((args.bind_address, args.bind_port), wsgiref.simple_server.WSGIRequestHandler, args.thread_count, args.bind_v6only)
    server.set_app(prometheus_client.make_wsgi_app())
    server.serve_forever(poll_interval=600)
