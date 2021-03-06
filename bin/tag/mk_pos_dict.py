#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import sys
import re
import os
import subprocess
import logging
import locale

import affix
from affix import affixMap
from affix import prefixes
from compar_forms import COMPAR_FORMS
from compar_forms import COMPAR_SOFT_BASE


logger = logging.getLogger('tofsa')

#spell_uk_dir = os.getenv("HOME") + "/work/ukr/spelling/spell-uk/"

PLURAL_FLAGS_RE = '[bfjlq9]'
NOUN_FLAGS_RE = '[a-z]';

CONSONANTS="бвгґджзклмнпрстфхцчшщ"

allWords = []

comparatives = []
comparatives_shy = []
adverbs_compar = []
adverbs = []

with_flags_re = re.compile('.*[а-яіїєґА-ЯІЇЄҐ]/.*')
with_Y_flag_re = re.compile('[^ ]*/[^ ]*Y.*')
yi_V_flag_re = re.compile('[^ ]*[іи]й/[^ ]*V.*')
advp_re = re.compile('.*[уаяю]чи$')
advp_rev_re = re.compile('.*[уаяю]чись$')

tag_split0_re = re.compile('[^ ]+$')
tag_split1_re = re.compile('[^: ]+$')
tag_split2_re = re.compile('[a-z]:v_[a-z]{3}(/v_[a-z]{3})*')

ending_a_aja_re = re.compile('.*[ая]$')
ending_i_nnia_re = re.compile(r'.*(([бвгґджзклмнпрстфхцчшщ])\2|\'|[джлнрт])я$')
ending_ae_ets_re = re.compile('.*[еє]ць$')
ending_a_n_re = re.compile('.*([ео]нь|оль|оть)$')
ending_ae_ik_re = re.compile('.*і[дйрлгсзкп]$')
ending_a_numr_re = re.compile('.*(ять|сят|сто)$')
ending_masc_dull_re = re.compile('.*[бвжлнртьшк]$')

ending_evi_re = re.compile('^.*?[еоє]ві .*$')
ending_iv_re = re.compile('^.* .*?[ії]в .*$')
ending_istu_re = re.compile('^.*?[иі]сту .* .*$')
ending_iku_re = re.compile('^.*?(р|ст|пот)оку .* .*$')
ending_uyu_re = re.compile('^.*?[ую] .* .*$')

ishy_re = re.compile('іший/.*$')
shy_re = re.compile('[^ін][шщч]ий/.*$')
shy_remove_re = re.compile('[шщч]ий/.*$')
yi_sub_re = re.compile('[іи]й/.*$')
shyi_sub_re = re.compile('(кий|с?окий)/.*$')

end_tag1_re = re.compile('((?::(?:fname|lname|patr))+)(:.+)')
end_tag2_re = re.compile('((?::(?:&[a-z]+|v-u|bad|slang|rare|coll))+)(:.+)')

#@profile
def expand_alts(lines, splitter, regexp):
    out = []

    for line in lines:

        if not splitter in line:
            out.append( line )
            continue
            
        try:
          if splitter == '/':
            groups = re.match("^([^/]+:)([^:]+)(:[^/]+)?$", line).groups()
          elif splitter == '|':
            groups = re.match("^(.* )(.*)$", line).groups()
          else:
#            print(line, file=sys.stderr)
            groups = re.match("^(.* .+?:)((?:.:(?:nv|v_...)(?:/(?:nv|v_...))*)(?://.:(?:nv|v_...)(?:/(?:nv|v_...))*)+)(:[^/]+)?$", line).groups()
        except:
          print("invalid format for", line, file=sys.stderr)
          raise

#        print(groups)

        split1 = groups[1].split(splitter)
        base = groups[0]
        end = ""
        if len(groups) > 2 and groups[2] :
          end = groups[2]

        for split_ in split1:
#            print('split', splitter, base, split_)
            out.append( base + split_ + end )

    return out



#def isAcegSuffix(affixFlag, allAffixFlags):
 #   return (affixFlag == 'e' and not 'g' in allAffixFlags) #or (affixFlag == 'a' and 'c' in allAffixFlags)

def lastname(word, allAffixFlags):
  return '+' in allAffixFlags
#    or ('+' in allAffixFlags and word.endswith('о'))
#    or ('e' in allAffixFlags and word[0].isupper() \
#           and ( word.endswith('ич') or word.endswith('ук') or word.endswith('юк') or word.endswith('як')) )

#def lastname_dual(word, allAffixFlags):
#  return '+' in allAffixFlags and ('e' in allAffixFlags and word[0].isupper() \
#           and (word.endswith('ко'))) # or word.endswith('ич') or word.endswith('ук') or word.endswith('юк') or word.endswith('як')) )

def istota(word, allAffixFlags):
  return ('p' in allAffixFlags or '<' in allAffixFlags) \
    or lastname(word, allAffixFlags)

def person(word, allAffixFlags):
  return ('p' in allAffixFlags or ('<' in allAffixFlags and not '>' in allAffixFlags)) \
    or lastname(word, allAffixFlags)

def firstname(word, affixFlag, allAffixFlags):
  return ('p' in allAffixFlags or ('<' in allAffixFlags and not '>' in allAffixFlags)) and not '+' in allAffixFlags \
    and affixFlag != 'p' and word[0].isupper() and (word[1].islower() or word[1] == "'")

def secondVZna(line):
  return False

