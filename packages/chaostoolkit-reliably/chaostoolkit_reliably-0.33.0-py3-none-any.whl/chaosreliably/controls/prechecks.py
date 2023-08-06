from typing import Any, Optional

from chaoslib.run import EventHandlerRegistry
from chaoslib.types import Configuration, Secrets
from logzero import logger

from . import ReliablySafeguardHandler

__all__ = ["configure_control"]


def configure_control(
    event_registry: EventHandlerRegistry,
    url: str,
    auth: Optional[str] = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
    **kwargs: Any,
) -> None:
    logger.debug("Configure Reliably's prechecks control")

    event_registry.register(
        ReliablySafeguardHandler(url, auth, None, configuration, secrets)
    )
