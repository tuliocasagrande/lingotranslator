#!/usr/bin/python
# This Python file uses the following encoding: utf-8

import os
import re

# On most systems this includes the characters space, tab, linefeed, return, formfeed, and vertical tab.
# '\t\n\x0b\x0c\r '
from string import whitespace as tokenizer

lingoDict = {}
englishDict = {}

englishMode = False
lingoMode = False
keepMode = False

def translate(fileName, mode):
  global lingoDict, englishDict, englishMode, lingoMode, keepMode

  englishMode = mode[0] == 'Y'
  lingoMode = mode[1] == 'Y'
  keepMode = mode[2] == 'Y'

  try:
    input = open(fileName)

    module_path = os.path.dirname(__file__)
    lingoDict = readDictFile(open(os.path.join(module_path, 'dictionaries', 'lingoDict.txt')))
    englishDict = readDictFile(open(os.path.join(module_path, 'dictionaries', 'englishDict.txt')))

    file_path, file_name = os.path.split(fileName)
    output = open(os.path.join(file_path, 'translated_{0}_{1}'.format(mode, file_name)), 'w')

    # Translating line by line
    for line in input:

      # Writing the translated line to the output file
      output.write(parser(line))

  except IOError as e:
    print e
    print 'This file really exists?'
    sys.exit()


def parser(line):

  # To ensure that will tokenize the last word of the line
  line = line + ' '

  buffer = ''
  english_token = ''
  lingo_token = ''
  last_english_token = ''
  token_changed = True

  for c in line:

    # First conversion, the character is lowercased
    c = c.lower()

    # The english_token just accepts letters and apostrophes
    if c.isalpha() or c == '\'':
      english_token += c
      lingo_token += c

    else:
      # English translation
      if englishMode and len(english_token) > 1 and english_token in englishDict:
        if englishDict[english_token] == english_token:
          buffer += putSpace(buffer) + english_token
          token_changed = False
        else:
          buffer += putSpace(buffer) + englishDict[english_token]

        last_english_token = english_token

      english_token = ''

      # The lingo_token continues accepting characters until reach a tokenizer
      if c not in tokenizer:  # '\t\n\x0b\x0c\r '
        lingo_token += c

      else:
        # Lingo translation
        if lingo_token != last_english_token:

          # It will perform 4 searches in the Lingo dictionary:
          # 1- With the entire token
          # 2- With the entire token, but the last character
          # 3- With the entire token, but the first character
          # 4- With the entire token, but the first and last characters
          lingo_token_wo_last = lingo_token[:-1]
          lingo_token_wo_first = lingo_token[1:]
          lingo_token_wo_first_last = lingo_token[1:-1]

          first_character = lingo_token[0]
          last_character = lingo_token[-1]

          if lingoMode and lingo_token in lingoDict:
            buffer += putSpace(buffer) + lingoDict[lingo_token]

          elif lingoMode and lingo_token_wo_last in lingoDict:
            buffer += putSpace(buffer) + lingoDict[lingo_token_wo_last] + last_character

          elif lingoMode and lingo_token_wo_first in lingoDict:
            buffer += putSpace(buffer) + first_character + lingoDict[lingo_token_wo_first]

          elif lingoMode and lingo_token_wo_first_last in lingoDict:
            buffer += putSpace(buffer) + first_character + lingoDict[lingo_token_wo_first_last] + last_character

          # Converting numbers to zeros
          elif lingo_token.isdigit():
            buffer += putSpace(buffer)

            for each in lingo_token:
              buffer += '0'


        # Last translation, writing the original token
        if keepMode:
          if token_changed or lingo_token != last_english_token:
            buffer += putSpace(buffer) + lingo_token

        lingo_token = ''
        last_english_token = ''
        token_changed = True

        # Writing the tokenizer
        if c == ' ':
          buffer += putSpace(buffer)
        else:
          buffer += c

  # Removing the whitespace of the first line of this function
  return buffer[:-1]


def readDictFile(dictFile):
  d = {}

  for line in dictFile:
    line = line.replace("\n", "")
    s = line.split("\t", 1)
    d[s[0]] = s[1]

  return d


def putSpace(buffer):
  if buffer and buffer[-1] not in tokenizer:
    return ' '
  else:
    return ''
