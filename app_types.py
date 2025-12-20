# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.etf_controller import EtfController
    from controllers.quote_controller import QuoteController


# Protocol for type-safe access to controllers attached to Flask app
class ApplicationContainer(Protocol):
    """Protocol defining the structure of the Flask app with attached controllers."""

    etf_controller: "EtfController"
    quote_controller: "QuoteController"


# Made with Bob
