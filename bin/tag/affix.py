#!/usr/bin/python3

# -*- coding: utf-8 -*-
# This script loads hunspell affixes and allows to perform some actions:
# like expand, munch etc

import sys
import re
import os
import subprocess
import logging


#logging.basicConfig(filename='affix.log',level=logging.DEBUG)
logger = logging.getLogger('affix')
#logger.setLevel(logging.DEBUG)

class AffixGroup(object):
    #@profile
    def __init__(self, match_, pfx):
        self.match = match_
        self.affixes = []
        self.pfx = pfx

        if pfx:
          self.match_start_re = re.compile('^'+match_)
        else:
          self.match_ends_re = re.compile(match_+'$')

        self.counter = 0

    def matches(self, word):
        if self.pfx:
          return self.match_start_re.match(word)
        
        return self.match_ends_re.search(word)



class Affix(object):

    #@profile
    def __init__(self, from_, to_, tags_, pfx):
        if from_ != '0':
          self.fromm = from_
        else:
          self.fromm = ''
        if to_ != '0':
          self.to = to_
        else:
          self.to = ''
          
        self.tags = tags_   # optional tags field for POS dictionary
        self.pfx = pfx
        
        if pfx:
           self.sub_from_len = len(self.fromm)
#          self.sub_from_pfx = re.compile('^'+self.fromm)
        else:
           self.sub_from_len = -len(self.fromm) if self.fromm != '' else 100
#          self.sub_from_sfx = re.compile(self.fromm+'$')

    def apply(self, word):
      if self.pfx:
        return self.to + word[self.sub_from_len:]

      return word[:self.sub_from_len] + self.to


prefixes = []
affixMap = {}


#@profile
def expand_prefixes(word, affixFlags):
    words = [ word ]

    for affixFlag in affixFlags:
      if affixFlag not in prefixes:
        continue
          
      appliedCnt = 0
      affixGroupMap = affixMap[affixFlag]
      for affixGroup in affixGroupMap.values():
        if affixGroup.matches(word):
            for affix in affixGroup.affixes:
#                wrd = affix.sub_from_pfx.sub(affix.to, word)
                wrd = affix.apply(word)
                words.append( wrd )
                appliedCnt += 1
            affixGroup.counter += 1

      if appliedCnt == 0:
        print("WARNING: Flag", affixFlag, "not applicable to", word, file=sys.stderr)
    
    return words



#@profile
def expand_suffixes(word, affixFlags):
    words = [ word ]

    for affixFlag in affixFlags:
      if affixFlag in prefixes:
          continue
          
      if not affixFlag in affixMap:
          print("ERROR: Invalid flag", affixFlag, "for", word, file=sys.stderr)
          continue
          
      appliedCnt = 0
        
      affixGroupMap = affixMap[affixFlag]
      for match, affixGroup in affixGroupMap.items():
        if affixGroup.matches(word):
          for affix in affixGroup.affixes:
#             deriv = affix.sub_from_sfx.sub(affix.to, word)
             deriv = affix.apply(word)
             words.append(deriv)
             appliedCnt += 1
          affixGroup.counter += 1
        
      if appliedCnt == 0:
        print("WARNING: Flag", affixFlag, "not applicable to", word, file=sys.stderr)

    return words



#@profile
def load_affixes(filename):
 re_afx=re.compile('^[SP]FX[ \t]+[a-zA-Z0-9][ \t]+[a-zA-Z0-9][ \t]+[0-9]+')
 re_pfx=re.compile('^PFX[ \t]+[a-zA-Z][ \t]+[a-zA-Z][ \t]+[0-9]+')
 re_whitespace=re.compile('[ \t]+')
 decl_aff_counts = {}
 real_aff_counts = {}

 with open(filename, "r") as aff_file:

  for line in aff_file:

    line = line.strip()
    
    is_pfx = line.startswith('PFX')
    if not is_pfx and not line.startswith('SFX'):
        continue

    if re_afx.match(line):
        line_parts = re_whitespace.split(line)
        affixFlag = line_parts[1]
        affixMap[ affixFlag ] = {}
        decl_aff_counts[ affixFlag ] = int(line_parts[3])
        real_aff_counts[ affixFlag ] = 0
        
        if re_pfx.match(line):
            prefixes.append(affixFlag)

        continue

    halfs = line.split('@')
    parts = re_whitespace.split(halfs[0].strip())

    if len(parts) < 5:
        continue

    if len(halfs) > 1:
        tags = halfs[1].strip()
    else:
        tags = ''
        
    affixFlag = parts[1]
    fromm = parts[2]
    to = parts[3]
    match = parts[4]

    if not affixFlag in affixMap:
      affixMap[affixFlag] = {}

    affixGroupMap = affixMap[affixFlag]

    if not match in affixGroupMap:
      affixGroup = AffixGroup(match, is_pfx)