def filter_lines(lines, inStr):
  return [line for line in lines if not inStr in line]

#@profile
def generate(word, allAffixFlags, origAffixFlags, main_tag):

    all_forms = []
    allAffixFlagsStr = ''.join(allAffixFlags)
    
    for affixFlag in allAffixFlags:
        if affixFlag in "<>+@":
          break

        if not affixFlag in affixMap:
          print("ERROR: Invalid flag", affixFlag, "for", word, file=sys.stderr)
          continue

        affixGroups = affixMap[affixFlag]

        lines = generate_suffix(word, affixFlag, affixGroups, allAffixFlags, origAffixFlags)
        
#        print(lines, file=sys.stderr)
        
        for line in lines:
#            print(affixFlag, word, ':', line, file=sys.stderr)

            
            # remove plurals
            if '//p:v_' in line:
                if affixFlag in 'eg' and 'f' not in allAffixFlags and 'j' not in allAffixFlags:
                    line = re.sub('//p:v_[a-z]+(/v_[a-z]+)*', '', line)
                if affixFlag in 'ux' and 'v' not in allAffixFlags:
                    line = re.sub('//p:v_[a-z]+(/v_[a-z]+)*', '', line)
                if affixFlag == 'i' and 'j' not in allAffixFlags and 'f' not in allAffixFlags and (not 'o' in allAffixFlags or not word.endswith("ря")):
                    line = re.sub('//p:v_[a-z]+(/v_[a-z]+)*', '', line)
                if affixFlag == 'r' and 's' not in allAffixFlags:
                    line = re.sub('//p:v_[a-z]+(/v_[a-z]+)*', '', line)
                if affixFlag in 'lq' and 'm' not in allAffixFlags:
                    line = re.sub('//p:v_[a-z]+(/v_[a-z]+)*', '', line)
                if affixFlag in 'ac' and 'o' not in allAffixFlags and 'b' not in allAffixFlags and 'f' not in allAffixFlags:
                    line = re.sub('//p:v_[a-z]+(/v_[a-z]+)*', '', line)

            if '/v_kly' in line:
                if not person(word, origAffixFlags) \
                  or ('v_dav' in line and 'h' in origAffixFlags and affixFlag != 'p') \
                  or ('v_dav' in line and word.endswith('ло')) \
                  or (('v_zna' in line or 'v_dav' in line) and 'd' in origAffixFlags and affixFlag != 'p') \
                  or lastname(word, origAffixFlags):
                    line = re.sub('/v_kly', '', line)

            if '<' in allAffixFlags:
                if not '>' in allAffixFlags: # animal
                    if affixFlag in 'V9jU' and 'adj:p:v_naz/v_zna' in line:
                        line = line.replace('/v_zna', '')
                    elif affixFlag in 'V' and ':m:v_naz/v_zna' in line:
                        line = line.replace('/v_zna', '')
#              else:
#                if 'noun' in main_tag:
#                  line = line.replace('v_naz/', '')



            # handle rodovyi for singular
            if affixFlag == 'e':
                if not 'g' in allAffixFlags and 'noun:m:v_dav' in line and ending_uyu_re.match(line) and not 'о ' in line:
                    line = line.replace('m:v_dav', 'm:v_rod/v_dav')
#                if not 'g' in allAffixFlags and 'noun:m:v_dav' in line and ending_uyu_re.match(line) and 'о ' in line and word[0].isupper():
#                    line = line.replace('m:v_dav', 'm:v_dav/v_mis')
#                if ending_istu_re.match(line):
#                    line = line.replace('m:v_dav/v_mis', 'm:v_dav')
                if ('j' in allAffixFlags or 'b' in allAffixFlags) and word.endswith('о'):
                    if istota(word, allAffixFlags):
                        new_aff = 'm:v_rod/v_zna//p:v_naz'
                    else:
                        new_aff = 'm:v_rod//p:v_naz'
                    line = line.replace('m:v_rod', new_aff)
                    line = line.replace(':m:', ':n:')

                if istota(word, allAffixFlags):
                    if 'm:v_rod' in line:
                        line = line.replace('m:v_rod', 'm:v_rod/v_zna')
#                else:
#                    if not ending_iv_re.match(word) and ending_evi_re.match(line):
#                        line = line.replace('m:v_dav/v_mis', 'm:v_dav')
            elif affixFlag in "ir":
                 if istota(word, allAffixFlags):
                   if 'noun:f:v_rod' in line and not word[-1:] in 'аь' and not word.endswith('матір'):
                     line = line.replace('f:v_rod', 'f:v_rod/v_zna')
                 else:
                   if 'noun:m:v_rod/v_zna' in line:
                     line = line.replace('/v_zna', '')
#                   if 'noun:f:v_naz' in line:
#                     line = line.replace('f:v_naz', 'f:v_naz/v_zna')
            elif affixFlag in 'au':
                if 'c' not in allAffixFlags and 'x' not in allAffixFlags:
                    if 'noun:m:v_dav' in line and ('у ' in line or 'ю ' in line):
                        line = line.replace('m:v_dav', 'm:v_rod/v_dav')
