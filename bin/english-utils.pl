## English language utilities for text processing

## Check whether the apostrophe placement follows English rules

sub allow_word ($)
{
 my $word = shift;

 return ($word =~ /^[A-Z][A-Z\'-]+$/) && (index($word,"'") < 0 || allow_apostrophe($word));

}

sub allow_apostrophe ($)
{
  my $word = shift;
  my $ok = 0;

	# Possessive singular (e.g. baron's)
	if ($word =~ /[A-Z-]+'S$/) {
		$ok = 1;
	}

	# Names (e.g. O'Reilly)
	if ($word =~ /^O'/) {
		$ok = 1;
	}

	# Contraction with will (e.g. I'll, we'll, they'll)
	if ($word =~ /'LL$/) {
		$ok = 1;
	}

	# Contraction with have (e.g. they've, I've, you've)
	if ($word =~ /'VE$/) {
		$ok = 1;
	}

	# Possessive plural (e.g. barons')
	if ($word =~ /S'$/) {
		$ok = 1;
	}

	# Colloquial omitted G (e.g. rainin')
	if ($word =~ /N'$/) {
		$ok = 1;
	}

	# Contraction with not (e.g. won't, shan't, can't)
	if ($word =~ /N'T$/) {
		$ok = 1;
	}

	# Contraction with would (e.g. I'd, he'd, they'd)
	if ($word =~ /'D$/) {
		$ok = 1;
	}

	# Contraction with are (e.g. we're, they're)
	if ($word =~ /'RE$/) {
		$ok = 1;
	}

	# Names (e.g. D'Oliveira)
	if ($word =~ /^D'/) {
		$ok = 1;
	}

	# Contraction of I am = I'm
 	if ($word eq "I'M") {
		$ok = 1;
	}

  return $ok;

}

1;

