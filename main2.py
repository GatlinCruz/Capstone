"""
This file creates a PyWebView screen and displays the server using local host
Currently this is not being used
__author__: Gatlin Cruz
__author__: Cade Tipton
"""
import webview
import time

if __name__ == '__main__':
    webview.create_window('Capstone 1', 'http://127.0.0.1:8000/', resizable=True, background_color='#000')
    webview.start(http_server=True)
