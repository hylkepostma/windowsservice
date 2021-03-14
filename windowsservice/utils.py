import os
import sys
import sysconfig
import servicemanager
import shutil
import multiprocessing


def log(msg):
    servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, 0xF000, (msg, ""))


def get_base_dir():
    """Returns the folder where the file with the entrypoint of the application lives."""
    if hasattr(sys, "frozen"):
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_bundle_dir():
    """Returns the folder with the bundled files.

    Useful when you bundle files with PyInstaller.
    """
    if hasattr(sys, "frozen"):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_service_host():
    """Returns the path to service host pythonservice.exe.

    If the application is frozen using PyInstaller
    the service is hosted by the frozen executable (sys.executable) itself

    If the application is run directly from the source files, pythonservice.exe needs
    to be in the Scripts folder to prevent ModuleNotFoundErrors when importing other packages

    However, pywin32 installs pythonservice.exe in the Lib\site-packages\win32 folder
    so if it is not in the Scripts folder, we try to copy it.
    """
    if hasattr(sys, "frozen"):
        service_host = sys.executable
    else:
        service_host = os.path.join(
            sysconfig.get_paths()["scripts"], "pythonservice.exe"
        )
        log(f"Service host: {service_host}")
        if not os.path.exists(service_host):
            log("pythonservice.exe not found in Scripts folder.")
            src = os.path.join(
                sysconfig.get_paths()["platlib"], "win32", "pythonservice.exe"
            )
            if not os.path.exists(src):
                msg = f"pythonservice.exe not found in pywin32 location: {src}."
                log(msg)
                raise FileNotFoundError(msg)
            log(
                f"pythonservice.exe found in pywin32 location. Copying from {src} to {service_host}..."
            )
            shutil.copy2(src, service_host)
            log("pythonservice.exe found in Scripts folder.")
    return service_host


def configure_multiprocessing():
    """Points the multiprocessing module to the Python interpreter (python.exe).

    Embedding executables like the service host pythonservice.exe need this before they can create child processes.
    """
    if not hasattr(sys, "frozen"):
        executable = os.path.join(os.path.dirname(sys.executable), "python.exe")
        multiprocessing.set_executable(executable)
        log(f"Using {executable} as the Python interpreter for child processes.")
        del executable
