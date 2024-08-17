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
    UmlInteractionOperatorEnum,
    UmlOperand, 
    UmlEnclosedLifelinePart,
    UmlCombinedFragment
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

lifeline1 = UmlLifeline(
    id="lifeline1",
    name="PersonLifeline",
    represents=UmlIdReference(idref="class1")
)

lifeline2 = UmlLifeline(
    id="lifeline2",
    name="AddressLifeline",
    represents=UmlIdReference(idref="class2")
)

# Define occurrences
occurrence1 = UmlOccurrenceSpecification(
    id="occurrence1", lifeline=UmlIdReference(idref="lifeline1")
)

occurrence2 = UmlOccurrenceSpecification(
    id="occurrence2", lifeline=UmlIdReference(idref="lifeline2")
)

# Define messages between lifelines
message1 = UmlMessage(
    id="message1",
    name="RequestAddress",
    source=UmlIdReference(idref="occurrence1"),
    target=UmlIdReference(idref="occurrence2"),
    signature=UmlOperation(id="op1", name="getAddress")
)

message2 = UmlMessage(
    id="message2",
    name="ReturnAddress",
    source=UmlIdReference(idref="occurrence2"),
    target=UmlIdReference(idref="occurrence1"),
    signature=UmlOperation(id="op2", name="returnAddress")
)

# Define enclosed lifeline parts
enclosed_part1 = UmlEnclosedLifelinePart(
    id="enclosedPart1",
    lifeline=UmlIdReference(idref="lifeline1"),
    occurences=[occurrence1],
    enclosed_by=UmlIdReference(idref="combinedFragment1")
)

enclosed_part2 = UmlEnclosedLifelinePart(
    id="enclosedPart2",
    lifeline=UmlIdReference(idref="lifeline2"),
    occurences=[occurrence2],
    enclosed_by=UmlIdReference(idref="combinedFragment1")
)

lifeline1.covered_by = [enclosed_part1]
lifeline2.covered_by = [enclosed_part2]


# Define operands that enclose the lifeline parts
operand1 = UmlOperand(
    id="operand1",
    guard="addressExists",
    covered=[UmlIdReference(idref="enclosedPart1"), UmlIdReference(idref="enclosedPart2")]
)

# Define a combined fragment that includes the operand
combined_fragment = UmlCombinedFragment(
    id="combinedFragment1",
    interaction_operator=UmlInteractionOperatorEnum.ALT,
    operands=[operand1]
)

# Define the interaction that includes the lifelines, messages, and combined fragment
interaction = UmlInteraction(
    id="interaction1",
    name="PersonAddressInteraction",
    lifelines=[lifeline1, lifeline2],
    messages=[message1, message2],
    combined_fragments=[combined_fragment]
)

# Combine everything into a UML model
uml_model = UmlModel(
    id="model1",
    elements=UmlModelElements(
        classes=[class1, class2, UmlClass(id="class1", name="Person"), UmlClass(id="class2", name="Address"),],
        interfaces=[interface1],
        associations=[association1],
        generalizations=[generalization1],
        interactions=[interaction]
    ),
)


with open("model-dump.json", "w") as f:
    f.write(uml_model.model_dump_json(indent=2))
    # f.write(uml_model.model_dump_json(indent=2, exclude_none=True))
