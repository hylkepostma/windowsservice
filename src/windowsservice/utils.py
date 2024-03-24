import servicemanager


def log(msg):
    """
    Logs a message to the Windows event log.

    Args:
        msg (str): The message to log.
    """
    servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, 0xF000, (msg, ""))
