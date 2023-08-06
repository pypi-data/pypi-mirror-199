import idna


def convert(input_text:str):

    if not isinstance(input_text, str):
        raise ValueError("Input must be string.")

    if (input_text[:4] == "xn--") | (".xn--" in input_text):
        punycode_text = idna.decode(input_text)
    else:
        punycode_text = idna.encode(input_text).decode('utf-8')
     
    return punycode_text