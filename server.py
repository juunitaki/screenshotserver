from http.server import HTTPServer, BaseHTTPRequestHandler
import io
import os
import pyscreenshot as ImageGrab
import time

html = """<!doctype html>
<html>
    <head>
    </head>
    <body>
        <img id="img" width="100%" src="fullscreen.jpg">
        <script>
        function update() {
            var source = 'fullscreen.jpg',
                timestamp = (new Date()).getTime(),
                newUrl = source + '?_=' + timestamp;
            document.getElementById("img").src = newUrl;
            setTimeout(update, 1000);
        }
        update();
        </script>
    </body>
</html>
"""

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    imageUpdatedAt = 0
    imageData = ""

    def updateScreenshot(self):
        im = ImageGrab.grab(childprocess=False)
        buf = io.BytesIO()
        im.save(buf, "jpeg")
        self.imageData = buf.getvalue()

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            global html
            self.wfile.write(html.encode())
        elif self.path.startswith("/fullscreen.jpg"):
            if time.time() - self.imageUpdatedAt > 0.5:
                self.updateScreenshot()
                self.imageUpdatedAt = time.time()
            self.send_response(200)
            self.send_header('Content-Type', 'image/jpg')
            self.end_headers()
            self.wfile.write(self.imageData)

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
