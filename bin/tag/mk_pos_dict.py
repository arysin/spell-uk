#!/usr/bin/python3

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


logger = logging.getLogger('tofsa')

#spell_uk_dir = os.getenv("HOME") + "/work/ukr/spelling/spell-uk/"
all_out_lines = []

PLURAL_FLAGS_RE = '[bfjlq9]'
NOUN_FLAGS_RE = '[a-z]';

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
ending_i_nnia_re = re.compile(r'.*(([бвгджзклмнпрстфхцчшщ])\2|\'|[рдтж])я$')
ending_ae_ets_re = re.compile('.*[еє]ць$')
ending_a_n_re = re.compile('.*([ео]нь|оль|оть)$')
ending_ae_ik_re = re.compile('.*і[дйрлгсзкп]$')
ending_a_numr_re = re.compile('.*(ять|сят|сто)$')
ending_masc_dull_re = re.compile('.*[бвжлнртьшк]$')

ending_evi_re = re.compile('^.*?[еоє]ві .*$')
ending_iv_re = re.compile('^.* .*?[ії]в .*$')
ending_istu_re = re.compile('^.*?[иі]сту .* .*$')
ending_uyu_re = re.compile('^.*?[ую] .* .*$')

ishy_re = re.compile('іший/.*$')
shy_re = re.compile('[^і][шщч]ий/.*$')
shy_remove_re = re.compile('[шщч]ий/.*$')
yi_sub_re = re.compile('ий/.*$')
shyi_sub_re = re.compile('(кий|с?окий)/.*$')

end_tag_re = re.compile('((?::(?:&[a-z]+|bad|slang|rare|coll))+)(:.+)')

#@profile
def expand_alts(lines, splitter, regexp):
    out = []

    for line in lines:

        if not splitter in line:
            out.append( line )
            continue
            
        if splitter == '/':
          groups = re.match("^([^/]+:)([^:]+)(:[^/]+)?$", line).groups()
        elif splitter == '|':
          groups = re.match("^(.* )(.*)$", line).groups()
        else:
          groups = re.match("^([^/:]+:)(.*)$", line).groups()

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
  return '+' in allAffixFlags \
    or ('+' in allAffixFlags and word.endswith('о'))
#    or ('e' in allAffixFlags and word[0].isupper() \
#           and ( word.endswith('ич') or word.endswith('ук') or word.endswith('юк') or word.endswith('як')) )

def lastname_dual(word, allAffixFlags):
  return '+' in allAffixFlags and ('e' in allAffixFlags and word[0].isupper() \
           and (word.endswith('ко') or word.endswith('ич') or word.endswith('ук') or word.endswith('юк') or word.endswith('як')) )

def istota(word, allAffixFlags):
  return ('p' in allAffixFlags or '<' in allAffixFlags) \
    or lastname(word, allAffixFlags)

def person(word, allAffixFlags):
  return ('p' in allAffixFlags or ('<' in allAffixFlags and not '>' in allAffixFlags)) \
    or lastname(word, allAffixFlags)



#@profile
def generate(word, allAffixFlags, origAffixFlags, main_tag):

    all_forms = []
    
    for affixFlag in allAffixFlags:
        if affixFlag in "<>+":
          continue

        if not affixFlag in affixMap:
          print("ERROR: Invalid flag", affixFlag, "for", word, file=sys.stderr)
          continue

        affixGroups = affixMap[affixFlag]

        lines = generate_suffix(word, affixFlag, affixGroups, allAffixFlags, origAffixFlags)
        
        for line in lines:
