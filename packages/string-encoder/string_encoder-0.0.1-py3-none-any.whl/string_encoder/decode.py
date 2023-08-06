import base64

def Decode(str):
	base64_bytes = str.encode("ascii")  
	string_bytes = base64.b64decode(base64_bytes)
	b64_string = string_bytes.decode("ascii")
	return b64_string

print(Decode("SGVsbG8gV29ybGQ="))

