# -*- coding: utf-8 -*-


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    body = '<h1>Hello, {0}!</h1>'.format(environ['PATH_INFO'][1:] or 'web')
    return [body.encode('utf-8')]
