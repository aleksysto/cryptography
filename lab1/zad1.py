#copyright aleksy stocki B)
import argparse

parser = argparse.ArgumentParser()

# -c cezar, -a afiniczny, -e szyfruj, -d odszyfruj
# -j kryptoanaliza z tekstem jawnym, -k kryptoanaliza w oparciu o kryptogram
code_group = parser.add_mutually_exclusive_group(required=True)

code_group.add_argument("-c", default=False)
code_group.add_argument("-a", default=False) 

use_group = parser.add_mutually_exclusive_group(required=True)
use_group.add_argument("-e", default=False)
use_group.add_argument("-d", default=False)
use_group.add_argument("-j", default=False)
use_group.add_argument("-k", default=False)

args = parser.parse_args()

print(args)
