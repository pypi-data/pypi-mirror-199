import base64

def Encode(str):
        string_bytes = str.encode("ascii")
        base64_bytes = base64.b64encode(string_bytes)
        base64_string = base64_bytes.decode("ascii")
        return base64_string

print(Encode("SGVsbG8gV29ybGQ="))

