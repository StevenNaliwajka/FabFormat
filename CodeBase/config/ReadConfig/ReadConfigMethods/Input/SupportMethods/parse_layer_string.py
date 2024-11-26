def parse_layer_string(input_string):
    if '-' in input_string and ',' not in input_string:  # Case 3: Range format
        start, end = map(int, input_string.split('-'))
        return list(range(start, end + 1))  # Return a list of numbers in the range
    elif ',' in input_string:  # Case 2: Comma-separated format
        return [int(num.strip()) for num in input_string.split(',')]  # Return a list of numbers
    else:  # Case 1: Single number
        return [int(input_string.strip())]  # Return a single number as a list