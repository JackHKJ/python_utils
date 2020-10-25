# -*- coding: UTF-8 -*-
# Dependencies
import psutil


class GetResourceUsage:
    """
    This is a class that wraps the psutil utilities for easy usage
    """
    __author__ = "Kejie He"

    @classmethod
    def get_pid_by_name(cls, name: str, accurate=False) -> int:
        """
            find the pid of the process by its name
            :param name: the name of the process
            :param accurate: if True then only return pid if there is a perfect match
            :return the pid if there is a match, -1 otherwise
        """
        for pid in psutil.pids():
            try:
                process = psutil.Process(pid)
                if accurate:
                    if name == process.name():
                        return process.pid
                elif not accurate:
                    if name in process.name():
                        return process.pid
            except(psutil.AccessDenied, psutil.NoSuchProcess, ValueError, AttributeError):
                pass
        return -1

    @classmethod
    def get_pid_by_path(cls, cmdline: str) -> int:
        """
        find the pid of the process by its path
        :param cmdline: the cmdline(path) of the process
        :return: the pid if there is a match, -1 otherwise
        """
        for pid in psutil.pids():
            try:
                process = psutil.Process(pid)
                if cmdline == process.cmdline():
                    return process.pid
            except(psutil.AccessDenied, psutil.NoSuchProcess, ValueError, AttributeError):
                pass
        return -1

    @classmethod
    def get_cpu_usage(cls, pid=None, interval=0.1):
        """
        :param pid: the pid of the target process
        :param interval: the interval
        :return: the usage of the cpu of the pid given (None for overall system usage) in percentage
        the percentage shall not exceed 100% as the usage is evenly divided by the cpu_count
        the general cpu usage will be returned if the pid cannot be found
        """
        if pid is None:
            return psutil.cpu_percent(interval=interval) / psutil.cpu_count()
        try:
            process = psutil.Process(pid)
            return process.cpu_percent(interval=interval) / psutil.cpu_count()
        except(psutil.NoSuchProcess, ValueError, TypeError):
            return psutil.cpu_percent(interval=interval) / psutil.cpu_count()

    @classmethod
    def get_memory_usage(cls, pid=None):
        """
        :param pid: the pid of the target process
        :return: the usage of the memory of the pid given (None for overall system usage) in percentage
        the general memory usage will be returned if the pid cannot be found
        """
        if pid is None:
            return psutil.virtual_memory().percent
        try:
            process = psutil.Process(pid)
            return process.memory_percent()
        except(psutil.NoSuchProcess, ValueError, TypeError):
            return psutil.virtual_memory().percent

    @classmethod
    def get_handle_usage(cls, pid=None):
        """
        :param pid: the pid of the target process
        :return: the usage of the handle of the pid given, or None if pid is None
        the general handle usage will be returned if the pid cannot be found
        """
        if pid is None:
            return None
        try:
            process = psutil.Process(pid)
            return process.num_handles()
        except(psutil.NoSuchProcess, ValueError, TypeError):
            return None

    @classmethod
    def get_name_by_pid(cls, pid=None):
        """
        get the name of the process by the pid given
        :param pid: the pid of the process
        :return: the name of the process with pid, or None if None is given
        """
        if pid is None:
            return None
        try:
            process = psutil.Process(pid)
            return process.name()
        except(psutil.NoSuchProcess, ValueError, TypeError):
            return None

    @classmethod
    def get_cmdline_by_pid(cls, pid=None):
        """
        get the cmdline of the process by the pid given
        :param pid: the pid of the process
        :return: the cmdline of the process with pid, or None if None is given
        """
        if pid is None:
            return None
        try:
            process = psutil.Process(pid)
            return process.cmdline()
        except(psutil.NoSuchProcess, ValueError, TypeError):
            return None


if __name__ == "__main__":
    python_pid = GetResourceUsage.get_pid_by_name(name="python.exe",accurate=False)
    print("pid of the python process: {}".format(python_pid))
    print("name of pid {}: {}".format(python_pid, GetResourceUsage.get_name_by_pid(pid=python_pid)))
    print("cmdline of pid {}: {}".format(python_pid, GetResourceUsage.get_cmdline_by_pid(pid=python_pid)))
    print("cpu usage of pid {}: {}".format(python_pid, GetResourceUsage.get_cpu_usage(pid=python_pid)))
    print("memory usage of pid {}: {}".format(python_pid, GetResourceUsage.get_memory_usage(pid=python_pid)))
    print("handle usage of pid {}: {}".format(python_pid, GetResourceUsage.get_handle_usage(pid=python_pid)))