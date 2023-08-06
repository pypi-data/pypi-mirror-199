from http.server import BaseHTTPRequestHandler, HTTPServer

import datetime

hostName = "localhost"
serverPort = 8080

def dateandtime():
    now = datetime.datetime.now()

    return now.strftime("%Y-%m-%d %H:%M:%S")



class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://CYB600timeanddate.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>current time and date: </p>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes(dateandtime(), 'utf-8'))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


