from typing import Protocol
from controllers import EtfController, QuoteController


class ApplicationContainer(Protocol):
    etf_controller: EtfController
    quote_controller: QuoteController
