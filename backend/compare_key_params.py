def differing_params_dict(base_dict, other_dicts):
    for other_dict in other_dicts:
        differing_params = {}
        for key, value in base_dict.items():
            if other_dict.get(key) != value:
                differing_params[key] = other_dict.get(key)
        if differing_params:  # If there are differing parameters, return the dictionary
            return differing_params
    return None  # If no differing parameters found in any dictionary, return None

# Example usage
base_dict = {
    "commercial_use": "allowed"
    "open_source": "yes"
    "attribution": "required"
    "redistribution": "allowed"
    "profit": "allowed"
}

other_dicts = [
    {
    "commercial_use": "allowed"
    "open_source": "no"
    "attribution": "required"
    "redistribution": "allowed"
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
