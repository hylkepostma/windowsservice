import time

from multiprocessing import freeze_support
from multiprocessing import Process

from windowsservice import BaseService
from windowsservice import utils


def mocked_server():
    while True:
        utils.log("Hello from within a process that is hosted by a Windows service...")
        time.sleep(5)


class ExampleService(BaseService):
    _svc_name_ = "PythonExampleWindowsService"
    _svc_display_name_ = "Python Example Windows Service"
    _svc_description_ = "This is a Windows Service in Python!"

    def __init__(self, args):
        super().__init__(args)
        self.server_process = None

    def start(self):
        self.server_process = Process(target=mocked_server)
        self.server_process.start()

    def stop(self):
        self.server_process.terminate()


if __name__ == "__main__":
    freeze_support()
    ExampleService.parse_command_line()
