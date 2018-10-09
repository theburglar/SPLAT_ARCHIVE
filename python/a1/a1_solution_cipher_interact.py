from string import ascii_letters
from typing import Tuple

from a1_support import is_word_english

MIN_OFFSET = 1
MAX_OFFSET = 25

def cipher_interact(mode: str, cipher_function):
    """
    Prompts the user for text and an offset and then
    either encrypts or decrypts depending on which
    function is provided for 'cipher_function'
    """
    text = input(f"Please enter some text to {mode}: ")
    offset = int(input("Please enter a shift offset (1-25): "))
    if offset != 0:
        cipher_text = cipher_function(text, offset)
        print(f"The {mode}ed text is: {cipher_text}")
    else:
        print(f"The {mode}ed text is:")
        for offset in range(MIN_OFFSET, MAX_OFFSET + 1):
            cipher_text = cipher_function(text, offset)
            print(f'  {offset:02d}: {cipher_text}')
