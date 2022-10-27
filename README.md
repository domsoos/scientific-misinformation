# Scientific Misinformation
In this work we would like to expand the dataset from the previously curated 100 papers in the [related work](https://arxiv.org/abs/2205.00126). 

The goal of this task is to build a corpus from ScienceAlert articles. We have automated the extraction of a sample of 500 scientific articles. The next steps are to manually verify the evidence links.

# The task at hand
The annotator will be provided with the file that contains the 500 articles with about 1938 evidence URL's. Each row in the .csv file has the URL of the ScienceAlert article along with the content of the article and an evidence link that either support/refute/neutral. For these measure we will be using an extra field next to the evidence link to manually verify the article. To mark if an evidence article support/refute/neutral mark it with 1/0/-1 respectively. 
