def clean_word(word: str) -> str:
    result = ''
    for char in word:
        if char.isalpha():
            result += char
    return result
