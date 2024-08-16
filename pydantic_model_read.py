from pydantic_model import UmlModel

with open("model-dump.json", "r") as f:
    model = UmlModel.model_validate_json(f.read())

print("\nmodel")
print(model.model_dump_json(indent=2))
