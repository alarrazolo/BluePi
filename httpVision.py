import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server


# class Vision:
#     def __init__(self):
#         with picamera.PiCamera(resolution='1280x720', framerate=30) as camera:
#             self.camera = camera
#             self.camera.rotation = 180
#             self.output = StreamingOutput()
#             self.camera.start_recording(self.output, format='mjpeg')
#             try:
#                 address = ('', 8000)
#                 self.server = StreamingServer(address, StreamingHandler)
#                 self.server.serve_forever()
#             finally:
#                 print("done")


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


class StreamingHandler(server.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.output = StreamingOutput()

    def do_GET(self):

        # if self.path == '/stream.mp4' or self.path == '/':
        if self.path == '/stream.mp4':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera() as camera:
    # camera.resolution = (1920, 1080)
    camera.resolution = (1280, 720)
    camera.framerate = 30
    camera.rotation = 180
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()

# def main():
#     with picamera.PiCamera() as camera:
#         # camera.resolution = (1920, 1080)
#         camera.resolution = (1280, 720)
#         camera.framerate = 30
#         camera.rotation = 180
#         output = StreamingOutput()
#         camera.start_recording(output, format='mjpeg')
#         try:
#             address = ('', 8000)
#             server = StreamingServer(address, StreamingHandler)
#             server.serve_forever()
#         finally:
#             camera.stop_recording()
#
#
# if __name__ == "__main__":
#     main()