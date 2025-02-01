# code/src/rptgen1/uno_client_config.py

from dataclasses import dataclass


@dataclass
class UnoClientConfig:
    server: str = "127.0.0.1"
    port: str = "2003"
    host_location: str = "auto"  # Possible values: "auto", "remote", "local", "process"
