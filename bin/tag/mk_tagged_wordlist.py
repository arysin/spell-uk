#!/usr/bin/python3

# -*- coding: utf-8 -*-

import sys
import re


except_base_tag = ''

def process_line_exceptions(line, extra_tags):
    global except_base_tag

    if not ' ' in line or re.match('.*[а-яіїєґ]/.*', line):
      return line
    if re.match('^[^ ]+ [^ ]+ [^:]?[a-z].*$', line):
      return line

    if line.startswith('# !'):
      except_base_tag = re.findall('![a-z:-]+', line)[0][1:] + ':'
      return ''
    
    base = re.findall('^[^ ]+', line)[0]
      
    out_line = re.sub('([^ ]+) ?', '\\1 ' + base + ' ' + except_base_tag + 'unknown' + extra_tags + '\n', line)
    
    if except_base_tag == 'verb:':
      base_add = 'inf:'
      if base.endswith('ся'):
        base_add = base_add + 'rev:'
      out_line = out_line.replace(except_base_tag, except_base_tag+base_add, 1)
    
    return out_line[:-1]


def process_line(line, extra_tags):
  line = re.sub('-$', '', line)

  if not ' ' in line or re.match('.*[а-яіїєґ]/.*', line):
    out_line = line
  elif re.match('^[^ ]+ [^ ]+ [^:]?[a-z].*$', line):
    out_line = line
  elif re.match('^[^ ]+ [:^<a-z0-9_].*$', line):
    out_line = re.sub('^([^ ]+) ([^<a-z].*)$', '\\1 \\1 \\2', line)
  else:
    print('hit-', line, file=sys.stderr)
    base = re.findall('^[^ ]+', line)[0]
    out_line = re.sub('([^ ]+) ?', '\\1 ' + base + ' unknown' + extra_tags + '\n', line)
    return out_line[:-1]

#  if extra_tags != '' and not re.match('.* [a-z].*$', out_line):
  if extra_tags != '' and (not ' ' in out_line or ' ^' in out_line):
    extra_tags = ' ' + extra_tags

#  if not "/" in out_line and not re.match("^[^ ]+ [^ ]+ [^ ]+$", out_line + extra_tags):
#    print("bad line:", out_line + extra_tags, file=sys.stderr)

#  if len(out_line)> 100:
#      print(out_line, file=sys.stderr)
#      sys.exit(1)

  return out_line + extra_tags



extra_tag_map = {
  'base-abbr.lst': ':abbr',
  'twisters.lst': ':bad',
  'rare.lst': ':rare',
  'slang.lst': ':slang',
  'alt.lst': ':alt'
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

      line = line.strip()
      if line == '' or (line.startswith('#') and not line.startswith('# !')):
        continue

      if '-' in line:
        line = re.sub('-( |$)', '\\1', line)

      if filename == 'twisters.lst':
        line = re.sub(' [^:^a-z].*$', '', line)

      if filename == 'exceptions.lst':
        out_line = process_line_exceptions(line, extra_tags)
      else:
        out_line = process_line(line, extra_tags)

      if out_line == '':
        continue

      print( out_line )