#                if not istota(word, allAffixFlags):
#                    if not ending_iv_re.match(word) and ending_evi_re.match(line):
#                        line = line.replace('m:v_dav/v_mis', 'm:v_dav')
#                    elif ending_iku_re.match(line):
#                        line = line.replace('v_dav/v_mis', 'v_dav')
#                    elif line.startswith('кону кін '):
#                        line = line.replace('v_dav', 'v_dav/v_mis')
            elif affixFlag in "l" and not 'q' in allAffixFlags:
                if 'noun:m:v_dav' in line and re.match(".*[аиі][дтнр]$", word) and ending_uyu_re.match(line):
                    line = line.replace('m:v_dav', 'm:v_rod/v_dav')
            elif affixFlag in 'cgqx' or (affixFlag == "l" and re.match(".*(боєць|і[тдрн])$", word)):
                if istota(word, allAffixFlags) or secondVZna(line) and 'noun:m:v_rod' in line:
                    line = line.replace('m:v_rod', 'm:v_rod/v_zna')
            elif affixFlag == 'p':
                line += ':patr'

            if not '/v_kly' in line:
              if 'p:v_naz' in line and person(word, allAffixFlags):
                line = line.replace('p:v_naz', 'p:v_naz/v_kly')

            # handle znahidny for plural
            
            allAffixFlags_ = list(re.sub('\+[mf]', '', allAffixFlagsStr))
#            print(allAffixFlags_, file=sys.stderr)
            
            if len(set(allAffixFlags_) & set("bofjmsv")) > 0:
                    if istota(word, allAffixFlags):
                        line = line.replace('p:v_rod', 'p:v_rod/v_zna')
                        if '>' in allAffixFlags: # animal
                            line = line.replace('p:v_naz', 'p:v_naz/v_zna')
                    else:
                        line = line.replace('p:v_naz', 'p:v_naz/v_zna')
#                elif istota(word, allAffixFlags):
#                    line = line.replace('p:v_rod', 'p:v_rod/v_zna')
#            else:
#                    line = line.replace('p:v_naz', 'p:v_naz/v_zna')

#                print("--", word, allAffixFlags, line, file=sys.stderr)

            if affixFlag in "cgq":
              if "@" in allAffixFlags:
                line = line.replace('m:v_rod', 'm:v_rod/v_zna')  # TODO: add :&v_zna2

            out = expand_alts([line], '//', tag_split2_re)
            out = expand_alts(out, '/', tag_split1_re)
            
            if "U" in allAffixFlags and "<+m" in allAffixFlagsStr: # remove :f:
              out = filter_lines(out, ':f:')
              out = filter_lines(out, ':p:')

            all_forms.extend(out)
            
    return all_forms

#@profile
def get_word_base(word, affixFlag, allAffixFlags):
        str = ''
        
        v_zna_for_inanim = ""
        v_kly_for_anim = ""

        if not istota(word, allAffixFlags):
            v_zna_for_inanim = "/v_zna";
        else:
            if ('d' not in allAffixFlags and 'h' not in allAffixFlags):
                v_kly_for_anim = "/v_kly"

        if affixFlag == 'U' and '+' in allAffixFlags:
            str = word + ' ' + word + ' noun:m:v_naz'
        elif affixFlag == 'U' and word.endswith('ий'):
            str = word + ' ' + word + ' adj:m:v_naz/v_zna:np'
        elif affixFlag == 'V' or affixFlag == 'U':
            if word.endswith('е'):
                str = word + ' ' + word + ' adj:n:v_naz/v_zna'
            elif word.endswith('і'):
                str = word + ' ' + word + ' adj:p:v_naz/v_zna:ns'
            elif word.endswith('а'):
                str = word + ' ' + word + ' adj:f:v_naz'
                if not "<+" in allAffixFlags:
                    str += v_kly_for_anim

            elif word.endswith('ій'):
                str = word + ' ' + word + ' adj:m:v_naz/v_zna//f:v_dav/v_mis'
            else:
              if istota(word, allAffixFlags):
                str = word + ' ' + word + ' noun:m:v_naz'
                if not lastname(word, allAffixFlags) and not '>' in allAffixFlags:
                    str += '/v_kly'
              else:
                str = word + ' ' + word + ' adj:m:v_naz/v_zna'
                
        elif affixFlag in '[AIKMC]':
            str = word + ' ' + word + ' verb:inf'
        elif affixFlag in '[BJLN]':
            str = word + ' ' + word + ' verb:rev:inf'
        elif affixFlag in 'S':
            if word.endswith("ся"):
                str = word + ' ' + word + ' verb:rev:inf'
            else:
                str = word + ' ' + word + ' verb:inf'
            
        elif affixFlag == 'a' and ending_a_numr_re.match(word):
            str = word + ' ' + word + ' numr:p:v_naz/v_zna'
        elif affixFlag == 'a' and ending_a_aja_re.match(word):
            str = word + ' ' + word + ' noun:f:v_naz'
        elif affixFlag in 'au':
            str = word + ' ' + word + ' noun:m:v_naz' + v_zna_for_inanim
        elif affixFlag in 'bfox':
            str = word + ' ' + word + ' noun:p:v_naz/v_kly'
        elif affixFlag == 'e':
            if word.endswith('е'):# or (word.endswith("ло") and "j" in allAffixFlags):
                str = word + ' ' + word + ' noun:n:v_naz/v_zna'
            else:
                str = word + ' ' + word + ' noun:m:v_naz' + v_zna_for_inanim
        elif affixFlag == 'l' and word[-1] in 'р':
            str = word + ' ' + word + ' noun:m:v_naz' + v_zna_for_inanim
        elif affixFlag == 'l' and word[-1] in 'яа':
            str = word + ' ' + word + ' noun:n:v_naz/v_zna' + v_kly_for_anim
        elif affixFlag == 'l' and re.match('.*([еє][цн]ь|і[тднр]|ен|ок)$', word):
            str = word + ' ' + word + ' noun:m:v_naz' + v_zna_for_inanim
        elif affixFlag == 'l' and re.match('.*([^ц]ь|[чш]|іць)$', word):
            str = word + ' ' + word + ' noun:f:v_naz/v_zna'
        elif affixFlag in 'ilu' and (word.endswith("ів") or word.endswith("їв")):
            str = word + ' ' + word + ' noun:m:v_naz' + v_zna_for_inanim
        elif affixFlag == 'i' and (word.endswith('ий') or word.endswith('ій')):
            str = word + ' ' + word + ' noun:m:v_naz'  + v_zna_for_inanim + v_kly_for_anim
        elif affixFlag == 'i' and ending_i_nnia_re.match(word):
            str = word + ' ' + word + ' noun:n:v_naz/v_rod/v_zna//p:v_naz'
        elif affixFlag == 'i' and (word.endswith('о') or word.endswith('е')):
            str = word + ' ' + word + ' noun:n:v_naz'
            if word[-1] in 'ео' and istota(word, allAffixFlags):# and not word.endswith('ко'):
                if word.endswith("ще") or word.endswith("ко"):
                    str += "/v_zna"
                str += '/v_kly'
            else:
                str += '/v_zna'
        elif affixFlag == 'i' and (word.endswith('а')):
            str = word + ' ' + word + ' noun:f:v_naz' + v_kly_for_anim
        elif affixFlag == 'i' and (word.endswith('м')):
            str = word + ' ' + word + ' noun:f:v_naz' + v_zna_for_inanim + v_kly_for_anim
        elif affixFlag in "ir" and word[-1] in "ьаячшжрбвф":
            str = word + ' ' + word + ' noun:f:v_naz'
            if not istota(word, allAffixFlags) or word.endswith('матір') or word[-1:] == 'ь':
              str += '/v_zna'
        elif affixFlag == 'i' and word.endswith('ін'):
            str = word + ' ' + word + ' noun:m:v_naz'
        elif affixFlag == 'j' and word[-1] in 'іа':
            str = word + ' ' + word + ' noun:p:v_naz:ns'
        elif re.match('[a-p]', affixFlag):
            if affixFlag == 'p' and allAffixFlags[0] == 'p':
              return str
              
            str = word + ' ' + word + ' noun:unknown'
            print(str, '---', word, affixFlag)
            str = ""
        else:
            str = word + ' ' + word + ' unknown'
            print(str, '---', word, affixFlag)

        if firstname(word, affixFlag, allAffixFlags):
          str += ':fname'

        return str


