import secrets
import string

def pwgen(length = 8, digits = True, uppercase = True, special_symbols = False, separator = '', part_length = 1):
    """    
    Simple password generator (pwgen)
    
    pwgen(int, bool, bool, bool, str, int) -> (str)
    
    length            (int > 0)       - length of a password
    digits            (bool)          - should a password contain digits
    uppercase         (bool)          - should a password contain UPPERCASE letters
    special_symbols   (bool)          - should a password contain special symbols
    separator         (str)           - symbols to separate groups of letters in password
    part_length       (int > 0)       - length of each group of letters in password
    
    Dependencies: string, secrets """
    
    if length > 0:
    
        special = '_?!$#@+-=&`~'  
        alphabet = string.ascii_lowercase
    
        if uppercase:
            alphabet += string.ascii_uppercase    
        if digits:
            alphabet += string.digits
        if special_symbols:
            alphabet += special

        while True:
            result = []
            correct = True
            for i in range(1, length + 1):
                result.append(secrets.choice(alphabet))
                
            if not(any(letter.islower() for letter in result)):
                correct = False
            
            if digits and not(any(letter.isdigit() for letter in result)):
                correct = False
                
            if uppercase and not(any(letter.isupper() for letter in result)):
                correct = False
            
            if special_symbols and not(any(letter in special for letter in result)):
                correct = False
            
            if correct:
                break
        
        if part_length > 0:
            parts = length // part_length
            
            if length % part_length == 0:
                parts -= 1
            
            for i in range(parts):
                result.insert(part_length * (i + 1) + i, separator)
        
        else:
            raise ValueError('Nonpositive length of parts in a password!')

        return ''.join(result)
        
    else:
        raise ValueError('Nonpositive length of a password!')
    