#copyright aleksy stocki B)
import argparse
import math
parser = argparse.ArgumentParser()

# -c cezar, -a afiniczny, -e szyfruj, -d odszyfruj
# -j kryptoanaliza z tekstem jawnym, -k kryptoanaliza w oparciu o kryptogram
code_group = parser.add_mutually_exclusive_group(required=True)

code_group.add_argument("-c", action='store_true', default=False)
code_group.add_argument("-a", action='store_true', default=False) 

use_group = parser.add_mutually_exclusive_group(required=True)
use_group.add_argument("-e", action='store_true', default=False)
use_group.add_argument("-d", action='store_true', default=False)
use_group.add_argument("-j", action='store_true', default=False)
use_group.add_argument("-k", action='store_true', default=False)

args = parser.parse_args()
alphabet = "abcdefghijklmnoprstquvwxyz"
upper_alphabet = "ABCDEFGHIJKLMNOPRSTQUVWXYZ"
class Cezar():
    def __init__(self):
        pass

    @classmethod
    def cypher(cls):
        key_file = open("key.txt")
        text_file = open("plain.txt")
        key = int(key_file.readline().split()[0])
        if not isinstance(key, int):
            raise ValueError
        text = text_file.readline()
        cyphered = ""
        for letter in text:
            if letter.isalpha():
                if letter.islower():
                    idx = alphabet.find(letter)
                    move = key + idx
                    if move > 25:
                        move = move - 26
                    cyphered += alphabet[move]
                else:
                    idx = upper_alphabet.find(letter)
                    move = key + idx
                    if move > 25:
                        move = move - 26
                    idx = upper_alphabet.find(letter)
                    cyphered += upper_alphabet[move]
            elif letter == " ":
                cyphered += " "
            elif not letter.isspace():
                raise ValueError
        with open("crypto.txt", "w") as file:
            file.write(cyphered)
            return cyphered

    @classmethod
    def decypher(cls):
        key_file = open("key.txt")
        text_file = open("crypto.txt")
        key = int(key_file.readline().split()[0])
        if not isinstance(key, int):
            raise ValueError
        text = text_file.readline()
        decyphered = ""
        for letter in text:
            if letter.isalpha():
                if letter.islower():
                    idx = alphabet.find(letter)
                    move = idx - key
                    if move < 0:
                        move = 26 + move
                    decyphered += alphabet[move]
                else:
                    idx = upper_alphabet.find(letter)
                    move = idx - key
                    if move < 0:
                        move = 26 + move
                    idx = upper_alphabet.find(letter)
                    decyphered += upper_alphabet[move]
            elif letter == " ":
                decyphered += " "
            elif not letter.isspace():
                raise ValueError
        with open("decrypt.txt", "w") as file:
            file.write(decyphered)
            return decyphered

    @classmethod
    def break_bruteforce(cls):
        text_file = open("crypto.txt")
        text = text_file.readline()
        with open('candidates.txt', 'w') as file:
            file.write("")
        for i in range(26): 
            decyphered = ""
            for letter in text:
                if letter.isalpha():
                    if letter.islower():
                        idx = alphabet.find(letter)
                        move = i + idx
                        if move > 25:
                            move = move - 26
                        decyphered += alphabet[move]
                    else:
                        idx = upper_alphabet.find(letter)
                        move = i + idx
                        if move > 25:
                            move = move - 26
                        idx = upper_alphabet.find(letter)
                        decyphered += upper_alphabet[move]
                elif letter == " ":
                    decyphered += " "
                elif not letter.isspace():
                    raise ValueError
            with open("candidates.txt", "a") as file:
                file.write(decyphered + "\n")
    @classmethod
    def break_help(cls):
        text_file = open("crypto.txt")
        help_text = open("extra.txt")
        text = text_file.readline()
        help = help_text.readline().split()[0]
        decyphered = ""
        possible_key = alphabet.find(str.lower(text[0])) - alphabet.find(str.lower(help))
        for letter in text:
            if letter.isalpha():
                if letter.islower():
                    idx = alphabet.find(letter)
                    move = idx - possible_key
                    if move < 0:
                        move = 26 + move
                    decyphered += alphabet[move]
                else:
                    idx = upper_alphabet.find(letter)
                    move = idx - possible_key
                    if move < 0:
                        move = 26 + move
                    idx = upper_alphabet.find(letter)
                    decyphered += upper_alphabet[move]
            elif letter == " ":
                decyphered += " "
            elif not letter.isspace():
                raise ValueError
        with open("decrypt.txt", "w") as file:
            file.write(decyphered)
        with open("key-found.txt", "w") as file:
            file.write(str(possible_key))
            return possible_key


