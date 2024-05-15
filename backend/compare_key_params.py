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
    "commercial_use": "true",
    "copyright": "true",
    "limited_liability": "true",
    "damages_claim": "true",
    "non_profit": "true",
    "distribution": "true",
    "modifications": "true",
    "warranty": "true",
    "guarranty": "true",
    "non_infringement": "true",
    "no_revenue": "true",
    "attribution": "true",
    "enforceable": "true",
    "reserve_right_change": "true",
    "law_associated_country": "us",
    "derivate_word": "not_allowed",
    "original_work": "true",
    "trademark": "false",
    "date_of_expiry": "02/2025"
}

other_dicts = [
    {
        "commercial_use": "true",
        "copyright": "true",
        "limited_liability": "true",
        "damages_claim": "false",
        "non_profit": "true",
        "distribution": "true",
        "modifications": "true",
        "warranty": "true",
        "guarranty": "true",
        "non_infringement": "true",
        "no_revenue": "true",
        "attribution": "false",
        "enforceable": "true",
        "reserve_right_change": "true",
        "law_associated_country": "us",
        "derivate_word": "not_allowed",
        "original_work": "true",
        "trademark": "false",
        "date_of_expiry": "02/2026"
    },
    # Add more dictionaries for comparison if needed
]

result = differing_params_dict(base_dict, other_dicts)
if result:
    print("Differences found:")
    print(result)
else:
    print("No differences found.")
