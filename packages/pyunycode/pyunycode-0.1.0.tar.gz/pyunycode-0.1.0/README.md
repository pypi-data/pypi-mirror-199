# pyunycode

**Punycode Converter Library for Python**

You can convert Punycode domain to/from Unicode domain with only one function.

## How to use

### Install

```sh
pip install pyunycode
```

### Code sample

```python
import pyunycode

# Convert Unicode domain to Punycode domain
str1 = "美しい.世界"
str2 = "こっち.みんな"
str3 = "日本語.jp"
print(f"{str1} -> {pyunycode.convert(str1)}")
print(f"{str2} -> {pyunycode.convert(str2)}")
print(f"{str3} -> {pyunycode.convert(str3)}")

# 僕だけの.世界 -> xn--08j3a5b142t.xn--rhqv96g
# あんまり.みんな -> xn--l8j9flb8a.xn--q9jyb4c
# 日本語.jp -> xn--wgv71a119e.jp

# Punycode domain to Unicode domain
str4 = "xn--n8jub8754b.xn--rhqv96g"
str5 = "xn--28j2af.xn--q9jyb4c"
str6 = "xn--wgv71a119e.jp"
print(f"{str4} -> {pyunycode.convert(str4)}")
print(f"{str5} -> {pyunycode.convert(str5)}")
print(f"{str6} -> {pyunycode.convert(str6)}")

# xn--n8jub8754b.xn--rhqv96g -> 美しい.世界
# xn--28j2af.xn--q9jyb4c -> こっち.みんな
# xn--wgv71a119e.jp -> 日本語.jp
```