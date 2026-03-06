"""
This program encrypts and decrypts the payment message using my custom

stream cipher based on an LCG PRNG. It also shows details for the first
9 characters like in my report.

How to run:
- Run in Python 
- Enter an integer key when asked (try 12345 to match my examples)
- It will show encryption details, full ciphertext, and decrypt back

"""

def lcg_keystream(seed):
    """Generate keystream bytes using LCG"""
    a = 1103515245
    c = 12345
    m = 1 << 31  # 2^31
    state = seed
    
    while True:
        state = (a * state + c) % m
        # Use higher bits for better randomness
        yield (state >> 16) & 0xFF

def encrypt_or_decrypt(text, key):
    """XOR text with keystream - same for encrypt and decrypt"""
    stream = lcg_keystream(key)
    result = ""
    for char in text:
        keystream_byte = next(stream)
        cipher_byte = ord(char) ^ keystream_byte
        result += chr(cipher_byte)
    return result

def show_first_nine_details(message, key):
    """Print table for first 9 characters (like in my report)"""
    stream = lcg_keystream(key)
    print("\nFirst 9 characters encryption details (key = {}):".format(key))
    print("-" * 65)
    print("{:<6} {:<8} {:<10} {:<8} {:<8}".format("Char", "ASCII", "Keystream", "XOR", "Hex"))
    print("-" * 65)
    
    for i in range(min(9, len(message))):
        plain = ord(message[i])
        key_byte = next(stream)
        cipher = plain ^ key_byte
        print("{:<6} {:<8} {:<10} {:<8} {:<8}".format(
            repr(message[i]), plain, key_byte, cipher, format(cipher, '02X')))
    print("-" * 65)

# Main part
if __name__ == "__main__":
    message = "Convert $502.89 AUD to 98283.04 LKR on 5 January 2026."
    
    print("My Stream Cipher with LCG PRNG")
    print("=" * 60)
    print("Original message:")
    print(message)
    print("Length:", len(message), "characters")
    
    # Get key from user
    try:
        key = int(input("\nEnter integer key (seed): "))
    except ValueError:
        print("Not a number! Using 12345 instead.")
        key = 12345
    
    # Show first 9 details
    show_first_nine_details(message, key)
    
    # Encrypt
    print("\nEncrypting...")
    encrypted = encrypt_or_decrypt(message, key)
    
    print("\nCiphertext in hex:")
    print(" ".join(format(ord(c), "02X") for c in encrypted))
    
    # Decrypt
    print("\nDecrypting...")
    decrypted = encrypt_or_decrypt(encrypted, key)
    
    print("\nDecrypted message:")
    print(decrypted)
    
    # Check success
    if decrypted == message:
        print("\n" + "=" * 60)
        print("SUCCESS! Decryption matches the original message perfectly.")
        print("=" * 60)
    else:
        print("\nSomething went wrong!")
