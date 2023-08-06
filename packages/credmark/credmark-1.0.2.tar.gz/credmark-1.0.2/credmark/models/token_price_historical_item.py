from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="TokenPriceHistoricalItem")


@attr.s(auto_attribs=True)
class TokenPriceHistoricalItem:
    """
    Attributes:
        block_number (float): Block number. Example: 15490034.
        block_timestamp (float): Block timestamp. Number of seconds since January 1, 1970. Example: 1662550007.
        price (float): Price of the token in quote units. Example: 82.82911921.
        src (str): Source of the token price. Example: dex or cex.
        src_internal (str): The internal source for tracing Example: db, model, cache, etc..
    """

    block_number: float
    block_timestamp: float
    price: float
    src: str
    src_internal: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        block_number = self.block_number
        block_timestamp = self.block_timestamp
        price = self.price
        src = self.src
        src_internal = self.src_internal

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
                "price": price,
                "src": src,
                "srcInternal": src_internal,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        block_number = d.pop("blockNumber")

        block_timestamp = d.pop("blockTimestamp")

        price = d.pop("price")

        src = d.pop("src")

        src_internal = d.pop("srcInternal")

        token_price_historical_item = cls(
            block_number=block_number,
            block_timestamp=block_timestamp,
            price=price,
            src=src,
            src_internal=src_internal,
        )

        token_price_historical_item.additional_properties = d
        return token_price_historical_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
