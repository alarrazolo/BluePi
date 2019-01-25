from threading import Thread
from Securitron import Securitron
from btConnection import BtConnection
import time
import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
# import RPi.GPIO as GPIO
# from vision import SecureVision


class BtConnectionThread:
    def __init__(self, bt_connection):
        self.connection = bt_connection
        self.connection.start_connection()
        self._running = True

    def terminate(self):
        self.connection.close_connection()
        self._running = False

    def receive_bt_data(self):
        while self._running:
            self.connection.get_data()


# class SecureVisionThread:
#     def __init__(self, secure_vision):
#         self.vision = secure_vision
#         self.vision.begin_stream()
#         self._running = True
#
#     def terminate(self):
#         self.vision.stop_stream()
#         self._running = False
#
#     def start_stream(self):
#         while self._running:
#             self.vision.transmit_video()

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

        if self.path == '/stream.mp4' or self.path == '/':
        # if self.path == '/stream.mp4':
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


print("Hello world!")
victor = Securitron()
print(victor.robot_name)

btc = BtConnection(victor=victor)
bt_thread_super = BtConnectionThread(btc)
bt_thread = Thread(target=bt_thread_super.receive_bt_data, daemon=True)
bt_thread.start()

time.sleep(2)

with picamera.PiCamera() as camera:
    camera.resolution = (1920, 1080)
    # camera.resolution = (1280, 720)
    camera.framerate = 30
    camera.rotation = 180
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')

    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
        # while btc.is_connected():
        # while True:
        #     victor.beat_heart()

    except KeyboardInterrupt:
        camera.stop_recording()
        print("Exiting")

    finally:
        bt_thread_super.terminate()
        victor.go_home()
        print("\nGood Bye Creator!")
