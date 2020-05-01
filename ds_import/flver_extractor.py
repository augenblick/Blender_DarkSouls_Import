from ds_import import binary_reader
from ds_import import errors

test_file_path = "D:\\DATA\\map\\m10_01_00_00\\m3210B1A10.flver"

class FlverExtractor:

    __flver_file_path = ""

    '''def __init__(self, flver_file_path):
        self.__file_path = flver_file_path'''

    def __is_ds1_flver(self):

        with binary_reader.BinaryReader(self.__file_path):
            if self.__file_path == "":
                raise errors.UnreadableFormatError("Test")
            is_flver = False
            is_little_endian = False
            is_v2_12 = False

        pass


    def extract_model(self, __flver_file_path):

        self.__flver_file_path = __flver_file_path

        self.__is_ds1_flver()

        # how many meshes
        # how many vert sets
        # where is vertex buffer(s)

        # get vertex buffer format(s)
        # get vertices

