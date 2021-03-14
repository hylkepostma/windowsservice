# windowsservice

`windowsservice` is a Python package for building Windows services.

The key features are:

- Easy to use
- Support for [PyInstaller](https://www.pyinstaller.org/)
- Support for [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.freeze_support)

## Dependencies

- Python 3.6+
- windowsservice depends on Mark Hammond's [`pywin32`](https://github.com/mhammond/pywin32)

## Getting ready

Create and activate a virtual environment with the name `venv`:

```powershell
python -m venv venv
```

```powershell
.\venv\Scripts\activate
```

## Installation

Install from PyPI:

```powershell
pip install windowsservice
```

You will also need to run the post install script to configure pywin32:

```powershell
python .\venv\Scripts\pywin32_postinstall.py -install
```

The windowsservice package takes care of the pywin32 installation (which is responsible for the Python Service Framework). It also moves the service host (`pythonservice.exe`) to the correct location which is necessary when working from a virtual environment.

## Coding

1. Import the `BaseService` using `from windowsservice import BaseService`

2. Create a new child class that inherits from the `BaseService` class

3. Define the following variables inside the child class:
    - `_svc_name_` = "NameOfWindowsService"
    - `_svc_display_name_` = "Name of the Windows service that will be displayed in scm"
    - `_svc_description_` = "Description of the Windows service that will be displayed in scm"

4. Override the three main methods:
    - `start` runs at service initialization. Can be used it to initialize a running condition
    - `stop` runs just before the service is stopped. Can be used to invalidate the running condition
    - `main` is your actual run loop. Commonly based on your running condition

5. Define the entry point of your module calling the method `parse_command_line` of the new class

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

There is also an example that demonstrates support for `multiprocessing` in `example_service_multiprocessing.py`.

```python
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
```

## Usage

For some interactions with a Windows service you might need adminstrative rights, so you need to use an elevated command line interface.

All the arguments and options can be listed by calling the module:

```powershell
python -m windowsservice.example_service
```

```text
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

If you want to install the service from `example_service.py`:

```powershell
python -m windowsservice.example_service install
```

You can also install the service so that it starts automatically when Windows is started:

```powershell
python -m windowsservice.example_service --startup=auto install
```

### Start the service

You can now start/stop the service using Windows' service control manager or from the command line interface like this:

```powershell
python -m windowsservice.example_service start
```

You can also start the service in debug mode:

```powershell
python -m windowsservice.example_service debug
```

To inspect if the service is working make sure it is running and then have a look at `stdout` (when running in debug mode) and/or the Windows Event Viewer. You should see a message every 5 seconds.

### Remove the service

You can remove the service like this:

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

Create a stand-alone (one-file bundled) executable using the `pyinstaller` command:

```powershell
pyinstaller windowsservice\example_service.py --clean --noupx --onefile --noconfirm --hidden-import=win32timezone
```

The resulting executable can be found in the `dist` folder.

The arguments and options of the executable are the same as above. For example, to install:

```powershell
example_service.exe install
```

You can also create a one-folder bundle containing an executable. Because the excutable does not need to be unpacked first at a temporary location, this has the advantage that the service starts faster.

```powershell
pyinstaller windowsservice\example_service.py --clean --noupx --onedir --noconfirm --hidden-import=win32timezone
```

In this case, the resulting executable can be found in the `dist\example_service` folder.
