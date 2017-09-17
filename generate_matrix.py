from argparse import ArgumentParser
from itertools import count
from random import randint

def main():
  parser = ArgumentParser(description="Generate random matrices for P2")
  parser.add_argument("mat_a", default="matA_gen.mif",
                      help="Matrix A .mif output")
  parser.add_argument("mat_b", default="matB_gen.mif",
                      help="Matrix B .mif output")
  args = parser.parse_args()

  header_template = (
  "DEPTH = {};\n"
  "WIDTH = 8;\n"
  "ADDRESS_RADIX = HEX;\n"
  "DATA_RADIX = HEX;\n\n"
  "CONTENT BEGIN\n\n")

  datum_template = "{:03x} : {:02x};"

  footer_template = "\nEND;"

  mat_a = [[randint(0, 255) for c in range(64)] for r in range(64)]
  mat_b = [[randint(0, 255)] for r in range(64)]
  acc_product = 0

  for i in range(64):
    for j in range(64):
      acc_product += mat_a[i][j] * mat_b[j][0]

  with open(args.mat_a, "w") as fout:
    addr_counter = count(0)
    data_lines = [
        datum_template.format(next(addr_counter), c) for r in mat_a for c in r]
    fout.write(header_template.format(4096) + "\n".join(data_lines)
               + footer_template)

  with open(args.mat_b, "w") as fout:
    addr_counter = count(0)
    data_lines = [
        datum_template.format(next(addr_counter), c) for r in mat_b for c in r]
    fout.write(
        header_template.format(64) + "\n".join(data_lines) + footer_template)

  print("Matrix files created: {} {}".format(args.mat_a, args.mat_b))
  print("Accumulated product: {:04x}".format(acc_product % 65536))

if __name__ == "__main__":
  main()
