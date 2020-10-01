import webview
import time

if __name__ == '__main__':
    webview.create_window('Capstone 1', 'http://127.0.0.1:8000/', resizable=True, background_color='#000')
    webview.start(http_server=True)