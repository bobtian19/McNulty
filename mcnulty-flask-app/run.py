#!/usr/bin/env python
from __future__ import absolute_import
from app import app as application

if __name__ == '__main__':
    application.run(port=9000, debug=True)
