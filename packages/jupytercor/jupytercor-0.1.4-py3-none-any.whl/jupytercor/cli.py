#!/usr/bin/env python3



import argparse

import os

import re


from jupytercor.images import *
from jupytercor.latex import *
from jupytercor.utils import *




# Create an argument parser object
parser = argparse.ArgumentParser(
    description="Convert markdown cells in a jupyter notebook with pandoc"
)
# Add an input file argument
parser.add_argument("input_file", help="The name of the input notebook file")
# Add an output file argument with no default value
parser.add_argument(
    "-o", "--output_file", help="The name of the output notebook file", default=None
)
# Add a clean flag argument with a default value of False
parser.add_argument(
    "--clean",
    help="Clean the markdown cells with pandoc conversions",
    action="store_true",
)
# Add a latex flag argument with a default value of False
parser.add_argument(
    "--latex", help="Convert the output to latex format", action="store_true"
)
# Add a images flag argument with a default value of False
parser.add_argument(
    "--images", help="Downlad image in images folder", action="store_true"
)

# Add a debug flag argument with a default value of False
parser.add_argument(
    "--debug", help="Debug mode", action="store_true"
)
# Parse the arguments
args = parser.parse_args()



def main():
    print("Hello from jupytercor !")
    if args.debug:
        data_path = os.path.join(os.path.dirname(__file__),'data')
        print(data_path)
        return None
    print(f"Input file: {args.input_file}")
    print(f"Output file: {args.output_file}")

    # Read the input notebook file from the input_file argument
    nb = nbformat.read(args.input_file, as_version=4)
    if args.clean:
        print("Démarrage du nettoyage...")
        nb = clean_markdown(nb)
        # Write the output notebook file in the same file as the input file if output_file is None or in a different file otherwise
        if args.output_file is None:
            nbformat.write(nb, args.input_file)
        else:
            nbformat.write(nb, args.output_file)
        print("Nettoyage effectué avec succès !")
    elif args.images:
        
        print("Téléchargement d'images éventuelles...")
        nb = process_images(nb)
        # Write the output notebook file in the same file as the input file if output_file is None or in a different file otherwise
        if args.output_file is None:
            nbformat.write(nb, args.input_file)
        else:
            nbformat.write(nb, args.output_file)

    elif args.latex:
        print("Latex...")
        out = convert_to_latex(nb)
        # Write the output notebook file in the same file as the input file if output_file is None or in a different file otherwise
        if args.output_file is None:
            output_file = args.input_file.replace(".ipynb",".tex")
            with open( args.output_file,"w") as f:
                f.write(out)
        else:
            with open( args.output_file,"w") as f:
                f.write(out)
        print("Latex !")


if __name__ == "__main__":
    main()
