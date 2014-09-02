#!/usr/bin/python3

import sys
import re


def process_line(line, extra_tags):
  line = re.sub('-$', '', line)

  if not ' ' in line or re.match('.*[а-яіїєґ]/.*', line):
    out_line = line
  elif re.match('^[^ ]+ [^ ]+ [^:]?[a-z].*$', line):
    out_line = line
  elif re.match('^[^ ]+ [^:]?[a-z].*$', line):
    out_line = re.sub('^([^ ]+) ([a-z].*)$', '\\1 \\1 \\2', line)
  else:
    out_line = re.sub(' ', '\n', line)
    
    
  if extra_tags != '' and not re.match('.* [a-z].*$', out_line):
    extra_tags = ' ' + extra_tags

  return out_line + extra_tags



extra_tag_map = {
  'base-abbr.lst': ':abbr',
  'twisters.lst': ':bad',
  'rare.lst': ':rare',
  'verify.lst': ':rare'
}


for filename in sys.argv:
  if filename == sys.argv[0]:
    continue

  if filename in extra_tag_map:
    extra_tags = extra_tag_map[filename]
  else:
    extra_tags = ''

  with open(filename) as f:
    for line in f:

      if filename == 'twisters.lst':
        line = re.sub(' .*$', '', line)

      line = line.strip()
      if line.startswith('#') or line == '':
        continue

      print( process_line(line, extra_tags) )

