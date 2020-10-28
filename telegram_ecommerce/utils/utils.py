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


def hash_password(plain_txt):
    plain_txt_in_bytes = bytes(str(plain_txt), 'utf-8')
    HASH = sha256()
    HASH.update(plain_txt_in_bytes)
    return HASH.hexdigest()

