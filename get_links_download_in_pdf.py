import numpy as np
import pdfx, wget
import time, os, sys
import argparse

help_message = """ 

Search or download the refs as links in a pdf file.

example: 
(suppose you have Refs/PhysRevLett.122.067203.pdf)
python get_links_download_in_pdf.py --pdf="Refs/PhysRevLett.122.067203.pdf" --dwn=1 --dir="aspdf"
python get_links_download_in_pdf.py --pdf="Refs/PhysRevLett.122.067203.pdf" --dir="aspdf"

Developer : yuechangming8@gmail.com
Good Luck !

"""

if len(sys.argv)>1 and ( "help" in sys.argv[1] or "-h" in sys.argv[1] ) : print help_message

parser = argparse.ArgumentParser(description="")
parser.add_argument('--dir', help='directory, string', type=str, default = ".")
parser.add_argument('--dwn', help='download or not: 0, 1', type=int, default = 0)
parser.add_argument('--pdf', help='the pdf, absolute dir', type=str, default = "None")
args = parser.parse_args()
params=vars(args)

if params["pdf"] == "None": 
   print "pdf not given"
   sys.exit(0)

mdir=params["dir"]
if params["dir"] == "aspdf": 
   mdir=str(params["pdf"])+"_refs"

hdir="/Users/changmingyue/Documents/arXiv_papers/"
newdir = hdir+mdir
if not os.path.exists(newdir): os.system("mkdir " + newdir)

#pdf = pdfx.PDFx("PhysRevLett.122.067203.pdf")
#mdir="refs_prb_101_041104_NdNiO2_SC_spinfreezing"
#mdir="Refs"

pdf =  pdfx.PDFx(params["pdf"])
metadata = pdf.get_metadata()
references_list = pdf.get_references()
references_dict = pdf.get_references_as_dict()
urls=references_dict['url']
N=len(urls)


ff=open(newdir+"/failed.log","w")
for i in range(N):
   if params["dwn"]==0: 
      print "\n refs ", i+1, ", link ==> ", urls[i]
      print>>ff, i+1, "\n",  "refs, link ==> ", urls[i]

   elif  params["dwn"]==1:
       tm = 5.0*(1.0+np.random.random()) # in case of breaking law...
       print ". Now sleep ", tm, " secs";  time.sleep(tm)

       if "nature" in urls[i] or "nphys" in  urls[i]:  
           idx_g = urls[i].find('g')
           idx_j=urls[i].find('n')
           paper = urls[i][idx_j:]	 	     
           url="https://www.nature.com/articles/"+paper+".pdf" 
           print "\n downloading nat,   url ==> ", url
           print>>ff, "\n downloading nat,   url ==> ", url
       elif "srep" in urls[i] : 
           idx_g = urls[i].find('g')
           idx_j=urls[i].find('e')
           paper = urls[i][idx_j-2:]	 	     
           url="https://www.nature.com/articles/"+paper+".pdf" 
           print "\n downloading nat,   url ==> ", url
           print>>ff, "\n downloading nat,   url ==> ", url
       elif "JPSJ" in urls[i]:
           idx_g = urls[i].find('g')
           idx_j = urls[i].find('J')
           paper = urls[i][idx_j:]
           url="https://journals.jps.jp/doi/pdf" + urls[i][idx_g+1:idx_j-1]+ "/"+paper 
           print "\n downloading jps,   url ==> ", url
           print>>ff, "\n downloading jps,   url ==> ", url
       elif "annurev" in urls[i]:
           idx_g = urls[i].find('g')
           idx_j = urls[i].find('a')
           paper = urls[i][idx_j:]
           url="https://www.annualreviews.org/doi/pdf/" + urls[i][idx_g+1:idx_j-1]+ "/"+paper 
           print "\n downloading jps,   url ==> ", url
           print>>ff, "\n downloading jps,   url ==> ", url
       elif "RevModPhys" in urls[i]:
           idx_g = urls[i].find('g')
           idx_j=urls[i].find('R')
           jrn="rmp"
           paper = urls[i][idx_j:]	 	     
           url="https://journals.aps.org/"+jrn+"/pdf"+urls[i][idx_g+1:idx_j-1]+"/"+paper
           print "\n downloading aps,   url ==> ", url
           print>>ff, "\n downloading aps,   url ==> ", url
       elif "PhysRev" in urls[i] :
           idx_g = urls[i].find('g')
           idx_j=urls[i].find('P')
           jrn="pr"+urls[i][idx_j+7].lower()
           paper = urls[i][idx_j:]
           url="https://journals.aps.org/"+jrn+"/pdf"+urls[i][idx_g+1:idx_j-1]+"/"+paper
           print "\n downloading aps,   url ==> ", url
           print>>ff, "\n downloading aps,   url ==> ", url
       elif "10.1038" in urls[i] :  
           idx_g = urls[i].find('g')
           idx_j=urls[i].find('n')
           paper = urls[i][idx_g+9:] 	     
           url="https://www.nature.com/articles/"+paper+".pdf" 
           print "\n downloading nat,   url ==> ", url
           print>>ff, "\n downloading nat,   url ==> ", url
       else: 
           print "\n not support to download  ==> ", urls[i]
           print>>ff, "\n not support to download  ==> ", urls[i]
           continue

       try: 
           wget.download(url,newdir)

       except:
           print "\n failed to download ==> ", urls[i]
           print>>ff, "\n failed to download ==> ", urls[i]
           pass
ff.close()
