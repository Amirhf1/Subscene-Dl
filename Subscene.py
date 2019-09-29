# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 12:28:28 2019

@author: Matin Baloochestani

Website : MatinB.ir
Instagram : Matin.Baloochestani
Twitter : Matin__B
"""
import requests
from os import remove
from zipfile import ZipFile
from bs4 import BeautifulSoup

movieName = str(input('Enter Movie Name [Example: Avengers Endgame]: ')).replace(' ', '+')
movieEncode = str(input('Enter Movie Encode [Example: BluRay]: '))
movieResolution = str(input('Enter Movie Resolution [Example: 1080p]: '))

baseUrl = 'https://subscene.com'
searchUrl = baseUrl + f'/subtitles/searchbytitle?query={movieName}'
searchPage = requests.get(searchUrl)
soup = BeautifulSoup(searchPage.content, 'html.parser')

searchFound0 = soup.find_all('div', {'class' : 'title'})[0].find('a')
searchFound1 = soup.find_all('div', {'class' : 'title'})[1].find('a')
searchFound2 = soup.find_all('div', {'class' : 'title'})[2].find('a')
movieName = movieName.replace('+', ' ')
print(f'\nYou searched for {movieName}\n')
print(f'1. {searchFound0.text}\n2. {searchFound1.text}\n3. {searchFound2.text}')
userSelection = str(input('Please Select: '))
if userSelection == '1' :
    movieUrl = baseUrl + soup.find_all('div', {'class' : 'title'})[0].find('a')['href'] + '/farsi_persian'
elif userSelection == '2' :
    movieUrl = baseUrl + soup.find_all('div', {'class' : 'title'})[1].find('a')['href'] + '/farsi_persian'
elif userSelection == '3' :
    movieUrl = baseUrl + soup.find_all('div', {'class' : 'title'})[2].find('a')['href'] + '/farsi_persian'
else :
    print('Error !')
    exit(0)
# print(movieUrl)
moviePage = requests.get(movieUrl)
soup = BeautifulSoup(moviePage.content, 'html.parser')
subs = soup.find_all("td", class_ = "a1")

counter = 0
subCounter = 1
for item in subs:
    subsText = item.find('span', {'class' : None})
    if movieEncode and movieResolution in subsText.text.strip() :
        subsLink = baseUrl + item.find('a')['href']
        # print(subsLink)
        subtitlePage = requests.get(subsLink)
        soup = BeautifulSoup(subtitlePage.content, 'html.parser')
        # movieFullName = soup.find('span', {'itemprop' : 'name'}).text.strip()
        downloadUrl = baseUrl + soup.find('a', {'id' : 'downloadButton'})['href']
        downloadLink = requests.get(downloadUrl).content
        subtitleName = f'Subtitle{subCounter}.zip'
        with open(subtitleName, 'wb') as f :
            f.write(downloadLink)
        zip = ZipFile(subtitleName)
        zip.extractall(f'{movieName} Subtitles')
        zip.close()
        counter += 1
    else :
        continue

print(f'\n{counter} Subtitle found.')