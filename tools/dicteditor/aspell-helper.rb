#!/usr/bin/ruby
# encoding: utf-8

require 'open3'

Dictionary_Src_Dir="../../src/Dictionary"
Aspell_Personal_Dic="#{ENV['HOME']}/.aspell.uk.pws"
Output_Dir="./out"
Language="uk"

Not_In_Dict_List=['misc.lst']


#Sort_Command="LC_ALL=uk_UA.UTF-8 sort -d "
Sort_Command="sort -d "
Sort_Command="cat "


def aspell_expand(word)
	return [] if word.empty? 
	return [word] if !word.include?('/')
	
puts "expanding: #{word}"

    begin

    if $exp_stdin == nil
	   $exp_stdin = IO.popen("/usr/bin/python3 ../../bin/tag/affix.py -f", mode: 'r+:UTF-8')
	   $exp_stdin.sync = true
    end

    $exp_stdin.puts(word + "\n")
    res = $exp_stdin.gets
#    rescue
#	    puts "Failed to expand"
    end
#	cmd = IO.popen("echo \"#{word}\" | aspell -l #{Language} expand", mode: 'r+:UTF-8')
#	res = cmd.gets
#    cmd.close
    
    if res != nil
        puts "expanded: #{res.split(/[ \n]/).uniq}"
	res.split(/[ \n]/).uniq
    else
        res = []
    end
end

def aspell_munch(word)
#	cmd = IO.popen("echo \"#{word}\" | LC_ALL=uk_UA.UTF-8 aspell -l #{Language} munch", mode: 'r+:UTF-8')
#	res = cmd.gets
#	cmd.close
#	res, status = Open3.capture2("echo \"#{word}\" | LC_ALL=uk_UA.UTF-8 aspell -l #{Language} munch")
    begin

    if $munch_stdin == nil
	   $munch_stdin = IO.popen("/usr/bin/python3 ../../bin/tag/affix.py munch", mode: 'r+:UTF-8')
	   $munch_stdin.sync = true
    end
    
    $munch_stdin.puts(word + "\n")
    res = $munch_stdin.gets

#	res = `echo \"#{word}\" | LC_ALL=uk_UA.UTF-8 /usr/bin/aspell -l #{Language} munch`
	return res.split(/[ \n]/)
    rescue
	puts "Failed to munch"
#	begin
#	    res = `echo \"#{word}\" | LC_ALL=uk_UA.UTF-8 /usr/bin/aspell -l #{Language} munch`
#	    return res.split(/[ \n]/)
#	rescue
#	    puts "Failed to munch twice"
#	    return []
#	end
    end
end

#def munch_all(input_file)
##	cmd = IO.popen("echo #{word} | aspell -l #{Language} munch", "r+")
#	cmd = IO.popen("grep -E '...' #{input_file} | sort | uniq | aspell -l #{Language} munch", mode: 'r+:UTF-8');
#	res = cmd.gets
#    cmd.close
#	return res.split(/[ ]/)
#end


#def create_munch_freqs(input_file)
#  freqs = Hash.new(0)
#
#  munch_list = munch_all(input_file)
#  for munch_ver in munch_list
##		if freqs.has_key?(munch_ver)
#	freqs[ munch_ver ] += 1
#  end
#
#  freqs.each {|key, value| puts "#{key} is #{value}" }
#end


$SrcFile = Aspell_Personal_Dic
SrcLatinLines = []
SrcList = []

def load_source_list(inputFile)
  if inputFile != nil
	$SrcFile = inputFile
  end
  
  puts "Loading source from: #{$SrcFile}"

#  f = File.open(Aspell_Personal_Dic, "r") do |f|
  f = IO.popen(Sort_Command + $SrcFile, mode: 'r+:UTF-8')
  while line = f.gets
	  line.chop!
	  if ! /[A-Za-z]/.match(line)
		SrcList << line
	  else
		SrcLatinLines << line
	  end
  end
  f.close

  puts "Input words: #{SrcList.size}"

#  SrcList.sort!
end

def save_source_list()
#  input_file = Aspell_Personal_dic if input_file == nil

	File.open($SrcFile, mode: 'w:UTF-8') { |f|
	  for word in SrcLatinLines
		f << word << "\n"
	  end
	  for word in SrcList
		f << word << "\n"
	  end
	}
end


DictList = []

def load_dictionary_list
  f = Dir.foreach(Dictionary_Src_Dir) { |line|
	if (/\.lst$/ =~ line) and (! Not_In_Dict_List.include?(line))
	  DictList << line 
	  puts line
	end
  }
  DictList.sort!
end


load_dictionary_list


