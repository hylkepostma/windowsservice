import time
from multiprocessing import Process, freeze_support

from windowsservice import BaseService, utils


def stub_server():
    """
    A function that simulates a server process hosted by the Windows service.

    This function logs a message every 5 seconds for a total of 100 times.
    """
    for _ in range(100):
        utils.log("Hello from a process hosted by a Windows service...")
        time.sleep(5)


class ExampleService(BaseService):
    """Example Windows service in Python."""

    _svc_name_ = "PythonExampleWindowsService"
    _svc_display_name_ = "Python Example Windows Service"
    _svc_description_ = "Example Windows service in Python"

    def start(self):
        self.server_process = Process(target=stub_server)

    def main(self):
        self.server_process.start()
        self.server_process.join()

    def stop(self):
        if self.server_process:
            self.server_process.terminate()


if __name__ == "__main__":
    freeze_support()
    ExampleService.parse_command_line()
