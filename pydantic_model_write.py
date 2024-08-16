from pydantic_model import (
    UmlModel,
    UmlModelElements,
    UmlClass,
    UmlAttribute,
    UmlPrimitiveType,
    UmlPrimitiveTypeTypesEnum,
    UmlOperation,
    UmlInterface,
    UmlAssociation,
    UmlAssociationEnd,
    UmlGeneralization,
    UmlIdReference,
    UmlLifeline,
    UmlMessage,
    UmlOccurrenceSpecification,
    UmlInteraction,
)



# Create some basic UML elements
class1 = UmlClass(
    id="class1",
    name="Person",
    attributes=[
        UmlAttribute(
            name="name",
            type=UmlPrimitiveType(
                id="type1", name="String", type=UmlPrimitiveTypeTypesEnum.STRING
            ),
        ),
        UmlAttribute(
            name="age",
            type=UmlPrimitiveType(
                id="type2", name="Integer", type=UmlPrimitiveTypeTypesEnum.INTEGER
            ),
        ),
    ],
    operations=[
        UmlOperation(
            name="getName",
            return_type=UmlPrimitiveType(
                id="type1", name="String", type=UmlPrimitiveTypeTypesEnum.STRING
            ),
        )
    ],
)

class2 = UmlClass(
    id="class2",
    name="Address",
    attributes=[
        UmlAttribute(
            name="street",
            type=UmlPrimitiveType(
                id="type1", name="String", type=UmlPrimitiveTypeTypesEnum.STRING
            ),
        ),
        UmlAttribute(
            name="zipcode",
            type=UmlPrimitiveType(
                id="type2", name="Integer", type=UmlPrimitiveTypeTypesEnum.INTEGER
            ),
        ),
    ],
)

interface1 = UmlInterface(
    id="interface1",
    name="PersonInterface",
    operations=[
        UmlOperation(
            name="getAge",
            return_type=UmlPrimitiveType(
                id="type2", name="Integer", type=UmlPrimitiveTypeTypesEnum.INTEGER
            ),
        )
    ],
)

# Create an association between the classes
association1 = UmlAssociation(
    id="assoc1",
    name="PersonAddressAssociation",
    end1=UmlAssociationEnd(id="end1", object=UmlIdReference(idref="class1")),
    end2=UmlAssociationEnd(id="end2", object=UmlIdReference(idref="class2")),
)

# Create a generalization relationship
generalization1 = UmlGeneralization(
    id="gen1",
    specific=UmlIdReference(idref="class1"),
    general=UmlIdReference(idref="interface1"),
)

# Create an interaction with lifelines, messages, and fragments
lifeline1 = UmlLifeline(
    id="lifeline1", name="PersonLifeline", represents=UmlIdReference(idref="class1")
)

lifeline2 = UmlLifeline(
    id="lifeline2", name="AddressLifeline", represents=UmlIdReference(idref="class2")
)

message1 = UmlMessage(
    id="message1",
    name="RequestAddress",
    source=UmlOccurrenceSpecification(
        id="occ1", lifeline=UmlIdReference(idref="lifeline1")
    ),
    target=UmlOccurrenceSpecification(
        id="occ2", lifeline=UmlIdReference(idref="lifeline2")
    ),
    signature=UmlOperation(id="op1", name="getAddress"),
)

interaction1 = UmlInteraction(
    id="interaction1",
    name="PersonAddressInteraction",
    lifelines=[lifeline1, lifeline2],
    messages=[message1],
)

# Combine everything into a UML model
uml_model = UmlModel(
    id="model1",
    elements=UmlModelElements(
        classes=[class1, class2],
        interfaces=[interface1],
        associations=[association1],
        generalizations=[generalization1],
        interactions=[interaction1],
    ),
)


with open("model-dump.json", "w") as f:
    f.write(uml_model.model_dump_json(indent=2))
    # f.write(uml_model.model_dump_json(indent=2, exclude_none=True))
