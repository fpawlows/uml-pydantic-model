import pprint
import json
from typing import List, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum

class VisibilityEnum(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"

class MultiplicityEnum(str, Enum):
    ZERO_OR_ONE = "0..1"
    ONE = "1"
    ZERO_OR_MORE = "0..*"
    ONE_OR_MORE = "1..*"

class AssociationTypeEnum(str, Enum):
    ASSOCIATION = "association"
    AGGREGATION = "aggregation"
    COMPOSITION = "composition"

class AssociationDirectionEnum(str, Enum):
    UNDIRECTED = "undirected"
    DIRECTED = "directed"

class Element(BaseModel):
    id: str
    name: Optional[str]

class Attribute(BaseModel):
    name: str
    type: str
    visibility: VisibilityEnum = VisibilityEnum.PUBLIC

class Parameter(BaseModel):
    name: str
    type: str

class Operation(BaseModel):
    name: str
    parameters: List[Parameter] = Field(default_factory=list)
    return_type: Optional[str]
    visibility: VisibilityEnum = VisibilityEnum.PUBLIC

class AssociationEnd(BaseModel):
    role: Optional[str]
    multiplicity: MultiplicityEnum = MultiplicityEnum.ONE
    type: str
    navigability: bool = True

class Class(Element):
    attributes: List[Attribute] = Field(default_factory=list)
    operations: List[Operation] = Field(default_factory=list)
    super_classes: List[str] = Field(default_factory=list)  # References to Generalization ids
    interfaces: List[str] = Field(default_factory=list)  # References to Interface ids

class Interface(Element):
    operations: List[Operation] = Field(default_factory=list)

class DataType(Element):
    pass

class Enumeration(Element):
    literals: List[str] = Field(default_factory=list)

class Generalization(Element):
    specific: str  # Reference to Class id
    general: str  # Reference to Class id

class Dependency(Element):
    client: str  # Reference to Classifier id
    supplier: str  # Reference to Classifier id

class Association(Element):
    end1: AssociationEnd
    end2: AssociationEnd
    association_type: AssociationTypeEnum = AssociationTypeEnum.ASSOCIATION
    direction: AssociationDirectionEnum = AssociationDirectionEnum.UNDIRECTED

class Message(BaseModel):
    id: str
    name: Optional[str]
    sender: str  # Reference to InteractionParticipant id
    receiver: str  # Reference to InteractionParticipant id
    content: str
    timestamp: str

class Fragment(BaseModel):
    id: str
    name: Optional[str]
    type: str
    interaction_operator: str
    covered: List[str] = Field(default_factory=list)  # References to InteractionParticipant ids
    messages: List[Message] = Field(default_factory=list)

class Operand(BaseModel):
    id: str
    name: Optional[str]
    guard: str
    fragments: List[Fragment] = Field(default_factory=list)

class Interaction(BaseModel):
    id: str
    name: Optional[str]
    participants: List[str] = Field(default_factory=list)  # References to Class, Interface, or DataType ids
    messages: List[Message] = Field(default_factory=list)
    fragments: List[Fragment] = Field(default_factory=list)
    operands: List[Operand] = Field(default_factory=list)

class ModelElements(BaseModel):
    classes: List[Class] = Field(default_factory=list)
    interfaces: List[Interface] = Field(default_factory=list)
    dataTypes: List[DataType] = Field(default_factory=list)
    enumerations: List[Enumeration] = Field(default_factory=list)
    associations: List[Association] = Field(default_factory=list)
    generalizations: List[Generalization] = Field(default_factory=list)
    dependencies: List[Dependency] = Field(default_factory=list)
    interactions: List[Interaction] = Field(default_factory=list)


class UmlModel(BaseModel):
    elements: ModelElements


model = UmlModel(
    elements=ModelElements(
        classes=[
            Class(id="class1", name="Person"),
            Class(id="class2", name="Address"),
        ],
        associations=[
            Association(
                id="assoc1",
                name="PersonAddress",
                end1=AssociationEnd(role="person", type="class1"),
                end2=AssociationEnd(role="address", type="class2"),
            ),
        ],
    )
)

print("\nmodel.model_json_schema")
with open('model.json', 'w') as f:
    f.write(json.dumps(model.model_json_schema(), indent=2))