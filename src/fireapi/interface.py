from typing import Dict


class IAPIOperations:
    def get_config(self) -> Dict:
        pass

    def get_status(self) -> Dict:
        pass

    def start_server(self) -> Dict:
        pass

    def stop_server(self) -> Dict:
        pass

    def restart_server(self) -> Dict:
        pass

    def incidences(self) -> Dict:
        pass

    def timings(self) -> Dict:
        pass

    def backup_list(self) -> Dict:
        pass

    def backup_create(self) -> Dict:
        pass

    def backup_delete(self) -> Dict:
        pass
