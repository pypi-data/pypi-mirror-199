from hashlib import sha256
from typing import Optional, cast

from chaosaddons.controls import safeguards
from chaoslib.run import RunEventHandler
from chaoslib.types import (
    Configuration,
    Experiment,
    Extension,
    Journal,
    Secrets,
)


###############################################################################
# Private
###############################################################################
class ReliablySafeguardHandler(RunEventHandler):  # type: ignore
    def __init__(
        self,
        url: str,
        auth: Optional[str],
        frequency: Optional[float],
        configuration: Configuration,
        secrets: Secrets,
    ) -> None:
        RunEventHandler.__init__(self)
        self.configuration = configuration
        self.secrets = secrets

        self.probes = [
            {
                "name": f"precheck-{sha256(url.encode('utf-8')).hexdigest()}",
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
