#!/usr/bin/python -B
################################################################################
# @Title: pickle_cereal.py
#
# @Author: Phil Smith
#
# @Date: Fri, 02-Jan-15 10:15AM
#
# @Project: Python Examples
#
# @Purpose: Demonstrate serialization using pickles.
#
#
################################################################################
import dummy
import pickle

def main(mode):

  pickle_name = "example.pkl"

  # In 'dump' mode, the script will serialize data and write it to the pickle
  # file.
  if mode == 'dump':
    dump_example( pickle_name )

  # In 'load' mode, the script will read serialized data from the pickle file.
  if mode == 'load':
    load_example( pickle_name )

  # In 'both' mode, the script will serialize a set of data, then read it back
  # into a second object.
  if mode == 'both':
    both_example( pickle_name )


def dump_example( pkl_name ):
  """
  Example demonstrating how to load several pieces of data into a pickle.
  """

  # Create some slush data to pickle.

  # A single basic type.
  foo = "bar"

  # A built-in aggregated type.
  jar = {}
  jar["sauce"] = "apple"
  jar["jelly"] = "apricot"
  jar["jam"]   = "strawberry"

  # A single user-defined type.
  dumb = dummy.Dummy("First dummy!")

  # An aggregation of user-defined types. (uses list comprehension)
  dum_dums = [dummy.Dummy("Dum Dum %s" % x) for x in range(0,5)]

  # Open the pickle file for writing.
  pkl = open( pkl_name, 'w' )

  # Use the dump() method to write to the pickle file.
  # NOTE: The end-user must unpickle into the correct order. Unpickling will
  #       return references in the order that the objects were pickled.
  pickle.dump( foo, pkl )
  pickle.dump( jar, pkl )

  # NOTE: This script pickles a user-defined type. Any script that uses the
  #       resulting pickle file does not necessarily need to import the same
  #       type, but the class defintion module MUST be available in the Python
  #       path so that the Pickler can access it.
  pickle.dump( dumb, pkl )
  pickle.dump( dum_dums, pkl )
  pkl.close()

def load_example( pkl_name ):
  """
  Example showing how to read from a pickle.
  """

  # Open the pickle for reading.
  pkl = open( pkl_name, 'r')

  # Use the load() method to unpickle data. The data will come out however it
  # was pickled.

  # If the pickling order is not known, you can keep loading until EOFError is
  # returned.
  pickles = []
  while True:

    # Append each object from the pickle into a single list.
    try:
      pickles.append( pickle.load( pkl ) )
    except EOFError:
      break

  # Reassociate the data to named variables.
  foo_loaded = pickles[0]
  jar_loaded = pickles[1]
  dumb_loaded = pickles[2]
  dum_dum_loaded = pickles[3]

  # Print the data to show that it has been unpickled correctly.
  print "Foo: %s" % foo_loaded
  print
  print "Jar:"
  for each in jar_loaded:
    print jar_loaded[each]

  print
  # The unpickling process returns references to the same type, so
  # the methods defined in the dummy class can be used.
  print "Dumb:"
  dumb_loaded.test()
  print

  print "Dum Dum:"
  for each in dum_dum_loaded:
    each.test()

  # Close the pickle.
  pkl.close()

def both_example( pkl_name ):
  dump_example( pkl_name )
  load_example( pkl_name )

if __name__ == "__main__":
   main( 'both' )