#            print(affixFlag, word, ':', line, file=sys.stderr)
            
            # remove plurals
            if '//p:v_' in line:
                if affixFlag in 'eg' and 'f' not in allAffixFlags and 'j' not in allAffixFlags:
                    line = re.sub('//p:v_[a-z]+(/v_[a-z]+)*', '', line)
                if affixFlag == 'i' and 'j' not in allAffixFlags:
                    line = re.sub('//p:v_[a-z]+(/v_[a-z]+)*', '', line)
                if affixFlag == 'r' and 's' not in allAffixFlags:
                    line = re.sub('//p:v_[a-z]+(/v_[a-z]+)*', '', line)
                if affixFlag in 'lq' and 'm' not in allAffixFlags:
                    line = re.sub('//p:v_[a-z]+(/v_[a-z]+)*', '', line)
                if affixFlag in 'ac' and 'o' not in allAffixFlags and 'b' not in allAffixFlags:
                    line = re.sub('//p:v_[a-z]+(/v_[a-z]+)*', '', line)

            if '/v_kly' in line:
                if not person(word, origAffixFlags) \
                  or ('v_dav' in line and 'h' in origAffixFlags and affixFlag != 'p') \
                  or (('v_zna' in line or 'v_dav' in line) and 'd' in origAffixFlags and affixFlag != 'p') \
                  or lastname(word, origAffixFlags):
                    line = re.sub('/v_kly', '', line)

            if affixFlag in 'V9j' and 'adj:p:v_naz/v_zna' in line:
              if '<' in allAffixFlags:
                if not '>' in allAffixFlags:
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
                if ending_istu_re.match(line):
                    line = line.replace('m:v_dav/v_mis', 'm:v_dav')
                if ('j' in allAffixFlags or 'b' in allAffixFlags) and word.endswith('о'):
                    line = line.replace('m:v_rod', 'm:v_rod//p:v_naz')
                    line = line.replace(':m:', ':n:')

                if istota(word, allAffixFlags):
                    if 'm:v_rod' in line:
                        line = line.replace('m:v_rod', 'm:v_rod/v_zna')
                else:
                    if not ending_iv_re.match(word) and ending_evi_re.match(line):
                        line = line.replace('m:v_dav/v_mis', 'm:v_dav')
            elif affixFlag in "ir":
                 if istota(word, allAffixFlags):
                   if 'noun:f:v_rod' in line and not word.endswith('а') and not word.endswith('матір'):
                     line = line.replace('f:v_rod', 'f:v_rod/v_zna')
#                 else:
#                   if 'noun:f:v_naz' in line:
#                     line = line.replace('f:v_naz', 'f:v_naz/v_zna')
            elif affixFlag == 'a':
                if 'c' not in allAffixFlags:
                    if 'noun:m:v_dav' in line and ('у ' in line or 'ю ' in line):
                        line = line.replace('m:v_dav', 'm:v_rod/v_dav')
                if not istota(word, allAffixFlags):
                    if not ending_iv_re.match(word) and ending_evi_re.match(line):
                        line = line.replace('m:v_dav/v_mis', 'm:v_dav')
            elif affixFlag in 'cgq':
                if istota(word, allAffixFlags) and 'noun:m:v_rod' in line:
                    line = line.replace('m:v_rod', 'm:v_rod/v_zna')

            if not '/v_kly' in line:
              if 'p:v_naz' in line and person(word, allAffixFlags):
                line = line.replace('p:v_naz', 'p:v_naz/v_kly')

            # handle znahidny for plural
            if len(set(allAffixFlags) & set("bofjms")) > 0:
                if len(set(allAffixFlags) & set("bojms")) > 0:
                    if '<' in allAffixFlags or 'p' in allAffixFlags:
                        line = line.replace('p:v_rod', 'p:v_rod/v_zna')
                        if '>' in allAffixFlags:
                            line = line.replace('p:v_naz', 'p:v_naz/v_zna')
                    else:
                        line = line.replace('p:v_naz', 'p:v_naz/v_zna')
                elif istota(word, allAffixFlags):
                    line = line.replace('p:v_rod', 'p:v_rod/v_zna')
                else:
                    line = line.replace('p:v_naz', 'p:v_naz/v_zna')

#                print("--", word, allAffixFlags, line, file=sys.stderr)

            out = expand_alts([line], '//', tag_split2_re)
            out = expand_alts(out, '/', tag_split1_re)

            all_forms.extend(out)
            
    return all_forms

