from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="TokenTotalSupplyHistoricalItem")


@attr.s(auto_attribs=True)
class TokenTotalSupplyHistoricalItem:
    """
    Attributes:
        block_number (float): Block number. Example: 15490034.
        block_timestamp (float): Block timestamp. Number of seconds since January 1, 1970. Example: 1662550007.
        total_supply (float): Token total supply Example: 16000000.
    """

    block_number: float
    block_timestamp: float
    total_supply: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        block_number = self.block_number
        block_timestamp = self.block_timestamp
        total_supply = self.total_supply

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
                "totalSupply": total_supply,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        block_number = d.pop("blockNumber")

        block_timestamp = d.pop("blockTimestamp")

        total_supply = d.pop("totalSupply")

        token_total_supply_historical_item = cls(
            block_number=block_number,
            block_timestamp=block_timestamp,
            total_supply=total_supply,
        )

        token_total_supply_historical_item.additional_properties = d
        return token_total_supply_historical_item

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
