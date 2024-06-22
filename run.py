#!/usr/bin/env python
# coding : utf-8

"""
    Flask App : URL Shortner
"""

from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
