with open("yourfile.dat", "rb") as f:
    header = f.read(32)
    
print("=== HEX HEADER ===")
print(" ".join(f"{b:02x}" for b in header))

print("\n=== READABLE PORTION ===")
print("".join(chr(b) if 32 <= b < 127 else "·" for b in header))

print("\n=== FILE SIZE ===")
import os
print(f"{os.path.getsize('yourfile.dat'):,} bytes")
