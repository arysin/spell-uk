#!/usr/bin/ruby
# encoding: utf-8


class Stats

  def initialize()
	@suffixStats = Hash.new(0)
	load_stats3
  end

def load_stats3

  sum = 0

#  f = File.open("data/uk_words3f.stat", "r") do |f|
  f = File.open("data/uk_words3.stat", mode: 'r:UTF-8') do |f|
    f.each_line { |line|
	  line = line.chop.strip
	  line_stats = line.split(/[ \/]/)

	  k = line_stats[0].to_i
	  suff = line_stats[1]
	  flag = line_stats[2]

	  if k > 1 
		if ! @suffixStats.has_key?( suff )
		  @suffixStats[ suff ] = [ [ flag, k ] ]		# вий => [ [ 'V', 30 ], [ 'i', 5 ] ]
#puts "putting #{suff} #{flag} #{k}"
		else
		  @suffixStats[ suff ].push( [ flag, k ] )		# вий => [ 'V', 30 ]
#puts "adding #{suff} #{flag} #{k}"
		end
		
		sum += k

		@suffixStats[ suff ] = @suffixStats[ suff ].sort_by { | stat | -stat[1] }	# sort desc by k
	  end
	}
  end

  puts "stats: #{sum}"

end



def suggestions_by_suffix(word)
  if word == nil or word.length < 5
	return []
  end

  suffix = word[-4, 4]
  puts "пропозиція: #{word} sfx: #{suffix}  #{@suffixStats[ suffix ]}"
  @suffixStats[ suffix ]
end



def guess_type2(word)
  if /ий$/ =~ word
	flag = ADJ_FLAGS[0]
  end
  if /ти$/ =~ word
	flag = VERB_FLAGS[0]
  end
  if /ій$/ =~ word
	flag = "i"
  end
  if /ік$/ =~ word
	flag = "i"
  end
  puts "#{word}/#{flag}"
  [ flag ]
end


end
