from http.server import HTTPServer, BaseHTTPRequestHandler
import io
import os
import pyscreenshot as ImageGrab
import time

def updateScreenshot2():
    cmd = "ffmpeg -video_size 3840x2160 -f x11grab -i :0.0+0,0 -vframes 1 -q:v 2 -y fullscreen.jpg"
    os.system(cmd)

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
            f = open("index.html", "rb")
            data = f.read()
            f.close()
            self.wfile.write(data)
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
