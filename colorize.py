#!/usr/bin/python -B
################################################################################
# @Title: colorize.py
#
# @Author: Phil Smith
#
# @Date: Mon, 29-Dec-14 11:36PM
#
# @Project: Python Examples
#
# @Purpose: Demonstrate how to use ANSI escape sequences to add color to 
#           output.
#
#
################################################################################
import sys

# Define some names to make
BOLD       = 'bold'
FAINT      = 'faint'
ITALIC     = 'italic'
CROSSED    = 'crossed'
ITALICS    = 'italic'
NEGATIVE   = 'negative'
CONCEALED  = 'concealed'
UNDERLINE  = 'underline'
UNDERLINED = 'underline'

RED     = 'red'
BLUE    = 'blue'
CYAN    = 'cyan'
GREEN   = 'green'
BLACK   = 'black'
WHITE   = 'white'
YELLOW  = 'yellow'
MAGENTA = 'magenta'

def print_line( text, bg=None, fg=None, st=None, eol='\n'):
  """
  Print a line of text. Optionally change the background (bg) color, foreground 
  (fg) color, print style (st) or line terminator (eol).

  Colors Supported:
    BLACK
    YELLOW
    RED
    GREEN
    BLUE
    MAGENTA
    CYAN
    WHITE

  Styles Supported:
   BOLD
   FAINT
   ITALIC
   UNDERLINE
   NEGATIVE
   CONCEALED
   CROSSED 
  """

  if not bg:
    bg = ''

  if not fg:
    fg = ''
  
  if not st:
    st = ''

  bg = bg.upper()
  fg = fg.upper()
  st = st.upper()

  # Set the background colors
  if 'BLACK' in bg:
    bg = '\x1B[40m'
  if 'RED' in bg:
    bg = '\x1B[41m'
  if 'GREEN' in bg:
    bg = '\x1B[42m'
  if 'YELLOW' in bg:
    bg = '\x1B[43m'
  if 'BLUE' in bg:
    bg = '\x1B[44m'
  if 'MAGENTA' in bg:
    bg = '\x1B[45m'
  if 'CYAN' in bg:
    bg = '\x1B[46m'
  if 'WHITE' in bg:
    bg = '\x1B[47m'

  # Set the foreground colors
  if 'BLACK' in fg:
    fg = '\x1B[30m'
  if 'RED' in fg:
    fg = '\x1B[31m'
  if 'GREEN' in fg:
    fg = '\x1B[32m'
  if 'YELLOW' in fg:
    fg = '\x1B[33m'
  if 'BLUE' in fg:
    fg = '\x1B[34m'
  if 'MAGENTA' in fg:
    fg = '\x1B[35m'
  if 'CYAN' in fg:
    fg = '\x1B[36m'
  if 'WHITE' in fg:
    fg = '\x1B[37m'

  # Build the style format string
  style = ''
  if 'BOLD' in st:
    style += '\x1B[1m'
  if 'FAINT' in st:
    style += '\x1B[2m'
  if 'ITALIC' in st:
    style += '\x1B[3m'
  if 'UNDERLINE' in st:
    style += '\x1B[4m'
  if 'NEGATIVE' in st:
    style += '\x1B[7m'
  if 'CONCEALED' in st:
    style += '\x1B[8m'
  if 'CROSSED' in st:
    style += '\x1B[9m'
 
  # This check prevents writing ANSI escape codes into files.
  # It's not foolproof, but works pretty well with Linux terminals.
  is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

  if is_a_tty:
    sys.stdout.write( style + bg + fg + text + '\x1B[0m' + eol)
  else:
    sys.stdout.write(text +  eol)
