from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="TokenHolder")


@attr.s(auto_attribs=True)
class TokenHolder:
    """
    Attributes:
        address (str): Account address
        balance (float): Token balance Example: 248367.58266143446.
        value (float): Token value in quoted currency. Example: 18990392.724937014.
    """

    address: str
    balance: float
    value: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address = self.address
        balance = self.balance
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address": address,
                "balance": balance,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address = d.pop("address")

        balance = d.pop("balance")

        value = d.pop("value")

        token_holder = cls(
            address=address,
            balance=balance,
            value=value,
        )

        token_holder.additional_properties = d
        return token_holder

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
