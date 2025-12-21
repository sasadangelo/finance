# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from __future__ import annotations
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.etf_controller import EtfController
    from controllers.quote_controller import QuoteController
    from controllers.index_controller import IndexController
    from services.update_quotes_cronjob import UpdateQuotesCronJob


# Protocol for type-safe access to controllers and cron jobs attached to Flask app
class ApplicationContainer(Protocol):
    """Protocol defining the structure of the Flask app with attached controllers and cron jobs."""

    etf_controller: EtfController
    quote_controller: QuoteController
    index_controller: IndexController
    update_quotes_cronjob: UpdateQuotesCronJob
