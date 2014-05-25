#
#
#    Adapted from Simon Sapin's PBKDF2 hasher, but using a different PBKDF2 library.
#    
#    http://exyr.org/2011/hashing-passwords/
#    
#
import hashlib
from os import urandom
from base64 import b64encode, b64decode

from pbkdf2 import PBKDF2

HASH_NAME = 'SHA256'
HASH_FUNCTION = hashlib.sha256
KEY_LENGTH = 32     # bytes
SALT_LENGTH = 16    # bytes
COST_FACTOR = 1000

def create_hash(password):
    """Generate a random salt and hash the password per NIST 800-132 recommendation."""
    if isinstance(password, unicode):
        password = password.encode('utf-8')
    salt = urandom(SALT_LENGTH)
    key = PBKDF2(password, salt, COST_FACTOR, HASH_FUNCTION).read(KEY_LENGTH)
    return 'PBKDF2$%s$%s$%s$%s' % (HASH_NAME,
                                   COST_FACTOR,
                                   b64encode(salt),
                                   b64encode(key))

def check_hash(password, hash):
    """Compare the generated password hash to the stored hash."""
    if isinstance(password, unicode):
        password = password.encode('utf-8')
    kdf, hf, cost, salt, key_a = hash.split('$')
    assert kdf == 'PBKDF2'
    assert hf == HASH_NAME
    cost = int(cost)
    salt = b64decode(salt)
    key_a = b64decode(key_a)
    key_b = PBKDF2(password, salt, cost, HASH_FUNCTION).read(KEY_LENGTH)
    return key_a == key_b

