#!/usr/bin/perl
use warnings;
use strict;
use diagnostics;
use feature 'say';
#use Cwd;

# symbols for categories
my $cat_sym = qr#\\/:\w\)\(#;

print ":- op(601, xfx, (/)).\n";
print ":- op(601, xfx, (\\)).\n";
#print ":- multifile ccg/2, w/8.\n";
print ":- discontiguous ccg/2, w/8.\n\n";


my $text = join '', <>;
my @trees = ($text =~ m&ccg\(.+?w\(.+?\)\.\n\n&sg);
my $id = 0;
my $sid = 0; #sub id

# for enumarating multi parse trees
#foreach my $tr (@trees) {
#	$tr =~ m&ccg\((\d+),&;
#	if ($id == $1) { $sid++	} else { $id = $1; $sid = 1}
#	# replacing ccg, w, lf - id pairs with structired id
#	$tr =~ s/\b(ccg|w|lf)\(${id},/$1\(${id}:${sid},/g;   
#}


#foreach (0..20) { print $trees[$_] }


#sub comment {
foreach (@trees){
	#replace [features] by :features
	s/\[([a-zA-Z]+)\]/:$1/g; 

    #o 'clock -> '\'clock
	s/, *''/,'\\'/g; 

	s/'([${cat_sym}]+)'([).,]+)\n/lc($1).$2."\n"/ge; 
	#e interprets replace-expression as a Perl code and evaluates it
	s/lex\('([${cat_sym}]+)'/"lx\(".lc($1)/ge; 
	s/:x/:_/g; 
	# fixes fx to bx and vice versa, since this comes from EasyCCG
	#s/(fx|bx)\(/if($1 eq "fx"){"bx("}else{"fx("}/ge; # remains in easyccg 0.2 but not in lemma version
	s/''s'/'\\'s'/g;
	print;
}
#}



