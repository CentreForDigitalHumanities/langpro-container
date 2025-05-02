#!/usr/bin/perl
use warnings;
use strict;
use diagnostics;
use feature 'say';
use LWP::Simple;
use CGI;
use CGI::Carp 'fatalsToBrowser'; # sends compilation errors to the browser window
use Switch;
use POSIX qw(strftime);
use Capture::Tiny ':all'; # capture `exe' errors


my ($sentence) = @ARGV;

say "<OUT>\n".&sen_to_ccg_by_offline_easyCCG($sentence)."\n</OUT>";

sub sen_to_ccg_by_offline_easyCCG {
	($_) = @_; 
	my $candc_bin = "../candc/rebank_dist_32/bin";
	my $candc_model = "../candc/models";
	my $candc_pos_ner = "$candc_bin/pos -model $candc_model/pos | $candc_bin/ner -model $candc_model/ner -ofmt \"%w|%p|%n \n\""; 
	my $easy = "java -jar easyccg-lemma/easyccg.jar --model model -i POSandNERtagged -o prolog -r S[dcl]"; 
	my $perl = "perl prolog_to_boxer.perl";   
	my $easyCCG_out = `echo "$_" | $candc_pos_ner | $easy | $perl`;
	return $easyCCG_out;
	#my $assert = &assertz_prolog_clauses($easyCCG_out);
	#my $ccg_pl = `swipl -f prologCCG_to_boxerCCG.pl -t "$assert, prolog_to_boxer_stdout, halt."`;  
	#return $ccg_pl; 
}


sub assertz_prolog_clauses {
	($_) = @_;
	my @clauses = ($_ =~ m&((?:sen_id|ccg|w)\(.+?\))\.&sg);
	@clauses = map {"assertz($_)"} @clauses;
	my $asserts = join(", ", @clauses);
	#say "<pre>$asserts</pre>";
	return $asserts;
}