[![Build Status](https://travis-ci.org/mdtomo/wispysvr.svg?branch=master)](https://travis-ci.org/mdtomo/wispysvr)[![Coverage Status](https://coveralls.io/repos/github/mdtomo/wispysvr/badge.svg?branch=master)](https://coveralls.io/github/mdtomo/wispysvr?branch=master)
# Wispysvr - Flask web server for [wispy](https://github.com/mdtomo/wispy).

This is a flask web server backend for [wispy](https://github.com/mdtomo/wispy), built with SocketIO for viewing probe requests from wispy in real time. Wispysvr stores probe requests into a Mongodb database, which enables further insight into probe patterns and features token based authentication.

## Installing
```
pip install -r requirements.txt
```

## Testing
```
export APP_CONFIG=config.cfg
python -m unittest test.test_wispysvr
```
