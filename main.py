from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
import random
from itertools import count
from kivy.core.clipboard import Clipboard
import numpy as np
from kivymd.app import MDApp
import secrets
import webbrowser as web

secGen = secrets.SystemRandom()
class RsaApp(ScreenManager):
#code to open a web browser
 def openWeb(self):
  web.open('https://github.com/Ojile93/RSA-APP')

#Copy to clipboard code
 def copy1(self,arg,args):
  btn = args
  target = arg
  try:
   tar = str(target)
   Clipboard.copy(tar)
   btn.disabled =True
   btn.text = "Sucessfully copied"
  except:
   btn.text = "Error! unable to copy"
   print("cant copy")

#Token generation page
 def keyPage(self,root):
  self.current = "keyPage"
  self.ids.cp1.disabled = False
  self.ids.cp1.text = "Click to copy Public key to clipboard"
  self.ids.cp2.disabled = False
  self.ids.cp2.text = "Click to copy Private key to clipboard"
  self.ids.cp3.disabled = False
  self.ids.cp3.text = "Click to copy totient to clipboard"
  def isPrime(num):
   if num<2:
    return False
   for x in range(2,num//2+1):
    if num%x ==0:
     return False
   return True
    
  primeAr =[]
  count1 = 0
  for x in range(243,832):
   count1+=1
   primes = isPrime(x)
   if primes ==True:
    primeAr.append(x)
    if len(primeAr) ==120 or count1 ==832-243:
     break
  arr1 =secGen.sample(primeAr,2)
  n1 = arr1[0]
  n2 = arr1[1]
  global n
  n = n1*n2
  tn = (n1-1)*(n2-1)
  count2 =0
  arr2 =[]
  for x in range(3,tn+1):
   count2+=1
   if tn%x !=0 and isPrime(x) ==True and x in range(1000,9000):
    arr2.append(x)
    if len(arr2)== 700 or count2 == tn-3:
     break
    else:
     pass
    
  pubkeys = secGen.choice(arr2)
  global pubKey
  pubKey = pubkeys
  arr3 = []
  for i in count():
   if (pubKey*i)%tn ==1 and i != pubKey:
    arr3.append(i)
    break
  global prvKey
  prvKey = arr3[0]
  self.n = n
  self.pubKey = pubKey
  self.prvKey = prvKey
  self.ids.pub.text = f"Public key generated is {self.pubKey}"
  self.ids.prv.text = f"Private key generated is {self.prvKey}"
  self.ids.tnkey.text = f"Totient generated is {n}"

#Encode page codes 
 def encodeMsg(self,root):
  btn = self.ids.cp4
  btn.disabled = False
  btn.text = "Click to copy"
  errMsg = self.ids.err
  puk = self.ids.pbk1.text
  tot = self.ids.totk.text
  msgEn = self.ids.msgEn.text
  if puk and tot and msgEn =="":
   errMsg.text="Enter valid RSA parameters"
  elif puk =="":
   errMsg.text = "Enter a valid public key"
  elif tot =="":
   errMsg.text = "Enter a valid Totient value"
  elif msgEn =="":
   errMsg.text ="Enter a valid message"
  else:
   try:
    puk = int(puk)
    tot =int(tot)
    asciCh=[ord(ch) for ch in msgEn]
    cipher = [np.mod(pow(ciph,puk),tot) for ciph in asciCh]
    msg1 =[]
    for x in cipher:
     y=str(x)
     msg1.append(y)
    msg = "".join(msg1)
    ciph = str(cipher)
    ciph1 = ciph.replace('[','')
    self.ciph2 = ciph1.replace(']','')
    self.ids.encryptMsg.text =f"{self.ciph2}"
    root.current= "encryptedMsgPage"
    self.ids.pbk1.text =""
    self.ids.totk.text =""
    self.ids.msgEn.text =""
    self.ids.err.text =""
   except ValueError:
    errMsg.text="public key or totient not in number"
  
#Decode page codes
 def decodeMsg(self,root):
  btn = self.ids.cp5
  btn.disabled = False
  btn.text = "Click to copy to clipboard"
  prk= self.ids.prk1.text
  msg3 = self.ids.msgDcr.text
  tot = self.ids.tot2.text
  errMsg2 =self.ids.err2
  if prk and msg3 and tot =="":
   errMsg2.text = "Invalid RSA parameters! Enter valid Parameters"
  elif msg3 =="":
   errMsg2.text ="No code to decode"
  elif prk =="":
   errMsg2.text="No private key entered"
  elif tot =="":
   errMsg2.text ="No Totient value entered"
  else:
   try:
    prk = int(prk)
    tot = int(tot)
    v1 = msg3.replace(",",'')
    vx = v1.replace('[','')
    vc = vx.replace(']','')
    v2 = vc.split()
    v3=[]
    for x in v2:
     y = int(x)
     v3.append(y)
    decrt = [np.mod(pow(msg,prk),tot) for msg in v3]
    frmAsci = [chr(c) for c in decrt]
    self.decrtMsg = "".join(frmAsci)
    self.ids.shwCrt.text=self.decrtMsg
    root.current = "ShowDecryptMsgPage"
    self.ids.prk1.text = ""
    self.ids.msgDcr.text =""
    self.ids.tot2.text =""
    self.ids.err2.text =""
   except ValueError:
    errMsg2.text ="Error! either your private key or totient or encoded message contain a non interger value, pls check and try once more"
class app(MDApp):
 def build(self):
  return RsaApp()

if __name__=="__main__":
 app().run()