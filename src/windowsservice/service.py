import pathlib
import sys

import pywintypes
import servicemanager
import win32event
import win32service
import win32serviceutil


class BaseService(win32serviceutil.ServiceFramework):
    """`BaseService` is a base class for creating a Windows service in Python.

    Steps to use:

    1. Import the `BaseService` class:

        ```python
        from windowsservice import BaseService
        ```

    2. Create a new subclass that inherits from the `BaseService` class.

    3. Define the following three class variables in the subclass:

        - `_svc_name_`: A unique identifier for your service.
        - `_svc_display_name_`: The name shown in the service control manager.
        - `_svc_description_`: The description shown in the service control manager.

        For example:

        ```python
        _svc_name_ = "MyWindowsService"
        _svc_display_name_ = "My Windows Service"
        _svc_description_ = "This is my custom Windows service."
        ```

    4. Override the following methods in the subclass:

        - `start(self)`: This method is invoked when the service starts. Override
        this to add setup code, such as initializing a running condition.

        - `main(self)`: This method is invoked after `start`. Override this to
        create a run loop, typically based on a running condition.

        - `stop(self)`: This method is invoked when the service stops. Override
        this to add cleanup code, such as releasing resources or to invalidate a
        running condition.

        For example:

        ```python
        def start(self):
            self.is_running = True

        def main(self):
            while self.is_running:
                time.sleep(5)

        def stop(self):
            self.is_running = False
        ```

    5. Call the `parse_command_line` class method from the module's entry point.
    This handles command-line arguments for installing, starting, stopping,
    and debugging the service.
    """

    _svc_name_ = "PythonWindowsService"
    _svc_display_name_ = "Python Windows service"
    _svc_description_ = "About the Python Windows service"

    _exe_name_ = sys.executable  # either python.exe or the bundled executable
    if not hasattr(sys, "frozen"):
        script = pathlib.Path(sys.argv[0]).resolve()
        _exe_args_ = f'-u -E "{script}"'

    def SvcRun(self):
        """Called when the service is started."""
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.start()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.SvcDoRun()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)

    def SvcDoRun(self):
        """Called by SvcRun once the service is started.

        As long as this method is blocking, the service runs.
        When this method returns, the service stops."""
        self.main()

    def SvcStop(self):
        """Called when the service is stopped."""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.stop()

    def start(self):
        """This method is invoked when the service starts.

        Override this to add setup code, such as initializing a running condition.
        """
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def main(self):
        """This method is invoked after `start`.

        Override this to create a run loop, typically based on a running condition.
        """
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)

    def stop(self):
        """This method is invoked when the service stops.

        Override this to add cleanup code, such as releasing resources or
        to invalidate a running condition.
        """
        win32event.SetEvent(self.stop_event)

    @classmethod
    def parse_command_line(cls):
        """Class method to parse the command line."""
        if len(sys.argv) == 1:
            try:
                servicemanager.Initialize()
                servicemanager.PrepareToHostSingle(cls)
                servicemanager.StartServiceCtrlDispatcher()
            except pywintypes.error:
                win32serviceutil.HandleCommandLine(cls)
        else:
            win32serviceutil.HandleCommandLine(cls)
