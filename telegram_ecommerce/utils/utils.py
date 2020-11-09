from hashlib import sha256
from json import load


def load_file(path):
    with open(path, "r") as io_file:
        return io_file.read()


def load_json_file(path):
    with open(path, "r") as json_string:
        return load(json_string)


def get_sql_commands_from_a_file(path, delimiter=";"):
    sql = load_file(path)
    commands = ( sql
        .replace("\n", "")
        .split(delimiter)
        )
    commands.pop()
    return commands


def extract_value_from_a_query(query):
    try:
        return query[0][0]
    except:
        raise Exception("cannot extract value from a null query")


def extract_list_of_values_from_a_query(query):
    extract_fist_value_from_a_tuple = (lambda tupl: tupl[0])
    return list(map(
        extract_fist_value_from_a_tuple, query))


def hash_password(plain_txt):
    plain_txt_in_bytes = bytes(str(plain_txt), 'utf-8')
    HASH = sha256()
    HASH.update(plain_txt_in_bytes)
    return HASH.hexdigest()


def get_bytes_from_a_incomming_photo(message):
    photo_size = message.photo
    telegram_file = photo_size.get_file()
    byte = telegram_file.download_as_bytearray()
    return byte


def write_file(data, file_path):
    with open(file_path, 'wb') as f:
        f.write(data)


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


