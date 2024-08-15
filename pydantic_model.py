import json
import uuid
from typing import List, Any, Type, Optional, Union, Callable
from functools import wraps


from pydantic import BaseModel, Field, model_serializer, field_serializer, model_validator, field_validator
from enum import Enum


def serialize_field_to_id_reference(field: Union['UmlElement', 'UmlIdReference']) -> dict:
    return UmlIdReference.from_uml_element(field).model_dump() if isinstance(field, UmlElement) else field.model_dump()


class UmlIdReference(BaseModel):
    idref: str
    
    @classmethod
    def from_uml_element(cls: Type['UmlIdReference'], element: 'UmlElement') -> 'UmlIdReference':
        return cls(idref=element.id)


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
    name: Optional[str]


class UmlAttribute(UmlNamedElement):
    type: Union['UmlPrimitiveType', 'UmlClass', 'UmlInterface', 'UmlDataType', 'UmlEnumeration', 'UmlIdReference'] 
    visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC
    is_static: Optional[bool] = None
    is_ordered: Optional[bool] = None
    is_unique: Optional[bool] = None
    is_read_only: Optional[bool] = None
    is_query: Optional[bool] = None
    is_derived: Optional[bool] = None
    is_derived_union: Optional[bool] = None

    @field_serializer("type")
    def type_to_json(type: Union['UmlPrimitiveType', 'UmlClass', 'UmlInterface', 'UmlDataType', 'UmlEnumeration', 'UmlIdReference']) -> dict:
        return serialize_field_to_id_reference(type)

            
class UmlParameter(UmlNamedElement):
    type: Union['UmlPrimitiveType', 'UmlClass', 'UmlInterface', 'UmlDataType', 'UmlEnumeration', 'UmlIdReference'] 

    @field_serializer("type")
    def type_to_json(type: Union['UmlPrimitiveType', 'UmlClass', 'UmlInterface', 'UmlDataType', 'UmlEnumeration', 'UmlIdReference']) -> dict:
        return serialize_field_to_id_reference(type)
    

class UmlOperation(UmlNamedElement):
    parameters: List[UmlParameter] = Field(default_factory=list)
    return_type: Optional[Union['UmlPrimitiveType', 'UmlClass', 'UmlInterface', 'UmlDataType', 'UmlEnumeration', 'UmlIdReference']] 
    visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC
    is_static: Optional[bool] = None
    is_ordered: Optional[bool] = None
    is_unique: Optional[bool] = None
    is_query: Optional[bool] = None
    is_derived: Optional[bool] = None
    is_derived_union: Optional[bool] = None
    is_abstract: bool = False
    exceptions: List[str] = Field(default_factory=list)

    @field_serializer("return_type")
    def return_type_to_json(return_type: Optional[Union['UmlPrimitiveType', 'UmlClass', 'UmlInterface', 'UmlDataType', 'UmlEnumeration', 'UmlIdReference']]) -> dict:
        return serialize_field_to_id_reference(return_type)
    


class UmlClassifier(UmlNamedElement):
    visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC
    attributes: List[UmlAttribute] = Field(default_factory=list)
    operations: List[UmlOperation] = Field(default_factory=list)


class UmlClass(UmlClassifier):
    generalizations: List[Union['UmlGeneralization', 'UmlIdReference']] = Field(default_factory=list) 
    interfaces: List[Union['UmlRealization', 'UmlIdReference']] = Field(default_factory=list) 

    @field_serializer("generalizations")
    def generalizations_to_json(generalizations: List[UmlIdReference]) -> List[dict]:
        return [serialize_field_to_id_reference(super_class) for super_class in generalizations]
    
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
    object: Union['UmlPrimitiveType', 'UmlClass', 'UmlInterface', 'UmlDataType', 'UmlEnumeration', 'UmlAttribute', 'UmlIdReference']
    role: Optional[str] = None
    navigability: bool = True

    @field_serializer("object")
    def object_to_json(object: Union['UmlPrimitiveType', 'UmlClass', 'UmlInterface', 'UmlDataType', 'UmlEnumeration', 'UmlAttribute', 'UmlIdReference']) -> dict:
        return serialize_field_to_id_reference(object)
    

