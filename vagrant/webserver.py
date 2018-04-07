from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from database_setup import Restaurant, create_db_session


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # create new SQLAlcehmy session
                session = create_db_session()

                # query the database and get names of all the restaurants
                q = session.query(Restaurant.name, Restaurant.Id).all()
                sub_html = ''

                for r in q:
                    sub_html += '''<div>
                                      {0}
                                      <div>
                                        <a href="/restaurant/{1}/edit?name={0}&id={1}">Edit</a>
                                        <a href="/restaurants">Delete</a>
                                      </div>
                                    </div>'''.format(r[0], r[1])

                html_wrapper = '''
                <html>
                <head><title>Restaurants</title></head>
                <body>
                {0}
                </body>
                </html>
                '''

                mesg = html_wrapper.format(sub_html)
                self.wfile.write(mesg.encode())

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = '''
                <html>
                <body>
                <h1>New Restaurant Form</h1>
                <form method="POST" action="/restaurants/new">
                    <label><h2>Please enter the name of the new restaurant</h2>
                        <input name="message">
                    </label>
                    <button type="submit">Submit!</button>
                </form>
                </body>
                </html>
                '''

                self.wfile.write(output.encode())

            if self.path.find("/edit") != -1:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                parsed = urlparse(self.path)
                params = parse_qs(parsed.query)

                # create new SQLAlcehmy session
                session = create_db_session()

                # query the database and get names of all the restaurants
                q = session.query(Restaurant).filter(
                    Restaurant.name == params['name'][0],
                    Restaurant.Id == params['id'][0]).first()
                session.close()

                if q is None:
                    self.send_response(301)
                    self.send_header('Location', '/restaurants/edit_err')
                    self.end_headers()

                if q is not None:
                    output = '''
                    <html>
                    <body>
                    <h1>Edit Restaurant</h1>
                    <form method="POST" action="/restaurant/{1}/edit?name={0}&id={1}">
                        <label><h2>Please enter the new name for the restaurant</h2>
                            <input name="new_name">
                        </label>
                        <button type="submit">Submit!</button>
                    </form>
                    </body>
                    </html>
                    '''.format(params['name'][0], params['id'][0])

                    self.wfile.write(output.encode())

            if self.path.endswith("/restaurants/create_err"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = '''
                <html>
                <body>
                  <h1>Restaurant already exists!
                   Go back and try a different name.
                  </h1>
                </body>
                </html>
                '''

                self.wfile.write(output.encode())

        except IOError:
            self.send_error(404, 'file not found {}'.format(self.path))

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                length = int(self.headers.get('Content-length', 0))
                body = self.rfile.read(length).decode()
                params = parse_qs(body)
                print(params)
                print(self.path)

                # create new SQLAlcehmy session
                session = create_db_session()

                # query the database to verify restaurant doesnt exist
                q = session.query(Restaurant).filter_by(
                    name=params['message'][0]).first()
                session.close()

                if q is None:
                    self.send_response(201)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    session = create_db_session()

                    new_rest = Restaurant(name=params['message'][0])

                    session.add(new_rest)
                    session.commit()

                    output = '''
                    <html>
                    <body>
                    <h1>{} was added!</h1>
                    </body>
                    </html>
                    '''

                    self.wfile.write(output.format(
                        params['message'][0]).encode())

                if q is not None:
                    self.send_response(301)
                    self.send_header('Location', '/restaurants/create_err')
                    self.end_headers()

            if self.path.find("/edit"):
                length = int(self.headers.get('Content-length', 0))
                body = self.rfile.read(length).decode()
                body_params = parse_qs(body)

                parsed_path = urlparse(self.path)
                path_params = parse_qs(parsed_path.query)
                print(self.path)
                print(parsed_path.query)

                self.send_response(201)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                session = create_db_session()

                session.query(Restaurant).filter(
                    Restaurant.name == path_params['name'][0],
                    Restaurant.Id == path_params['id'][0]).update(
                    {Restaurant.name: body_params['new_name'][0]},
                    synchronize_session=False)

                session.commit()

                output = '''
                <html>
                <body>
                <h1>{} was updated!</h1>
                </body>
                </html>
                '''

                self.wfile.write(output.format(
                    path_params['name'][0]).encode())
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
