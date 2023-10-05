import datetime
import os
import struct
import time
import uuid

# Expose function used by uuid7() to get current time in milliseconds
# since the Unix epoch.
time_ms = lambda: int(time.time() * 1e3)

def uuid7(
    ms=None,
    as_type=None,
    time_func=time_ms,
    _last=[0, 0, 0, 0],
    _last_as_of=[0, 0, 0, 0],
):
    if ms is None:
        ms = time_func()
    else:
        ms = int(ms)  # Fail fast if not an int

    rand_a = int(os.urandom(2).encode('hex'), 16)
    rand_b = int(os.urandom(8).encode('hex'), 16)
    uuid_bytes = uuidfromvalues(ms, rand_a, rand_b)

    uuid_int = int(uuid_bytes.encode('hex'), 16)
    if as_type == "int":
        return uuid_int
    elif as_type == "bin":
        return bin(uuid_int)
    elif as_type == "hex":
        return "{:>032x}".format(uuid_int)
    elif as_type == "bytes":
        return uuid.UUID(int=uuid_int).bytes
    elif as_type == "str":
        return format_byte_array_as_uuid(uuid_bytes)
    else:
        return uuid.UUID(int=uuid_int)

def uuidfromvalues(unix_ts_ms, rand_a, rand_b):
    version = 0x07
    var = 2
    rand_a &= 0xfff
    rand_b &= 0x3fffffffffffffff

    final_bytes = struct.pack(">Q", unix_ts_ms)
    final_bytes += struct.pack(">H", (version << 12) + rand_a)
    final_bytes += struct.pack(">Q", (var << 62) + rand_b)

    return final_bytes

def format_byte_array_as_uuid(arr):
    # Convert the input string to bytes
    uuid_bytes = arr.decode("hex")  # Python 2 specific

    # Create a UUID from the byte array
    return str(uuid.UUID(bytes=uuid_bytes))
    # return "{}-{}-{}-{}-{}".format(
    #     arr[:4].hex(),
    #     arr[4:6].hex(),
    #     arr[6:8].hex(),
    #     arr[8:10].hex(),
    #     arr[10:].hex()
    # )

def uuid7str(ms=None):
    "uuid7() as a string without creating a UUID object first."
    return str(uuid7(ms))  # type: ignore

print(uuid7str())