class UmlAssociation(UmlNamedElement):
    end1: Union['UmlAssociationEnd', 'UmlIdReference']
    end2: Union['UmlAssociationEnd', 'UmlIdReference']

    @field_serializer("end1")
    def end1_to_json(end1: Union['UmlAssociationEnd', 'UmlIdReference']) -> dict:
        return serialize_field_to_id_reference(end1)
    
    @field_serializer("end2")
    def end2_to_json(end2: Union['UmlAssociationEnd', 'UmlIdReference']) -> dict:
        return serialize_field_to_id_reference(end2)
    

class UmlDirectedAssociation(UmlNamedElement):
    source: Union['UmlAssociationEnd', 'UmlIdReference']
    target: Union['UmlAssociationEnd', 'UmlIdReference']

    @field_serializer("source")
    def source_to_json(source: Union['UmlAssociationEnd', 'UmlIdReference']) -> dict:
        return serialize_field_to_id_reference(source)
    
    @field_serializer("target")
    def target_to_json(target: Union['UmlAssociationEnd', 'UmlIdReference']) -> dict:
        return serialize_field_to_id_reference(target)


class Aggregation(UmlDirectedAssociation):
    pass

class UmlComposition(UmlDirectedAssociation):
    pass


class UmlDependency(UmlNamedElement):
    supplier: Union['UmlClass', 'UmlInterface', 'UmlIdReference']
    client: Union['UmlClass', 'UmlInterface', 'UmlIdReference']

    @field_serializer("supplier")
    def supplier_to_json(supplier: Union['UmlClass', 'UmlInterface', 'UmlIdReference']) -> dict:
        return serialize_field_to_id_reference(supplier)
    
    @field_serializer("client")
    def client_to_json(client: Union['UmlClass', 'UmlInterface', 'UmlIdReference']) -> dict:
        return serialize_field_to_id_reference(client)

class UmlRealization(UmlDependency):
    pass


class UmlGeneralization(UmlNamedElement):
    specific: Union['UmlClass', 'UmlInterface', 'UmlIdReference']
    general: Union['UmlClass', 'UmlInterface', 'UmlIdReference']

    @field_serializer("specific")
    def specific_to_json(specific: Union['UmlClass', 'UmlInterface', 'UmlIdReference']) -> dict:
        return serialize_field_to_id_reference(specific)
    
    @field_serializer("general")
    def general_to_json(general: Union['UmlClass', 'UmlInterface', 'UmlIdReference']) -> dict:
        return serialize_field_to_id_reference(general)



class UmlMessage(UmlNamedElement):
    sender: UmlIdReference  # Reference to UmlLifeline id
    receiver: UmlIdReference  # Reference to UmlLifeline id
    content: str
    timestamp: str

class UmlFragment(UmlNamedElement):
    type: str
    interaction_operator: str
    covered: List[UmlIdReference] = Field(default_factory=list) 
    messages: List[UmlMessage] = Field(default_factory=list)

class UmlOperand(UmlNamedElement):
    guard: str
    fragments: List[UmlFragment] = Field(default_factory=list)

class UmlInteraction(UmlNamedElement):
    lifelines: List[UmlIdReference] = Field(default_factory=list) 
    messages: List[UmlMessage] = Field(default_factory=list)
    fragments: List[UmlFragment] = Field(default_factory=list)
    operands: List[UmlOperand] = Field(default_factory=list)

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



class UmlModel(UmlElement):
    elements: UmlModelElements


# Example usage
class1 = UmlClass(id="class1", name="Person")
class2 = UmlClass(id="class2", name="Address")
class1.attributes.append(UmlAttribute(name="name", type=class2))
class2.attributes.append(UmlAttribute(name="street", type=class1))
model = UmlModel(
    elements=UmlModelElements(
        classes=[
            class1,
            UmlClass(id="class1", name="Person", attributes=[UmlAttribute(name="name", type=class1)]),
            UmlClass(id="class2", name="Address"),
        ],
        associations=[
            UmlAssociation(
                id="assoc1",
                name="PersonAddress",
                end1=UmlAssociationEnd(role="person", object=UmlIdReference(idref="class1")),
                end2=UmlAssociationEnd(role="address", object=UmlIdReference(idref="class2")),
            ),
        ],
    )
)

print("\nmodel.model_json_schema")
with open('model-notation.json', 'w') as f:
    f.write(json.dumps(model.model_json_schema(), indent=2))

with open('model-dump.json', 'w') as f:
    f.write(model.model_dump_json(indent=2))
