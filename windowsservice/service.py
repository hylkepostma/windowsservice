import sys

import pywintypes
import servicemanager
import win32event
import win32service
import win32serviceutil

from windowsservice import utils


class BaseService(win32serviceutil.ServiceFramework):
    """Base class to create a Windows service in Python.

    Instructions:

    1. Import the `BaseService` class: `from windowsservice import BaseService`.

    2. Create a new child class that inherits from the `BaseService` class.

    3. Define the following three class variables:

        1. `_svc_name_` = "NameOfTheWindowsService"
        2. `_svc_display_name_` = "The display name of the Windows service that will be displayed in service control manager"
        3. `_svc_description_` = "The description of the Windows service that will be displayed in service control manager"
        
    4. Override the following three methods:

        1. `def start(self):` Called when the service is asked to start. Override this method to add code that is executed before the service starts, for example to set a running condition.
        2. `def stop(self):` Called when the service is asked to stop. Override this method to add code that is executed before the service stops, for example to invalidate a running condition.
        3. `def main(self):` Called right after the start method. Override this method to create a run loop, usually based on a running condition.

    5. Call the `parse_command_line` method from the entry point of the module.

    You can find an example in `example_service.py`:

    ```Python
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

        def stop(self):
            self.is_running = False

        def main(self):
            while self.is_running:
                utils.log(f"{self._svc_display_name_} is running...")
                time.sleep(5)


    if __name__ == "__main__":
        ExampleService.parse_command_line()
    ```

    """

    _svc_name_ = "PythonWindowsService"
    _svc_display_name_ = "Python Windows service"
    _svc_description_ = "About the Python Windows service"
    _exe_name_ = utils.get_service_host()

    win32serviceutil.noise = ""

    @classmethod
    def parse_command_line(cls):
        """Class method to parse the command line."""
        if len(sys.argv) == 1:
            try:
                # Add PyInstaller support: https://stackoverflow.com/a/25934756
                servicemanager.Initialize()
                servicemanager.PrepareToHostSingle(cls)
                servicemanager.StartServiceCtrlDispatcher()
            except pywintypes.error:
                win32serviceutil.HandleCommandLine(cls)
        else:
            win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        """Called when the service is asked to stop."""
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        """Called when the service is asked to start."""
        utils.configure_multiprocessing()
        self.start()
        self.main()

    def start(self):
        """Called when the service is asked to start. Override this method to add code that is executed before the service starts, for example to set a running condition."""

    def stop(self):
        """Called when the service is asked to stop. Override this method to add code that is executed before the service stops, for example to invalidate a running condition."""

    def main(self):
        """Called right after the start method. Override this method to create a run loop, usually based on a running condition."""
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
