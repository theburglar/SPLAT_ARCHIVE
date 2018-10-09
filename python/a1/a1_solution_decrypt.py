def decrypt(text: str, offset: int) -> str:
    """
    Decrypts text that was encrypted by the 'encrypt' function by the offset.
    Returns the decrypted text
    """
    return encrypt(text, -offset)