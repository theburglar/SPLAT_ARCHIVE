from string import ascii_letters
from typing import Tuple

from a1_support import is_word_english

MIN_OFFSET = 1
MAX_OFFSET = 25

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