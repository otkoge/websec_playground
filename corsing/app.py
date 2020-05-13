import random
import string
from flask import Flask, jsonify, request, make_response, render_template

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH', 'RANDOM']

cases = {
        'nocors': {'headers': []},
        'nocors_creds': {'headers': [
                                     {'header': 'Access-Control-Allow-Credentials', 'value': 'true'}
                                    ]},
        'null': {'headers': [
                             {'header': 'Access-Control-Allow-Origin', 'value': 'null'},
                             {'header': 'Access-Control-Allow-Methods', 'value': ', '.join(HTTP_METHODS)},
                            ]},
        'null_creds': {'headers': [
                             {'header': 'Access-Control-Allow-Origin', 'value': 'null'},
                             {'header': 'Access-Control-Allow-Credentials', 'value': 'true'},
                             {'header': 'Access-Control-Allow-Methods', 'value': ', '.join(HTTP_METHODS)},
                            ]},
        'wildcard': {'headers': [
                                    {'header': 'Access-Control-Allow-Origin', 'value': '*'},
                                    {'header': 'Access-Control-Max-Age', 'value': '0'},
                                    {'header': 'Access-Control-Allow-Methods', 'value': ', '.join(HTTP_METHODS)},
                                ]
                    },
        'wildcard_creds': {'headers': [
                                       {'header': 'Access-Control-Allow-Origin', 'value': '*'},
                                       {'header': 'Access-Control-Max-Age', 'value': '0'},
                                       {'header': 'Access-Control-Allow-Methods', 'value': ', '.join(HTTP_METHODS)},
                                       {'header': 'Access-Control-Allow-Credentials', 'value': 'true'},
                                      ]
                          },
        'reflected': {'headers': [
                                    {'header': 'Access-Control-Max-Age', 'value': '0'},
                                    {'header': 'Access-Control-Allow-Methods', 'value': ', '.join(HTTP_METHODS)},
                                 ],
                      'reflected': True,
                     },
        'reflected_creds': {'headers': [
                                        {'header': 'Access-Control-Max-Age', 'value': '0'},
                                        {'header': 'Access-Control-Allow-Credentials', 'value': 'true'},
                                        {'header': 'Access-Control-Allow-Methods', 'value': ', '.join(HTTP_METHODS)},
                                       ],
                      'reflected': True,
                     },
        }


app = Flask(__name__)

@app.route('/<case>', methods=HTTP_METHODS)
def case_router(case):
    origin = request.headers.get('origin')
    if case not in cases.keys():
        case = 'nocors'
    reflected = cases[case].get('reflected', False)
    token = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)])
    cookie = request.headers.get("Cookie")
    response = jsonify({'cookies': cookie})
    response.headers.add('X-Access-Token', token)
    response.set_cookie('simple', token)
    for header in cases[case]['headers']:
        response.headers.add(header['header'], header['value'])
    if reflected:
        response.headers.add('Access-Control-Allow-Origin', origin)
    return response


@app.route('/', methods=HTTP_METHODS)
def index():
    response = make_response(render_template('index.html'), 200)
    token = 'ASDQWE'
    response.set_cookie('samesite_none_secure', token, samesite='None', secure=True);
    response.set_cookie('samesite_none', token, samesite='None');
    response.set_cookie('samesite_lax_secure', token, samesite='Lax', secure=True);
    response.set_cookie('samesite_lax', token, samesite='Lax');
    response.set_cookie('samesite_strict_secure', token, samesite='Strict', secure=True);
    response.set_cookie('samesite_strict', token, samesite='Strict');
    return response

