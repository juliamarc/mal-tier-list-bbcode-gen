class EntriesPerRowMissingError(Exception):  # pragma: no cover
    def __init__(self, message):
        super().__init__(message)


class EntriesPerRowNotANumberError(Exception):  # pragma: no cover
    def __init__(self, message):
        super().__init__(message)


class GoogleDriveSourceError(Exception):  # pragma: no cover
    def __init__(self, message):
        super().__init__(message)


class HeaderIncompleteError(Exception):  # pragma: no cover
    def __init__(self, message):
        super().__init__(message)
