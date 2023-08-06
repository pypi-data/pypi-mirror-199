# external imports
import sha3

# local imports
from .encoding import to_checksum_address


def to_digest(data):
    h = sha3.keccak_256()
    h.update(data)
    return h.digest()

# ERC191 - version 0x00
def to_validator_message(data, validator, digest=False):
    a = to_checksum_address(validator)
    v = bytes.fromhex(a)
    r = b'\x19\x00' + v + data
    if digest:
        r = to_digest(r)
    return r


# ERC191 - version 0x45
def to_personal_message(data, digest=False):
    ethereumed_message_header = b'\x19\x45' + 'thereum Signed Message:\n{}'.format(len(data)).encode('utf-8')
    r = ethereumed_message_header + data
    if digest:
        r = to_digest(r)
    return r



