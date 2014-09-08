#!/usr/bin/python3

# -*- coding: utf-8 -*-

import sys
import re
import os
import subprocess
import logging


#logging.basicConfig(filename='affix.log',level=logging.DEBUG)
logger = logging.getLogger('affix')
#logger.setLevel(logging.DEBUG)

class Affix(object):
#    _flag = ''
#    _fromm = ''
#    _to = ''
#    _match = ''
#    _tags = ''

    #@profile
    def __init__(self, from_, to_, match_, tags_, pfx):
        if from_ != '0':
          self.fromm = from_
        else:
          self.fromm = ''
        if to_ != '0':
          self.to = to_
        else:
          self.to = ''
          
        self.match = match_
        self.tags = tags_
        
        if pfx:
          self.match_start_re = re.compile('^'+match_)
          self.sub_from_pfx = re.compile('^'+self.fromm)
        else:
          self.match_ends_re = re.compile(match_+'$')
          self.sub_from_sfx = re.compile(self.fromm+'$')


#    def __eq__(self, other):
#        if isinstance(other, Affix):
#            return self. == other._flag \
#                and self._suffix == other._suffix
#        else:
#            return False


prefixes = []
affixMap = {}


#@profile
def expand_prefixes(word, affixFlags):
    words = [ word ]

#    affixFlagsToRemove = list()
    for affixFlag in affixFlags:
        if affixFlag in prefixes:
            affix_list = affixMap[affixFlag]
            for affix in affix_list:
                if affix.match_start_re.match(word):
                    wrd = affix.sub_from_pfx.sub(affix.to, word)
                    words.append( wrd )
#            affixFlagsToRemove.append(affixFlag)
    
#    for f in affixFlagsToRemove:
#        affixFlags.remove(f)
    
    return words



#@profile
def expand_suffixes(word, affixFlags):
    words = [ word ]

    for affixFlag in affixFlags:
        if not affixFlag in prefixes:
            affix_list = affixMap[affixFlag]
            for affix in affix_list:
             if affix.match_ends_re.search(word):
                 deriv = affix.sub_from_sfx.sub(affix.to, word)
                 words.append(deriv)

    return words



#@profile
def load_affixes(filename):
 re_afx=re.compile('^[SP]FX[ \t]+[a-zA-Z0][ \t]+[a-zA-Z0][ \t]+[0-9]+')
 re_pfx=re.compile('^PFX[ \t]+[a-zA-Z][ \t]+[a-zA-Z][ \t]+[0-9]+')
 re_whitespace=re.compile('[ \t]+')

 with open(filename, "r") as aff_file:

  for line in aff_file:

    line = line.strip()
    
    is_pfx = line.startswith('PFX')
    if not is_pfx and not line.startswith('SFX'):
        continue

    if re_afx.match(line):
        affixFlag = re_whitespace.split(line)[1]
        affixMap[ affixFlag ] = []
        
        if re_pfx.match(line):
            prefixes.append(affixFlag)

        continue

    halfs = re.split('@', line)
    parts = re_whitespace.split(halfs[0].strip())

    if len(parts) < 5:
        continue

    if len(halfs) > 1:
        tags = halfs[1].strip()
    else:
        tags = ''
        
    affix = parts[1]
    fromm = parts[2]
    to = parts[3]
    match = parts[4]
    
    affixObj = Affix(fromm, to, match, tags, is_pfx)
    affixMap[affix].append(affixObj)


  if len(affixMap) == 0:
    print("ERROR: Failed to load affixes from", filename, file=sys.stderr)
    sys.exit(1)

  print("Loaded", len(affixMap), "affixes", ", prefixes:", prefixes, file=sys.stderr)


#@profile
def expand_input(word, flags, flush_stdout):
  pfx_words = expand_prefixes(word, flags)
  words = []
  for w in pfx_words:
    sfx_words = expand_suffixes(w, flags)
    words.extend( sfx_words )

  print(' '.join(words))
  if flush_stdout:
    sys.stdout.flush()

  logger.debug("expanded", ' '.join(words), file=sys.stderr)


#----------
# main code
#----------
if __name__ == "__main__":

  flush_stdout = False
  arg_idx = 1

  if len(sys.argv) > arg_idx and sys.argv[arg_idx] in ['-f', '--flush']:
    flush_stdout=True
    arg_idx += 1

  affix_filename=sys.argv[arg_idx] if len(sys.argv) > arg_idx else os.path.dirname(os.path.abspath(__file__)) + "/../../src/Affix/uk_affix.tag"

  load_affixes(affix_filename)

#word='вкутий'
#flags = ['W', 'X']
#lines = argv[1] if len(argv)>1 else sys.stdin

  for line in sys.stdin:
    logger.debug("expanding", line, file=sys.stderr)
    wsp = line.strip().split('/')
    flags = wsp[1] if len(wsp) > 1 else ''
    expand_input(wsp[0], list(flags), flush_stdout)
