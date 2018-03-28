from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = '''
                <html>
                <body>
                <h1>Hello!</h1>
                <form method="POST" action="/hello">
                    <label><h2>What would you like me to say?</h2>
                        <input name="message">
                    </label>
                    <button type="submit">Submit!</button>
                </form>
                </body>
                </html>
                '''

                self.wfile.write(output.encode())
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = '''
                <html>
                <body>
                <h1>Hola!</h1>
                <form method="POST" action="/hello">
                    <label><h2>What would you like me to say?</h2>
                        <input name="message">
                    </label>
                    <button type="submit">Submit!</button>
                </form>
                </body>
                </html>
                '''

                self.wfile.write(output.encode())
                return

        except IOError:
            self.send_error(404, 'file not found {}'.format(self.path))

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-length', 0))
            body = self.rfile.read(length).decode()
            params = parse_qs(body)
            print(params)

            output = '''
            <html>
            <body>
            <h2>Okay, how about this: </h2>
            <h1> {} </h1>
            <form method="POST" action="/hello">
                <label><h2>What would you like me to say?</h2>
                    <input name="message">
                </label>
                <button type="submit">Submit!</button>
            </form>
            </body>
            </html>
            '''

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(output.format(params['message'][0]).encode())

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), Handler)
        print('Server is running on port {}'.format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C entered, stopping the webserver')
        server.socket.close()


if __name__ == '__main__':
    main()
