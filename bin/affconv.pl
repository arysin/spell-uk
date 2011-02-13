#! /usr/bin/perl -w

# Converts aspell affixes to ispell format

use strict;
use locale;
use utf8;
use encoding 'utf8';

my (%pfx, %sfx);

my $inside = 0;
my $num = 0;

while (my $line = <STDIN>) { 
	chomp $line;
	next if (!($line =~ /^PFX .*/ || $line =~ /^SFX .*/));
	if ($inside) {
		my ($aff, $name, $from, $to, $cond, $other) = split /[ \t]+/, $line;
		my $newcond = ($cond ne '.') ? $cond : '.';
		$newcond =~ s/(\[[^]]*\]|.)/$1 /g;
		my $newfrom = ($from ne '0') ? "-$from," : '';
		my $newto = ($to ne '0') ? $to : '-';
		
		my $translated = "    $newcond\t>\t$newfrom$newto";
		if ($aff eq "SFX") {
			push @{$sfx{$name}}, $translated;
		}
		else {
			push @{$pfx{$name}}, $translated;
		}
		$inside = 0 if (!--$num);
	}
	else {
		my ($aff, $name, $flag, $count) = split /[ \t]+/,$line;
		my $translated = "flag ".(($flag eq "Y")?"*":"")."$name:";
		if ($aff eq "SFX") {
			$sfx{$name}  = [($translated)];
		}
		else {
			$pfx{$name} = [($translated)];
		}
		$inside = 1;
		$num = $count;
	}
}

print "prefixes\n\n";
foreach my $name (keys %pfx) {
	foreach my $line (@{$pfx{$name}}) {
		print "$line\n";
	}
	print "\n";
}

print "suffixes\n\n";
foreach my $name (keys %sfx) {
	foreach my $line (@{$sfx{$name}}) {
		print "$line\n";
	}
	print "\n";
}
