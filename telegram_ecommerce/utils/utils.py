from binascii import Error as Base64Error
from base64 import urlsafe_b64decode, urlsafe_b64encode
from hashlib import pbkdf2_hmac, sha256
from hmac import compare_digest
from secrets import token_bytes


PASSWORD_SCHEME = "pbkdf2_sha256"
PASSWORD_ITERATIONS = 600_000


def create_admins_set(admins_str):
    admins_map = map(lambda name: name.replace(" ", "").replace("\n", ""), admins_str.split(","))
    return set(filter(bool, admins_map))


def hash_password(plain_txt):
    """Create a per-password salted PBKDF2 hash suitable for database storage."""
    if not isinstance(plain_txt, str) or not plain_txt:
        raise ValueError("A nonempty password is required")
    salt = token_bytes(16)
    digest = pbkdf2_hmac("sha256", plain_txt.encode("utf-8"), salt, PASSWORD_ITERATIONS)
    return "$".join((PASSWORD_SCHEME, str(PASSWORD_ITERATIONS),
                     urlsafe_b64encode(salt).decode("ascii"),
                     urlsafe_b64encode(digest).decode("ascii")))


def verify_password(plain_txt, stored_hash):
    """Return (valid, needs_rehash); accept old SHA-256 hashes for upgrade."""
    if not isinstance(plain_txt, str) or not isinstance(stored_hash, str):
        return False, False
    if stored_hash.startswith(PASSWORD_SCHEME + "$"):
        try:
            scheme, iterations, salt_text, digest_text = stored_hash.split("$")
            count = int(iterations)
            if scheme != PASSWORD_SCHEME or not 1 <= count <= PASSWORD_ITERATIONS:
                return False, False
            salt = urlsafe_b64decode(salt_text.encode("ascii"))
            expected = urlsafe_b64decode(digest_text.encode("ascii"))
            if len(salt) != 16 or len(expected) != 32:
                return False, False
        except (ValueError, UnicodeError, Base64Error):
            return False, False
        candidate = pbkdf2_hmac("sha256", plain_txt.encode("utf-8"), salt, count)
        valid = compare_digest(candidate, expected)
        return valid, valid and count < PASSWORD_ITERATIONS
    if len(stored_hash) == 64:
        try:
            int(stored_hash, 16)
        except ValueError:
            return False, False
        valid = compare_digest(sha256(plain_txt.encode("utf-8")).hexdigest(), stored_hash)
        return valid, valid
    return False, False


def get_bytes_from_a_incomming_photo(message):
    photo_size = message.photo
    telegram_file = photo_size.get_file()
    byte = telegram_file.download_as_bytearray()
    return byte


def float_from_user_input(user_input):
    return float(
        user_input
        .replace(" ", "")
        .replace("\n", "")
        .replace(",", ".")
    )


def get_key(dictionary, value):
    """ Funtion to return the key that match with the passed value
        >>> get_key({'py' : 3.14, 'other' : 666}, 3.14)
        'py'
    """
    values = list(dictionary.values())
    keys = list(dictionary.keys())
    return (keys[
        values.index(value)
        ])
