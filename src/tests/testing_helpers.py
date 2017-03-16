def deep_sort(data_structure):
    """
    Recursively sort nested python data structures (lists and dicts (combined))
    """

    if isinstance(data_structure, list):
        unsorted_result = []
        for val in data_structure:
            unsorted_result.append(deep_sort(val))
        return sorted(unsorted_result)

    elif isinstance(data_structure, dict):
        sorted_dict = {}
        for key in sorted(data_structure):
            sorted_dict[key] = deep_sort(data_structure[key])
        return sorted_dict

    else:
        return data_structure
