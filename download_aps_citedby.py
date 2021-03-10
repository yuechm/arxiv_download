from bs4 import BeautifulSoup
import urllib2
import re,sys
import requests
import webbrowser
import numpy as np
import time, os, sys
import argparse
import wget
import arxiv

help_message= """

Search or download the citing papers for an aps cite-by link
													
Developer : changming.yue@unifr.ch, based on arxiv interfaces.
usage:
python download_aps_citedby.py --url="https://journals.aps.org/prl/cited-by/10.1103/PhysRevLett.123.090605" --dir="prl_123090605"
Good Luck !
	
"""
if len(sys.argv)<3 or ( "help" in sys.argv[1] or "-h" in sys.argv[1] ) : print help_message
if len(sys.argv)<3: sys.exit()

parser = argparse.ArgumentParser(description="")
parser.add_argument('--dir', help='directory, string', type=str, default = "new")
parser.add_argument('--url', help='url, string', type=str, default = "")
parser.add_argument('--dwn',  help='download or not: 0, 1', type=int, default = 1)

args = parser.parse_args()
params=vars(args)

newdir=os.getcwd()

url=params["url"]
html_page = urllib2.urlopen(url)
soup = BeautifulSoup(html_page,features="html.parser")

for link in soup.findAll('a', attrs={'href': re.compile("^https://doi.org/")}):
    doi_link=link.get('href')
    mydoi=doi_link[16:]
    url=""
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

    # fail to download the pdf by wget
    elif "10.1116" in mydoi :
        res=requests.get(doi_link)
        mylink=res.url
        mylink="https://avs.scitation.org/doi/pdf/"+mydoi
        #url=mylink
        print "\n open a link from avs.sci,  mylink ==> ==> ", mylink
        webbrowser.open(mylink); time.sleep(5.0) 
    elif "10.1063" in mydoi :
        res=requests.get(doi_link)
        mylink=res.url
        mylink="https://aip.scitation.org/doi/pdf/"+mydoi
        #url=mylink
        print "\n open a link from aip.sci,  mylink ==> ==> ", mylink
        webbrowser.open(mylink); time.sleep(5.0) 
    elif "10.1088" in mydoi :
        paper=mydoi[8:]
        mylink="https://iopscience.iop.org/article/10.1088/"+paper+"/pdf"
        #url=mylink
        print "\n open a link from iopscience,  mylink ==> ", mylink
        webbrowser.open(mylink); time.sleep(5.0) 
    elif "10.22331" in mydoi : 
        paper=mydoi[8:]
        mylink="https://quantum-journal.org/papers/"+paper+"/pdf"
        #url=mylink
        print "\n open a link from quan-jour,  mylink ==> ", mylink
        webbrowser.open(mylink); time.sleep(5.0)  
    elif "10.1080" in mydoi :
        res=requests.get(doi_link)
        mylink=res.url
        mylink="https://www.tandfonline.com/doi/pdf/"+mylink[37:]+"?needAccess=true"
        #url=mylink
        print "\n open a link from tandf,  mylink ==>", mylink
        webbrowser.open(mylink); time.sleep(5.0) 
    elif "10.1109" in mydoi :
        res=requests.get(doi_link)
        mylink=res.url
        mylink="https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber="+mylink[37:len(mylink)-1]
        #url=mylink
        print "\n open a link from quan-jour,  mylink ==>", mylink
        webbrowser.open(mylink); time.sleep(5.0) 

    else:
        print "unable to find pdf link of ", doi_link
        try: 
            res=requests.get(doi_link)
            mylink=res.url
            print "redirect to ", mylink,"\n open the redirected link ... \n"
            webbrowser.open(mylink); time.sleep(5.0) 
        except:
            print "redirect failed \n "

    if len(url)>4:
        fn=wget.filename_from_url(url)
        if "pdf" not in fn: 
           fn=fn+".pdf"
        elif "pdf"==fn: 
           fn=(mydoi.replace("/","_"))+".pdf" 
        if os.path.exists(fn): 
           print fn, "existed"
        else: 
           try:
              if params["dwn"]: 
                 print "downloading", url
                 #fn_new=wget.download(url,newdir)
                 #wget.download(url,newdir)
                 #os.system("mv "+fn_new+" " + fn)
                 r=requests.get(url)
                 open(fn, 'wb').write(r.content)
                 tm = 3.0*(1.0+np.random.random()) # in case of breaking law...
                 print "Now sleep ", tm, " secs";  time.sleep(tm)
           except:
              print " fail to download ", url

