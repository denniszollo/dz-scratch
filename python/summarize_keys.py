#!/bin/python
import sys

assert len(sys.argv)==2
df = pd.read_csv(sys.argv[1], sep=',')
#print df
num_walley = len(df[df['product']=='wally']['dna'].drop_duplicates())
print "total number of keys generated by license server (Removing any duplicate generations)"
print "walley:{0}".format(num_walley)
num_sats = len(df[df['product']=='seattle']['dna'].drop_duplicates())
print "seattle:{1}".format(num_sats)