class Affine():
    def __init__(self):
        pass

    @classmethod
    def egcd(cls, a, b):
        x, y, u, v = 0, 1, 1, 0
        while a != 0:
            q, r = b // a, b % a
            m, n = x-u * q, y - v * q
            b, a, x, y, u, v = a, r, u, v, m, n
        gcd = b
        return gcd, x, y

    @classmethod
    def modinv(cls, a, m):
        gcd, x, y = cls.egcd(a, m)
        if gcd != 1:
            return None  # modular inverse does not exist
        else:
            return x % m

    @classmethod
    def cypher(cls):
        key_file = open("key.txt")
        text_file = open("plain.txt")
        key = list(map(int, key_file.readline().split()))
        if not isinstance(key[0], int) or not isinstance(key[1], int):
            raise ValueError
        if math.gcd(key[1], 26) != 1:
            raise ValueError
        text = text_file.readline()
        cyphered = ""
        for letter in text:
            if letter.isalpha():
                if letter.islower():
                    move = (((ord(letter) - 97) * key[1]) + key[0]) % 26
                    cyphered += chr(97+move)
                else:
                    move = (((ord(letter) - 65) * key[1]) + key[0]) % 26
                    cyphered += chr(65+move)
            elif letter == " ":
                cyphered += " "
            elif not letter.isspace():
                raise ValueError
        with open("crypto.txt", "w") as file:
            file.write(cyphered)
            return cyphered
    
    @classmethod
    def decypher(cls):
        key_file = open("key.txt")
        text_file = open("crypto.txt")
        key = list(map(int, key_file.readline().split()))
        if not isinstance(key[0], int) or not isinstance(key[1], int):
            raise ValueError
        if math.gcd(key[1], 26) != 1:
            raise ValueError
        text = text_file.readline()
        decyphered = ""
        for letter in text:
            if letter.isalpha():
                if letter.islower():
                    dec_letter = chr(((cls.modinv(key[1], 26) * (ord(letter) - 97 - key[0])) % 26) + 97)
                    decyphered += dec_letter
                else:
                    dec_letter = chr(((cls.modinv(key[1], 26) * (ord(letter) - 65 - key[0]) % 26) + 65))
                    decyphered += dec_letter
            elif letter == " ":
                decyphered += " "
            elif not letter.isspace():
                raise ValueError
        with open("decrypt.txt", "w") as file:
            file.write(decyphered)
            return decyphered       

    @classmethod
    def break_bruteforce(cls):
        text_file = open("crypto.txt")
        text = text_file.readline()
        with open('candidates.txt', 'w') as file:
            file.write("")
        a_options = [i for i in range(26) if math.gcd(i, 26) == 1]

        for i in range(26):
            for k in a_options:
                decyphered = ""
                for letter in text:
                    if letter.isalpha():
                        if letter.islower():
                            dec_letter = chr(((cls.modinv(k, 26) * (ord(letter) - 97 - i)) % 26) + 97)
                            decyphered += dec_letter
                        else:
                            dec_letter = chr(((cls.modinv(k, 26) * (ord(letter) - 65 - i) % 26) + 65))
                            decyphered += dec_letter
                    elif letter == " ":
                       decyphered += " "
                    elif not letter.isspace():
                        raise ValueError
                with open("candidates.txt", "a") as file:
                    file.write(decyphered + "\n")
                
    @classmethod
    def break_help(cls):
        text_file = open("crypto.txt")
        help_text = open("extra.txt")
        plain_text = open("plain.txt")
        text = text_file.readline()
        help = help_text.readline().split()[0]
        plain = plain_text.readline()
        decyphered = ""
        a_options = [i for i in range(26) if math.gcd(i, 26) == 1]
        possible_keys = []
        for i in range(26):
            for k in a_options:
                dec_letter = chr(((cls.modinv(k, 26) * (ord(str.lower(text[0])) - 97 - i)) % 26) + 97)
                if dec_letter == str.lower(help):
                    possible_keys.append([i, k])
        if len(possible_keys) == 0:
            print("brak klucza")
            return

        for key_pair in possible_keys:
            decyphered = ""
            for letter in text:
                if letter.isalpha():
                    if letter.islower():
                        dec_letter = chr(((cls.modinv(key_pair[1], 26) * (ord(letter) - 97 - key_pair[0])) % 26) + 97)
                        decyphered += dec_letter
                    else:
                        dec_letter = chr(((cls.modinv(key_pair[1], 26) * (ord(letter) - 65 - key_pair[0]) % 26) + 65))
                        decyphered += dec_letter
                elif letter == " ":
                    decyphered += " "
                elif not letter.isspace():
                    raise ValueError    
            if decyphered == plain.split('\n')[0]:
                with open("decrypt.txt", "w") as file:
                    file.write(decyphered)           
                with open("key-found.txt", "w") as file:
                    file.write(" ".join(list(map(str, key_pair))))
                    return decyphered

if args.c:
    if args.e:
        Cezar.cypher()
    if args.d:
        Cezar.decypher()
    if args.j:
        Cezar.break_help()
    if args.k:
        Cezar.break_bruteforce()
elif args.a:
    if args.e:
        Affine.cypher()
    if args.d:
        Affine.decypher()
    if args.j:
        Affine.break_help()
    if args.k:
        Affine.break_bruteforce()

