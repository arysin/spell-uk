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


PLURAL_FLAGS_RE = '[bfjlq]'
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


#@profile
def expand_alts(lines, splitter, regexp):
    out = []

    for line in lines:

        if not splitter in line:
            out.append( line )
            continue

        split1 = line.split(splitter)
        base = split1[0]

        out.append( base )

        for split_ in split1[1:]:
#            print('split', splitter, base, split_)
            new_tags1 = regexp.sub( split_, base )
            out.append( new_tags1 )

    return out



#def isAcegSuffix(affixFlag, allAffixFlags):
 #   return (affixFlag == 'e' and not 'g' in allAffixFlags) #or (affixFlag == 'a' and 'c' in allAffixFlags)

def istota(word, allAffixFlags):
  return ('p' in allAffixFlags or '<' in allAffixFlags) \
    or ('e' in allAffixFlags and word[0].isupper() and word.endswith('ко'))
#    and ('g' in allAffixFlags or 'c' in allAffixFlags or ('e' in allAffixFlags and word.endswith('о')))) \


#@profile
def generate(word, allAffixFlags, origAffixFlags):

    all_forms = []
    
    for affixFlag in allAffixFlags:
        if affixFlag in "<>":
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
                if affixFlag in 'lq' and 'm' not in allAffixFlags:
                    line = re.sub('//p:v_[a-z]+(/v_[a-z]+)*', '', line)
                if affixFlag in 'ac' and 'o' not in allAffixFlags and 'b' not in allAffixFlags:
                    line = re.sub('//p:v_[a-z]+(/v_[a-z]+)*', '', line)

            if '/v_kly' in line:
                if not istota(word, origAffixFlags) or '>' in origAffixFlags:
                    line = re.sub('/v_kly', '', line)

            # handle rodovyi for singular
            if affixFlag == 'e':
                if not 'g' in allAffixFlags and 'noun:m:v_dav' in line and ending_uyu_re.match(line) and not 'о ' in line:
                    line = line.replace('m:v_dav', 'm:v_rod/v_dav')
                if not 'g' in allAffixFlags and 'noun:m:v_dav' in line and ending_uyu_re.match(line) and 'о ' in line and word[0].isupper():
                    line = line.replace('m:v_dav', 'm:v_dav/v_mis')
                if ending_istu_re.match(line):
                    line = line.replace('m:v_dav/v_mis', 'm:v_dav')
                if 'j' in allAffixFlags and word.endswith('о'):
                    line = line.replace('m:v_rod', 'm:v_rod//p:v_naz')

                if istota(word, allAffixFlags):
                    if 'm:v_rod' in line:
                        line = line.replace('m:v_rod', 'm:v_rod/v_zna')
                else:
                    if not ending_iv_re.match(word) and ending_evi_re.match(line):
                        line = line.replace('m:v_dav/v_mis', 'm:v_dav')
            elif affixFlag == 'a':
                if 'c' not in allAffixFlags:
                    if 'noun:m:v_dav' in line and ('у ' in line or 'ю ' in line):
                        line = line.replace('m:v_dav', 'm:v_rod/v_dav')
                if not istota(word, allAffixFlags):
                    if not ending_iv_re.match(word) and ending_evi_re.match(line):
                        line = line.replace('m:v_dav/v_mis', 'm:v_dav')
            elif affixFlag in 'cgq':
                if istota(word, allAffixFlags) and 'noun:m:' in line:
                    line = line.replace('m:v_rod', 'm:v_rod/v_zna')
  
            # handle znahidny for plural
            if len(set(allAffixFlags) & set("bofjm")) > 0:
                if len(set(allAffixFlags) & set("bojm")) > 0:
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

        if affixFlag == 'U' and ( word.endswith('ов') or word.endswith('єв') ):
            str = word + ' ' + word + ' noun:m:v_naz'
        elif affixFlag == 'V' or affixFlag == 'U':
            if word.endswith('е'):
                str = word + ' ' + word + ' adj:n:v_naz'
            elif word.endswith('ій'):
                str = word + ' ' + word + ' adj:m:v_naz/v_zna//f:v_dav/v_mis'
            else:
                str = word + ' ' + word + ' adj:m:v_naz/v_zna'
        elif re.match('[AIKM]', affixFlag):
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
        elif affixFlag == 'e' and (word.endswith('ко') or ('<' in allAffixFlags and (word.endswith('ич') or word.endswith('ук') or word.endswith('юк')))) and word[0].isupper():
            str = word + ' ' + word + ' noun:m:v_naz//f:nv'
        elif affixFlag == 'e':
            if not istota(word, allAffixFlags):
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
            #else:
            #    str = word + ' ' + word + ' noun:n:v_naz'
        elif affixFlag == 'l' and re.match('.*[еє]нь$', word):
            str = word + ' ' + word + ' noun:m:v_naz/v_zna'
        elif affixFlag == 'l' and re.match('.*ець$', word):
            str = word + ' ' + word + ' noun:m:v_naz'
        elif affixFlag == 'l' and re.match('.*([^ц]ь|[чш]|іць)$', word):
            str = word + ' ' + word + ' noun:f:v_naz/v_zna'
        elif affixFlag == 'i' and (word.endswith('ий') or word.endswith('ій')):
            str = word + ' ' + word + ' noun:m:v_naz/v_zna'
        elif affixFlag == 'i' and ending_i_nnia_re.match(word):
            str = word + ' ' + word + ' noun:n:v_naz/v_rod/v_zna//p:v_naz'
        elif affixFlag == 'i' and (word.endswith('о') or word.endswith('е')):
            str = word + ' ' + word + ' noun:n:v_naz/v_zna'
        elif affixFlag == 'i' and word[-1] in "ьаячшжрвф":
            str = word + ' ' + word + ' noun:f:v_naz/v_zna'
        elif affixFlag == 'i' and word.endswith('ін'):
            str = word + ' ' + word + ' noun:m:v_naz'
        elif affixFlag == 'j' and word[-1] in 'іа':
            if not istota(word, allAffixFlags):
                str = word + ' ' + word + ' noun:p:v_naz/v_zna'
            else:
                str = word + ' ' + word + ' noun:p:v_naz'
        elif re.match('[a-p]', affixFlag):
            str = word + ' ' + word + ' noun:unknown'
            print(str, '---', word, affixFlag)
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

