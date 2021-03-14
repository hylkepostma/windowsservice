import time

from windowsservice import BaseService
from windowsservice import utils


class ExampleService(BaseService):
    _svc_name_ = "PythonExampleWindowsService"
    _svc_display_name_ = "Python Example Windows service"
    _svc_description_ = "This is a Windows service in Python!"

    def __init__(self, args):
        super().__init__(args)
        self.is_running = None

    def start(self):
        self.is_running = True
        # The two lines below can be removed safely...
        # The utils.get_base_dir() and get_bundle_dir() are just helper functions
        # that might be useful when working with PyInstaller `--onefile`
        utils.log(f"Base dir: {utils.get_base_dir()}")
        utils.log(f"Bundle dir: {utils.get_bundle_dir()}")

    def stop(self):
        self.is_running = False

    def main(self):
        while self.is_running:
            utils.log(f"{self._svc_display_name_} is running...")
            time.sleep(5)


if __name__ == "__main__":
    ExampleService.parse_command_line()
