from random import choice


def get_n(uid):
    uids = str(uid)
    for m in range(len(uids)):
        n = int(uids[5] + uids[-m])
        if n > 0:
            break

    if n <= 0:
        n = 13
    return n


def transform(char):
    if char == ",":
        return "'"
    elif char == "'":
        return ","
    elif char == '!':
        return "?"
    elif char == "?":
        return '!'
    elif char == '"':
        return "-"
    elif char == "-":
        return '"'
    elif char == ".":
        return "\n"
    elif char == "\n":
        return "."
    return char


def encrypt(uid, text) -> str:
    n = get_n(uid)
    cipher_text = "§"
    for char in text:
        if char.isalpha():
            shifted_char = chr((ord(char.lower()) - 97 + n) % 26 + 97)
            if char.isupper():
                shifted_char = shifted_char.upper()
            add = shifted_char
        elif char == " ":
            add = choice("§‰¶©¤—")
        else:
            add = transform(char)
        cipher_text += add
    return cipher_text


def decrypt(uid, cipher_text) -> str:
    if not cipher_text.startswith("§"):
        return cipher_text

    n = get_n(uid)
    text = ""
    for char in cipher_text[1:]:
        if char.isalpha():
            shifted_char = chr((ord(char.lower()) - 97 - n) % 26 + 97)
            if char.isupper():
                shifted_char = shifted_char.upper()
            add = shifted_char
        elif char in "§‰¶©¤—":
            add = " "
        else:
            add = transform(char)
        text += add
    return text
