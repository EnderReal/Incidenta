from datetime import date
import requests
import pdfplumber
import os
import msvcrt as m

print("Conectare...")

luni=["index","Ianuarie","Februarie","Martie","Aprilie","Mai","Iunie","Iulie","August","Noiembrie","Decembrie"]
zi_fin=[0,31,28,31,30,31,30,31,31,30,31,30,31]
today=date.today()
zi=today.strftime("%d")
luna=today.strftime("%m")
an=today.strftime("%Y")
data= zi+"."+luna+"."+an

link="http://dsp-galati.ro/images/stories/"+an+"/incidenta/"+luni[int(luna)]+"/INCIDENTA-JUDETUL-GALATI-"+data+".pdf"

get=requests.get(link)
if str(get) == "<Response [404]>":
	link=link[:-4]+"-1.pdf"
get=requests.get(link)
if str(get) == "<Response [200]>":
	print("A fost adaugata rata de infectare pentru", data)
elif str(get) == "<Response [404]>":
	print("Nu a fost adaugata o rata de infectare pentru data", data)
else:
	print("Eroare. Raspuns URL necunoscut.Response:",get)

ieri=0
luna_ieri=""
data_ieri=""
if int(zi)==1:
	ieri=zi_fin[int(luna)-1]
	luna_ieri=luni[int(luna)-1]
	if int(luna)-1 < 10:
		data_ieri=str(ieri)+".0"+str(int(luna)-1)+"."+an
	else:
		data_ieri=str(ieri)+str(int(luna)-1)+"."+an
else:
	if int(zi)-1<=9:
		ieri="0"+str(int(zi)-1)
	else:
		ieri=str(int(zi)-1)
	luna_ieri=luni[int(luna)]
	data_ieri=ieri+"."+luna+"."+an

link_ieri="http://dsp-galati.ro/images/stories/"+an+"/incidenta/"+luna_ieri+"/INCIDENTA-JUDETUL-GALATI-"+data_ieri+".pdf"

get=requests.get(link_ieri)
if str(get) == "<Response [200]>":
	if str(requests.get(link)) == "<Response [404]>":
		print("dar ", end='')
	print("exista o rata de infectare pentru ieri:", data_ieri)
else:
	link_ieri=link_ieri[:-4]+"-1.pdf"
	if str(requests.get(link_ieri)) == "<Response [200]>":
		if str(requests.get(link)) == "<Response [404]>":
			print("dar ", end='')
		print("exista o rata de infectare pentru ieri:", data_ieri)
if str(requests.get(link_ieri)) == "<Response [404]>":
	print("Nu a fost adaugata o rata de infectare pentru ieri", data_ieri)

if str(requests.get(link)) == "<Response [200]>" or str(requests.get(link_ieri)) == "<Response [200]>":
	print("\nObtinere informatii...\n")
else:
	print("\nNu au fost gasite fisiere corespunzatoare zilelor de azi si de ieri.\nEste posibil sa fie publicate intr-un format care nu este suportat la momentul actual.")

pdf_azi=""
if str(requests.get(link))=="<Response [200]>":
	try:
		comm='curl '+link+' -s '+' --output "aux_azi.pdf"'
		os.system(comm)
	except:
		with open('aux_azi.pdf', 'wb') as file:
			file.write(requests.get(link).content)
			f.close()
	with pdfplumber.open('aux_azi.pdf') as pdf:
		text=pdf.pages
		for i in range(0,len(pdf.pages)):
			pdf_azi+=text[i].extract_text()+"\n"
	os.remove('aux_azi.pdf')
	file=open('auz_clear.txt','wb')
	file.write(pdf_azi.encode("utf-8"))
	file.close()
	file=open('auz_clear.txt','r')
	lines=file.readlines()
	print("Incidenta COVID 19 in judetul Galati,", data ,"\n")
	for i in lines:
		if "TECUCI" in i:
			if i[-1] == "\n":
				i=i[:-1]
			print(i[0:17:],i[27::])
	for i in lines:
		if "DR" in i and "G" in i and "NE" in i and "TI" in i:
			if i[-1] == "\n":
				i=i[:-1]
			print("DRAGANESTI", i[20::])
	file.close()
	os.remove('auz_clear.txt')
	print("\n")

pdf_ieri=""
if str(requests.get(link_ieri))=="<Response [200]>":
	try:
		comm='curl '+link_ieri+' -s'+' --output "aux_ieri.pdf"'
		os.system(comm)
	except:
		with open('aux_ieri.pdf', 'wb') as file:
			file.write(requests.get(link_ieri).content)
			file.close()
	with pdfplumber.open('aux_ieri.pdf') as pdf:
		text=pdf.pages
		for i in range(0,len(pdf.pages)):
			pdf_ieri+=text[i].extract_text()+"\n"
	os.remove('aux_ieri.pdf')
	file=open('aux_clear.txt','wb')
	file.write(pdf_ieri.encode("utf-8"))
	file.close()
	file=open('aux_clear.txt','r')
	lines=file.readlines()
	print("Incidenta COVID 19 in judetul Galati,", data_ieri, "\n")
	for i in lines:
		if "TECUCI" in i:
			if i[-1] == "\n":
				i=i[:-1]
			print(i[0:17:],i[27::])
	for i in lines:
		if "DR" in i and "G" in i and "NE" in i and "TI" in i:
			if i[-1] == "\n":
				i=i[:-1]
			print("DRAGANESTI", i[20::])
	file.close()
	os.remove('aux_clear.txt')


print("\n")
print("Press any key to continue...")
m.getch()