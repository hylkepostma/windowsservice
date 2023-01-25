# windowsservice

`windowsservice` is a Python package for building Windows services.

The key features are:

- Easy to use
- Support for [PyInstaller](https://www.pyinstaller.org/)
- Support for [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.freeze_support)

## Getting ready

Create and activate a virtual environment named `venv`:

```powershell
python -m venv venv
```

```powershell
.\venv\Scripts\activate
```

## Installation

Install the windowsservice package from PyPI:

```powershell
pip install windowsservice
```

Finally, run the post install script to configure pywin32:

```powershell
python .\venv\Scripts\pywin32_postinstall.py -install
```

The windowsservice package depends on [pywin32](https://github.com/mhammond/pywin32) created by Mark Hammond. Installing the windowsservice package also installs the pywin32 dependency.

## Coding

1. Import the `BaseService` class: `from windowsservice import BaseService`.

2. Create a new child class that inherits from the `BaseService` class.

3. Define the following three class variables:

    1. `_svc_name_` = "NameOfTheWindowsService"
    2. `_svc_display_name_` = "The display name of the Windows service that will be displayed in service control manager"
    3. `_svc_description_` = "The description of the Windows service that will be displayed in service control manager"

4. Override the following three methods:

    1. `def start(self):` Called when the service is asked to start. Override this method to add code that is executed before the service starts, for example to set a running condition.
    2. `def stop(self):` Called when the service is asked to stop. Override this method to add code that is executed before the service stops, for example to invalidate a running condition.
    3. `def main(self):` Called right after the start method. Override this method to create a run loop, usually based on the running condition.

5. Call the `parse_command_line` method from the entry point of the module.

You can find an example in `example_service.py`:

```python
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

There is also an example that demonstrates support for `multiprocessing` in `example_service_multiprocessing.py`:

```python
import time
from multiprocessing import Process
from multiprocessing import freeze_support

from windowsservice import BaseService
from windowsservice import utils


def mocked_server():
    while True:
        utils.log("Hello from a process hosted by a Windows service...")
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
```

## Usage

For some interactions with a Windows service, you may need administrative privileges, so you must use an elevated command line interface.

All the arguments and options can be listed by calling the module:

```powershell
python -m windowsservice.example_service
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

```powershell
python -m windowsservice.example_service install
```

You can also install the service so that it starts automatically when Windows starts:

```powershell
python -m windowsservice.example_service --startup=auto install
```

### Start the service

To start/stop the service you can now use the [service control manager](https://docs.microsoft.com/en-us/windows/win32/services/service-control-manager).

Or, from the command line interface, run:

```powershell
python -m windowsservice.example_service start
```

To start the service in debug mode, run:

```powershell
python -m windowsservice.example_service debug
```

To inspect if the service is working, make sure it is running and then have a look at the standard output stream (when running in debug mode) and/or the Windows Event Viewer. You should see a message every 5 seconds.

### Remove the service

To remove the service, run:

```powershell
python -m windowsservice.example_service remove
```

## PyInstaller

You can use PyInstaller to bundle the service into a convenient stand-alone executable.

### Install PyInstaller

Install [PyInstaller](https://www.pyinstaller.org/) inside your activated virtual environment:

```powershell
pip install pyinstaller
```

### Create executable

To create a stand-alone (**one-file**) executable, use the `pyinstaller` command:

```powershell
pyinstaller windowsservice\example_service.py --clean --noupx --onefile --noconfirm --hidden-import=win32timezone
```

The resulting `example_service.exe` executable can be found in the `dist` directory.

The arguments and options of `example_service.exe` are the same as above. For example, to install the service, run:

```powershell
example_service.exe install
```

You can also create a **one-folder** bundle. Because the executable does not have to be unpacked first in a temporary location, this has the advantage of making the service start faster.

```powershell
pyinstaller windowsservice\example_service.py --clean --noupx --onedir --noconfirm --hidden-import=win32timezone
```

In this case, the resulting executable can be found in the `dist\example_service` directory.
