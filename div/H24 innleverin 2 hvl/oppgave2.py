#1 
def telefonnummer(text: str):
    # Remove all non-digit characters first
    digits = ''.join(char for char in text if char.isdigit())
    
    # Remove country code if present
    if digits.startswith("47"):
        digits = digits[2:]
    
    return int(digits)

print(telefonnummer("+ 47 9119-4592"))  # Output: 91194592