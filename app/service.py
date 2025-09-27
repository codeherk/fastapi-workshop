from .storage import Storage

class Service:
    def __init__(self):
        super().__init__()
        # TODO: add config as class arg and reference when init Storage
        sqlite_file_name = "database.db"
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        connect_args = {"check_same_thread": False}
        self.storage = Storage(sqlite_url, connect_args=connect_args)
        return