def post_process(line, affixFlags):
    if "impers" in line:
        if ':bad' in line:
           line = re.sub('impers.*:bad', 'impers:bad', line)
        else:
           line = re.sub('impers.*', 'impers', line)
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
    if not ':bad' in line and not ':rare' in line:
        allWords.append(line.split(' ')[0])
    if ' adv' in line:
        adverbs.append(line.split(' ')[0])


#@profile
def process_line(line):
    if " " in line and not " :" in line and not " ^" in line:
        out = expand_alts([line], '//', tag_split2_re)
        out = expand_alts(out, '/', tag_split1_re)
        ofile.write("\n".join(out) + '\n')
        
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
        extra_tag += ':ist'
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
        ofile.write(outline + '\n')

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
          out_lines.extend( generate(word, affixFlags, origAffixFlags) )

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
            if main_tag:
              if not " adv" in out_line2 and (not 'Z' in origAffixFlags or not out_line2.startswith('не') or not main_tag.startswith('adjp')):
                 out_line2 = re.sub(' [a-z]+', ' ' + main_tag, out_line2)
              if " adjp" in out_line2:
                if 'Z' in origAffixFlags or 'W' in origAffixFlags:
                  out_line2 += ":+adj"
        
            ofile.write( out_line2 + '\n' )
        
            collect_all_words(out_line2)


# end

# --------------
# main code
# --------------

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
        ofile.write( adv_line + '\n' )


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
