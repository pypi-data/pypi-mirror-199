from typing import Any, List, Dict, TypedDict, Union
from typing_extensions import Required


class PayloadV3(TypedDict, total=False):
    """payload_v3."""

    subscription_id: Required[str]
    """
    minLength: 1

    Required property
    """

    request: Required[Dict[str, Any]]
    """Required property"""

    result: Required["_PayloadV3Result"]
    """Required property"""

    timestamp: Required[str]
    """Required property"""

    entity: Required[str]
    """
    minLength: 1

    Required property
    """



class SubscriptionResults(TypedDict, total=False):
    """subscription_results."""

    version: Required[int]
    """Required property"""

    payload: Required["PayloadV3"]
    """Required property"""



class _PayloadV3Result(TypedDict, total=False):
    data: Required[List["_PayloadV3ResultDataItem"]]
    """
    minItems: 0

    Required property
    """



_PayloadV3ResultDataItem = Dict[str, Union[Union[int, float], None]]
"""minProperties: 1"""

