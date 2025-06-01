from Levenshtein import distance

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