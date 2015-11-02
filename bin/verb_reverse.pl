#!/usr/bin/perl
#
# Скрипт для створення зворотніх форм дієслів з файлу афіксів
# Цей скрипт залежить від форматування файлу афіксів, навіть у коментарях
# Притримуйтесь, будь ласка, цього формату
#
# (c) Андрій Рисін, 2001, 2005
#
use strict;
use locale;
use utf8;
use encoding 'utf8';


my $UK_CAP	="'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ";
my $UK_LOW	="'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя";

my $start = '0';
my $tmp;

my $section_header;
my $line_count;
my @lines;
    
my %SFX_REV = (
    A => "B", I => "J", K => "L", M => "N",
    G => "H", C => "D", E => "F",
    O => "P", Q => "R", 6 => "7", 8 => "9"
);

# для слів, які мають і "-ся" і "-сь"
#my $GENERIC	="([аяийіїоуюв])|(те)";
my $GENERIC	="([аяийіїоуюв])|(те)";

print "# DO NOT EDIT!! Use bin/verb_reverse.pl instead to generate this file from ukrainian.aff.VERB!\n";
print "\n";

while(<>) {

    if( /^#/ ) {
	if( $start eq '1' ) {	# cutting off leading comments
	    push(@lines, $_);
	}
	next;
    }
    if( /^[\s]*$/ ) {
	push(@lines, $_);
	next;
    }
    
    $tmp = $_;
    $start = '1';
    $_ = $tmp;
    
# Заміна груп відповідними парами та зворотні інфінітиви

    if( /SFX\s[AIKMGCEOQ68]\s[YN]\s[0-9]+/ ) {
	my @SFX = split /\s+/, $_;
	my $sfx_rev = $SFX_REV{$SFX[1]};

	if( $line_count > 0 ) {
	    print "\n";
	    print $section_header, $line_count, "\n";
	
	    print @lines;
	}

	$section_header = $SFX[0] . ' ' . $sfx_rev . ' ' . $SFX[2] . ' ';
	@lines = ();
	$line_count = 0;
	
	if( $SFX[1] =~ /[AIKM]/ ) {
	    push(@lines, "# Зворотня форма дієслів (-ся та -сь)\n");
	    push(@lines, "SFX ", $sfx_rev, "   0\tся	ти		#  ~ти  ~тися    @ verb:rev:inf\n");
	    push(@lines, "SFX ", $sfx_rev, "   0\tсь	ти		#  ~ти  ~ись     @ verb:rev:inf\n");
	    push(@lines, "SFX ", $sfx_rev, "   ся	сь	тися		#  ~тися  ~ись    @ verb:rev:inf\n");

	    $line_count += 3;
	}
	
	next;
    }

    if( /SFX\s[AIKMGCEOQ68]\s/ ) {

	my @LINE = split /\s+/, $_;
	my @LINE_COMMENT = split /#/, $_;
	my $comment = $LINE_COMMENT[1];
	my $sfx_rev = $SFX_REV{$LINE[1]};
	my $suffix_oldbody = $LINE[2];
	my $suffix_newbody = $LINE[3];
	my $suffix_match = $LINE[4];


# Створення правил для афіксів та прикладів
    $comment =~ s/@ verb:/@ verb:rev:/;
    $comment =~ s/@ advp:/@ advp:rev:/;

    # перші дві умови для спецвипадку "мести - мететься"
    if( ( !($suffix_oldbody =~ /^сти$/) || !($suffix_newbody =~ /^те$/)) 
            &&  ( !($suffix_oldbody =~ /^ти$/) || !($suffix_newbody =~ /^те$/) || !($suffix_match =~ /^ости$/)) 
            && $suffix_newbody =~ s/($GENERIC)$/$1сь/ ) {
            
        if( $comment =~ /.*advp.*/ ) { # для дієприслівників, які мають тільки "-сь"
            $suffix_newbody =~ s/(чи|ши)$/$1сь/;
            $comment =~ s/([^#\s]\s+[$UK_LOW]+)(\s)/$1сь$2/;

	    push(@lines, $LINE[0], " ", $sfx_rev, "   ", $suffix_oldbody, "\t", $suffix_newbody, "\t", $suffix_match, "\t\t#", $comment);
	    push(@lines, $LINE[0], " ", $sfx_rev, "   ", get_reversed($suffix_oldbody, $suffix_newbody, $suffix_match, $comment));

	    $line_count += 2;
	}
        else {

            
	$comment =~ s/([^#\s]\s+[$UK_LOW]+$GENERIC)(\s)/$1сь$4/;

	push(@lines, $LINE[0]. " ". $sfx_rev. "   ". $suffix_oldbody. "\t". $suffix_newbody. "\t". $suffix_match. "\t\t#". $comment);
	push(@lines, $LINE[0]. " ". $sfx_rev. "   ". get_reversed($suffix_oldbody, $suffix_newbody, $suffix_match, $comment));

	$suffix_newbody =~ s/($GENERIC)сь$/$1ся/;
	$comment =~ s/([^#\s]\s+[$UK_LOW]+$GENERIC)сь(\s)/$1ся$4/;

	push(@lines, $LINE[0]. " ". $sfx_rev. "   ". $suffix_oldbody. "\t". $suffix_newbody. "\t". $suffix_match. "\t\t#". $comment);
	push(@lines, $LINE[0]. " ". $sfx_rev. "   ". get_reversed($suffix_oldbody, $suffix_newbody, $suffix_match, $comment));

	$line_count += 4;
	}
    }
    else {
            if( $suffix_newbody =~ s/([еє])$/$1ться/ ) { # для слів, які мають тільки "-ться"
	        $comment =~ s/([^#\s]\s+[$UK_LOW]+)(\s)/$1ться$2/;
	    }
	    else {
	        if ( $suffix_newbody =~ s/([$UK_LOW])$/$1ся/ ) { # для слів, які мають тільки "-ся"
		    $comment =~ s/([^#\s]\s+[$UK_LOW]+)(\s)/$1ся$2/;
	        }
	        else { # для слів, які не мали закінчень"
		    $suffix_newbody =~ s/0/ся/;
		    $comment =~ s/([^#\s]\s+[$UK_LOW]+)(\s)/$1ся$2/;
	        }
	    }
	
	    push(@lines, $LINE[0], " ", $sfx_rev, "   ", $suffix_oldbody, "\t", $suffix_newbody, "\t", $suffix_match, "\t\t#", $comment);
	    push(@lines, $LINE[0], " ", $sfx_rev, "   ", get_reversed($suffix_oldbody, $suffix_newbody, $suffix_match, $comment));

	    $line_count += 2;
    }

  }
     
}
	if( $line_count > 0 ) {
	    print "\n";
	    print $section_header, $line_count, "\n";
	
	    print @lines;
	}

# для слів що мають лише зворотню форму
# тобто для кожного напр. "вбити - вбитись ..." зробити додатково "вбитися - вбитись ..."
# suff_old, suff_new, suff_match, comment
sub get_reversed {
    my $suffix_oldbody = @_[0];
    my $suffix_newbody = @_[1];
    my $suffix_match = @_[2];
    my $comment = @_[3];
    
	if( $suffix_oldbody eq "0" ) {
	    $suffix_oldbody = "ся";
	}
	else {
	    $suffix_oldbody .= "ся";
	}
	$suffix_match .= "ся";
	$comment =~ s/^([\s]*[$UK_LOW]+ти)([\s]+)/$1ся$2/;
	
    return $suffix_oldbody . "\t" . $suffix_newbody . "\t" . $suffix_match . "\t\t#" . $comment;
}
