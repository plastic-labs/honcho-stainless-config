import json


def transform_security(data):
    def update_security(obj):
        if isinstance(obj, dict):
            if "security" in obj and isinstance(obj["security"], list):
                if len(obj["security"]) == 1 and "HTTPBearer" in obj["security"][0]:
                    obj["security"] = [{"HTTPBearer": []}, {}]
            for value in obj.values():
                update_security(value)
        elif isinstance(obj, list):
            for item in obj:
                update_security(item)

    update_security(data)
    return data


def transform_pagination_fields(data):
    pagination_fields = ["page", "pages", "size", "total"]

    def update_fields(obj):
        if isinstance(obj, dict):
            for field in pagination_fields:
                if field in obj and isinstance(obj[field], dict):
                    field_data = obj[field]
                    if "anyOf" in field_data:
                        for option in field_data["anyOf"]:
                            if option.get("type") == "integer":
                                obj[field] = {
                                    "type": "integer",
                                    "minimum": option.get("minimum", 0.0),
                                    "title": field_data.get(
                                        "title", field.capitalize()
                                    ),
                                }
                                break
            for value in obj.values():
                update_fields(value)
        elif isinstance(obj, list):
            for item in obj:
                update_fields(item)

    update_fields(data)
    return data


def transform_metadata(data):
    def update_metadata(obj):
        if isinstance(obj, dict):
            if "metadata" in obj and isinstance(obj["metadata"], dict):
                metadata = obj["metadata"]
                if "anyOf" in metadata:
                    for option in metadata["anyOf"]:
                        if option.get("type") == "object":
                            option["additionalProperties"] = True
                elif metadata.get("type") == "object":
                    metadata["additionalProperties"] = True
            for value in obj.values():
                update_metadata(value)
        elif isinstance(obj, list):
            for item in obj:
                update_metadata(item)

    update_metadata(data)
    return data


def transform_openapi(input_file, output_file):
    # Read the input file
    with open(input_file, "r") as f:
        data = json.load(f)

    # Apply all transformations
    data = transform_security(data)
    data = transform_pagination_fields(data)
    data = transform_metadata(data)

    # Write the transformed data to the output file
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)


# Usage
input_file = "openapi-new.json"
output_file = "output.json"
transform_openapi(input_file, output_file)
print(f"Transformation complete. Output written to {output_file}")