#@profile
def generate_suffix(word, affixFlag, affixGroups, allAffixFlags, origAffixFlags):
    addTag = ''
    lines = []

    if affixFlag == allAffixFlags[0]:
        base_line = get_word_base(word, affixFlag, allAffixFlags)
        if base_line != '':
            lines.append(base_line)

    for affixGroup in affixGroups.values():

      if affixGroup.matches(word):
         for affix in affixGroup.affixes:
            deriv = affix.apply(word)
            
            if( affixFlag == 'W' and not word.endswith('ти') ):
                lines.append( deriv + ' ' + deriv + ' ' + 'adv' )
#            elif 'advp' in affix.tags:
#                lines.append( deriv + ' ' + deriv + ' ' + affix.tags )
            else:
                # по-батькові
                if affixFlag == 'p':
                    if 'm:v_naz' in affix.tags:
                        patronim_base_m = deriv
                    elif 'f:v_naz' in affix.tags:
                        patronim_base_f = deriv
                        
                    if ':m:' in affix.tags:
                        word_base = patronim_base_m
                    elif ':f:' in affix.tags:
                        word_base = patronim_base_f
                    else:
                        word_base = patronim_base_m   # odd case for plurals, TODO: fix or remove plural patronim
                elif affixFlag in "BDFHJLNP" and word.endswith('ти'):
                    word_base = word + 'ся'
                else:
                    word_base = word
                    
                
                ln = deriv + ' ' + word_base + ' ' + affix.tags
                
                if firstname(word, affixFlag, allAffixFlags):
                     ln += ':fname'

                lines.append(ln)

    return lines


#@profile
def expand_word(word, affixFlags):
    words = [ word ]

    affixFlagsToRemove = list()
    for affixFlag in affixFlags:
        if affixFlag in prefixes:
#            print(affixFlag, 'in prefixes for', word)
            affixGroups = affixMap[affixFlag]
            words.extend( expand_prefix(word, affixFlag, affixGroups) )
            affixFlagsToRemove.append(affixFlag)
    
    for f in affixFlagsToRemove:
        affixFlags.remove(f)
    
    return words


#@profile
def expand_prefix(word, affixFlag, affixGroups):
    words = []

    for affixGroup in affixGroups.values():
      if affixGroup.matches(word):
        for affix in affixGroup.affixes:
          words.append( affix.apply(word) )

    return words

def retain_tags(line, tags):
    parts = line.split(':')
    line = parts[0]
    for part in parts:
        if part in tags:
            line += ':' + part
    return line


extra_gen_re=re.compile(':\\+([mnf])')
gen_tag_re=re.compile(':[mfn]:')


