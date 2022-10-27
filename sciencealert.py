import csv
import pandas as pd
from bs4 import BeautifulSoup

filters = ["publishers_list","springer","umi","ebscohost","sciencedirect","emeraldinsight","sagepub","scopusnlai","intechopen","dart-europe","digitool","highwiredoaj",
"pnas","eprints.nottingham","digital.library.upenn.edu/books/","etd.ohiolink","escholarship","lib","ieeexplore","acm","wiley","sciencedirect",
"acs","aiaa","aip","ajpe","aps","ascelibrary","asm","asme","bioone","birpublications","bmj","emeraldinsight","geoscienceworld","icevirtuallibrary","informs","ingentaconnect",
"iop","jamanetwork","joponline","jstor","mitpressjournals","nrcresearchpress","oxfordjournals","royalsociety","rsc","rubberchemtechnol","sagepub","scientific","spiedigitallibrary","tandfonline","theiet",
"doi", "arxiv","eurekalert", "article", "journal","science", ".gov", ".org", "frontiersin"]
rejectfilters = ["thetimes","futurity", "news","press-release" ,"nytimes", "reuters", "magazine", "mevzuat", "gov.uk", "scientificamerican", "energy.gov", "wikipedia", "cdc.gov", "planalto.gov", "planetary.org", "/maps/"]
reject_count = 0
evidence_count = 0

with open("sciencealertarticles.csv") as file:
	reader = csv.reader(file, delimiter=',')
	header = next(reader)
	#,title,category,author,url,plaintext,html

	article_id = 0
	dictionary = []
	for row in reader:
		article_id += 1
		# remove linebreaks
		plain_text = row[5].replace("<linebreak>","")
		html = row[6]
		hrefs = []
		evidence = []


		soup = BeautifulSoup(html, "html.parser")
		#print(soup)

		for link in soup.find_all('a', href=True):
			hrefs.append(str(link.get('href')))
		

		# iterate thru all links and filter out the ones that has strings that could potentially be evidence
		for url in hrefs:
			for strs in filters:
				if strs in url:
					if url in evidence:
						break
					if "eurekalert" in url:
						evidence.append(url)
						continue
					if strs == "science":
						if "sciencealert" in url or "livescience" in url:
							reject_count+=1
							break
					else:
						for reject in rejectfilters:
							if reject in url or url[len(url)-5:] == ".org/" or url[0] == "/":
								reject_count+=1
								break
						else:
							evidence.append(url)
							evidence_count += 1

		eid = 0
		for url in evidence:
			eid+=1
			data = {
				'id': article_id,
	            'title': row[1],
	            'category': row[2],
	            'author': row[3],
	            'url': row[4],
	            'plaintext': plain_text,
	            'keep/filter': '  ',
	            'evidence_id': eid,
	            'evidence': url,
	        }

			dictionary.append(data)


print("total evidence: ", evidence_count)
print("total reject: ",reject_count)
df_articles = pd.DataFrame(dictionary)
df_articles.to_csv('evidencetofilter.csv', encoding='utf-8-sig')