def find_in_dicts(word)
	ret = []

	if word.include?("-")
	  word = /-(.+)$/.match(word)[1] 	# try to match second part if '-' present
	else
	  word = /^(авіа|авто|агро|аеро|анти|аудіо|багато|відео|гео|гідро|гіпер|електро|кіно|мега|мета|мікро|мото|не|пере|під|по|радіо|стерео|спорт|теле|фото|супер)*(.+)*$/.match(word)[2]
	  if (word == nil)
		 return ret
	  end
	  word = word[0..-5] if word[-4..-1] == "ся"
	end

	cmd = IO.popen("grep -i -E \"#{word}(/[/A-Za-z]+)?( .*)?$\" #{Dictionary_Src_Dir}/??[!_]*.lst out/*.lst", mode: 'r+:UTF-8',)
	while r = cmd.gets
	  ret << r.chop
	end
    cmd.close

	newRet = []
	for r in ret
	  r = r.split(':')
	  r[0] = r[0][ r[0].rindex('/')+1, 100 ]
	  newRet << r
	end

	newRet
end

def find_in_krym(word)
    ret = []
    
    cmd = IO.popen("grep -i -E \"#{word}$\" data/dict*.lst", mode: 'r+:UTF-8',)
    while r = cmd.gets
      ret << r.chop
    end
    cmd.close
    
    ret
end


AddWords = Hash.new()
RemoveWords = Hash.new()

def add_word_to_dict(dict, word)
  puts "appending #{word} to #{dict}"
  AddWords[ dict ] = Array.new() if AddWords[ dict ] == nil
  AddWords[ dict ] << word
end

def remove_word_from_dict(dict, word)
  puts "removing #{word} to #{dict}"
  RemoveWords[ dict ] = Array.new() if RemoveWords[ dict ] == nil
  RemoveWords[ dict ] << word
end

def save_changes()
  for dict in AddWords.keys
#	File.open("#{Dictionary_Src_Dir}/#{dict}", "a") { |f|
	File.open("#{Output_Dir}/#{dict}", mode: 'a:UTF-8') { |f|
	  for word in AddWords[dict]
		f << word
		f << "\n"
	  end
	}
  end
  AddWords.clear
  
  for dict in RemoveWords.keys
#	File.open("#{Dictionary_Src_Dir}/#{dict}", "a") { |f|
	File.open("#{Output_Dir}/#{dict}-remove", mode: 'a:UTF-8') { |f|
	  for word in RemoveWords[dict]
		f << word
		f << "\n"
	  end
	}
  end
  RemoveWords.clear

  save_source_list  
end

def merge
  dictsTouched = []
  f = Dir.foreach(Output_Dir) { |file|
	if (/\.lst-remove$/ =~ file)
	  dictFile = file.gsub(/-remove/, '')
puts "removing list: #{file} from #{dictFile}"
	  dictFilePath = "#{Dictionary_Src_Dir}/#{dictFile}"
	  
	  cmdStr = "grep -v -x -f #{Output_Dir}/#{file} #{dictFilePath} > #{dictFilePath}.tmp"
	  cmdStr << " && cp #{dictFilePath} #{dictFilePath}.bak"
	  cmdStr << " && mv -f #{dictFilePath}.tmp #{dictFilePath}"
	  cmdStr << " && mv -f #{Output_Dir}/#{file} #{Output_Dir}/#{file}.old"
#	  cmd = IO.popen("grep -v -x -f #{Output_Dir}/#{file} #{dictFilePath} > #{dictFilePath}.tmp && cp #{dictFilePath} #{dictFilePath}.bak && mv -f #{dictFilePath}.tmp #{dictFilePath} && mv -f #{Output_Dir}/#{file} #{Output_Dir}/#{file}.old", "r+");
	  cmd = IO.popen(cmdStr, mode: 'r+:UTF-8')
	  cmd.close
	  dictsTouched << dictFile
	end 
  }

  f = Dir.foreach(Output_Dir) { |file|
	if (/\.lst$/ =~ file)
puts "adding list: #{file}"
	  dictFilePath = "#{Dictionary_Src_Dir}/#{file}"
	  bakCmd = ""
	  if ! dictsTouched.include?(file)
		bakCmd = "cp #{dictFilePath} #{dictFilePath}.bak && "
	  else
		dictsTouched << file
	  end
	  
	  cmdStr = "#{bakCmd} cat #{Output_Dir}/#{file} >> #{dictFilePath}"
	  cmdStr << " && mv -f #{Output_Dir}/#{file} #{Output_Dir}/#{file}.old"
	  cmd = IO.popen(cmdStr, mode: 'r+:UTF-8')
	  cmd.close
	end 
  }

puts "Sorting..."
  `/usr/bin/make -C #{Dictionary_Src_Dir} sort`

end


if $0 == __FILE__
  if ARGV.length >= 1 and ARGV[0] == '-m'
	merge
  end
end
