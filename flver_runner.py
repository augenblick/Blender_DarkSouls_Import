'''import os
import GetOffsets
import flver
import DDS_extract'''
from ds_import import flver_extractor




'''
filepath = "D:\\DATA\\map\\m10_01_00_00\\m2510B1A10.flver"
pathTPFs = ""
pathDDSs = ""

# fileExtension = os.path.splitext(os.path.split(filepath)[1])[1]
# meshName = os.path.splitext(os.path.split(filepath)[1])[0]

flverDataOffsets = [0]


for offset in flverDataOffsets:
    thisFile = flver.flv_file(filepath, pathTPFs, pathDDSs, offset)
    meshInfo = thisFile.get_meshInfo()
    faceTotal = 0
    materialList = thisFile.get_MaterialsForBlender()
'''

filepath = "D:\\DATA\\map\\m10_01_00_00\\m2510B1A10.flver"
# filepath = "D:\\† Carpenter Brut † TURBO KILLER † Directed by Seth Ickerman † Official Video †.mp4"

importer = flver_extractor.FlverExtractor()
importer.extract_model(filepath)