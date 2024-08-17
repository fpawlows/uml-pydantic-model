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
    UmlCombinedFragment,
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


# Define classes
person_class = UmlClass(id="class_person", name="Person")
address_class = UmlClass(id="class_adds", name="Address")

# Define lifelines
lifeline_person = UmlLifeline(
    id="lifeline1",
    name="PersonLifeline",
    represents=person_class
)

lifeline_address = UmlLifeline(
    id="lifeline2",
    name="AddressLifeline",
    represents=UmlIdReference(idref="class2")
)

# Define occurrence specifications
occurrence1 = UmlOccurrenceSpecification(
    id="occurrence1",
    covered=lifeline_person
)

occurrence2 = UmlOccurrenceSpecification(
    id="occurrence2",
    covered=UmlIdReference(idref="lifeline2")
)

# Define operations
get_address_operation = UmlOperation(id="op1", name="getAddress", return_type=address_class)
return_address_operation = UmlOperation(id="op2", name="returnAddress", return_type=person_class)

# Define messages between lifelines
message_request = UmlMessage(
    id="message1",
    name="RequestAddress",
    send_event=occurrence1,
    receive_event=occurrence2,
    signature=get_address_operation
)

message_return = UmlMessage(
    id="message2",
    name="ReturnAddress",
    send_event=UmlIdReference(idref="occurrence2"),
    receive_event=UmlIdReference(idref="occurrence1"),
    signature=UmlIdReference(idref="op2")
)

# Define fragments and operands
fragment1 = UmlCombinedFragment(
    id="fragment1",
    name="CombinedFragment",
    operator=UmlInteractionOperatorEnum.ALT,
    covered=[lifeline_person, UmlIdReference(idref="lifeline2")]
)

operand1 = UmlOperand(
    id="operand1",
    guard="addressExists",
    fragments=[occurrence1, UmlOccurrenceSpecification(id="occurrence3", covered=UmlIdReference(idref="lifeline2"))]
)

operand2 = UmlOperand(
    id="operand2",
    guard="addressNotExists",
    fragments=[occurrence2, UmlOccurrenceSpecification(id="occurrence4", covered=UmlIdReference(idref="lifeline2")), UmlOccurrenceSpecification(id="some_occurence_name", covered=UmlIdReference(idref="lifeline1"))]
)

# Add operands to the main fragment
fragment1.operands.append(operand1)
fragment1.operands.append(operand2)

# Define the interaction
interaction = UmlInteraction(
    id="interaction1",
    name="PersonAddressInteraction",
    lifelines=[lifeline_person, lifeline_address],
    messages=[message_request, message_return],
    fragments=[UmlOccurrenceSpecification(covered=UmlIdReference(idref="lifeline1")), fragment1, occurrence1, occurrence2]
)


# Combine everything into a UML model
uml_model = UmlModel(
    id="model1",
    elements=UmlModelElements(
        classes=[class1, class2, person_class, address_class],
        interfaces=[interface1],
        associations=[association1],
        generalizations=[generalization1],
        interactions=[interaction]
    ),
)


with open("model-dump.json", "w") as f:
    f.write(uml_model.model_dump_json(indent=2))
    # f.write(uml_model.model_dump_json(indent=2, exclude_none=True))
