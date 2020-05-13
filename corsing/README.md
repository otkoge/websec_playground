
# Simple app to test CORS requests

## To run the victim server
flask run
http://127.0.0.1:5000

## To run attack server
cd attack
python -m http.server

http://127.0.0.1:8000


# Ceveats

Please note that secure cookies will not work over http (per definition).

## Same site cookie considerations
Cookies shared across ports on the same host. To test the behaviour of same site cookies use localhost for on of the servers.
