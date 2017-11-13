# ECIES
Elliptic Curve Integrated Encryption Scheme 

![ECIES Diagram](https://raw.github.com/ZaneWithSpoon/ECIES/master/ECIES_diagram.png)

1. Key Generated with SECP_256k1 curve
2. Key Areement function is Elliptic-curve Diffie–Hellman (ECDH)
3. Key Derrivation Function: ANSI X9.42
4. AEAD Encryption is AES-SIV
5. MAC is used inside of AES-SIV
6. Cryptogram

The most extended encryption and decryption scheme
based on ECC is the Elliptic Curve Integrated Encryption
Scheme (ECIES). 

As an example, any standard symmetric key encrypted
with a 1024 bits RSA key produces an output of 128 bytes
compared with the output of 84 bytes if the encryption is
performed with one of the possible configurations of
ECIES.