#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests  
from bs4 import BeautifulSoup  
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd
import os
from selenium.webdriver.common.by import By
import time


# ### Funcion para lectura de la pagina

# In[2]:


def get_valores(tags):
    categ=''
    valor=''
    datos['marca']=marca
    datos['modelo']=modelo
    datos['pasajeros']=pasajeros
    datos['descripcion']=descrip
    datos['precio']=precio
    datos['preciodolar']=preciodolar
    
    for tag in tags:
      if tag.has_attr('class'):
        if tag['class'] == 'spec' or tag['class']==['spec']:
          valor=tag.text.strip()
        else:
          categ=tag.text.strip()

      if categ!='' and valor!='':
         datos[categ]=valor
         categ=''
         valor=''


# In[3]:


df=[]


# In[4]:


url = "https://crautos.com/autosusados/searchresults.cfm"
driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(url)
soup=BeautifulSoup(driver.page_source,'html.parser')
df = pd.DataFrame()


# In[ ]:


for pagina in range(1,720):
 print ("Pagina {}: ".format(pagina)) 
 text = "javascript:p({})".format(pagina)
 
 driver.execute_script(text)
 time.sleep(2)
    
 soup=BeautifulSoup(driver.page_source,'html.parser')
 anuncios = soup.find_all('div', class_ ='inventory')

 for anuncio in anuncios:
   datos = {}
   nombre=anuncio.find('div').text.split() #Descripcion

       
   datos['year']=nombre[0]
   try:
     pos=nombre.index('Pas.')  
     pasajeros=nombre[pos-1]
     descrip=nombre[1:pos-2]
     nombre=nombre[0:pos-2]
   except ValueError:
     pos=0
     pasajeros="0"
     descrip=nombre[1:]

   nombre=' '.join(nombre)
    
   dummy=nombre.split()[2]
   minuscula=False
   for char in dummy:
      if char.islower():
          minuscula=True
          break
   if minuscula:
      marca=nombre.split()[1:3]
      marca=' '.join(marca)
      modelo=' '.join(nombre.split()[3:])
   else:
      marca=nombre.split()[1]
      modelo=' '.join(nombre.split()[2:])

   #print("Marca: ",marca," Modelo: ",modelo)
    
   precio=""
   preciodolar=""
   p=anuncio.find('div',class_='pricetext')
   if p!=None:
    precio= anuncio.find('div',class_='pricetext').text
    precio = precio.replace('¢','')  
    precio = precio.replace(',','')  
     
   p=anuncio.find('div',class_='pricedollars')
   if p!=None:  
     preciodolar = anuncio.find('div',class_='pricedollars').text
     preciodolar = preciodolar.replace('$','')  
     preciodolar = preciodolar.replace(',','')
     preciodolar = preciodolar.replace('(','')  
     preciodolar = preciodolar.replace(')*','')
   
   #Revisar si precio en dolares y colones estan invertidos
   if len(precio)==0:  precio="0"
   if len(preciodolar)==0: preciodolar="0" 
   if precio[0]=='$':
    prc=preciodolar
    prd=precio
    precio=prc.replace("¢","")
    preciodolar=prd.replace("$","")

   tags = anuncio.find_all('td')           #Caracteristicas
   get_valores(tags)
   
   registro = pd.DataFrame([datos])
   df = pd.concat([df,registro])
   


# In[ ]:


df.to_csv("crautos.csv",index=False)
#nombre=anuncio.find('div').text.split() 


# In[ ]:


df.shape


# In[ ]:


precio="$1500"   
preciodolar="¢800000"
print("Precio Dolar: ",preciodolar)    
print("Precio Colon: ",precio, "\n")
    
if precio[0]=='$':
  prc=preciodolar
  prd=precio
  precio=prc.replace("¢","")
  preciodolar=prd.replace("$","")
    
print("Precio Dolar: ",preciodolar)    
print("Precio Colon: ",precio)


# In[ ]:


len(precio)



# In[ ]:




