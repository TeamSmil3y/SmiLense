def differing_params_dict(base_dict, other_dicts):
    for other_dict in other_dicts:
        differing_params = {}
        for key, value in base_dict.items():
            if other_dict.get(key) != value:
                differing_params[key] = other_dict.get(key)
        if differing_params:  # If there are differing parameters, return the dictionary
            return differing_params
    return None  # If no differing parameters found in any dictionary, return None

def calc_score(base_dict, other_dict):
    level = 0

    if other_dict.get('additional') != "There are no additions.":
        level = 1

    if base_dict.get('commercial_use') == 'allowed':
        match other_dict.get('commercial_use').lower().replace(" ", ""):
            case "notmentioned" | "unknown":
                level = max(level, 1)
            case 'notallowed':
                level = 3

    if base_dict.get('open_source') == 'yes':
        match other_dict.get('open_source').lower().replace(" ", ""):
            case "notmentioned" | "unknown":
                level = max(level, 1)
            case 'no':
                level = 3

    if base_dict.get('attribution') == 'required':
        match other_dict.get('attribution').lower().replace(" ", ""):
            case "notmentioned" | "unknown":
                level = max(level, 1)
            case 'required':
                level = 2

    if base_dict.get('redistribution') == 'allowed':
        match other_dict.get('redistribution').lower().replace(" ", ""):
            case "notmentioned" | "unknown":
                level = max(level, 1)
            case 'notallowed':
                level = 3

    if base_dict.get('profit') == 'allowed':
        match other_dict.get('profit').lower().replace(" ", ""):
            case "notmentioned" | "unknown":
                level = max(level, 1)
            case 'notallowed':
                level = 3

    return level


# Example usage
base_dict = {
    "commercial_use": "allowed",
    "open_source": "yes",
    "attribution": "required",
    "redistribution": "allowed",
    "profit": "allowed",
}

other_dicts = [
    {
    "commercial_use": "allowed",
    "open_source": "no",
    "attribution": "required",
    "redistribution": "allowed",
    "profit": "notallowed"
    },
    # Add more dictionaries for comparison if needed
]

result = differing_params_dict(base_dict, other_dicts)
if result:
    print("Differences found:")
    print(result)
else:
    print("No differences found.")
