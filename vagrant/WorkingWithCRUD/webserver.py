from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:

            # if self.path.endswith("/hello"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #     output = ""
            #     output += "<html><body>"
            #     output += "<h1>Hello!</h1>"
            #     output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #     output += "</body></html>"
            #     self.wfile.write(output)
            #     print output
            #     return

            # if self.path.endswith("/hola"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #     output = ""
            #     output += "<html><body>"
            #     output += "<h1>&#161 Hola !</h1>"
            #     output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #     output += "</body></html>"
            #     self.wfile.write(output)
            #     print output
            #     return

            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = '''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>Title</title>
                    </head>
                    <body>
                    <form method='POST' enctype='multipart/form-data'>
                        <h1>Enter the name of the new restaurant!</h1>
                        <input name="new_restaurant" type="text" >
                        <input type="submit" value="Submit"> 
                    </form>
                    </body>
                    </html>                                
                '''
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = '''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>Title</title>
                    </head>
                    <body>
                    <form method='POST' enctype='multipart/form-data'>
                        <h1>Change the restaurants name!</h1>
                        <input name="new_restaurant" type="text" >
                        <input type="submit" value="Submit"> 
                    </form>
                    </body>
                    </html>                                
                '''
                self.wfile.write(output)
                return

            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = '''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>Title</title>
                    </head>
                    <body>
                    <form method='POST' enctype='multipart/form-data'>
                        <h1>Enter the restaurant you with to delete!</h1>
                        <input name="new_restaurant" type="text" >
                        <input type="submit" value="Submit"> 
                    </form>
                    </body>
                    </html>                                
                '''
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = session.query(Restaurant)
                output = ""
                output += "<html><body>"
                for restaurant in restaurants:
                    output += "<h1>" + restaurant.name + "</h1>"
                    output += "<p><a href=\"edit\">Edit</a></p>"
                    output += "<p><a href=\"delete\">Delete</a></p>"
                "<p><a href=\"new\">Make a new Restaurant</a></p>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Location', '/restaurants')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))

            if self.path.endswith("/new"):
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new_restaurant')
                    myFirstRestaurant = Restaurant(name=messagecontent[0])
                    session.add(myFirstRestaurant)
                    session.commit()
                    return

            if self.path.endswith("/delete"):
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new_restaurant')
                    restaurant = session.query(Restaurant).filter_by(name=messagecontent).one()
                    session.detete(restaurant)
                    session.commit()
                    return
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()


if __name__ == '__main__':
    main()
