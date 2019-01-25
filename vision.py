import socket
import struct
import time

import io
import picamera


class SecureVision:

    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1920, 1080)
        self.camera.framerate = 30
        self.camera.rotation = 180
        self.server_socket = None
        # self.server_socket.connect(("Desktop-EK1IM0Q", 8000))
        self.connection = None

        # self.server_socket = socket.socket()
        # self.server_socket.bind(('0.0.0.0', 8000))
        # self.server_socket.listen(0)

    def begin_stream(self):
        pass
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8000))
        self.server_socket.listen(0)
        # self.connection = self.server_socket.accept()[0].makefile('wb')

    def transmit_video(self):
        self.connection = self.server_socket.accept()[0].makefile('wb')
        print("gets here")
        try:
            self.camera.start_recording(self.connection, format='mjpeg')
            try:
                while True:
                    self.camera.wait_recording(1)
            finally:
                self.camera.stop_recording()
                # self.begin_stream()


        # except KeyboardInterrupt:
        #     self.camera.stop_recording()
        #     self.stop_stream()
        #     print("Keyboard interrupt")
        # except ConnectionResetError:
        #     self.stop_stream()
        #     print("Connection reset error")
        #     self.camera.stop_recording()
        #     self.begin_stream()
        finally:
            print("Connection reset error")
            self.camera.stop_recording()
            self.stop_stream()
            # self.begin_stream()

    def stop_stream(self):
        if self.connection:
            self.connection.close()
        if self.server_socket:
            self.server_socket.close()


def main():
    sv = SecureVision()
    sv.begin_stream()
    try:
        sv.transmit_video()
    except KeyboardInterrupt:
        # sv.stop_stream()
        print("Ending Program")


if __name__ == "__main__":
    main()











    # def begin_stream(self):
    #     # try:
    #     #     self.camera.start_recording(self.connection, format='h264')
    #     #     while True:
    #     #         self.camera.wait_recording(100)
    #     # except ConnectionResetError:
    #     #     self.camera.stop_recording()
    #     #     self.stop_stream()
    #     self.connection = self.server_socket.accept()[0].makefile('wb')
    #
    #     try:
    #         with picamera.PiCamera() as camera:
    #             camera.resolution = (640, 480)
    #             camera.framerate = 30
    #             time.sleep(2)
    #             start = time.time()
    #             count = 0
    #             stream = io.BytesIO()
    #             # Use the video-port for captures...
    #             for foo in camera.capture_continuous(stream, 'jpeg',
    #                                                  use_video_port=True):
    #                 self.connection.write(struct.pack('<L', stream.tell()))
    #                 self.connection.flush()
    #                 stream.seek(0)
    #                 self.connection.write(stream.read())
    #                 count += 1
    #                 if time.time() - start > 30:
    #                     break
    #                 stream.seek(0)
    #                 stream.truncate()
    #         self.connection.write(struct.pack('<L', 0))
    #     finally:
    #         self.connection.close()
    #         self.server_socket.close()
    #         finish = time.time()
    #     print('Sent %d images in %d seconds at %.2ffps' % (
    #         count, finish - start, count / (finish - start)))