def get_word_base(word, affixFlag, allAffixFlags):
        str = ''
        
        v_zna_for_anim = ""
        if istota(word, allAffixFlags):
            v_zna_for_anim = "/v_zna";

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
            elif word.endswith('ій'):
                str = word + ' ' + word + ' adj:m:v_naz/v_zna//f:v_dav/v_mis'
            else:
              if istota(word, allAffixFlags):
                str = word + ' ' + word + ' noun:m:v_naz'
              else:
                str = word + ' ' + word + ' adj:m:v_naz/v_zna'
                
        elif re.match('[AIKMC]', affixFlag):
            str = word + ' ' + word + ' verb:inf'
        elif re.match('[BJLN]', affixFlag):
            str = word + ' ' + word + ' verb:rev:inf'
            
        elif affixFlag == 'a' and ending_a_numr_re.match(word):
            str = word + ' ' + word + ' numr:v_naz/v_zna'
        elif affixFlag == 'a' and ending_a_aja_re.match(word):
            str = word + ' ' + word + ' noun:f:v_naz'
        elif affixFlag == 'a':
            if not istota(word, allAffixFlags):
                str = word + ' ' + word + ' noun:m:v_naz/v_zna'
            else:
                str = word + ' ' + word + ' noun:m:v_naz'
        elif affixFlag in 'bfo':
            str = word + ' ' + word + ' noun:p:v_naz/v_kly'
        elif affixFlag == 'e' and word.endswith('е'):
            str = word + ' ' + word + ' noun:n:v_naz/v_zna'
        elif affixFlag == 'e' and lastname_dual(word, allAffixFlags):
            str = word + ' ' + word + ' noun:m:v_naz//f:nv'
        elif affixFlag == 'e':
            if not istota(word, allAffixFlags) or ('j' in allAffixFlags and word.endswith('о')):
                str = word + ' ' + word + ' noun:m:v_naz/v_zna'
            else:
                str = word + ' ' + word + ' noun:m:v_naz'
#        elif affixFlag == 'o' and (word.endswith('и')):
#            str = word + ' ' + word + ' noun:p:v_naz/v_zna'
        elif affixFlag == 'l' and word[-1] in 'р':
            if not istota(word, allAffixFlags):
                str = word + ' ' + word + ' noun:m:v_naz/v_zna'
            else:
                str = word + ' ' + word + ' noun:m:v_naz'
        elif affixFlag == 'l' and word[-1] in 'яа':
            #if not istota(word, allAffixFlags):
            str = word + ' ' + word + ' noun:n:v_naz/v_zna'
            if istota(word, allAffixFlags):
              str += '/v_kly'
            #else:
            #    str = word + ' ' + word + ' noun:n:v_naz'
        elif affixFlag == 'l' and re.match('.*[еє]нь$', word):
            str = word + ' ' + word + ' noun:m:v_naz/v_zna'
        elif affixFlag == 'l' and re.match('.*ець$', word):
            str = word + ' ' + word + ' noun:m:v_naz'
        elif affixFlag == 'l' and re.match('.*([^ц]ь|[чш]|іць)$', word):
            str = word + ' ' + word + ' noun:f:v_naz/v_zna'
        elif affixFlag == 'i' and (word.endswith('ий') or word.endswith('ій')):
            str = word + ' ' + word + ' noun:m:v_naz'
            if istota(word, allAffixFlags):
              str += '/v_kly'
            else:
              str += '/v_zna'
        elif affixFlag == 'i' and word.endswith('ів'):
            str = word + ' ' + word + ' noun:m:v_naz/v_zna'
        elif affixFlag == 'i' and ending_i_nnia_re.match(word):
            str = word + ' ' + word + ' noun:n:v_naz/v_rod/v_zna//p:v_naz'
        elif affixFlag == 'i' and (word.endswith('о') or word.endswith('е')):
            str = word + ' ' + word + ' noun:n:v_naz'
            if word.endswith('е') and istota(word, allAffixFlags):
              str += '/v_kly'
            else:
              str += '/v_zna'
        elif affixFlag == 'i' and (word.endswith('а')):
            str = word + ' ' + word + ' noun:f:v_naz'
            if istota(word, allAffixFlags):
              str += '/v_kly'