def tail_tag(line, tags):
    for tag in tags:
        tag = ':' + tag
        if tag in line and not line.endswith(tag):
            line = line.replace(tag, '') + tag
    return line


compar_line_re=re.compile('[^ ]+([чшщ]е) [^ ]+ .*v_naz.*(compr|super).*')

#@profile
def post_process(line, affixFlags, extra_tag):
    if "advp" in line:
    
        if "ись " in line and "ти " in line:
            line = line.replace("ти ", "тися ")
    
        if re.search("чи(с[яь])? ", line):
            line = re.sub('(advp:(?:rev:)?(?:im)?perf):(?:im)?perf(?::(?:im)?perf)?(.*)', '\\1\\2', line)
        else:
            if ":imperf:perf" in line:
                line1 = re.sub('(advp:(?:rev:)?)(?:im)?perf:(?:im)?perf(?::(?:im)?perf)?(.*)', '\\1imperf\\2', line)
                line2 = re.sub('(advp:(?:rev:)?)(?:im)?perf:(?:im)?perf(?::(?:im)?perf)?(.*)', '\\1perf\\2', line)
                return [line1, line2]
            else:
                line = re.sub('(advp:(?:rev:)?)(?:im)?perf:((?:im)?perf)(.*)', '\\1\\2\\3', line)
# дієприслівник, як окрема лема
#        line = re.sub('([^ ]+) [^ ]+ (advp:(?:rev:)?(?:im)?perf):(?:im)?perf(?::(?:im)?perf)?(.*)', '\\1 \\1 \\2\\3', line)
        if ":rev" in line and "tran" in line:
            line = re.sub(':(in)?tran(:rv_[a-z]+)*', '', line)
    elif "verb" in line:
        if "impers" in line:
            line = retain_tags(line, ['impers', 'imperf', 'perf', 'v-u', 'bad', 'slang', 'coll', 'alt', 'rare'])
            
        if ":rev" in line and "tran" in line:
            line = re.sub(':(in)?tran(:rv_[a-z]+)*', '', line)
            
        if ":imperf:perf" in line:
            line1 = line.replace(":perf", "")
            line2 = line.replace(":imperf", "")

            if re.search("тим(у|усь|уся|еш|ешся|е|еться|емо|ем|емося|емось|емся|ете|етеся|етесь|уть|уться)? .*:perf", line2):
              return [line1]

            if ":pres" in line2:
                line2 = line2.replace(':pres', ':futr')

            return [line1, line2]
        
        if ":pres" in line and ":perf" in line:
#            if not ":imperf" in line:
            line = line.replace(':pres', ':futr')
#            else: # :imperf:perf
#                line = line.replace(':perf', '') + "\n" + line.replace(':pres', ':futr').replace(':imperf', '')
    elif 'comp' in line or 'super' in line: # and not ' якнай' in line:
    
        line = re.sub(' (як|що)?най', ' ', line)

        lemma = line.split(' ')[1]
        if lemma in COMPAR_FORMS:
            base = COMPAR_FORMS[lemma]
            l1 = ' '+lemma+' '
            l2 = ' '+base+' '
            line = line.replace(l1, l2)
        elif lemma in COMPAR_SOFT_BASE:
            line = line.replace('іший adj', 'ій adj')
        else:
            #if lemma.replace('іший', 'ий') in :
            line = line.replace('іший adj', 'ий adj')

        if ':compr' in line and re.match('(як|що)?най.*', line):
            line = line.replace(':compr', ':super')
            
        if ":bad:compb" in line:
            line = line.replace(":bad:compb", ":compb:bad")
    
    if line.startswith("не") and ":v-u" in line:
        line = line.replace(":v-u", "")
    
    lines = [line]
    
    if compar_line_re.match(line):
 #       line1 = re.sub('([^ ]+ще [^ ]+)ий adj:n:v_naz.*((compr|super).*)', '\\1о adv:\\2', line)
        if re.search("[чшщ]ий adj", line):
            line1 = re.sub('([^ ]+ше [^ ]+)ий adj:n:v_naz.*((compr|super).*)', '\\1е adv:\\2', line)
        elif "ий adj" in line or "ій adj" in line:
            if "ій adj" in line:
                adv_ending = "ьо"
                line2 = re.sub('([^ ]+[чшщ]е [^ ]+[^чшщ])[іи]й adj:n:v_naz.*((compr|super).*)', '\\1о adv:\\2', line)
                adverbs_compar.append( line2 )
            else:
                adv_ending = "о"
            line1 = re.sub('([^ ]+[чшщ]е [^ ]+[^чшщ])[іи]й adj:n:v_naz.*((compr|super).*)', '\\1'+adv_ending+' adv:\\2', line)
#        else:
#          line1 = line
#        elif "ій adj" in line:
#          line1 = re.sub('([^ ]+ше [^ ]+)ій adj:n:v_naz.*((compr|super).*)', '\\1о adv:\\2', line1)
        adverbs_compar.append( line1 )
#        print("adv compar", adverbs_compar, file=sys.stderr)

    # подвійний рід
    if extra_gen_re.search(extra_tag) and gen_tag_re.search(line):
        if 'm:v_kly' in line and re.match('([^ ]+)ле ', line):
            another_gen_line = re.sub('^([^ ]+)ле ', '\\1ло ', line).replace(':m:', ':n:')
        else:
            another_gen_line = gen_tag_re.sub(':'+ extra_gen_re.search(extra_tag).group(1) +':', line)
            
        if 'n:v_zna' in line and re.match('([^ ]+)а ', line):
            line = re.sub('^([^ ]+)а ', '\\1о ', line)
            lines = [line]
            
        lines.append(another_gen_line) 

    return lines


