from string import ascii_letters

MIN_OFFSET = 1
MAX_OFFSET = 25

def encrypt(text: str, offset: int) -> str:
    """
    Encrypts text by replacing each letter with the letter some fixed number
    of positions (the offset) down the alphabet.
    Returns the encrypted text
    """
    result = ''
    for char in text:
        if not char.isalpha():
            result += char
        else:
            index = (ascii_letters.index(char) + offset) % (MAX_OFFSET + 1)
            if char.isupper():
                index += (MAX_OFFSET + 1)
            result += ascii_letters[index]
    return result