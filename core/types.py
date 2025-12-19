from typing import Protocol
from controllers import EtfController


class ApplicationContainer(Protocol):
    etf_controller: EtfController
