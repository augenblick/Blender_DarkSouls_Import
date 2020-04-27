import os
import struct
import binascii

class BinaryReader:

    loaded_file_path = ""
    reader_file = None
    # TODO: allow for little-endian byte order?

    def __init__(self, file_path):
        self.loaded_file_path = file_path


    def __enter__(self):
        self.reader_file = open(self.loaded_file_path, 'rb')
        return self


    def __exit__(self, type, val, tb):
        self.reader_file.close()


    # returns a tuple of values from data starting at the current file position,
    # and  interpreted based on the given struct_fmt argument.
    # The file-read position will be moved forward a to the point directly after the obtained data
    #   (check the struct module from the python standard library for help defining struct_fmt)
    def get_struct(self, struct_fmt):
        try:
            fmt_size = struct.calcsize(struct_fmt)
            return_struct = struct.unpack(struct_fmt, self.reader_file.read(fmt_size))
        except struct.error as error:
            # TODO: handle exception
            pass
        if len(struct_fmt) == 1:
            return return_struct[0]
        return return_struct
        # TODO: return in a format besides tuple?


    # returns a boolean value, considering one byte at the current file position, and moves the position 8-bits forward
    # any non-zero value is counted as true
    def get_boolean(self):
        return self.get_struct("?")


    # returns a byte from the current file position, and moves the position 8-bits forward
    def get_byte(self):
        return self.reader_file.read(1)


    # returns an 8-bit signed integer from the current file position, and moves the position 8-bits forward
    def get_int8(self):
        return self.get_struct("b")


    # returns an 8-bit signed integer from the current file position, and moves the position 8-bits forward
    def get_u_int8(self):
        return self.get_struct("B")


    # returns a 32-bit signed integer from the current file position, and moves the position 32-bits forward
    def get_int32(self):
        return int.from_bytes(self.reader_file.read(4), byteorder = "big")


    # returns a 32-bit signed integer from the current file position, and moves the position 32-bits forward
    def get_u_int32(self):
        return self.get_struct("I")


    # returns a 16-bit signed integer from the current file position, and moves the position 16-bits forward
    def get_int16(self):
        return self.get_struct("h")


    # returns a 16-bit unsigned integer from the current file position, and moves the position 16-bits forward
    def get_u_int16(self):
        return self.get_struct("H")


    # returns a 32-bit float from the current file position, and moves the position 32-bits forward
    def get_float(self):
        return self.get_struct("f")


    def get_vec2(self):
        return self.get_float(), self.get_float()


    def get_vec3(self):
        return self.get_float(), self.get_float(), self.get_float()


    def get_vec4(self):
        return self.get_float(), self.get_float(), self.get_float(), self.get_float()


    # returns a string of length = string_length as read from the current position
    # encoding defaults to utf-8, but may be specified
    def get_string(self, string_length, decode_as = "utf-8"):
        char_list = []
        for count in range(0, string_length):
            char = self.reader_file.read(1)

            try:
                char_list.append(char.decode(decode_as))
            except:
                # TODO: throw exception
                print("Error: a character was reached that could not be decoded as " + decode_as + ".")
                return

        final_string = ""
        return final_string.join(char_list)

    # seek to the given offset in the file (relative to start of file, not current position)
    def seek(self, seek_location):
        self.reader_file.seek(seek_location)
        return


# ================= TESTING ==========================

with BinaryReader("D:\\DATA\\map\\m10_01_00_00\\m3190B1A10.flver") as br:
    print(br.get_struct("?4sIif"))