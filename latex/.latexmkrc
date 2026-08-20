# Refuse to build the book if a figure contains the known delegation watermark.
my $figure_audit = system('python fig_helper.py audit');
die "Figure audit failed; book.pdf was not rebuilt.\n" if $figure_audit != 0;
