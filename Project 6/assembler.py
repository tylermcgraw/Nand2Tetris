# wsl dir: /windir/c/Users/tyler/OneDrive/Desktop/Programming/Classes/Nand2Tetris/Projects/06

import sys


def main():
  # Initialize symbol table
  symbols = initSymbols()

  # Store assembly code in a list
  assembly = readData()

  # Add label symbols to table
  symbols = addLabels(assembly, symbols)

  # Add var symbols to table
  symbols = addVariables(assembly, symbols)

  # Convert assembly to machine language (binary)
  binary = assemblyToBinary(assembly, symbols)

  # Write binary to new file
  writeData(binary, symbols)


def writeData(binary, symbols):
  file_name = sys.argv[1][sys.argv[1].rfind("/") + 1:sys.argv[1].rfind(".")] + ".hack"
  with open(file_name, "w") as file:
    file.writelines(binary)
  with open("pong_symbols.txt", "w") as sym:
    sym.writelines(symbols)


def assemblyToBinary(assembly, symbols):
  binary = []
  for line in assembly:
    # If a command, convert to binary memory address
    if line[0] == "@":
      address = line[1:]
      # Convert to binary string
      if not address.isdigit():
        new_line = "{:b}".format(symbols[address])
      else:
        new_line = "{:b}".format(int(address))
      # Make sure first digit is 0 and length is 16
      length = len(new_line)
      if length > 15:
        new_line = new_line[length - 15:]
      elif length < 15:
        for i in range(1, 15 - length + 1):
          new_line = "0" + new_line
      # Length of line is 15, add 0 to make it an a command with length 16
      new_line = "0" + new_line + "\n"
      binary.append(new_line)
    #If c command, convert to binary command
    else:
      new_line = "1110000000000000"
      # Convert dest field
      if line.find("=") != -1:
        dest = line[:line.find("=")]
        line = line[line.find("=") + 1:]
        if dest == "M":
          append = "001"
        elif dest == "D":
          append = "010"
        elif dest == "MD":
          append = "011"
        elif dest == "A":
          append = "100"
        elif dest == "AM":
          append = "101"
        elif dest == "AD":
          append = "110"
        else: # dest == "AMD":
          append = "111"
        new_line = new_line[:-6] + append + new_line[-3:]
      # Convert jmp field
      if line.find(";") != -1:
        jmp = line[line.find(";") + 1:]
        line = line[:line.find(";")]
        if jmp == "JGT":
          append = "001"
        elif jmp == "JEQ":
          append = "010"
        elif jmp == "JGE":
          append = "011"
        elif jmp == "JLT":
          append = "100"
        elif jmp == "JNE":
          append = "101"
        elif jmp == "JLE":
          append = "110"
        else: # jmp == "JMP"
          append = "111"
        new_line = new_line[:-3] + append
      # Convert comp field
      # Convert a of comp
      m = line.find("M")
      if m != -1:
        new_line = new_line[:3] + "1" + new_line[4:]
        line = line[:m] + "A" + line[m + 1:] # For convenience replace M with A for following if statements
      # Convert c1-c6 of comp
      if line == "0":
        append = "101010"
      elif line == "1":
        append = "111111"
      elif line == "-1":
        append = "111010"
      elif line == "D":
        append = "001100"
      elif line == "A":
        append = "110000"
      elif line == "!D":
        append = "001101"
      elif line == "!A":
        append = "110001"
      elif line == "-D":
        append = "001111"
      elif line == "-A":
        append = "110011"
      elif line == "D+1":
        append = "011111"
      elif line == "A+1":
        append = "110111"
      elif line == "D-1":
        append = "001110"
      elif line == "A-1":
        append = "110010"
      elif line == "D+A":
        append = "000010"
      elif line == "D-A":
        append = "010011"
      elif line == "A-D":
        append = "000111"
      elif line == "D&A":
        append = "000000"
      else: # line == "D|A":
        append = "010101"
      new_line = new_line[:4] + append + new_line[-6:] + "\n"
      binary.append(new_line)
  return binary


def addVariables(assembly, symbols):
  next_address = 16
  for line in assembly:
    # Check if line has a variable - must be of the form @variable
    if line[0] == "@":
      # If no symbol exists, add to symbols dict; ignore if @[number]
      var = line[1:]
      if not var.isdigit():
        if symbols.get(var) == None:
          symbols[var] = next_address
          next_address += 1
  return symbols


def addLabels(assembly, symbols):
  line_num = 0
  for line in assembly:
    # Check if line has a label symbol - must be of the form (LABEL)
    start = line.find("(")
    if start != -1:
      end = line.find(")")
      # Add symbol to table
      symbols[line[start + 1:end]] = line_num
      # Remove line from assembly list
      assembly.pop(line_num)
    line_num += 1
  return symbols


def readData():
  # Ensure correct usage
  if len(sys.argv) != 2:
    sys.exit("Usage: python3 assembler.py path/file.asm")

  data = []
  # Import file and fill in list
  with open(sys.argv[1], "r") as file:
    for line in file:
      # Remove /n at end of line
      line = line[:-1]
      # Remove comments starting with //
      if line.find("//") != -1:
        line = line[:line.find("//")]
      # Remove white space
      line = line.strip()
      # Don't add if line is empty
      if line != "":
        data.append(line)
  return data


def initSymbols():
  # Predefined symbols
  symbols = {
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4
  }
  for i in range(16):
    symbols["R" + str(i)] = i
  return symbols


main()
