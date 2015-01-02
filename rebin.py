#!/usr/bin/python -B
################################################################################
# @Title: rebin.py
#
# @Author: Phil Smith
#
# @Date: Fri, 02-Jan-15 06:54AM
#
# @Project: Python Examples
#
# @Purpose: Demonstrates working with binary files. Tool will take a hexdump
#           formatted file and re-create the binary.
#
#
################################################################################
import sys
import os.path


def main( in_file ):
   """
   Main entry point of the program.
   """
   
   out_file = "generated_" + in_file

   in_data = open( in_file, 'r' )
   out_data = open( out_file, 'wb' )

   # Create a container for the binary data.
   # Data stored as a tuple in the form:
   # (ADDR, [DA0,...,DA7])
   bin_data = []

   for line in in_data:

     # Hexdump's format is as follows:
     #
     # ADDR DA0 DA1 DA2 DA3 DA4 DA5 DA6 DA7
     #
     # The ADDRs are not guaranteed to be word-wise contiguous. In some programs
     # there will be 'holes' (large blocks of '0000') between sections.
     addr = line.split()[0]

     data = line.split()[1:]

     # Don't add lines marked as holes. These lines will be accounted for later.
     # Also reject any addr that doesn't have data (usually the last line).
     if addr != '*' and data:
        bin_data.append((addr, data))

   # Now loop through the data file and start building the output.
   for addr_i in range(0,len(bin_data)):

     # Addresses are strings that need to be converted to numbers. This means
     # converting from a hex string to a decimal number.
     addr = int( bin_data[addr_i][0], 16 )


     # The data elements must also be converted (so they can be written to the
     # output file correctly).
     bin_line = binify( bin_data[addr_i][1] )

     for char in bin_line:
        out_data.write(char)

     # Add holes back to the binary
     if addr_i  < len(bin_data)-1:
       n_addr = int( bin_data[addr_i+1][0], 16 )

       gap = n_addr - addr

       if gap > 16:
         # Hole detected.
         hole_size = gap/16
         null_line = '\0\0\0\0\0\0\0\0'
         null_line += '\0\0\0\0\0\0\0\0'

         cnt = 0
         # Subtract 1 from the hole size because the next valid line of data
         # will occupy that line.
         while cnt < hole_size-1:
           out_data.write(null_line)
           cnt+=1

   in_data.close()
   out_data.close()


def binify( data ):
   """
   Function returns a binary list of data suitable to be written to a file.
   """

   raw_line = "".join(data)
   bin_data = []
   swapped  = []

   length = len(raw_line)
   for i in range(0, length, 2):
     char = ''
     # Create a string representation of the character so chr() can
     # turn it into a real character.
     char += raw_line[i]
     char += raw_line[i+1]

     # The loop will byte swap the chars, this will need to be undone.
     bin_data.append(chr(int(char,16)))

   for i in range(0, len(bin_data), 2):
     swapped.append( bin_data[i+1] )
     swapped.append( bin_data[i] )
   return swapped


if __name__ == "__main__":

  # Not using argparse because this example is pretty simple.
  if len( sys.argv ) != 2:
    print "Usage: rebin <file>"
    exit(1)
  if not os.path.isfile( sys.argv[1] ):
    print "Error: Argument must be a file!"
    exit(1)
  main( sys.argv[1] )