#@profile
def collect_all_words(line):
    if not ':bad' in line and not ':rare' in line and not ':coll' in line and not ". " in line: # and not ':alt' in line:
        allWords.append(line.split(' ')[0])
    if ' adv' in line:
        adverbs.append(line.split(' ')[0])



GEN=['m', 'f', 'n', 'p']
VIDM=['v_naz', 'v_rod', 'v_dav', 'v_zna', 'v_oru', 'v_mis', 'v_kly']
re_nv_vidm=re.compile('(noun):[mfn]:(.*)')

#@profile
def expand_nv(in_lines):
  lines = []
  
  for line in in_lines:
    if ('noun' in line or 'numr' in line) and ':nv' in line and not ":v_" in line:
        parts = line.split(':nv')
    
        for v in VIDM:
          if v == 'v_kly' and (not ':anim' in line or ':lname' in line):
            continue
          lines.append(parts[0] + ':' + v + ':nv' + parts[1])
        
        if 'noun' in line:
          if not ':p' in line and not ':np' in line and not ':lname' in line:
            for v in VIDM:
              if v != 'v_kly' or 'anim' in line:
                lines.append(re_nv_vidm.sub('\\1:p:' + v + ':\\2', line))
    elif ('adj' in line) and ':nv' in line and not ":v_" in line:
        parts = line.split(':nv')
        
        if re.match('.*:[mnfp]', parts[0]):
            gens = parts[0][-1:]
            parts[0] = parts[0][:-2]
        else:
            gens = GEN

        for g in gens:    
            for v in VIDM:
              if v == 'v_kly' and (not ':anim' in line or ':lname' in line):    # TODO: include v_kly? but not for abbr like кв.
                continue
              lines.append(parts[0] + ':' + g + ":" + v + ':nv' + parts[1])
    else:
        lines.append(line)

  return lines


#@profile
def apply_main_tag(out_line2, origAffixFlags, main_tag):
    if not " adv" in out_line2 and not ":patr" in out_line2:# and (not 'Z' in origAffixFlags or not out_line2.startswith('не') or not main_tag.startswith('adjp')):
        if 'noun:' in main_tag:
          if not ':p:' in out_line2:
            repl_str = re.sub('[^ :]+', '[^ :]+', main_tag)
            out_line2 = re.sub(' ' + repl_str, ' ' + main_tag, out_line2)
        else:
            repl_str = '[a-z]+'
            out_line2 = re.sub(' ' + repl_str, ' ' + main_tag, out_line2)
  
#              if " adjp" in out_line2:
#                if ('Z' in origAffixFlags or 'W' in origAffixFlags) and not "&adj" in out_line2:
#                  out_line2 += ":&adj"
           
    return out_line2


def dual_last_name_ending(line):
  return '+d' in line or re.match('.*(о|ич|ук|юк|як|аш|яш|сь|ун|ин|сон)/', line)

#@profile
def pre_process(line):
  out = []

  if re.search("[аиіїя]/[bfo]", line):
      if not " :" in line:
        line += " "
      line += ":ns"

  if "<+" in line:
    if " <+" in line:
      if not "<+f" in line:
        out.append( re.sub(" <\\+[fmd]?", " noun:m:nv:np:anim:lname", line) )
      if not "<+m" in line:
        out.append( re.sub(" <\\+[fmd]?", " noun:f:nv:np:anim:lname", line) )
    elif "e" in line or "ac" in line or "lq" in line or "U" in line:
      out.append( line )
      if not "<+m" in line and dual_last_name_ending(line):
        out.append( re.sub("/[efgabcU]+<\\+[fmd]?", " noun:f:nv:np:anim:lname", line) )
    elif "a" in line and not "^" in line:
        if "+m" in line:
            out.append( line + " ^noun:m" )
        else:
            out.append( line + ' :+m')
    else:
      out = [line]
  elif "<" in line and line[0].isupper():
    if "/" in line:
      if "a" in line and not "^" in line:
        if "<m" in line:
            line = line.replace("<m", "< ^noun:m")
#      if re.match(".* [:a-z^].*", line):
#        line += ":fname"
#      else:
#        line += " :fname"
      out = [line]
    else:
      if not "<f" in line:
        out.append( re.sub(" <[fm]?", " noun:m:nv:np:anim:fname", line) )
      if not "<m" in line:
        out.append( re.sub(" <[fm]?", " noun:f:nv:np:anim:fname", line) )
  else:
    out = [line]

  return out


#@profile
def process_line(line):
#     print("process line", line, file=sys.stderr)
    all_out_lines = []
    
    lines = pre_process(line)
    for line2 in lines:
        outs = process_line2(line2)
        if outs:
            all_out_lines.extend( outs )
        else:
            print("skipping no-tag item", line2, file=sys.stderr)
        
    return all_out_lines


