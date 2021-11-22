import struct


class BinaryReader:

    _loaded_file_path = ""
    _endianness = ""
    _reader_file = None
    _reader_position = None

    # TODO: allow for big-endian byte order?

    def __init__(self, file_path):
        self.loaded_file_path = file_path


    @property
    def reader_position(self):
        return self._reader_position


    # byte order defaults to "little", which is the only supported order for now
    def __enter__(self, endianness="little"):
        self.reader_file = open(self.loaded_file_path, 'rb')
        self._endianness = endianness
        self._reader_position = 0
        return self


    def __exit__(self, type, val, tb):
        self._reader_position = None
        self.reader_file.close()


    # returns a tuple of values from data starting at the current file position,
    # and  interpreted based on the given struct_fmt argument.
    # The file-read position will be moved forward a to the point directly after the obtained data
    #   (check the struct module from the python standard library for help defining struct_fmt)
    def get_struct(self, struct_fmt):
        if self._endianness == "big":
            struct_fmt = ">" + struct_fmt
        else:
            struct_fmt = "<" + struct_fmt

        fmt_size = struct.calcsize(struct_fmt)
        return_struct = struct.unpack(struct_fmt, self.reader_file.read(fmt_size))

        self._reader_position += fmt_size
        if len(return_struct) == 1:
            return return_struct[0]     # if returning a single value, no need for a tuple
        return return_struct


    # returns a boolean value, considering one byte at the current file position, and moves the position 8-bits forward
    # any non-zero value is counted as true
    def get_boolean(self):
        self._reader_position += 1
        return False if self.get_struct("?") == 0 else True


    # returns a byte from the current file position, and moves the position 8-bits forward
    def get_byte(self):
        self._reader_position += 1
        return self.reader_file.read(1)


    # returns an 8-bit signed integer from the current file position, and moves the position 8-bits forward
    def get_int8(self):
        return self.get_struct("b")


    # returns an 8-bit unsigned integer from the current file position, and moves the position 8-bits forward
    def get_u_int8(self):
        self._reader_position += 1
        return self.get_struct("B")


    # returns a 32-bit signed integer from the current file position, and moves the position 32-bits forward
    def get_int32(self):
        self._reader_position += 4
        return self.get_struct("i")


    # returns a 32-bit unsigned integer from the current file position, and moves the position 32-bits forward
    def get_u_int32(self):
        self._reader_position += 4
        return self.get_struct("I")


    # returns a 16-bit signed integer from the current file position, and moves the position 16-bits forward
    def get_int16(self):
        self._reader_position += 2
        return self.get_struct("h")


    # returns a 16-bit unsigned integer from the current file position, and moves the position 16-bits forward
    def get_u_int16(self):
        self._reader_position += 2
        return self.get_struct("H")


    # returns a 32-bit float from the current file position, and moves the position 32-bits forward
    def get_float(self):
        self._reader_position += 4
        return self.get_struct("f")


    def get_vec2(self):
        self._reader_position += 8
        return self.get_float(), self.get_float()


    def get_vec3(self):
        self._reader_position += 12
        return self.get_float(), self.get_float(), self.get_float()


    def get_vec4(self):
        self._reader_position += 16
        return self.get_float(), self.get_float(), self.get_float(), self.get_float()


    # returns a string of length = string_length as read from the current position
    # encoding defaults to utf-8, but may be specified
    def get_string(self, string_length, decode_as = "utf-8"):
        fmt = str(string_length) + "s"
        self._reader_position += string_length
        return self.get_struct(fmt).decode(decode_as)

    # seek to the given offset in the file (relative to start of file, not current position)
    def seek(self, seek_location):
        self._reader_position = seek_location
        self.reader_file.seek(seek_location)
        return

    def seek_from_current_pos(self, seek_distance):
        self._reader_position += seek_distance
        self.reader_file.seek(seek_distance, 1)
        return