#      print(affixGroupMap, file=sys.stderr)
      affixGroupMap[match] = affixGroup
    else:
      affixGroup = affixGroupMap[match]

    affixObj = Affix(fromm, to, tags, is_pfx)
    affixGroup.affixes.append(affixObj)

    real_aff_counts[ affixFlag ] += 1

  if len(affixMap) == 0:
    print("ERROR: Failed to load affixes from", filename, file=sys.stderr)
    sys.exit(1)
    
  for affixFlag in decl_aff_counts:
    if decl_aff_counts[affixFlag] != real_aff_counts[affixFlag]:
      print("Declared count of ", decl_aff_counts[affixFlag], "for", affixFlag, "not equals real line count", real_aff_counts[affixFlag], file=sys.stderr)

  print("Loaded", len(affixMap), "affixes", ", prefixes:", prefixes, file=sys.stderr)


#@profile
def expand(word, flags, flush_stdout):
  pfx_words = expand_prefixes(word, flags)
  words = []
  for w in pfx_words:
    sfx_words = expand_suffixes(w, flags)
    words.extend( sfx_words )

  print(' '.join(words))
  if flush_stdout:
    sys.stdout.flush()

  logger.debug("expanded", ' '.join(words), file=sys.stderr)

#@profile
def expand_line(line):
    logger.debug("expanding", line, file=sys.stderr)
    wsp = line.split('/')
    flags = wsp[1] if len(wsp) > 1 else ''
    expand(wsp[0], list(flags), flush_stdout)


def munch_match(word, affix, affixFlag):
  if affix.to == '':
    return True

  if affixFlag in prefixes:
    return word.startswith(affix.to)
  
  return word.endswith(affix.to)

# NOTE: does not suggest combined suffix with prefixes
def munch(word):
  words = [word]
  for affixFlag, affixGroupMap in affixMap.items():
   for match, affixGroup in affixGroupMap.items():
    for affix in affixGroup.affixes:
      if munch_match(word, affix, affixFlag):
        if affixFlag in prefixes:
          if len(affix.to) > 0:
            base = word[len(affix.to):]
          else:
            base = word
          base = affix.fromm + base
          if affixGroup.match_start_re.match(base):
            words.append(base + '/' + affixFlag)
            
        else:
          if len(affix.to) > 0:
            base = word[:-len(affix.to)]
          else:
            base = word
          base = base + affix.fromm
          if affixGroup.match_ends_re.search(base):
            words.append(base + '/' + affixFlag)

#        words.append(base + '/' + affixFlag)
        
  print(' '.join(words))
  sys.stdout.flush()


def log_usage():
    for affixFlag, affixGroups in affixMap.items():
      print(affixFlag, ':', len(affixGroups), file=sys.stderr)
      for match, affixGroup in affixGroups.items():
          print("\t", match, ':', affixGroup.counter, "\t\t(", len(affixGroup.affixes), ')', file=sys.stderr)



#----------
# main code
#----------
if __name__ == "__main__":

  flush_stdout = False
  mode = 'expand'
  arg_idx = 1

  if len(sys.argv) > arg_idx and sys.argv[arg_idx] in ['-f', '--flush']:
    flush_stdout=True
    arg_idx += 1

  if 'munch' in sys.argv:
    mode = 'munch'

  aff_arg_idx = sys.argv.index('-aff') if '-aff' in sys.argv else -1
  if aff_arg_idx != -1:
    affix_filename = sys.argv[aff_arg_idx+1]
  else:
    affix_filename = os.path.dirname(os.path.abspath(__file__)) + "/../../src/Affix/uk_affix.dat"

  load_affixes(affix_filename)

#word='вкутий'
#flags = ['W', 'X']
#lines = argv[1] if len(argv)>1 else sys.stdin

  for line in sys.stdin:
    line = line.strip()
    if mode == 'munch':
      munch(line)
    else:
      expand_line(line)

  if mode == 'expand' and '--log-usage' in sys.argv:
    log_usage()
 