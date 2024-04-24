

def clean_string(input_string: str):
    for x in range(len(input_string)):
        if input_string[x] == ' ':
            continue
        
        return input_string[x:] 
    