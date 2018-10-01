#!/usr/bin/env python3
"""
Assignment 1
CSSE1001/7030
Semester 2, 2018
"""

from a1_support import is_word_english

__author__ = "Your name & student number here"

YARN = 'I remember him looking round the cover and whistling to himself as he did so, and then breaking out in that old sea-song that he sang so often afterwards: "Fifteen men on the dead man\'s chest; Yo-ho-ho, and a bottle of rum!"'
TEST = "iynjo fuhsudj ev jxu jycu yj mehai qbb jxu jycu"
tESt = "iYnjO fUHsudJ eV Jxu jYCu yj MEhai qBB jXu jYCu"

# Write your functions here
def encrypt(text, offset):
    return ''.join([chr((((ord(c) - 97) + offset) % 26) + 97) if 97 <= ord(c) <= 122 else c for c in text])

def decrypt(text, offset):
    return encrypt(text, 26 - offset)

def is_sentence_english(sentence):
    return all(is_word_english(word) for word in sentence.split(' '))

def find_encryption_offsets(ctext):
    return tuple(i for i in range(26) if is_sentence_english(decrypt(ctext, i)))


def encrypt_wrapper(text, offset):
    """encrypt - but handles capitals letters"""
    mask = [1 if c.isupper() else 0 for c in text]
    return ''.join([c.upper() if i else c for c, i in zip(encrypt(text.lower(), offset), mask)])

def decrypt_wrapper(text, offset):
    return encrypt_wrapper(text, 26 - offset)

def main():
    # Add your main code here
    i = 'testystring'
    pass


##################################################
# !! Do not change (or add to) the code below !! #
#
# This code will run the main function if you use
# Run -> Run Module  (F5)
# Because of this, a "stub" definition has been
# supplied for main above so that you won't get a
# NameError when you are writing and testing your
# other functions. When you are ready please
# change the definition of main above.
###################################################

if __name__ == '__main__':
    main()

