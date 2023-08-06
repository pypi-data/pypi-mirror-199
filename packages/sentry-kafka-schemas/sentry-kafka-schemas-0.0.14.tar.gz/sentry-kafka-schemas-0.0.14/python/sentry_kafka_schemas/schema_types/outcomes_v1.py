from typing import TypedDict, Union
from typing_extensions import Required


class Outcome(TypedDict, total=False):
    """outcome."""

    timestamp: Required[str]
    """Required property"""

    org_id: Required[Union[int, None]]
    """Required property"""

    project_id: Required[Union[int, None]]
    """Required property"""

    key_id: Required[Union[str, None]]
    """Required property"""

    outcome: Required[int]
    """Required property"""

    reason: Required[Union[str, None]]
    """Required property"""

    event_id: Required[Union[str, None]]
    """Required property"""

    category: Required[Union[int, None]]
    """Required property"""

    quantity: Required[Union[int, None]]
    """Required property"""

