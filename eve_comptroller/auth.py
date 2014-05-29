import hashlib
import logging
log = logging.getLogger(__name__)
from os import urandom
from base64 import b64encode, b64decode

from pbkdf2 import PBKDF2

from eve_comptroller import settings
from eve_comptroller.models import DBSession, User


#
# Password hashing.
#

def create_hash(password, 
                hmac='sha512', 
                iterations=settings.auth_iterations,
                key_len=settings.auth_key_len,
                salt_len=settings.auth_salt_len):
    """
    Generate a random salt and hash the password per NIST 800-132 recommendation.
    
    Adapted from Simon Sapin's PBKDF2 hasher, but using a different PBKDF2 library.
    
    http://exyr.org/2011/hashing-passwords/
    """
    if isinstance(password, unicode):
        password = password.encode('utf-8')
    salt = urandom(salt_len)
    key = PBKDF2(password, salt, iterations, getattr(hashlib, hmac)).read(key_len)
    return 'PBKDF2$%s$%s$%s$%s$%s' % (hmac.upper(),
                                   key_len,
                                   iterations,
                                   b64encode(salt),
                                   b64encode(key))

def check_hash(password, hash):
    """
    Compare the generated password hash to the stored hash.
        
    Adapted from Simon Sapin's PBKDF2 hasher, but using a different PBKDF2 library.
    
    http://exyr.org/2011/hashing-passwords/
    """
    if isinstance(password, unicode):
        password = password.encode('utf-8')
    kdf, hmac, key_len, iterations, salt, key_a = hash.split('$')
    hmac = hmac.lower()
    key_len = int(key_len)
    iterations = int(iterations)
    salt = b64decode(salt)
    key_a = b64decode(key_a)
    
    assert kdf == 'PBKDF2'
    assert hmac in hashlib.algorithms
    
    key_b = PBKDF2(password, salt, iterations, getattr(hashlib, hmac)).read(key_len)
    return key_a == key_b

#
# Authentication utilities.
#
def check_credentials(username, password):
    try:
        user = DBSession.query(User).filter(User.username == username).one()
        if check_hash(password, user.password):
            return True
    except:
        pass
    return False

def list_groups(username, request):
    groups = []
    try:
        user = DBSession.query(User).filter(User.username == username).one()
        if user.is_admin:
            groups.append('admin')
    except:
        return
    return groups

