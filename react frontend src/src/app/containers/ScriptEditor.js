import React, {Component} from 'react';
import Editor from 'react-simple-code-editor';
import {highlight, languages} from 'prismjs';

import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-python';

// const code = ("def testy(x, y):\n" +
//     "  print('Hello World')");

const code = "from string import ascii_letters\n" +
    "from typing import Tuple\n" +
    "\n" +
    "from a1_support import is_word_english\n" +
    "\n" +
    "MIN_OFFSET = 1\n" +
    "MAX_OFFSET = 25\n" +
    "\n" +
    "OPTION_MSG = \"\"\"\n" +
    "Please choose an option [e/d/a/q]:\n" +
    "  e) Encrypt some text\n" +
    "  d) Decrypt some text\n" +
    "  a) Automatically decrypt English text\n" +
    "  q) Quit\"\"\"\n" +
    "\n" +
    "\n" +
    "def encrypt(text: str, offset: int) -> str:\n" +
    "    \"\"\"\n" +
    "    Encrypts text by replacing each letter with the letter some fixed number\n" +
    "    of positions (the offset) down the alphabet.\n" +
    "    Returns the encrypted text\n" +
    "    \"\"\"\n" +
    "    result = ''\n" +
    "    for char in text:\n" +
    "        if not char.isalpha():\n" +
    "            result += char\n" +
    "        else:\n" +
    "            index = (ascii_letters.index(char) + offset) % (MAX_OFFSET + 1)\n" +
    "            if char.isupper():\n" +
    "                index += (MAX_OFFSET + 1)\n" +
    "            result += ascii_letters[index]\n" +
    "    return result\n" +
    "\n" +
    "\n" +
    "def decrypt(text: str, offset: int) -> str:\n" +
    "    \"\"\"\n" +
    "    Decrypts text that was encrypted by the 'encrypt' function by the offset.\n" +
    "    Returns the decrypted text\n" +
    "    \"\"\"\n" +
    "    return encrypt(text, -offset)\n" +
    "\n" +
    "\n" +
    "def clean_word(word: str) -> str:\n" +
    "    result = ''\n" +
    "    for char in word:\n" +
    "        if char.isalpha():\n" +
    "            result += char\n" +
    "    return result\n" +
    "\n" +
    "\n" +
    "def find_encryption_offsets(encrypted_text: str) -> Tuple[int, ...]:\n" +
    "    \"\"\"\n" +
    "    Returns a tuple containing all possible offsets that\n" +
    "    could have been used if to encrypt some English text into encrypted_text\n" +
    "    \"\"\"\n" +
    "    result = []\n" +
    "    encrypted_words = encrypted_text.split()\n" +
    "    for offset in range(MIN_OFFSET, MAX_OFFSET + 1):\n" +
    "        all_valid = True\n" +
    "        for words in encrypted_words:\n" +
    "            # treat words with - separately\n" +
    "            for word in words.split('-'):\n" +
    "                # ignore contractions\n" +
    "                if \"'\" in word:\n" +
    "                    continue\n" +
    "                word = clean_word(word)\n" +
    "                decrypted = decrypt(word, offset)\n" +
    "                if not is_word_english(decrypted.lower()):\n" +
    "                    all_valid = False\n" +
    "                    break\n" +
    "        if all_valid:\n" +
    "            result.append(offset)\n" +
    "    return tuple(result)\n" +
    "\n" +
    "\n" +
    "def cipher_interact(mode: str, cipher_function):\n" +
    "    \"\"\"\n" +
    "    Prompts the user for text and an offset and then\n" +
    "    either encrypts or decrypts depending on which\n" +
    "    function is provided for 'cipher_function'\n" +
    "    \"\"\"\n" +
    "    text = input(f\"Please enter some text to {mode}: \")\n" +
    "    offset = int(input(\"Please enter a shift offset (1-25): \"))\n" +
    "    if offset != 0:\n" +
    "        cipher_text = cipher_function(text, offset)\n" +
    "        print(f\"The {mode}ed text is: {cipher_text}\")\n" +
    "    else:\n" +
    "        print(f\"The {mode}ed text is:\")\n" +
    "        for offset in range(MIN_OFFSET, MAX_OFFSET + 1):\n" +
    "            cipher_text = cipher_function(text, offset)\n" +
    "            print(f'  {offset:02d}: {cipher_text}')\n" +
    "\n" +
    "\n" +
    "def main():\n" +
    "    \"\"\" Handles top-level interaction with user \"\"\"\n" +
    "    print(\"Welcome to the simple encryption tool!\")\n" +
    "    while True:\n" +
    "        print(OPTION_MSG)\n" +
    "        inp = input(\"> \")\n" +
    "        if inp == 'e':\n" +
    "            cipher_interact('encrypt', encrypt)\n" +
    "        elif inp == 'd':\n" +
    "            cipher_interact('decrypt', decrypt)\n" +
    "        elif inp == 'a':\n" +
    "            text = input(\"Please enter some encrypted text: \")\n" +
    "            offsets = find_encryption_offsets(text)\n" +
    "            if not offsets:\n" +
    "                print(\"No valid encryption offset\")\n" +
    "            elif len(offsets) == 1:\n" +
    "                offset = offsets[0]\n" +
    "                decrypted_text = decrypt(text, offset)\n" +
    "                print(f\"Encryption offset: {offset}\")\n" +
    "                print(f\"Decrypted message: {decrypted_text}\")\n" +
    "            else:\n" +
    "                print(\"Multiple encryption offsets:\", ', '.join(map(str, offsets)))\n" +
    "\n" +
    "        elif inp == 'q':\n" +
    "            print('Bye!')\n" +
    "            break\n" +
    "\n" +
    "        else:\n" +
    "            print(\"Invalid command\")\n" +
    "\n" +
    "if __name__ == '__main__':\n" +
    "    main()"

export class ScriptEditor extends Component {

    state = {code};
    render() {
        return (
            <Editor
                value={this.state.code}
                onValueChange={code => this.setState({code})}
                highlight={code => highlight(code, languages.python)}
                padding={10}
                style={{
                    fontFamily: '"Fira code", "Fira Mono", monospace',
                    // fontSize: 32,
                }}
            />
        )
    }

}