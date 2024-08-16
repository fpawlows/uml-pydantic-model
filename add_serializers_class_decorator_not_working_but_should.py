from typing import List, Union, Callable, Type
from pydantic import BaseModel, field_serializer
from pydantic_model import (
    UmlPrimitiveType,
    UmlClass,
    UmlInterface,
    UmlDataType,
    UmlEnumeration,
    UmlVisibilityEnum,
)


class UmlElement(BaseModel):
    id: str


class UmlIdReference(BaseModel):
    idref: str

    @classmethod
    def from_uml_element(
        cls: Type["UmlIdReference"], element: "UmlElement"
    ) -> "UmlIdReference":
        return cls(idref=element.id)


def pydantic_field_serializer_func(
    field: Union["UmlElement", "UmlIdReference"]
) -> dict:
    return (
        UmlIdReference.from_uml_element(field).model_dump()
        if isinstance(field, UmlElement)
        else field.model_dump()
    )


def serialize_fields_to_id_reference(fields: List[str]) -> Callable:
    def decorator(original_class: Type[BaseModel]) -> Type[BaseModel]:
        for field in fields:
            field_serializer_func = field_serializer(field)(
                pydantic_field_serializer_func
            )
            field_serializer_func_name = f"{field}_to_json"
            setattr(original_class, field_serializer_func_name, field_serializer_func)

        return original_class

    return decorator


# This works
class UmlAttribute(UmlElement):
    type: Union[
        "UmlPrimitiveType",
        "UmlClass",
        "UmlInterface",
        "UmlDataType",
        "UmlEnumeration",
        "UmlIdReference",
    ]
    visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC

    @field_serializer("type")
    def type_to_json(
        type: Union[
            "UmlPrimitiveType",
            "UmlClass",
            "UmlInterface",
            "UmlDataType",
            "UmlEnumeration",
            "UmlIdReference",
        ]
    ) -> dict:
        return pydantic_field_serializer_func(type)


# This does not work
@serialize_fields_to_id_reference(["type"])
class UmlParameter(UmlElement):
    type: Union[
        "UmlPrimitiveType",
        "UmlClass",
        "UmlInterface",
        "UmlDataType",
        "UmlEnumeration",
        "UmlIdReference",
    ]


attribute = UmlAttribute(
    id="attribute_id",
    type=UmlPrimitiveType(id="primitive_type_id", name="primitive_type_name"),
)
parameter = UmlParameter(
    id="parameter_id",
    type=UmlPrimitiveType(id="primitive_type_id", name="primitive_type_name"),
)

class1 = UmlClass(id="class_id", name="class_name", attributes=[attribute])
class2 = UmlClass(id="class_id", name="class_name", attributes=[attribute])


print("\nattribute")
print(attribute)
print(attribute.model_dump())

print("\nparameter")
print(parameter)
print(parameter.model_dump())


print("\nclass1")
print(class1)
print(class1.model_dump())
