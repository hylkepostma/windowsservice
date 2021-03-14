import sys
import win32serviceutil
import servicemanager
import win32event
import win32service
import pywintypes
from windowsservice import utils


class BaseService(win32serviceutil.ServiceFramework):
    """Base class to create a Windows service in Python.

    Instructions:

        1. Import the `BaseService` using `from windowsservice import BaseService`

        2. Create a new child class that inherits from the `BaseService` class

        3. Define the following variables inside the child class:
            - `_svc_name_` = "NameOfWindowsService"
            - `_svc_display_name_` = "Name of the Windows service that will be displayed in scm"
            - `_svc_description_` = "Description of the Windows service that will be displayed in scm"

        4. Override the three main methods:
            - `start` runs at service initialization. Can be used it to initialize a running condition.
            - `stop` runs just before the service is stopped. Can be used to invalidate the running condition.
            - `main` is your actual run loop. Mostly based on your running condition.

        5. Define the entry point of your module calling the method `parse_command_line` of the new class
    """

    _svc_name_ = "PythonWindowsService"
    _svc_display_name_ = "Python Windows service"
    _svc_description_ = "About the Python Windows service"
    _exe_name_ = utils.get_service_host()

    @classmethod
    def parse_command_line(cls):
        """Class method to parse the command line"""
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
        """Constructor of the BaseService"""
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        """Called when the service is asked to stop"""
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        """Called when the service is asked to start"""
        utils.configure_multiprocessing()
        self.start()
        self.main()

    def start(self):
        """Override to add logic before the start, for example the running condition"""
        pass

    def stop(self):
        """Override to add logic before the stop, for example invalidating the running condition"""
        pass

    def main(self):
        """Main method to be overridden to add logic"""
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
