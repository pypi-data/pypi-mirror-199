import idna


def pyunycode(input_text:str):

    if not isinstance(input_text, str):
        raise ValueError("Input must be string.")

    if (input_text[:4] == "xn--") | (".xn--" in input_text):
        punycode_text = idna.decode(input_text)
    else:
        punycode_text = idna.encode(input_text).decode('utf-8')
     
    return punycode_text


if __name__=="__main__":
     
    # str1 = "僕だけの.世界"
    # str1 = "美しい.世界"
    # str2 = "あんまり.みんな"
    # str3 = "日本語.jp"

    # print(f"美しい.世界 -> {pyunycode(str1)}")
    # print(f"あんまり.みんな -> {pyunycode(str2)}")
    # print(f"日本語.jp -> {pyunycode(str3)}")
    # print("中国語.日本語.jp -> {}".format(pyunycode("中国語.日本語.jp")))

    # str4 = "xn--08j3a5b142t.xn--rhqv96g"
    # str5 = "xn--l8j9flb8a.xn--q9jyb4c"
    # str6 = "xn--wgv71a119e.jp"

    # print(f"xn--08j3a5b142t.xn--rhqv96g -> {pyunycode(str4)}")
    # print(f"xn--l8j9flb8a.xn--q9jyb4c -> {pyunycode(str5)}")
    # print(f"xn--wgv71a119e.jp -> {pyunycode(str6)}")

    # print("xn--wgv71a119e.xn--wgv71a119e.jp -> {}".format(pyunycode("xn--fiqs8s568b.xn--wgv71a119e.jp")))

    # str7 = "あああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああもちもち日本語.jp"
    # print(f"あああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああもちもち日本語.jp -> {pyunycode(str7)}")

    # Convert Unicode domain to Punycode domain
    str1 = "美しい.世界"
    str2 = "こっち.みんな"
    str3 = "日本語.jp"
    print(f"{str1} -> {pyunycode(str1)}")
    print(f"{str2} -> {pyunycode(str2)}")
    print(f"{str3} -> {pyunycode(str3)}")

    # 僕だけの.世界 -> xn--08j3a5b142t.xn--rhqv96g
    # あんまり.みんな -> xn--l8j9flb8a.xn--q9jyb4c
    # 日本語.jp -> xn--wgv71a119e.jp

    # Punycode domain to Unicode domain
    str4 = "xn--n8jub8754b.xn--rhqv96g"
    str5 = "xn--28j2af.xn--q9jyb4c"
    str6 = "xn--wgv71a119e.jp"
    print(f"{str4} -> {pyunycode(str4)}")
    print(f"{str5} -> {pyunycode(str5)}")
    print(f"{str6} -> {pyunycode(str6)}")