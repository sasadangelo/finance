from typing import TypeAlias
from werkzeug.wrappers.response import Response


# Type aliases for Flask response types
WebResponse: TypeAlias = str | Response  # HTML pages (templates or redirects)
APIResponse: TypeAlias = tuple[Response, int]  # JSON API with explicit status code
