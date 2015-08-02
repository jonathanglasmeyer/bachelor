#!/usr/bin/perl -w -CS

use feature 'unicode_strings';

binmode( STDIN,  ':utf8' );
binmode( STDOUT, ':utf8' );

## Condition plain text English sentences or word lists into a form suitable for constructing a vocabulary and language model

while (<STDIN>) {

  # Remove starting and trailing tags (e.g. <s>)
  # s/\<[a-z\/]+\>//g;

  # Remove ellipses 
  s/\.\.\./ /g;

  # Remove unicode 2500 (hex E2 94 80) used as something like an m-dash between words
  # Unicode 2026 (horizontal ellipsis)
  # Unicode 2013 and 2014 (m- and n-dash)
  s/[\x{2500}\x{2026}\x{2013}\x{2014}]/ /g;

  # Remove dashes surrounded by spaces (e.g. phrase - phrase)
  s/\s-+\s/ /g;

  # Remove dashes between words with no spaces (e.g. word--word)
  s/([A-Za-z0-9])\-\-([A-Za-z0-9])/$1 $2/g;

  # Remove dash at a word end (e.g. three- to five-year)
  s/(\w)-\s/$1 /g;

  # Remove some punctuation
  s/([\"\Ó,;:%¿?¡!()\[\]{}<>_\.])/ /g;

  # Remove quotes
  s/[\p{Initial_Punctuation}\p{Final_Punctuation}]/ /g;

  # Remove trailing space
  s/ $//;

  # Remove double single-quotes 
  s/'' / /g;
  s/ ''/ /g;

  # Replace accented e with normal e for consistency with the CMU pronunciation dictionary
  s/é/e/g;

  # Remove single quotes used as quotation marks (e.g. some 'phrase in quotes')
  s/\s'([\w\s]+[\w])'\s/ $1 /g;

  # Remove double spaces
  s/\s+/ /g;

  # Remove leading space
  s/^\s+//;

  chomp($_);

  print uc($_) . "\n";
#  print uc($_) . " ";
} print "\n"; 
