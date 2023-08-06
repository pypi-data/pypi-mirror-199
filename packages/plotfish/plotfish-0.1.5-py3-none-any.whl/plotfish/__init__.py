__version__ = "0.1.0"

from decimal import Decimal
from datetime import datetime, timezone
import time
from typing import Union, Optional, Dict, Any
import os
import logging
import socketio
from enum import Enum
import json

NumberLike = Union[int, float, Decimal]
TimestampLike = Union[int, float, datetime]

# Configuration
api_key = os.environ.get("PLOTFISH_API_KEY")
riverbed_url = os.environ.get("RIVERBED_URL") or "https://api.plot.fish"

logger = logging.getLogger(__name__)


class PlotfishError(RuntimeError):
    """For Plotfish SDK related exceptions"""


socket = socketio.Client(logger=logger)

plots: Dict[str, object] = {}

# TODO: is it possible to get mypy?


class PlotType(str, Enum):
    Line = "line"
    ProgressBar = "progress_bar"
    Counter = "counter"


# TODO: don't throw exceptions; or at least be more careful about error handling
# TODO: move into seperate thread


def _set_plot_metadata(
    name: str, plot_type: PlotType, **kwargs: Dict[str, Any]
) -> None:
    if name in plots and plots[name]["type"] != plot_type:
        # TODO: this check needs to exist in the backend too
        raise PlotfishError("Cannot change plot type after creating")
    metadata = {"type": plot_type, **kwargs}
    # TODO: how to decide when to dedupe plot metadata?
    # if name not in plots or plots[name] != metadata:
    #     # TODO: need to dedupe on backend too; in general i'm doing a lot of prototyping
    #     # in the client that should eventually be moved to backend
    #     plots[name] = metadata
    #     socket.emit("updatePlotMetadata", (name, json.dumps(metadata)))

    socket.emit("updatePlotMetadata", (name, json.dumps(metadata)))


def _connect() -> None:
    if not socket.connected:
        if api_key is None:
            raise PlotfishError("api_key cannot be null.")

        if riverbed_url is None:
            raise PlotfishError("riverbed_url cannot be null.")

        socket.connect(url=riverbed_url, auth={"apiKey": api_key})


def _record_datapoint(
    label: str,
    value: NumberLike,
    timestamp: Optional[TimestampLike] = None,
) -> None:
    if not socket.connected:
        if api_key is None:
            raise PlotfishError("api_key cannot be null.")

        if riverbed_url is None:
            raise PlotfishError("riverbed_url cannot be null.")

        socket.connect(url=riverbed_url, auth={"apiKey": api_key})

    if isinstance(timestamp, datetime):
        timestamp = timestamp.replace(tzinfo=timezone.utc).timestamp()
    elif isinstance(timestamp, int):
        timestamp = float(timestamp)
    elif timestamp is None:
        timestamp = time.time()

    socket.emit("recordDatapoints", (label, [[timestamp, value, None]]))


def line(
    name: str, value: NumberLike, timestamp: Optional[TimestampLike] = None
) -> None:
    _connect()
    _set_plot_metadata(name, PlotType.Line)
    _record_datapoint(name, value, timestamp)


def progress(name: str, value: NumberLike, total: Optional[NumberLike] = None) -> None:
    _connect()
    _set_plot_metadata(name, PlotType.ProgressBar, total=total)
    _record_datapoint(name, value, None)


def count(
    name: str, change: NumberLike, timestamp: Optional[TimestampLike] = None
) -> None:
    _connect()
    _set_plot_metadata(name, PlotType.Counter)
    _record_datapoint(name, change, timestamp)


# TODO: implement HTTP requests so that I can do actual sensible request-response (or just look up
# how to do it with socket io...maybe someone's figured it out)


def increment(name: str, timestamp: Optional[TimestampLike] = None) -> None:
    _connect()
    _set_plot_metadata(name, PlotType.Counter)
    _record_datapoint(name, 1, timestamp)
