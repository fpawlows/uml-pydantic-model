import pprint
import json
from typing import List, Optional, Union
from pydantic import BaseModel, Field, model_serializer
from enum import Enum

class UmlIdReference(BaseModel):
    id: str

    @model_serializer
    def to_json(self):
        return {"$idref": f"{self.id}"}

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


class UmlElement(BaseModel):
    id: str


class UmlNamedElement(UmlElement):
    name: Optional[str]

class UmlAttribute(BaseModel):
    name: str
    type: str
    visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC

class UmlParameter(BaseModel):
    name: str
    type: str

class UmlOperation(BaseModel):
    name: str
    parameters: List[UmlParameter] = Field(default_factory=list)
    return_type: Optional[str]
    visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC

class UmlAssociationEnd(BaseModel):
    role: Optional[str]
    multiplicity: UmlMultiplicityEnum = UmlMultiplicityEnum.ONE
    object: UmlIdReference  # Reference to UmlClass, UmlInterface, or UmlDataType id
    navigability: bool = True

class UmlClass(UmlNamedElement):
    attributes: List[UmlAttribute] = Field(default_factory=list)
    operations: List[UmlOperation] = Field(default_factory=list)
    super_classes: List[UmlIdReference] = Field(default_factory=list)  # References to UmlGeneralization ids
    interfaces: List[UmlIdReference] = Field(default_factory=list)  # References to UmlInterface ids

class UmlInterface(UmlNamedElement):
    operations: List[UmlOperation] = Field(default_factory=list)

class UmlDataType(UmlNamedElement):
    pass

class UmlEnumeration(UmlNamedElement):
    literals: List[str] = Field(default_factory=list)

class UmlGeneralization(UmlNamedElement):
    specific: UmlIdReference  # Reference to UmlClass Umlid
    general: UmlIdReference  # Reference to UmlClass Umlid

class UmlDependency(UmlNamedElement):
    client: UmlIdReference  # Reference to Classifier id
    supplier: UmlIdReference  # Reference to Classifier id

class UmlAssociation(UmlNamedElement):
    end1: UmlAssociationEnd
    end2: UmlAssociationEnd
    association_type: UmlAssociationTypeEnum = UmlAssociationTypeEnum.ASSOCIATION
    direction: UmlAssociationDirectionEnum = UmlAssociationDirectionEnum.UNDIRECTED

class UmlMessage(BaseModel):
    id: str
    name: Optional[str]
    sender: UmlIdReference  # Reference to InteractionParticipant id
    receiver: UmlIdReference  # Reference to InteractionParticipant id
    content: str
    timestamp: str

class UmlFragment(BaseModel):
    id: str
    name: Optional[str]
    type: str
    interaction_operator: str
    covered: List[UmlIdReference] = Field(default_factory=list)  # References to InteractionParticipant ids
    messages: List[UmlMessage] = Field(default_factory=list)

class UmlOperand(BaseModel):
    id: str
    name: Optional[str]
    guard: str
    fragments: List[UmlFragment] = Field(default_factory=list)

class UmlInteraction(BaseModel):
    id: str
    name: Optional[str]
    participants: List[UmlIdReference] = Field(default_factory=list)  # References to UmlClass, UmlInterface, or UmlDataType ids
    messages: List[UmlMessage] = Field(default_factory=list)
    fragments: List[UmlFragment] = Field(default_factory=list)
    operands: List[UmlOperand] = Field(default_factory=list)

class UmlModelElements(BaseModel):
    classes: List[UmlClass] = Field(default_factory=list)
    interfaces: List[UmlInterface] = Field(default_factory=list)
    dataTypes: List[UmlDataType] = Field(default_factory=list)
    enumerations: List[UmlEnumeration] = Field(default_factory=list)
    associations: List[UmlAssociation] = Field(default_factory=list)
    generalizations: List[UmlGeneralization] = Field(default_factory=list)
    dependencies: List[UmlDependency] = Field(default_factory=list)
    interactions: List[UmlInteraction] = Field(default_factory=list)


class UmlModel(BaseModel):
    elements: UmlModelElements


model = UmlModel(
    elements=UmlModelElements(
        classes=[
            UmlClass(id="class1", name="Person"),
            UmlClass(id="class2", name="Address"),
        ],
        associations=[
            UmlAssociation(
                id="assoc1",
                name="PersonAddress",
                end1=UmlAssociationEnd(role="person", object=UmlIdReference(id="class1")),
                end2=UmlAssociationEnd(role="address", object=UmlIdReference(id="class2")),
            ),
        ],
    )
)

print("\nmodel.model_json_schema")
with open('model-notation.json', 'w') as f:
    f.write(json.dumps(model.model_json_schema(), indent=2))

with open('model-dump.json', 'w') as f:
    f.write(model.model_dump_json(indent=2))