from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelMetadata")


@attr.s(auto_attribs=True)
class ModelMetadata:
    """
    Attributes:
        name (str): Short identifying name for the model Example: var.
        display_name (Union[Unset, str]): Name of the model Example: VAR.
        description (Union[Unset, str]): A short description of the model Example: Value at Risk.
        developer (Union[Unset, str]): Name of the developer Example: Credmark.
        input (Union[Unset, Dict[str, Any]]): Model input JSON schema
        output (Union[Unset, Dict[str, Any]]): Model output JSON schema
        error (Union[Unset, Dict[str, Any]]): Model error JSON schema
    """

    name: str
    display_name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    developer: Union[Unset, str] = UNSET
    input: Union[Unset, Dict[str, Any]] = UNSET
    output: Union[Unset, Dict[str, Any]] = UNSET
    error: Union[Unset, Dict[str, Any]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        display_name = self.display_name
        description = self.description
        developer = self.developer
        input = self.input
        output = self.output
        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if description is not UNSET:
            field_dict["description"] = description
        if developer is not UNSET:
            field_dict["developer"] = developer
        if input is not UNSET:
            field_dict["input"] = input
        if output is not UNSET:
            field_dict["output"] = output
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        display_name = d.pop("displayName", UNSET)

        description = d.pop("description", UNSET)

        developer = d.pop("developer", UNSET)

        input = d.pop("input", UNSET)

        output = d.pop("output", UNSET)

        error = d.pop("error", UNSET)

        model_metadata = cls(
            name=name,
            display_name=display_name,
            description=description,
            developer=developer,
            input=input,
            output=output,
            error=error,
        )

        model_metadata.additional_properties = d
        return model_metadata

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
