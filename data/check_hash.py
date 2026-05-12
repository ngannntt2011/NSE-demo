import hashlib
password = "hello123"
print(f"MD5 of '{password}': {hashlib.md5(password.encode()).hexdigest()}")
