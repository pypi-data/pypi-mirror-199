__author__ = 'Andrey Komissarov'
__date__ = '2022'


class RemoteCommandExecutionError(BaseException):
    def __init__(self, error: str = None):
        self.error = error

    def __str__(self):
        return f'During handling remote command execution error occurred!\n\t{self.error}'


class LocalCommandExecutionError(BaseException):
    def __init__(self, error: str = None):
        self.error = error

    def __str__(self):
        return f'During handling local command execution error occurred!\n\t{self.error}'


class PackageNotFoundError(BaseException):
    def __init__(self, package: str = None):
        self.package = package or 'name is not specified by user'

    def __str__(self):
        return f'Package ({self.package}) not found!'