#            else:
#              str += '/v_zna'
        elif affixFlag in "ir" and word[-1] in "ьаячшжрвф":
            str = word + ' ' + word + ' noun:f:v_naz'
            if not istota(word, allAffixFlags) or word.endswith('матір'):
              str += '/v_zna'
        elif affixFlag == 'i' and word.endswith('ін'):
            str = word + ' ' + word + ' noun:m:v_naz'
        elif affixFlag == 'j' and word[-1] in 'іа':
#            if not istota(word, allAffixFlags):
#                str = word + ' ' + word + ' noun:p:v_naz/v_zna'
#            else:
                str = word + ' ' + word + ' noun:p:v_naz'
        elif re.match('[a-p]', affixFlag):
            if affixFlag == 'p' and allAffixFlags[0] == 'p':
              return str
              
            str = word + ' ' + word + ' noun:unknown'
            print(str, '---', word, affixFlag)
            str = ""
        else:
            str = word + ' ' + word + ' unknown'
            print(str, '---', word, affixFlag)

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
                    
                lines.append( deriv + ' ' + word_base + ' ' + affix.tags )

    return lines


#@profile
def expand_word(word, affixFlags):
    words = [ word ]

    affixFlagsToRemove = list()
    for affixFlag in affixFlags:
        if affixFlag in prefixes:
#            print(affixFlag, 'in prefixes for', word)
            affixGroups = affixMap[affixFlag]
            words.append( expand_prefix(word, affixFlag, affixGroups) )
            affixFlagsToRemove.append(affixFlag)
    
    for f in affixFlagsToRemove:
        affixFlags.remove(f)
    
    return words


#@profile
def expand_prefix(word, affixFlag, affixGroups):
    str = word

    for affixGroup in affixGroups.values():
      if affixGroup.matches(word):
        for affix in affixGroup.affixes:
          str = affix.apply(word)

    return str

def retain_tags(line, tags):
    parts = line.split(':')
    line = parts[0]
    for part in parts:
        if part in tags:
            line += ':' + part
    return line

def post_process(line, affixFlags):
    if "impers" in line:
         line = retain_tags(line, ['impers', 'imperf', 'perf', 'bad', 'slang', 'coll', 'alt', 'rare'])
    elif "advp" in line:
        line = re.sub('(advp:(?:rev:)?(?:im)?perf):(?:im)?perf(?::(?:im)?perf)?(.*)', '\\1\\2', line)
# дієприслівник, як окрема лема
#        line = re.sub('([^ ]+) [^ ]+ (advp:(?:rev:)?(?:im)?perf):(?:im)?perf(?::(?:im)?perf)?(.*)', '\\1 \\1 \\2\\3', line)
        if ":rev" in line and "tran" in line:
            line = re.sub(':(in)?tran(:rv_[a-z]+)*', '', line)
    elif "verb" in line:
        if ":rev" in line and "tran" in line:
            line = re.sub(':(in)?tran(:rv_[a-z]+)*', '', line)
            
        if ":imperf:perf" in line:
            line1 = line.replace(":perf", "")
            line2 = line.replace(":imperf", "")

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
        else:
            line = line.replace('іший adj', 'ий adj')

        if ':compr' in line and line.startswith('най'):
            line = line.replace(':compr', ':super')
    
    lines = [line]
    
    if re.match('[^ ]+ше [^ ]+ .*v_naz.*(compr|super).*', line):
        line1 = re.sub('([^ ]+ше [^ ]+[чш])ий adj:n:v_naz.*((compr|super).*)', '\\1е adv:\\2', line)
        line1 = re.sub('([^ ]+ше [^ ]+[^чш])ий adj:n:v_naz.*((compr|super).*)', '\\1о adv:\\2', line1)
        adverbs_compar.append( line1 )

    return lines


def collect_all_words(line):
    if not ':bad' in line and not ':rare' in line and not ':obs' in line and not ':coll' in line: # and not ':alt' in line:
        allWords.append(line.split(' ')[0])
    if ' adv' in line:
        adverbs.append(line.split(' ')[0])



