#!/usr/bin/python -B
################################################################################
# Copyright (c) 2015 Phil Smith
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################
################################################################################
# @Title: watcherd.py
#
# @Author: Phil Smith
#
# @Date: Thu, 01-Jan-15 01:05AM
#
# @Project: Python Examples
#
# @Purpose: Demonstration of how to create daemons. Like a good daemon, it
#           causes trouble.
#
#
################################################################################
import os
import re
import sys
import time
import os.path as op


def daemonize( tgt, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
  """
  Function causes the calling process to become a daemon. Code originated
  from the book 'Python of Unix and Linux System Administration' by Noah Gift
  and Jeremy M. Jones (c) 2008 ISBN: 978-0-596-51582-9.
  """

  #
  # This fork causes the child to give up it's controlling terminal.
  #
  try:
    pid=os.fork()
    if pid > 0:
      # Execution is in the parent. The parent must exit.
      sys.exit(0)
  except OSError as err:
    sys.stderr.write("Fork #1 failed: (%d) %s\n" % (err.errno, err.strerror))
    exit(1)


  #
  # Now that the child is free of the parent, move to a safe location. This
  # prevents the child process from holding onto resources that may need to be
  # released. For instance, the child could prevent a file system from
  # unmounting if these steps were not taken.
  #

  # Normally, this would change to the root directory, but in this case it
  # must change to the directory to be targeted.
  # (normal) os.chdir('/')
  os.chdir(tgt)

  # Set a permissive mask so files created by the daemon are not completely
  # inaccessible.
  os.umask(0)

  # Claim session leadership by creating a new session.
  os.setsid()


  # Perform a second fork to ensure that no controlling terminal can gain
  # access to the process.
  try:
    pid=os.fork()
    if pid > 0:
      # Execution is in the parent. The parent must exit.
      sys.exit(0)
  except OSError as err:
    sys.stderr.write("Fork #2 failed: (%d) %s\n" % (err.errno, err.strerror))
    exit(1)

  #
  # The process is now a daemon. The final step is to clean up file descriptors.
  #

  for f in sys.stdout, sys.stderr: f.flush()
  si = file(stdin, 'r')
  so = file(stdout, 'a+')
  se = file(stderr, 'a+', 0)
  os.dup2(si.fileno(), sys.stdin.fileno())
  os.dup2(so.fileno(), sys.stdout.fileno())
  os.dup2(se.fileno(), sys.stderr.fileno())


def watcher( directory='.' ):
  """
  This function scans a directory looking for specific file extensions. If files
  match it's known extensions, it renames them. Remember kiddos, with great
  power comes great responsibility...
  """

  #
  # First things first, become a daemon.
  #
  daemonize( directory )

  # Define the types of files to watch. Each type will have their
  # names changed to reflect their type.
  pictures = "jpg jpeg bmp png gif svg "
  movies   = "wmv mp4 mov "
  music    = "mp3 ogg "
  docs     = "odt doc docx xls xlsx pdf "

  pic_prefix = "picture_"
  mov_prefix = "movie_"
  mus_prefix = "music_"
  doc_prefix = "document_"

  prefixes = pic_prefix + " " + mov_prefix + " " + mus_prefix + " " + doc_prefix
  types = pictures + movies + music + docs
  rules = []

  # Do this work forever.
  while(1):
    files = get_changeable_files( directory, prefixes, types )


    # When execution reaches here, the files list contains only files that need to
    # be renamed. The next step is to change the files based on their type.

    rules.append( (pictures, pic_prefix ) )
    rules.append( (movies, mov_prefix) )
    rules.append( (music, mus_prefix) )
    rules.append( (docs, doc_prefix) )
    rename( files, rules )

    # Don't hog the CPU
    time.sleep(1)


def rename( files, rules ):
  """
  This function applies the renaming rules to the file types.
  """

  # Look for the correct rule for each file type.
  for file_name in files:
    ext = file_name.split('.')[-1]

    for rule in rules:
      prefix = rule[1]

      if ext.lower() in rule[0]:
        file_count = 0

        # Build the string to create the new name.
        new_name = "%s%02d.%s" % ( prefix, file_count, ext.lower())

        # Take care not to overwrite any existing files.
        while op.exists( new_name ):
          file_count += 1
          new_name = "%s%02d.%s" % ( prefix, file_count, ext.lower())

        # Check to make sure the source file exists. This is a sampling
        # problem - the file may exist when the list is built, but
        # not exist when the rename is called ( because it was already
        # being renamed).
        if op.exists( file_name ):
          os.rename(file_name, new_name)


def get_changeable_files( directory, prefixes, types ):
  """
  This function returns a list of files that need to have their names changed.
  """

  # Get a list of all files in the directory.
  files = os.listdir( directory )
  changes = []

  # Find files that have not been renamed
  # Use regular expressions to determine if the name is a match.
  for file_name in files:

    # Build the regex to filter out the changed files.
    re_str = prefixes.split()

    re_str = "|".join(re_str)
    safe = re.search( re_str + "\d+", file_name )

    if safe:
      # Since the file has been renamed, it is "safe" and will not be touched.
      continue

    # Files here may not be safe. Check the extension to see if the file
    # Should be renamed.
    ext = file_name.split('.')[-1]
    if ext.lower() in types:
      changes.append(file_name)

  return changes

if __name__ == "__main__":
  watcher()
