import multiprocessing
import os
import shutil
import sys
import sysconfig

import servicemanager


def log(msg):
    servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, 0xF000, (msg, ""))


def get_base_dir():
    """Returns the directory which contains the file that is the entrypoint of the application."""
    if hasattr(sys, "frozen"):
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_bundle_dir():
    """Returns the directory with the bundled files.

    Useful when you bundle files with PyInstaller.
    """
    if hasattr(sys, "frozen"):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_service_host():
    """Returns the path to the executable file that hosts the service.

    If the application is frozen using PyInstaller,
    the service is hosted by the frozen executable itself (`sys.executable`).

    If the application is run directly from the source files,
    the service is hosted by `pythonservice.exe`.
    To work, `pythonservice.exe` must exist in the `Scripts` directory.
    Otherwise `ModuleNotFoundErrors` are raised when importing other packages.
    Because pywin32 installs `pythonservice.exe` in the `Lib\site-packages\win32` directory,
    this function copies `pythonservice.exe` to the `Scripts` directory.
    """
    if hasattr(sys, "frozen"):
        service_host = sys.executable
    else:
        service_host = os.path.join(
            sysconfig.get_paths()["scripts"], "pythonservice.exe"
        )
        if not os.path.exists(service_host):
            src = os.path.join(
                sysconfig.get_paths()["platlib"], "win32", "pythonservice.exe"
            )
            if not os.path.exists(src):
                msg = f"pythonservice.exe not found in pywin32 location: {src}."
                raise FileNotFoundError(msg)
            shutil.copy2(src, service_host)
    return service_host


def configure_multiprocessing():
    """Points the multiprocessing module to the Python interpreter (python.exe).

    Embedding executables like the service host pythonservice.exe need this before they can create child processes.
    """
    if not hasattr(sys, "frozen"):
        executable = os.path.join(os.path.dirname(sys.executable), "python.exe")
        multiprocessing.set_executable(executable)
        del executable
