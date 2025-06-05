from Levenshtein import distance

def dict_all_valid(string, valid_strings, accuracy=2):
	matched_strings = []
	string = string.lower()
	for valid_string in valid_strings:
		if string in valid_string.lower() or distance(string, valid_string) <= len(valid_string)/accuracy:
			matched_strings.append(valid_string)
		else:
			for alias in valid_strings[valid_string]:
				if string in alias.lower() or distance(string, alias) <= len(alias)/accuracy:
					matched_strings.append(valid_string)
					break
	return matched_strings

def dict_closest_match(string, valid_dict, distance_limit=0, accuracy=0):
	best_match = None
	best_distance = float('inf')
	string = string.lower()
	for key, aliases in valid_dict.items():
		if string == key.lower():
			return key
		for alias in aliases:
			if string == alias.lower():
				return key
		key_distance = distance(string, key)
		if key_distance < best_distance:
			best_match = key
			best_distance = key_distance
		for alias in aliases:
			alias_distance = distance(string, alias)
			if alias_distance < best_distance:
				best_match = key
				best_distance = alias_distance
	if accuracy > 0 and best_distance > len(best_match)/accuracy:
		return None
	if distance_limit > 0 and best_distance > distance_limit:
		return None
	return best_match

def list_all_valid(string, valid_strings, accuracy=2):
    matched_strings = []
    string = string.lower()
    
    for candidate in valid_strings:
        if string in candidate.lower():
            matched_strings.append(candidate)
            continue
            
        try:
            if distance(string, candidate.lower()) <= len(candidate)/accuracy:
                matched_strings.append(candidate)
        except NameError: pass
            
    return matched_strings

def list_closest_match(string, valid_list, distance_limit=0, accuracy=0):
    best_match = None
    best_distance = float('inf')
    string = string.lower()
    
    for item in valid_list:
        if isinstance(item, str):
            if string == item.lower():
                return item
            current_distance = distance(string, item.lower())
            if current_distance < best_distance:
                best_match = item
                best_distance = current_distance
        elif isinstance(item, (list, tuple)):
            for alias in item:
                if string == alias.lower():
                    return item[0]
                current_distance = distance(string, alias.lower())
                if current_distance < best_distance:
                    best_match = item[0]
                    best_distance = current_distance
    
    if accuracy > 0 and best_distance > len(best_match)/accuracy:
        return None
    if distance_limit > 0 and best_distance > distance_limit:
        return None
    
    return best_match