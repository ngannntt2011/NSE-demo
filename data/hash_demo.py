import hashlib

password = "password123"
hashed = hashlib.md5(password.encode()).hexdigest()

print("="*40)
print(" HASH DEMO (VULNERABLE MD5)")
print("="*40)
print("Password:", password)
print("MD5 Hash:", hashed)
print("="*40)
print("\n[i] Note: This hash is vulnerable to Rainbow Table attacks.")