VIDM=['v_naz', 'v_rod', 'v_dav', 'v_zna', 'v_oru', 'v_mis', 'v_kly']
re_nv_vidm=re.compile('(noun):[mfn]:(.*)')

def expand_nv(in_lines):
  lines = []
  
  for line in in_lines:
    if 'noun' in line and ':nv' in line:
        parts = line.split(':nv')
    
        for v in VIDM:
          if v != 'v_kly' or 'anim' in line:
            lines.append(parts[0] + ':' + v + ':nv' + parts[1])
          
        if not ':p' in line and not ':np' in line:
          for v in VIDM:
            if v != 'v_kly' or 'anim' in line:
              lines.append(re_nv_vidm.sub('\\1:p:' + v + ':\\2', line))
    else:
        lines.append(line)

  return lines

#@profile
def process_line(line):
    if " " in line and not " :" in line and not " ^" in line:
        out = expand_alts([line], '//', tag_split2_re)
        out = expand_alts(out, '/', tag_split1_re)
       
        out = expand_nv(out)
        
        all_out_lines.extend(out)
        
        [collect_all_words(w) for w in out]
        
        return

#    if line.endswith('ен'):
#        tag = 'adj:m:v_naz'
#        outline = line + ' ' + re.sub('ен$', 'ний', line)
#        ofile.write(outline + ' ' + tag + '\n')
#
#        tag = 'adj:m:v_zna'
#        ofile.write(outline + ' ' + tag + '\n')
#
#        collect_all_words(outline)
#        return


    extra_tag = ''
    
    if '/V' in line and '<' in line:
      line += ' ^noun'

    if not '^noun' in line:
      if with_Y_flag_re.match(line):
        if line.startswith('най'):
            extra_tag += ':super';
        else:
            extra_tag += ':compr';
      elif yi_V_flag_re.match(line):
        if (line.startswith('най') and 'іший/' in line) or line.startswith('якнай') or line.startswith('щонай'):
            extra_tag += ':super';
        elif shyi_sub_re.sub('', line) in comparatives_shy or yi_sub_re.sub('', line) in comparatives:
            extra_tag += ':compb'
#            print('compb for ' + line)
        elif re.sub('/.*', '', line) in COMPAR_FORMS.values():
            extra_tag += ':compb'
#    elif re.match('/[^ ]*p', line):
#       extra_tag += ':pers'

    main_tag = ''
    if " :" in line:
        spl = line.split(" ")
        extra_tag = spl[1]
        line = spl[0]
#        print("extra tag", extra_tag, "for", line)
    elif " ^" in line:
        spl = line.split(" ^")
        main_tag = spl[1]
        line = spl[0]

    if "X" in line:
        extra_tag += ':v-u'

    if "<" in line or "p" in line:
        extra_tag += ':anim'
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

    if not with_flags_re.match(line):
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

        collect_all_words(outline)
        return


    halfs = re.split('/', line)

    word = halfs[0]
    origAffixFlags = halfs[1]
    affixFlags = list(origAffixFlags)

    out_lines = []
    for word in expand_word( word, affixFlags ):
#        print("affixFlags", affixFlags, word)
        if not affixFlags:
          out_lines.append( word + ' ' + word + ' unknown')
        else:
          out_lines.extend( generate(word, affixFlags, origAffixFlags, main_tag) )

    for out_line in out_lines:
#        print("affixFlags", affixFlags, out_line, extra_tag)
#        print('--:', out_line, word, re.sub('ий$', '', word), extra_tag)

        if 'Z' in origAffixFlags and out_line.startswith('не'):
            if re.sub('ий$', '', word) in comparatives: # and word in COMPAR_FORMS.values():
                if not ':compb' in extra_tag:
                   extra_tag = ':compb' + extra_tag
            else:
                extra_tag = extra_tag.replace(':compb', '')
        
        out_line += extra_tag
        
        out_lines2 = post_process(out_line, affixFlags)
        
        for out_line2 in out_lines2:
            # пропустити середній для прізвищ
            if origAffixFlags.endswith('V<') and ':n:' in out_line2:
              continue
            

        
            if main_tag:
              if not " adv" in out_line2 and (not 'Z' in origAffixFlags or not out_line2.startswith('не') or not main_tag.startswith('adjp')):
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
            
              # put end tags at the end
              if end_tag_re.search(out_line2):
                #print('main tag for ', out_line2, file=sys.stderr)
                out_line2 = end_tag_re.sub('\\2\\1', out_line2)
        
            all_out_lines.append( out_line2 )
        
            collect_all_words(out_line2)


