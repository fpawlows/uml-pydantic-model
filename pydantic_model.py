import json
import uuid
from typing import List, Optional, Union, Type, Dict, Any
from pydantic import BaseModel, Field, field_serializer, model_validator
from enum import Enum


def serialize_field_to_id_reference(
    field: Optional[Union["UmlElement", "UmlIdReference"]]
) -> dict:
    if field is None:
        return None
    
    return (
        UmlIdReference.from_uml_element(field).model_dump()
        if isinstance(field, UmlElement)
        else field.model_dump()
    )


class UmlIdReference(BaseModel):
    idref: str

    @classmethod
    def from_uml_element(
        cls: Type["UmlIdReference"], element: "UmlElement"
    ) -> "UmlIdReference":
        return cls(idref=element.id)
    
    def __hash__(self) -> int:
        return hash(self.idref)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, UmlElement):
            return self.idref == other.id
        
        elif isinstance(other, UmlIdReference):
            return self.idref == other.idref
        
        return False

class UmlVisibilityEnum(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"


class UmlMultiplicityEnum(str, Enum):
    ZERO_OR_ONE = "0..1"
    ONE = "1"
    ZERO_OR_MORE = "0..*"
    ONE_OR_MORE = "1..*"


class UmlAssociationTypeEnum(str, Enum):
    ASSOCIATION = "association"
    AGGREGATION = "aggregation"
    COMPOSITION = "composition"


class UmlAssociationDirectionEnum(str, Enum):
    UNDIRECTED = "undirected"
    DIRECTED = "directed"


class UmlInteractionOperatorEnum(str, Enum):
    ALT = "alt"
    BREAK = "break"
    CRITICAL = "critical"
    ELSE = "else"
    IGNORE = "ignore"
    LOOP = "loop"
    PAR = "par"
    STRICT = "strict"
    NEG = "neg"
    ASSERT = "assert"
    REF = "ref"
    SEQ = "seq"
    SD = "sd"
    OPT = "opt"


class UmlElement(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class UmlNamedElement(UmlElement):
    name: Optional[str] = None
    visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC


class UmlAttribute(UmlNamedElement):
    type: Union[
        "UmlPrimitiveType",
        "UmlClass",
        "UmlInterface",
        "UmlDataType",
        "UmlEnumeration",
        "UmlIdReference",
    ]
    is_static: Optional[bool] = None
    is_ordered: Optional[bool] = None
    is_unique: Optional[bool] = None
    is_read_only: Optional[bool] = None
    is_query: Optional[bool] = None
    is_derived: Optional[bool] = None
    is_derived_union: Optional[bool] = None

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
        return serialize_field_to_id_reference(type)


class UmlParameter(UmlNamedElement):
    type: Union[
        "UmlPrimitiveType",
        "UmlClass",
        "UmlInterface",
        "UmlDataType",
        "UmlEnumeration",
        "UmlIdReference",
    ]

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
        return serialize_field_to_id_reference(type)


class UmlOperation(UmlNamedElement):
    parameters: List[UmlParameter] = Field(default_factory=list)
    return_type: Optional[
        Union[
            "UmlPrimitiveType",
            "UmlClass",
            "UmlInterface",
            "UmlDataType",
            "UmlEnumeration",
            "UmlIdReference",
        ]
    ] = None
    is_static: Optional[bool] = None
    is_ordered: Optional[bool] = None
    is_unique: Optional[bool] = None
    is_query: Optional[bool] = None
    is_derived: Optional[bool] = None
    is_derived_union: Optional[bool] = None
    is_abstract: bool = False
    exceptions: List[str] = Field(default_factory=list)

    @field_serializer("return_type")
    def return_type_to_json(
        return_type: Optional[
            Union[
                "UmlPrimitiveType",
                "UmlClass",
                "UmlInterface",
                "UmlDataType",
                "UmlEnumeration",
                "UmlIdReference",
            ]
        ]
    ) -> dict:
        return serialize_field_to_id_reference(return_type)


class UmlClassifier(UmlNamedElement):
    attributes: List[UmlAttribute] = Field(default_factory=list)
    operations: List[UmlOperation] = Field(default_factory=list)


class UmlClass(UmlClassifier):
    generalizations: List[Union["UmlGeneralization", "UmlIdReference"]] = Field(
        default_factory=list
    )
    interfaces: List[Union["UmlRealization", "UmlIdReference"]] = Field(
        default_factory=list
    )

    @field_serializer("generalizations")
    def generalizations_to_json(generalizations: List[UmlIdReference]) -> List[dict]:
        return [
            serialize_field_to_id_reference(super_class)
            for super_class in generalizations
        ]

    @field_serializer("interfaces")
    def interfaces_to_json(interfaces: List[UmlIdReference]) -> List[dict]:
        return [serialize_field_to_id_reference(interface) for interface in interfaces]


class UmlInterface(UmlClassifier):
    pass


class UmlDataType(UmlNamedElement):
    pass


class UmlEnumeration(UmlNamedElement):
    literals: List[str] = Field(default_factory=list)


class UmlPrimitiveTypeTypesEnum(str, Enum):
    BOOLEAN = "boolean"
    INTEGER = "integer"
    REAL = "real"
    STRING = "string"
    UNLIMITED_NATURAL = "unlimited_natural"


class UmlPrimitiveType(UmlNamedElement):
    type: UmlPrimitiveTypeTypesEnum | str


class UmlAssociationEnd(UmlElement):
    multiplicity: UmlMultiplicityEnum = UmlMultiplicityEnum.ONE
    object: Union[
        "UmlPrimitiveType",
        "UmlClass",
        "UmlInterface",
        "UmlDataType",
        "UmlEnumeration",
        "UmlAttribute",
        "UmlIdReference",
    ]
    role: Optional[str] = None
    navigability: bool = True

    @field_serializer("object")
    def object_to_json(
        object: Union[
            "UmlPrimitiveType",
            "UmlClass",
            "UmlInterface",
            "UmlDataType",
            "UmlEnumeration",
            "UmlAttribute",
            "UmlIdReference",
        ]
    ) -> dict:
        return serialize_field_to_id_reference(object)


class UmlAssociation(UmlNamedElement):
    end1: Union["UmlAssociationEnd", "UmlIdReference"]
    end2: Union["UmlAssociationEnd", "UmlIdReference"]

    @field_serializer("end1")
    def end1_to_json(end1: Union["UmlAssociationEnd", "UmlIdReference"]) -> dict:
        return serialize_field_to_id_reference(end1)

    @field_serializer("end2")
    def end2_to_json(end2: Union["UmlAssociationEnd", "UmlIdReference"]) -> dict:
        return serialize_field_to_id_reference(end2)


class UmlDirectedAssociation(UmlNamedElement):
    source: Union["UmlAssociationEnd", "UmlIdReference"]
    target: Union["UmlAssociationEnd", "UmlIdReference"]

    @field_serializer("source")
    def source_to_json(source: Union["UmlAssociationEnd", "UmlIdReference"]) -> dict:
        return serialize_field_to_id_reference(source)

    @field_serializer("target")
    def target_to_json(target: Union["UmlAssociationEnd", "UmlIdReference"]) -> dict:
        return serialize_field_to_id_reference(target)


class UmlAggregation(UmlDirectedAssociation):
    pass


class UmlComposition(UmlDirectedAssociation):
    pass


class UmlDependency(UmlNamedElement):
    supplier: Union["UmlClass", "UmlInterface", "UmlIdReference"]
    client: Union["UmlClass", "UmlInterface", "UmlIdReference"]

    @field_serializer("supplier")
    def supplier_to_json(
        supplier: Union["UmlClass", "UmlInterface", "UmlIdReference"]
    ) -> dict:
        return serialize_field_to_id_reference(supplier)

    @field_serializer("client")
    def client_to_json(
        client: Union["UmlClass", "UmlInterface", "UmlIdReference"]
    ) -> dict:
        return serialize_field_to_id_reference(client)


class UmlRealization(UmlDependency):
    pass


class UmlGeneralization(UmlNamedElement):
    specific: Union["UmlClass", "UmlInterface", "UmlIdReference"]
    general: Union["UmlClass", "UmlInterface", "UmlIdReference"]

    @field_serializer("specific")
    def specific_to_json(
        specific: Union["UmlClass", "UmlInterface", "UmlIdReference"]
    ) -> dict:
        return serialize_field_to_id_reference(specific)

    @field_serializer("general")
    def general_to_json(
        general: Union["UmlClass", "UmlInterface", "UmlIdReference"]
    ) -> dict:
        return serialize_field_to_id_reference(general)


class UmlOccurrenceSpecification(UmlElement):
    covered: Union["UmlLifeline", "UmlIdReference"]

    @field_serializer("covered")
    def covered_to_json(
        covered: Union["UmlLifeline", "UmlIdReference"]
    ) -> dict:
        return serialize_field_to_id_reference(covered)
    

class UmlCombinedFragment(UmlNamedElement):
    covered: List[Union["UmlLifeline", "UmlIdReference"]] = Field(default_factory=list)
    operands: List["UmlOperand"] = Field(default_factory=list)
    operator: UmlInteractionOperatorEnum

    @field_serializer("covered")
    def covered_to_json(
        covered: List[Union["UmlLifeline", "UmlIdReference"]]
    ) -> List[dict]:
        return [serialize_field_to_id_reference(lifeline) for lifeline in covered]
    

class UmlOperand(UmlElement):
    fragments: List[Union["UmlOccurrenceSpecification", "UmlCombinedFragment"]] = Field(
        default_factory=list
    )
    guard: Optional[str] = None


class UmlLifeline(UmlNamedElement):
    represents: Union["UmlClass", "UmlInterface", "UmlIdReference"]

    @field_serializer("represents")
    def represents_to_json(
        represents: Union["UmlClass", "UmlInterface", "UmlIdReference"]
    ) -> dict:
        return serialize_field_to_id_reference(represents)


class UmlMessageSortEnum(str, Enum):
    SYNCH_CALL = "synchCall"
    ASYNCH_CALL = "asynchCall"
    REPLY = "reply"
    CREATE = "create"
    DELETE = "delete"


class UmlMessageKindEnum(str, Enum):
    COMPLETE = "complete"
    LOST = "lost"
    FOUND = "found"
    UNKNOWN = "unknown"


class UmlMessage(UmlNamedElement):
    send_event: Union["UmlOccurrenceSpecification", "UmlIdReference"]
    receive_event: Union["UmlOccurrenceSpecification", "UmlIdReference"]
    signature: Optional[Union["UmlOperation", "UmlIdReference"]] = None
    arguments: Optional[List[str]] = Field(default_factory=list)
    sort: UmlMessageSortEnum = UmlMessageSortEnum.SYNCH_CALL
    kind: UmlMessageKindEnum = UmlMessageKindEnum.COMPLETE
    

    @field_serializer("send_event")
    def send_event_to_json(
        send_event: Union["UmlOccurrenceSpecification", "UmlIdReference"]
    ) -> dict:
        return serialize_field_to_id_reference(send_event)
    
    @field_serializer("receive_event")
    def receive_event_to_json(
        receive_event: Union["UmlOccurrenceSpecification", "UmlIdReference"]
    ) -> dict:
        return serialize_field_to_id_reference(receive_event)
    
    @field_serializer("signature")
    def signature_to_json(
        signature: Union["UmlOperation", "UmlIdReference"]
    ) -> dict:
        return serialize_field_to_id_reference(signature)
    


class UmlInteraction(UmlNamedElement):
    lifelines: List[UmlLifeline] = Field(default_factory=list)
    messages: List[UmlMessage] = Field(default_factory=list)
    fragments: List[Union["UmlOccurrenceSpecification", "UmlCombinedFragment"]] = Field(
        default_factory=list
    )
    """
    Fragments are used to represent the different types of events that can occur in an interaction.
    Their order is important and they can be nested.
    """


class UmlModelElements(BaseModel):
    classes: List[UmlClass] = Field(default_factory=list)
    interfaces: List[UmlInterface] = Field(default_factory=list)
    dataTypes: List[UmlDataType] = Field(default_factory=list)
    enumerations: List[UmlEnumeration] = Field(default_factory=list)
    primitiveTypes: List[UmlPrimitiveType] = Field(default_factory=list)
    associations: List[UmlAssociation] = Field(default_factory=list)
    generalizations: List[UmlGeneralization] = Field(default_factory=list)
    dependencies: List[UmlDependency] = Field(default_factory=list)
    realizations: List[UmlRealization] = Field(default_factory=list)
    interactions: List[UmlInteraction] = Field(default_factory=list)



    @model_validator(mode="before")
    def check_unique_ids(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        id_map: Dict[str, UmlElement] = {}

        def collect_ids(element: UmlElement):
            if isinstance(element, UmlElement):
                if element.id in id_map:
                    if id_map[element.id] != element:
                        raise ValueError(f"Duplicate id found with different objects: {element.id}")
                else:
                    id_map[element.id] = element

                # Recursively check nested objects like attributes, operations, etc.
                for field_name, field_value in element.__dict__.items():
                    if isinstance(field_value, list):
                        for item in field_value:
                            collect_ids(item)
                    elif isinstance(field_value, UmlElement):
                        collect_ids(field_value)

        # Iterate through each type of element in UmlModelElements
        for element_list in values.values():
            if isinstance(element_list, list):
                for element in element_list:
                    collect_ids(element)

        return values
    


class UmlModel(UmlElement):
    elements: UmlModelElements




print("\nmodel.model_json_schema")
with open("model-notation.json", "w") as f:
    f.write(json.dumps(UmlModel.model_json_schema(), indent=2))

