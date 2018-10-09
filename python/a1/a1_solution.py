from string import ascii_letters
from typing import Tuple

from a1_support import is_word_english

MIN_OFFSET = 1
MAX_OFFSET = 25

OPTION_MSG = """
Please choose an option [e/d/a/q]:
  e) Encrypt some text
  d) Decrypt some text
  a) Automatically decrypt English text
  q) Quit"""


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


def decrypt(text: str, offset: int) -> str:
    """
    Decrypts text that was encrypted by the 'encrypt' function by the offset.
    Returns the decrypted text
    """
    return encrypt(text, -offset)


def clean_word(word: str) -> str:
    result = ''
    for char in word:
        if char.isalpha():
            result += char
    return result


def find_encryption_offsets(encrypted_text: str) -> Tuple[int, ...]:
    """
    Returns a tuple containing all possible offsets that
    could have been used if to encrypt some English text into encrypted_text
    """
    result = []
    encrypted_words = encrypted_text.split()
    for offset in range(MIN_OFFSET, MAX_OFFSET + 1):
        all_valid = True
        for words in encrypted_words:
            # treat words with - separately
            for word in words.split('-'):
                # ignore contractions
                if "'" in word:
                    continue
                word = clean_word(word)
                decrypted = decrypt(word, offset)
                if not is_word_english(decrypted.lower()):
                    all_valid = False
                    break
        if all_valid:
            result.append(offset)
    return tuple(result)


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


def main():
    """ Handles top-level interaction with user """
    print("Welcome to the simple encryption tool!")
    while True:
        print(OPTION_MSG)
        inp = input("> ")
        if inp == 'e':
            cipher_interact('encrypt', encrypt)
        elif inp == 'd':
            cipher_interact('decrypt', decrypt)
        elif inp == 'a':
            text = input("Please enter some encrypted text: ")
            offsets = find_encryption_offsets(text)
            if not offsets:
                print("No valid encryption offset")
            elif len(offsets) == 1:
                offset = offsets[0]
                decrypted_text = decrypt(text, offset)
                print(f"Encryption offset: {offset}")
                print(f"Decrypted message: {decrypted_text}")
            else:
                print("Multiple encryption offsets:", ', '.join(map(str, offsets)))

        elif inp == 'q':
            print('Bye!')
            break

        else:
            print("Invalid command")

if __name__ == '__main__':
    main()