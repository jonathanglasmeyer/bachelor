#! /usr/bin/perl

use strict;
use warnings;

# Getting command line arguments:
use Getopt::Long;
# Documentation:
use Pod::Usage;
# I/O Handler
use IO::Handle;

use locale;
use POSIX qw(locale_h);
setlocale(LC_ALL,"");

use FindBin;
use lib "$FindBin::Bin";

require 'english-utils.pl';

## Create a list of words and their frequencies from an input corpus document
## (format: plain text, words separated by spaces, no sentence separators)

## TODO should words with hyphens be expanded? (e.g. three-dimensional)

my $stats;
my $cutoff;

# Command line arguments
GetOptions( 'stats|s=i'           => \$stats,
    'cutoff|c=i'           => \$cutoff
    ) || pod2usage(2);

my %dict;
my $min_len = 3;
my $min_freq = 1;

my $linecount = 0;

if (defined($stats)) {
    # print "Outputting line/vocab stats: $stats\n";
}

while (<>) {

    $linecount++;

    chomp($_);
    my @words = split(" ", $_);

    foreach my $word (@words) {

        # Check validity against regexp and acceptable use of apostrophe

        if ((length($word) >= $min_len) && ($word =~ /^[A-Z][A-Z\'-]+$/) && (index($word,"'") < 0 || allow_apostrophe($word))) {
            $dict{$word}++;
        }
    }

    if (defined($stats) && ($linecount % $stats == 0)) {
        my $vocab = keys(%dict);
        if (defined($cutoff)) {
            my $atcutoff = count_cutoff($cutoff);
            print "$linecount\t$vocab\t$atcutoff\n";
        } else {
            print "$linecount\t$vocab\n";
        }
    }    
}

# Output words which occur with the $min_freq or more often

if (!defined($stats)) {

    foreach my $dictword (keys %dict) {
      if ( $dict{$dictword} >= $min_freq ) {
        print $dictword . "\t" . $dict{$dictword} . "\n";
      }
    }

}


sub count_cutoff($) {

    my $cutoff = shift;
    my $count = 0;
    
    foreach my $dictword (keys %dict) {
        if ( $dict{$dictword} >= $cutoff ) {
            $count++;
        }
    }

    return $count;
}
