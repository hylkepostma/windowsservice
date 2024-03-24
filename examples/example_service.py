import time

from windowsservice import BaseService, utils


class ExampleService(BaseService):
    """Example Windows service in Python."""

    _svc_name_ = "PythonExampleWindowsService"
    _svc_display_name_ = "Python Example Windows Service"
    _svc_description_ = "Example Windows service in Python"

    def start(self):
        self.is_running = True

    def main(self):
        while self.is_running:
            utils.log(f"{self._svc_display_name_} is running...")
            time.sleep(5)

    def stop(self):
        self.is_running = False


if __name__ == "__main__":
    ExampleService.parse_command_line()