#@profile
def process_line2(line):
    all_out_lines = []

    if " " in line and not " :" in line and not " ^" in line:
        parts = line.split(' ')
        if len(parts) < 3:
          line = parts[0] + ' ' + parts[0] + ' ' + parts[1]
    
        out = expand_alts([line], '//', tag_split2_re)
        out = expand_alts(out, '/', tag_split1_re)

        out = expand_nv(out)

        out = [ tail_tag(line, ['&adj', 'v-u', 'bad', 'slang', 'rare', 'coll', 'abbr']) for line in out ]
        
        all_out_lines.extend(out)
        
        [collect_all_words(w) for w in out]

        return all_out_lines


    extra_tag = ''
    
    if 'ів/U' in line:
        if '<' in line:
            line += ' ^noun'
    elif '/V' in line:
        if '<' in line:
            line += ' ^noun'

        if not '^noun' in line:
            if "Y" in line and with_Y_flag_re.match(line):
                if re.match('(як|що)?най.*', line):
                    extra_tag += ':super';
                else:
                    extra_tag += ':compr';
            elif yi_V_flag_re.match(line):
                if (line.startswith('най') and 'іший/' in line):# or line.startswith('якнай') or line.startswith('щонай'):
                    extra_tag += ':super';
                elif shyi_sub_re.sub('', line) in comparatives_shy or yi_sub_re.sub('', line) in comparatives:
                    extra_tag += ':compb'
                elif re.sub('/.*', '', line) in COMPAR_FORMS.values():
                    extra_tag += ':compb'
    #    elif re.match('/[^ ]*p', line):
    #       extra_tag += ':pers'

    main_tag = ''
    if " :" in line:
        spl = line.split(" :")
        extra_tag += ":" + spl[1]
        line = spl[0]
#        print("extra tag", extra_tag, "for", line)
    
    if " ^" in line:
        spl = line.split(" ^")
        main_tag = spl[1]
        line = spl[0]

    if "<" in line or "p" in line:
        extra_tag += ':anim'
        
        if "<+" in line:
          extra_tag += ':lname'
        # if not ">" in line:
        #   extra_tag += ':pers'

#    if line.endswith('/X') and main_tag=='adv':
#        line = line.replace('/X', '')
#        ofile.write(line + ' ' + line + ' ' + main_tag + extra_tag + '\n')
#        collect_all_words(line)

#        line = re.sub('^в', 'у', line)
#        ofile.write(line + ' ' + line + ' ' + main_tag + extra_tag + '\n')
#        collect_all_words(line)
#        return

    if "X" in line:
        extra_tag += ':v-u'

    if not with_flags_re.match(line):
        if line.endswith('ен'):
            lemma = re.sub('ен$', 'ний', line)
            outline = line + ' ' + lemma
            tag = 'adj:m:v_naz' + extra_tag
            all_out_lines.append(outline + ' ' + tag)
            tag = 'adj:m:v_zna' + extra_tag
            all_out_lines.append(outline + ' ' + tag)
    
            [collect_all_words(w) for w in all_out_lines]
            
            return all_out_lines


        tag = ' unknown'

        if advp_re.match(line):
            tag = ' advp:imperf'
        elif advp_rev_re.match(line):
            tag = ' advp:rev:imperf'
        elif line.endswith('ши'):
            tag = ' advp:perf'
        elif line.endswith('шись'):
            tag = ' advp:rev:perf'
        
        if tag == '' and extra_tag != '':
            tag = ' '

        outline = line + ' ' + line + tag + extra_tag
        all_out_lines.append(outline)

        if tag == ' unknown':
            print('-', line, tag, file=sys.stderr)

        collect_all_words(outline)
        return all_out_lines


    halfs = re.split('/', line)

    word = halfs[0]
    origAffixFlags = halfs[1]
    affixFlags = list(origAffixFlags)

    out_lines = []
    for word in expand_word( word, affixFlags ):
        if not affixFlags:
          out_lines.append( word + ' ' + word + ' unknown')
        else:
          out_lines.extend( generate(word, affixFlags, origAffixFlags, main_tag) )



    fem_lastnames_deferred = []
    last_fem_lastname_v_naz = ''

    for out_line in out_lines:

        if 'Z' in origAffixFlags and out_line.startswith('не'):
            if re.sub('ий$', '', word) in comparatives: # and word in COMPAR_FORMS.values():
                if not ':compb' in extra_tag:
                   extra_tag = ':compb' + extra_tag
            else:
                extra_tag = extra_tag.replace(':compb', '')
        
        if ':+' in extra_tag:
            extra_tag2 = extra_gen_re.sub('', extra_tag)
        else:
            extra_tag2 = extra_tag
            
        if out_line.endswith(':fname'):
          extra_tag2 = extra_tag2.replace(':anim', ':anim:fname')
          out_line = out_line.replace(':fname', extra_tag2)
        elif out_line.endswith(':patr'):
          extra_tag2 = extra_tag2.replace(':anim', ':anim:patr')
          out_line = out_line.replace(':patr', extra_tag2)
        else:
          out_line += extra_tag2
        
        out_lines2 = post_process(out_line, affixFlags, extra_tag)


        
        for out_line2 in out_lines2:
            # пропустити середній для прізвищ
            if ('V<' in origAffixFlags or 'U<' in origAffixFlags) and ':n:' in out_line2:
              continue

            if main_tag:
              out_line2 = apply_main_tag(out_line2, origAffixFlags, main_tag)
            
              # put end tags at the end
              if end_tag1_re.search(out_line2):
                out_line2 = end_tag1_re.sub('\\2\\1', out_line2)
