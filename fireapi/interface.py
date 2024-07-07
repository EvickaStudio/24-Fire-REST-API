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