# end

tags_re = re.compile('(.*:)v_...(.*)')

def match_comps(lefts, rights):
    outs = []
    left_v = {}
    
    for ln in lefts:
        parts = ln.split(' ')
        rrr = re.search(':(.:v_...)', parts[2])
        if not rrr:
            print('ignoring left', ln)
            continue
        
        vidm = rrr.group(1)
        
        if not vidm in left_v:
            left_v[vidm] = []

        left_v[vidm].append(parts[0])
        left_wn = parts[1]
        left_tags = parts[2]

    for rn in rights:
        parts = rn.split(' ')
        rrr = re.search(':(.:v_...)', rn)
        if not rrr:
            print('ignoring right', rn)
            continue

        vidm = rrr.group(1)
        
        if not vidm in left_v:
            continue
        
        for left_wi in left_v[vidm]:
            wi = left_wi + '-' + parts[0]
            wn = left_wn + '-' + parts[1]
            outs.append(wi + ' ' + wn + ' ' + tags_re.sub('\\1'+vidm+'\\2', left_tags))

    return outs

# --------------
# main code
# --------------

if '-comp' in sys.argv:
    comp_flag = True
else:
    comp_flag = False

aff_arg_idx = sys.argv.index('-aff') if '-aff' in sys.argv else -1
if aff_arg_idx != -1:
  affix_filename = sys.argv[aff_arg_idx+1]
else:
  affix_filename = os.path.dirname(os.path.abspath(__file__)) + "/../../src/Affix/uk_affix.tag"

affix.load_affixes(affix_filename)


if not '-' in sys.argv:
  src_filename = os.path.dirname(os.path.abspath(__file__)) + "/../../src/Dictionary/uk_words.tag"

  file_sfx = ''
  if '-t' in sys.argv:
    print("Running in test mode")
    file_sfx = '.test'
    src_filename = "uk_words.tag.test"

  print("Working with word list from", src_filename)

  ifile = open(src_filename, "r")

  line_cnt = 0
  for line in ifile:
    line = line.strip()
    if 'ий/V' in line:
        if 'іший/V' in line and 'Y' in line:
            comparatives.append( ishy_re.sub('', line ) )
        elif shy_re.search(line):
            comparatives_shy.append( shy_remove_re.sub('', line ) )
        elif 'іший/V' in line and line.startswith('най'):
            comparatives.append( re.sub('^най(.*)іший/.*$', '\\1', line ) )
    line_cnt += 1

  if line_cnt < 1:
    print("ERROR: empty source file", file=sys.stderr)
    sys.exit(1)


print("comparatives", len(comparatives))
#print("comparatives " + str(comparatives))
print("comparatives_shy", len(comparatives_shy))

if '-' in sys.argv:
  ifile = sys.stdin
  ofile = sys.stdout
else:
  ifile = open(src_filename, "r")
  ofile = open("tagged.main.txt"+file_sfx, "w")

if comp_flag:

  for line in ifile:

    line = line.strip()
    if len(line) == 0:
      continue

    parts = line.split('-')
        
    process_line(parts[0])
    lefts = all_out_lines
    all_out_lines = []

    process_line(parts[1])
    rights = all_out_lines
    all_out_lines = []
    
    comps = match_comps(lefts, rights)
    ofile.write('\n'.join(comps) + '\n')

else:

  for line in ifile:

    line = line.strip()
    if len(line) == 0:
      continue

    lines = expand_alts([line], '|', tag_split0_re)

    for line in lines:
        process_line(line)


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
