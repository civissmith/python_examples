#!/usr/bin/python -B
################################################################################
# @Title: yaml_cereal.py
#
# @Author: Phil Smith
#
# @Date: Fri, 02-Jan-15 11:47AM
#
# @Project: Python Examples
#
# @Purpose: Demonstrate serialization using YAML.
#
#
################################################################################
# This script requires that the Python YAML library is installed.
import yaml
import dummy

def main(mode):

  yaml_name = "example.yml"

  # In 'dump' mode, the script will serialize data and write it to the YAML
  # file.
  if mode == 'dump':
    dump_example( yaml_name )

  # In 'load' mode, the script will read serialized data from the YAML file.
  if mode == 'load':
    load_example( yaml_name )

  # In 'both' mode, the script will serialize a set of data, then read it back
  # into a second object.
  if mode == 'both':
    both_example( yaml_name )


def dump_example( yml_name ):
  """
  Example demonstrating how to load several pieces of data into a YAML file.
  """

  # Create some slush data to put in the YAML file.

  # A single basic type.
  foo = "bar"

  # A built-in aggregated type.
  mammals = {}
  mammals["cat"]     = "Frisky"
  mammals["camel"]   = "Humpy"
  mammals["dolphin"] = "Flipper"

  # A single user-defined type.
  dumb = dummy.Dummy("First dummy!")

  # An aggregation of user-defined types. (uses list comprehension)
  dum_dums = [dummy.Dummy("Dum Dum %s" % x) for x in range(0,5)]

  # Open the YAML file for writing.
  yml = open( yml_name, 'w' )

  # Use the dump_all() method to write to the YAML file. The dump_all()
  # method takes a list or generator and will write all data to the
  # YAML file.
  data = [foo, mammals, dumb, dum_dums]
  yaml.dump_all(data, yml)
  yml.close()


def load_example( yml_name ):
  """
  Example showing how to read from a YAML file.
  """

  # Open the YAML file for reading.
  yml = open( yml_name, 'r')

  # Since the data was serialized with the dump_all() method, it must
  # be deserialized with the load_all() method. Attempting to use
  # the load() method will result in a "yaml.composer.ComposerError".

  # The object returned is a generator object, so it cannot be indexed
  # so it must be converted to a list.
  data  = list(yaml.load_all( yml ))

  # Reassociate the data to named variables.
  foo_loaded     = data[0]
  mammals_loaded = data[1]
  dumb_loaded    = data[2]
  dum_dum_loaded = data[3]

  # Print the data to show that it has been deserialized correctly.
  print "Foo: %s" % foo_loaded
  print
  print "Jar:"
  for each in mammals_loaded:
    print mammals_loaded[each]

  print
  # The deserialization process returns references to the same type, so
  # the methods defined in the dummy class can be used.
  print "Dumb:"
  dumb_loaded.test()
  print

  print "Dum Dum:"
  for each in dum_dum_loaded:
    each.test()

  # Close the YAML file.
  yml.close()

def both_example( yml_name ):
  dump_example( yml_name )
  load_example( yml_name )

if __name__ == "__main__":
   main( 'both' )

