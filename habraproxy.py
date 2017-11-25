import re
import urllib
import http.server
import shutil


class Proxy(http.server.BaseHTTPRequestHandler):
    target_host = 'http://habrahabr.ru'
    content = ''

    def set_content(self, content):
        content = re.sub(r'(<.*?>)(\s+)(<.*?>)', '\1 \2 \3', content)
        self.content = content

    def do_GET(self):
        url = self.target_host + self.path
        q = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(q)
            try:
                self.set_content(response.read().decode('utf-8'))
            except Exception:
                pass
            self.send_response(response.code)
            for resp_key, resp_value in response.getheaders():
                self.send_header(resp_key, resp_value)
            self.end_headers()
            self.wfile.write(bytes(self.content, "utf8"))
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.wfile.write(bytes(e.msg, "utf8"))
        return


def run(handler_class=http.server.BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    content = '<blockquote>алгоритм выработки сессионных ключей шифрования fds</blockquote>'
    content = re.sub(r'[a-zA-Zа-яА-Я0-9]{6,}', '\g<0>™', content)
    match = re.findall(r'([a-zA-Zа-яА-Я0-9]{6,})', content)
    content = re.sub(r'(>.*)([a-zA-Zа-яА-Я0-9]{6,})', '\g<1>\g<2>™', content)
    print(match)
    print(content)
    # run(handler_class=Proxy)
    # def get_ext_links(url):
    #     response = urllib.request.urlopen(url)
    #     html = response.read().decode('utf-8')
    #     url_parsed = urllib.parse.urlparse(url)
    #     return re.findall(r'href=[\'"]?(http[s]?://[www.]?[^%s][^\'">]+)' % url_parsed.netloc, html)
    #
    # ext_urls = get_ext_links('https://yandex.ru')
