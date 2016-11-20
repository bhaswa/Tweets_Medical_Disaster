# Basic data cleaning
import nltk
import pandas as pd 
import numpy
import HTMLParser
import re

file=pd.read_csv("2014_ebola_virus.csv")
file=file.rename(columns={'Unnamed: 4':'Clean_message','Unnamed: 5':'Tagged_message'})
file['Message']=file['Message'].astype(str)
file['Clean_message']=file['Clean_message'].astype(str)
file.Clean_message=file.Message
clean_message=file.Clean_message
#handling all the encoded symbols that are present in text
for i in range(file['Message'].shape[0]):
	clean_message[i]=clean_message[i].decode("utf8").encode('ascii','ignore')

#escaping html characters. eg: &amp;-> &
html_parser = HTMLParser.HTMLParser()
for i in range(file['Message'].shape[0]):
	clean_message[i] = html_parser.unescape(clean_message[i])

#removing URL's
for i in range(file['Message'].shape[0]):
	clean_message[i] = re.sub(r"http\S+", "", clean_message[i])

#removing RT(re-tweet) from every message
for i in range(file['Message'].shape[0]):
	clean_message[i]=re.sub(r'RT','',clean_message[i])
#removing @
for i in range(file['Message'].shape[0]):
 	clean_message[i]=re.sub("(@[A-Za-z0-9:]+)|(@[A-Za-z0-9]+)",'',clean_message[i])


for i in range(file['Message'].shape[0]):
	file.ix[i,'Tagged_message']=nltk.word_tokenize(file.ix[i,'Clean_message'])
	file.ix[i,'Tagged_message']=nltk.pos_tag(file.ix[i,'Tagged_message'])

file.to_csv('ebola.csv')
###################################################################################
#Extraction of medical dictionary
import requests
import bs4
import pandas as pd
name=[]
meaning=[]
t=[]
root_url = 'http://www.medicinenet.com'
le=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
for l in le:
	while True:
		try:
			response=requests.get('http://www.medicinenet.com/symptoms_and_signs/alpha_'+l+'.htm')
			break
		except: print("REQUEST ERROR!")
	soup = bs4.BeautifulSoup(response.text)
	links = [a.attrs.get('href') for a in soup.select('div.AZ_results a[href^=/script]')]
	
	for i in range(len(links)):
		print("ALPHA: %s, %d/%d"%(l,i,len(links)))
		while True:
			try:
				response = requests.get(root_url + links[i])
				break
			except: print("REQUEST ERROR!")
		soup = bs4.BeautifulSoup(response.text)
		if soup.find('div', attrs={'class':'aia_content_fmt'}):
			n=soup.find('div', attrs={'class':'aia_content_fmt'}).ul.text
			n=n.encode('utf-8')
			n=n.split(' ')
			for i in range(len(n)):
				t.append(n[i])
		
#####################################################################################


dic=pd.read_csv('Medical_Dic.csv')
for i in range(dic.shape[0]):
	dic.ix[i,'Symptoms']=re.sub("\n",'',dic.ix[i,'Symptoms'])#removing \n


new_dic=set(dic.Symptoms)
new_dic=list(new_dic)

list=['Or','And','In','Of','On','The','With','']
for i in list:
	new_dic.remove(i)




new=[]
for each in new_dic:
	for j in range(len(each)):
		if (each[j].isupper()) and (j!=0):
			new_1=each[0:j]
			new_2=each[j:len(each)]
			new.append(new_1)
			new.append(new_2)

for each in new:
	if each not in new_dic:
		new_dic.append(each)


new1=[]
for each in new_dic:
	for j in range(len(each)):
		if (each[j].isupper()) and (j!=0):
			new_1=each[0:j]
			new_2=each[j:len(each)]
			new1.append(new_1)
			new1.append(new_2)


for each in new1:
	if each not in new_dic:
		new_dic.append(each)
ebola= ['Fever', 'headache','Muscle pain','Weakness','Fatigue','Diarrhea','Vomiting','Abdominal', 'stomach pain']
for each in ebola:
	if each not in new_dic:
		new_dic.append(each)


mers=['Cough','Breathing difficulties','Chills','Chest pain','Body aches','Sore throat','Headache','Diarrhea','Nausea','Vomiting','Runny nose','Renal failure','Pneumonia']
for each in mers:
	if each not in new_dic:
		new_dic.append(each)

dic=pd.read_csv('nov_dic.csv')
ebola=pd.read_csv('ebola.csv')
mers=pd.read_csv('mers.csv')

for i in range(dic.shape[0]):
	dic.ix[i,'Symptoms']=dic.ix[i,'Symptoms'].lower()

for i in range(len(dic)):
	count=0
	for each in ebola['Clean_message']:
	    count=count+each.count(dic.ix[i,'Symptoms'])
	dic.ix[i,'Count']=count

sorted=dic.sort('Count',ascending=0)
sorted.to_csv('dic_count.csv',index=False)
sorted=sorted.loc[sorted.count!=0]

#e= ['Fever', 'headache','Muscle pain','Weakness','Fatigue','Diarrhea','Vomiting','Abdominal', 'stomach pain']

ebola_word_count=['Joint Pain','Muscle Pain','headache','Fever','Diarrhea','Pneumonia','Stomach pain','Rash','Weakness','Sore throat','Nausea','Chest pain','Vomiting','Discharge']

mers['Clean_message']=mers['Clean_message'].astype('string')
for i in range(len(dic)):
	count=0
	for each in mers['Clean_message']:
		count=count+each.count(dic.ix[i,'Symptoms'])
	dic.ix[i,'Count']=count

sorted=dic.sort('Count',ascending=0)
sorted.to_csv('dic_count.csv',index=False)
sorted=sorted.loc[sorted.count!=0]



hospitals=[]
for i in range(train.shape[0]):
	a=nltk.word_tokenize(train.ix[i,'Clean_message'])
	for j in range(len(a)):
		if a[j]=='Hospital': 
			hospitals.append(a[j-2]+" "+a[j-1]+" "+a[j])

hospitals_m=[]
for i in range(train_m.shape[0]):
	a=nltk.word_tokenize(train_m.ix[i,'Clean_message'])
	for j in range(len(a)):
		if a[j]=='Hospital': 
			hospitals_m.append(a[j-2]+" "+a[j-1]+" "+a[j])


modes=[]
for i in range(train.shape[0]):
	a=nltk.word_tokenize(train.ix[i,'Clean_message'])
	for j in range(len(a)):
		if a[j]=='transmit' or a[j]=='transmitted': 
			modes.append(a[j-3]+" "+a[j-2]+" "+a[j-1]+" "+a[j]+" "+a[j+1]+" "+a[j+2]+" "+a[j+3])

