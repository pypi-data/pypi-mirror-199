import os
from hashlib import sha256
from typing import Dict, Optional, Union, cast

from chaosaddons.controls import safeguards
from chaoslib.run import RunEventHandler
from chaoslib.types import (
    Configuration,
    Experiment,
    Extension,
    Journal,
    Secrets,
)
from logzero import logger


###############################################################################
# Private
###############################################################################
class ReliablySafeguardHandler(RunEventHandler):  # type: ignore
    def __init__(
        self,
        url: Union[str, Dict[str, str]],
        auth: Optional[Union[str, Dict[str, str]]],
        frequency: Optional[Union[float, Dict[str, str]]],
        configuration: Configuration,
        secrets: Secrets,
    ) -> None:
        RunEventHandler.__init__(self)
        self.configuration = configuration
        self.secrets = secrets

        url = get_value(url)  # type: ignore
        auth = get_value(auth)  # type: ignore

        if frequency is not None:
            frequency = max(float(get_value(frequency)), 0.3)  # type: ignore

        if not url:
            logger.debug("Missing URl for safeguard/precheck call")
            return None

        name = f"precheck-{sha256(url.encode()).hexdigest()}"  # type: ignore
        self.probes = [
            {
                "name": name,
                "type": "probe",
                "tolerance": True,
                "provider": {
                    "type": "python",
                    "module": "chaosreliably.activities.safeguard.probes",
                    "func": "call_endpoint",
                    "arguments": {"url": url, "auth": auth},
                },
            }
        ]

        if frequency:
            self.probes[0]["frequency"] = frequency

        self.guardian = safeguards.Guardian()
        self.guardian.prepare(self.probes)

    def started(self, experiment: Experiment, journal: Journal) -> None:
        self.guardian.run(
            experiment,
            self.probes,
            self.configuration or {},
            self.secrets or {},
            None,
        )

    def finish(self, journal: Journal) -> None:
        self.guardian.terminate()


def find_extension_by_name(
    experiment: Experiment, name: str
) -> Optional[Extension]:
    extensions = experiment.get("extensions")
    if not extensions:
        return None

    for extension in extensions:
        if extension["name"] == name:
            return cast(Extension, extension)

    return None


def get_value(value: Union[str, Dict[str, str]]) -> Optional[str]:
    if not value:
        return None

    if isinstance(value, str):
        return value

    if isinstance(value, float):
        return str(value)

    if value.get("type") == "env":
        return os.getenv(value["key"])

    return None
