################################################################
# Script to resort cap3 alignment files
# Author: Huaqin Xu
# Created Date: 9/21/2007
# Latest Update: 9/25/2007
# Input: alignment file
# Output: sorted alignment file
################################################################

use strict;
no strict "vars";
use File::Basename;

#--------------varaibles--------------------

my $infile;
my $outfile;


$#ARGV >1 || die "Please provide the directory and extension of input alignment file name and output file";

$indir=$ARGV[0];
$inext=$ARGV[1];
$outdir=$ARGV[2];
if($ARGV[3]){
	$outext=$ARGV[3];
}else{
	$outext=$inext;
}
-d($indir) || die $indir."does not exist!\n";
if(!-d($outdir)){
	print $outdir."does not exist!\n";
	if(mkdir $outdir, 0755){
		print "Create direstory $outdir!\n";
	}else{
		die "Can not create $outdir!\n";
	}
}

@inlist = <$indir*.$inext>;

foreach $infile (@inlist){

	#--------------Read plate addresses from platefile------------------
	print "Reading ... ".$infile."\n";	
	if( ! -r $infile) { die "Can't read input $infile\n"};
	if( ! -f $infile) { die "$infile is not a plain file.\n"};	
	open(inDATA, "<$infile")||die "Can't open $infile $!";
	
	$name = basename($infile);
	$name = substr($name, 0, length($name)-length($inext)).$outext;
	$outfile = $outdir.$name;
	open(outDATA, ">$outfile") || die "Can't output $outfile $!";
	print "Writing ... ".$outfile."\n";		
	
	my $i = 0;
	my %align = ();
	
	while($line=<inDATA>)
	{
	#       print "$i ".substr($line, 0, 22)."\n";
		if($i < 2){
			print outDATA $line;
	
		}else{
			chomp($line);
			$id = substr($line, 0, 22);
			$seq = substr($line, 22, length($line)-22);
			if($id !~ /\s{22}/){
				$align{$id} = $seq;
			}else{
				foreach $key (sort {$align{$b} cmp $align{$a}} keys %align){
					print outDATA "$key$align{$key}\n";
				}
				print outDATA $line."\n";
				$i = 0;
			}
		}
		$i=$i+1;
	}
	
	close inDATA;
	close outDATA;	
}

#--------------- end of program ------------------