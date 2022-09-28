import requests
import colorama
import smtplib,sys,ctypes
import re
import os
import shutil
from colorama import Fore, Back, Style
from os import system
from bs4 import BeautifulSoup


colorama.init(autoreset=True)
cookie = {                                            #Get cookies from your browser and past it here.
	"ZHE" : "401dd88889fa1e6a532530b0f80db626",
	"PHPSESSID" : "h3n0g5pkhbbjpue5pde445st34"
}
system('mode con: cols=50 lines=70')                  #Set terminal size.
os.system('cls' if os.name == 'nt' else 'clear')      #Clear terminal.
columns = shutil.get_terminal_size().columns          #Resize terminal.
print(Fore.RED +"|==   Zone-H Grabber   ==|".center(columns))
notifiers=[]                                          #Create new list.
print('Grabbing notifiers from 1st 10 pages...'.center(columns))
for n in range(10):                                   #How many pages you want the script to grab the notifiers URLs from. Changer 10 to whatever you need, recomended: 10 to 30.
 usr = requests.get('https://zone-h.org/archive/published=0/page='+str(n+1), cookies=cookie).content
 if 'If you often get this captcha when gathering data' in usr.decode('utf-8'):
  input('Please verify captcha and hit Enter ...')
  usr = requests.get('https://zone-h.org/archive/published=0/page='+str(n+1), cookies=cookie).content
 soup = BeautifulSoup(usr, 'html.parser')
 links = soup.findAll('a')
 for i in range(len(links)):
  if '/archive/notifier=' in str(links[i]):
    vv=str(links[i]).replace('<a href="/archive/notifier=','')
    notif=''
    for j in range(len(vv)-1):
    	if not(vv[j]+vv[j+1]=='">'):
    		notif=notif+vv[j]
    	else:
    		break
    if notif not in notifiers :
    	notifiers.append(notif)
    	open('notifiers.txt','a+').write(notif+'\n')
print('Total notifiers grabbed : '+str(len(notifiers)))  #Prints how many notifiers has been grabbed.
urls=[]                                                  #Create new list.
notifiers = list(filter(lambda url: ".." not in url,notifiers))
for i in range(len(notifiers)):
 print(Fore.RED +"     Grabbing sites from : "+str(notifiers[i]))
 for j in range(10):                                     #How many page URLs to grab from each notifier. Changer 10 to whatever you need, recomended: 10 to 30.
  verif = requests.get('http://www.zone-h.org/archive/notifier='+str(notifiers[i])+'/page='+str(j+1), cookies=cookie).content
  if 'If you often get this captcha when gathering data' in verif.decode('utf-8'):
   input('Please verify captcha and hit Enter ...')
  verif = requests.get('http://www.zone-h.org/archive/notifier='+str(notifiers[i])+'/page='+str(j+1), cookies=cookie).content
  soup = BeautifulSoup(verif, 'html.parser')
  links=soup.findAll("td", {"class": "defacepages"})
  if os.name == 'nt':
    ctypes.windll.kernel32.SetConsoleTitleW("Total notifiers: ["+str(len(notifiers))+"]" + " Total grabbed URLs: ["+str(len(urls))+"]")
  if '<strong>0</strong>' in str(links[0]):
  	break
  else:
   verif=verif.decode('utf-8')
   bitisp = re.findall('<td>(.*)\n							</td>',verif)
   for oo in bitisp:
    newurl= str(oo.split('/')[0])                   #If you want to get URLs with Http or Https change current command with this: newurl= 'http://'+str(oo.split('/')[0])
    if newurl not in urls and ".." not in newurl :  #Remove invalid URLs that has 3 or 5 dots on it.
   	 urls.append(newurl)                            #Add ne URL to grabbed_zh.txt.
   	 open('grabbed_zh.txt','a+').write(newurl+'\n') #Opens txt file and write new URL.
   	 print(Back.GREEN + Fore.BLACK + "[+]" + Fore.WHITE + Back.BLACK + " " + newurl) 
