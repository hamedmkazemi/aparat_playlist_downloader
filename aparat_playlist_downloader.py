import os
import requests
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm
import numpy as np

# url example: 'https://www.aparat.com/v/ShsAv?playlist=515087'
url= input('Please input url:')
print('Quality Selection')
quality=int(input('for highest quality input -1, for lowest quality input 0, or if you like to download mid quality input 1:'))

def downlaod_video(item_url,quality, index=None, path=os.getcwd()):
    url=item_url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find('h1', attrs={'id': 'videoTitle'}).text.strip()
    print(title)
    file_name = str(index) + '_' + title + '.mp4' if index != None else title + '.mp4'
    file_path = os.path.join(path, file_name)

    if os.path.exists(file_path)==False:
        if quality==1:
            quality=int(np.ceil(len(soup.find('div', attrs={'class': 'dropdown-content'}).find_all('li'))/2))
        file_url = soup.find('div', attrs={'class': 'dropdown-content'}).find_all('li')[quality].find('a')['href']
        print('url: ',file_url)
        r = requests.get(file_url)
        with open(file_path,"wb") as video:
            video.write(r.content)

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

playlist = soup.find('section', attrs={'class': 'single-playlist'})
playlist_items = playlist.find_all('div', attrs={'class': 'item'})

with tqdm(total=len(playlist_items)) as pbar:
    for index, a in enumerate(playlist_items):
        print('Downloading file ',index+1, ' ...')
        a_tag = a.find('a', href=True, text=True)
        item_url = 'https://www.aparat.com' + a_tag['href']
        downlaod_video(item_url,quality, index + 1, path=os.getcwd())
        print('File  ', index + 1, ' is ready to use.')
        pbar.update(1)