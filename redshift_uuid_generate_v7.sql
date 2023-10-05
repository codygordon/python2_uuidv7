CREATE OR REPLACE FUNCTION uuid_generate_v7()
RETURNS VARCHAR
STABLE 
AS $$
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

  return str(uuid7())
$$LANGUAGE plpythonu;