#              if end_tag2_re.search(out_line2):
#                out_line2 = end_tag2_re.sub('\\2\\1', out_line2)


            # жіночі прізвища мають жіночу лему
            if ('V' in origAffixFlags or 'U' in origAffixFlags) and "<+" in origAffixFlags and ':f:' in out_line2:
                    parts = out_line2.split(' ')
                    if ':f:v_naz' in out_line2:
                      last_fem_lastname_v_naz = parts[0]
                      out_line2 = parts[0] + ' ' + parts[0] + ' ' + parts[2]
                      
                      for lastname_line in fem_lastnames_deferred:
                        new_line = lastname_line.replace('XXX', last_fem_lastname_v_naz)

                        if last_fem_lastname_v_naz[:-1] in CONSONANTS + "o":
                          new_line = re.sub('^[^ ]+', last_fem_lastname_v_naz, new_line)

                        all_out_lines.append( new_line )
                        
                      fem_lastnames_deferred = []
                    else:
                      deriv = parts[0]
                      if last_fem_lastname_v_naz != '':
                        
                        if last_fem_lastname_v_naz[:-1] in CONSONANTS + "o":
                          deriv = last_fem_lastname_v_naz
                        
                        out_line2 = deriv + ' ' + last_fem_lastname_v_naz + ' ' + parts[2]
                      else:
                        out_line2 = deriv + ' XXX ' + parts[2]
                        fem_lastnames_deferred.append(out_line2)
                        continue

        
            all_out_lines.append( out_line2 )
        
            collect_all_words(out_line2)


    all_out_lines = [ tail_tag(line, ['&adj', 'v-u', 'bad', 'slang', 'rare', 'coll', 'abbr']) for line in all_out_lines ]

    for i, line in enumerate(all_out_lines):
        if " adjp" in line:
            all_out_lines[i] = re.sub(" (adjp(:pasv|:actv|:pres|:past|:perf|:imperf)+):(.*)(:&adj)", " adj:\\3:&\\1", line)

    return all_out_lines

# end

def collect_comparatives(ifile):
    line_cnt = 0
    for line in ifile:
      line = line.strip()
      if 'ий/V' in line:
          if 'іший/V' in line and 'Y' in line:
              comparatives.append( ishy_re.sub('', line ) )
          elif shy_re.search(line):
              comparatives_shy.append( shy_remove_re.sub('', line ) )
          elif 'іший/V' in line and re.match('(як|що)?най.*', line):
              comparatives.append( re.sub('^(?:як|що)?най(.*)іший/.*$', '\\1', line ) )
      line_cnt += 1
    
    if line_cnt < 1:
      print("ERROR: empty source file", file=sys.stderr)
      sys.exit(1)

    print("comparatives", len(comparatives), file=sys.stderr)
    print("comparatives_shy", len(comparatives_shy), file=sys.stderr)
    #print("comparatives", comparatives, file=sys.stderr)
    #print("comparatives_shy", comparatives_shy, file=sys.stderr)


# --------------
# main code
# --------------
    
aff_arg_idx = sys.argv.index('-aff') if '-aff' in sys.argv else -1
if aff_arg_idx != -1:
  affix_filename = sys.argv[aff_arg_idx+1]
else:
  affix_filename = os.path.dirname(os.path.abspath(__file__)) + "/../../src/Affix/uk_affix.tag"

affix.load_affixes(affix_filename)


if __name__ == "__main__":
    
    if not '-' in sys.argv:
        src_filename = os.path.dirname(os.path.abspath(__file__)) + "/../../src/Dictionary/uk_words.tag"
        
        file_sfx = ''
        if '-t' in sys.argv:
            print("Running in test mode")
            file_sfx = '.test'
            src_filename = "uk_words.tag.test"
        
        print("Working with word list from", src_filename)
        
        ifile = open(src_filename, "r")
        
        collect_comparatives(ifile)
    
    if '-' in sys.argv:
        ifile = sys.stdin
        ofile = sys.stdout
    else:
        ifile = open(src_filename, "r")
        ofile = open("tagged.main.txt"+file_sfx, "w")
    
    all_out_lines = []

    for line in ifile:
    
      line = line.strip()
      if len(line) == 0:
          continue
    
      lines = expand_alts([line], '|', tag_split0_re)
    
      for line in lines:
        out_lines = process_line(line)
        
        for out_line in out_lines:
            if " adv" in out_line and not "advp" in out_line and not ":comp" in out_line and not ":super" in out_line:
                adv = out_line.split(' ')[1]
                if adv[:-1] in comparatives:
                    out_line += ":compb"
            all_out_lines.append( out_line )

#    print('advs', adverbs, file=sys.stderr)
#    print('adv_compar', adverbs_compar, file=sys.stderr)
#    print('comparatives', comparatives, file=sys.stderr)
    
    for adv_line in adverbs_compar:
      adv = adv_line.split(' ')[1]
      if adv in adverbs:
          all_out_lines.append( adv_line )
      
      
    for out_line in all_out_lines:
        ofile.write(out_line + '\n')
      
      
    if not '-' in sys.argv:
      
        locale.setlocale(locale.LC_ALL, "uk_UA.UTF-8")
      
        lst_ofile = open("all_words.lst"+file_sfx, "w")
        allWords = list(set(allWords))
        allWords.sort(key=locale.strxfrm)
      
        for w in allWords:
          if not w.startswith('#'):
            lst_ofile.write(w + '\n')

## expand_alts
## process_line
##   expand_alts (2)
##   expand_word
##   generate
##      generate_suffix
##      expand_alts (2)
