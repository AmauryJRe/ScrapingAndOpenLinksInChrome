import requests
import lxml.html
import os
import json
from requests_html import HTMLSession
import ast
import webbrowser

session = HTMLSession()
DIRNAME = '/media/amaury/DATOS/ANIMES'
PROXIES = {'http':'http://localhost:3128','https':'http://localhost:3128'}

file_list = os.listdir(DIRNAME)
file_list_renamed = []
titles_Im_folowing = []
for file in file_list:
    if '_' in file:
        file_list_renamed.append(file[0:len(file)-4])
        titles_Im_folowing.append(file[0:file.index('_')])

SITE_URL = 'https://www3.animeflv.net'

root = requests.get(SITE_URL)
docFather = lxml.html.fromstring(root.content)
animeLinksList = docFather.xpath('//ul[@class="ListSdbr"]')[0]
urls = animeLinksList.xpath('.//a/@href')

for url in urls:
    animeXPage = session.get(SITE_URL+url)
    documentPage = lxml.html.fromstring(animeXPage.content)
    title = documentPage.xpath('.//h1[@class="Title"]/text()')[0]
    title=title.replace(':','-')
    title=title.replace('\t','')
    content = animeXPage.content
    strContent = str(content)
    arreglo = ast.literal_eval(strContent[strContent.index('[['):strContent.index(']]')+2])
    animeUrlName = url[url.rfind('/')::]
    lastEpisodePublished = title + '_' + str(arreglo[0][0])
    if title in titles_Im_folowing and lastEpisodePublished not in file_list_renamed:
        # print(SITE_URL +'/ver'+ animeUrlName+'-'+str(arreglo[0][0]))
        animeXLastEpisode = session.get(SITE_URL +'/ver'+ animeUrlName+'-'+str(arreglo[0][0]))
        documentLastEpisodePage = lxml.html.fromstring(animeXLastEpisode.content)
        zippyshareUrl = list(filter(lambda href: 'zippyshare' in href, documentLastEpisodePage.xpath('.//table[@class="RTbl Dwnl"]//a//@href')))
        print(title)
        print(zippyshareUrl[0])
        webbrowser.get(using='google-chrome').open(zippyshareUrl[0],new=2)