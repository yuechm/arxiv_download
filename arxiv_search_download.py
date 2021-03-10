import numpy as np
import time, os, sys
import argparse
import wget
import arxiv

### pip install arxiv

help_message= """
													
Search or download the arXiv or even aps papers!
													
Usage-1, find someone's paper (cat can be str-el, mtrl-sci, supr-con or all), eg:
python arxiv_search_download.py --aut="Piers Coleman" --num=50 --cat=all
													
Usage-2A, find some topic, eg:
python arxiv_search_download.py --key="machine learning" --num=50 --cat=all

Usage-2B, find some topic, and shown abstrct, eg:
python arxiv_search_download.py --key="machine learning" --num=50 --cat=all --abs=1 
													
Usage-3, find someone's paper and download to your directory, eg:
python arxiv_search_download.py --dir="ImpuritySolver" --key="Impurity Solver" --cat=all  --num=50 --dwn=1
													
Usage-4, get the latest papers (and even download it!), just run
python arxiv_search_download.py --num=10
python arxiv_search_download.py --num=10 --dwn=1 --dir="new" 
													
For more details, please refer to 
https://arxiv.org/help/api/user-manual or https://github.com/lukasschwab/arxiv.py

Developer : yuechangming8@gmail.com, based on arxiv interfaces.
													
Good Luck !
	
"""
if len(sys.argv)>1 and ( "help" in sys.argv[1] or "-h" in sys.argv[1] ) : print help_message

parser = argparse.ArgumentParser(description="")
parser.add_argument('--dir', help='directory, string', type=str, default = "new")
parser.add_argument('--key',  help='key words, string', type=str, default = ".")
parser.add_argument('--cat',  help='category, string : str-el, mtrl-sci, supr-con : string', type=str, default = "str-el")
parser.add_argument('--aut',  help='authors, string', type=str, default = ".")
parser.add_argument('--num',  help='number of articles, int', type=int, default = "50")
parser.add_argument('--dwn',  help='download or not: 0, 1', type=int, default = 0)
parser.add_argument('--abs',  help='show abstract or not: 0, 1', type=int, default = 0)
parser.add_argument('--srt',  help='sort by: relevance, submittedDate, or lastUpdatedDate ', type=str, default = "submittedDate")
parser.add_argument('--doi',  help='doi, string', type=str, default = ".")

args = parser.parse_args()
params=vars(args)

hdir="/Users/changmingyue/Documents/arXiv_papers/"
if not os.path.exists(hdir): os.system("mkdir " + hdir)
newdir=hdir+params["dir"]
if not os.path.exists(newdir): os.system("mkdir " + newdir)

if params["cat"]=="all": 
    catg=["cond-mat.mes-hall","cond-mat.str-el","cond-mat.supr-con","cond-mat.mtrl-sci"]
else:
    catg=["cond-mat."+params["cat"]]

for icat in range(len(catg)):
   myquery="au:"+params["aut"] + " AND " + params["key"] + " AND cat:" + catg[icat]
   # R=arxiv.query(myquery, max_results=params["num"],sort_order="ascending", sort_by=params["srt"])
   R=arxiv.query(myquery, max_results=params["num"],sort_order="descending", sort_by=params["srt"])
   
   print
   print "Your query for arxiv : ", myquery
   print
 
   for i in range(len(R)):
       mydoi=str(R[i].doi)
       print "\n # ", i+1, " doi: ", mydoi
       if not params["dwn"]:
           print " title : ", R[i].title.encode("utf-8")
           if not mydoi=="None":  print "   doi : ", mydoi
           if not R[i].journal_reference=="None": print R[i].journal_reference
           aus = ""; a = R[i].authors; 
           for j in range(len(a)): aus=aus + " " + a[j] + ","
           if len(a)>5: aus= a[0] + ", " + a[1] + ", " + a[2] + ", ... , " + a[-2] + ", " + a[-1]
           print "authors: ", aus.encode("utf-8")
           print "  time : ", R[i].updated
           if params["abs"]: print "  abs  : ", R[i].summary.encode("utf-8")
           print 
       else:
           larxv = 0
           if "JPSJ" in mydoi:
               url="https://journals.jps.jp/doi/pdf/" + mydoi
               print "\n downloading jps,   url ==> ", url
           elif "annurev" in mydoi:
               url="https://www.annualreviews.org/doi/pdf/" + mydoi 
               print "\n downloading jps,   url ==> ", url
           elif "RevModPhys" in mydoi:
               jrn="rmp"
               url="https://journals.aps.org/"+jrn+"/pdf/"+mydoi
               print "\n downloading aps,   url ==> ", url
           elif "PhysRev" in mydoi :
               idx_j=mydoi.find('P')
               for jj in range(idx_j,len(mydoi)): 
                   if mydoi[jj]==".": break

	       jrn="pr"+mydoi[idx_j+7:jj].lower()
	       if mydoi[idx_j+7]=="L": jrn="pr"+mydoi[idx_j+7].lower()
               url="https://journals.aps.org/"+jrn+"/pdf/"+mydoi
               print "\n downloading aps,   url ==> ", url
           elif "10.1038" in mydoi :  
               paper=mydoi[8:]
               url="https://www.nature.com/articles/"+paper+".pdf" 
               print "\n downloading nat,   url ==> ", url
           else:
               larxv = 1

           try: 
               if larxv==1: 
                   print "\n downloading axv, title ==> ", R[i].title.encode("utf-8")
                   arxiv.download(R[i],newdir)
                   tm = 5.0*(1.0+np.random.random()) # in case of breaking law...
                   print ". Now sleep ", tm, " secs";  time.sleep(tm)
               else:
                   wget.download(url,newdir)
                   tm = 5.0*(1.0+np.random.random()) # in case of breaking law...
                   print ". Now sleep ", tm, " secs";  time.sleep(tm)
           except:
               print "\n failed to download ==> ", mydoi
               pass
   print

