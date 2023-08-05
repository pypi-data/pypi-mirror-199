class InvalidReplicationMethodException(Exception):
    """Exception for errors related to replication methods"""

    def __init__(self, replication_method, message=None):
        msg = f"Invalid replication method {replication_method}!"

        if message is not None:
            msg = f'{msg} {message}'

        super().__init__(msg)


class UnsupportedKeyTypeException(Exception):
    """Raised if key type is unsupported"""


class InvalidDateTimeException(Exception):
    """Raised if we find an invalid date-time that we can't handle"""


class SyncException(Exception):
    """Raised if we there is an exception while syncing"""


class NoReadPrivilegeException(Exception):
    """Raised if the DB user has no read privilege on the DB"""

    def __init__(self, user, db_name):
        msg = f"The user '{user}' has no read privilege on the database '{db_name}'!"
        super().__init__(msg)


class InvalidAwaitTimeException(Exception):
    """Raised if the given await time used in log_based is invalid"""

    def __init__(self, time_ms, reason):
        msg = f"Invalid await time {time_ms}! {reason}"
        super().__init__(msg)
