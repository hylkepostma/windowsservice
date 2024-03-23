# windowsservice

`windowsservice` is a Python package for building Windows services.

The key features are:

- Easy to use
- Support for [PyInstaller](https://www.pyinstaller.org/)
- Support for [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.freeze_support)

## Getting ready

Create and activate a virtual environment:

```cli
python -m venv venv
```

```cli
.\venv\Scripts\activate
```

## Installation

Install the windowsservice package from PyPI:

```cli
pip install windowsservice
```

The windowsservice package depends on [pywin32](https://github.com/mhammond/pywin32) created by Mark Hammond. Installing the windowsservice package also installs the pywin32 dependency.

## Coding

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

### Examples

Basic example ([example_service.py](examples/example_service.py)):

```python
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
```

Example that demonstrates support for `multiprocessing` ([example_service_multiprocessing.py](examples/example_service_multiprocessing.py)):

```python
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
```

## Usage

Some interactions with a Windows service may require administrative privileges, so you must use an elevated command line interface.

All arguments and options can be listed by invoking the module:

```cli
python .\examples\example_service.py
```

```stdout
Usage: 'example_service.py [options] install|update|remove|start [...]|stop|restart [...]|debug [...]'
Options for 'install' and 'update' commands only:
 --username domain\username : The Username the service is to run under
 --password password : The password for the username
 --startup [manual|auto|disabled|delayed] : How the service starts, default = manual
 --interactive : Allow the service to interact with the desktop.
 --perfmonini file: .ini file to use for registering performance monitor data
 --perfmondll file: .dll file to use when querying the service for
   performance data, default = perfmondata.dll
Options for 'start' and 'stop' commands only:
 --wait seconds: Wait for the service to actually start or stop.
                 If you specify --wait with the 'stop' option, the service
                 and all dependent services will be stopped, each waiting
                 the specified period.
```

### Install the service

If you want to install the service from the `example_service.py` example, run:

```cli
python .\examples\example_service.py install
```

```stdout
Installing service PythonExampleWindowsService
Service installed
```

You can also choose to install the service so that it will start automatically when Windows starts:

```cli
python .\examples\example_service.py --startup=auto install
```

### Start the service

To start/stop the service you can now use the [service control manager](https://docs.microsoft.com/en-us/windows/win32/services/service-control-manager).

Or, from the command line interface, you can run:

```cli
python .\examples\example_service.py start
```

To start the service in debug mode, run:

```cli
python .\examples\example_service.py debug
```

To verify that the service is working, make sure it is running, and then look into the Windows Event Viewer or, if it is running in debug mode, look at the standard output stream. You should see a message every 5 seconds.

### Remove the service

To remove the service, run:

```cli
python .\examples\example_service.py remove
```

## PyInstaller

To bundle the service into a convenient standalone executable, you can use PyInstaller.

### Install PyInstaller

Install [PyInstaller](https://www.pyinstaller.org/) inside your activated virtual environment:

```cli
pip install pyinstaller
```

### Create executable

To create a standalone (**one-file**) executable, use the `pyinstaller` command:

```cli
pyinstaller .\examples\example_service.py --clean --noupx --onefile --noconfirm --hidden-import=win32timezone
```

The resulting `example_service.exe` executable can be found in the `.\dist` directory.

You can use this executable with the same arguments and options as discussed above. For example, to install the service, run:

```cli
.\dist\example_service.exe install
```

You can also create a **one-folder** bundle. Because the executable does not have to be unpacked first in a temporary location, this has the advantage of making the service start faster.

```cli
pyinstaller .\examples\example_service.py --clean --noupx --onedir --noconfirm --hidden-import=win32timezone
```

In this case, the resulting executable can be found in the `dist\example_service` directory.

### Acknowledgement

This package utilizes the [pywin32](https://github.com/mhammond/pywin32) library, a collection of Python extensions for Windows. The maintenance and development of this library is credited to Mark Hammond and others in the Python community. Their contributions enable the development of Windows services in Python. Please note that the `windowsservice` package does not aim to replace `pywin32` or `win32serviceutil.ServiceFramework`, it's just here to make it a little bit easier to use.
