# Adds hydrogens to the structure
# Requires two system argumnets: inputa nd output filepaths
from sys import argv
from pymol import cmd

input_filepath = argv[3]
output_filepath = argv[4]
print("Input filepath: {}".format(input_filepath))
print("Output filepath: {}".format(output_filepath))

cmd.load(input_filepath, "complex")
cmd.h_add("complex")
cmd.save(output_filepath)
