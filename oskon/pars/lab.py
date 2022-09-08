import requests
from bs4 import BeautifulSoup

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.673 Yowser/2.5 Safari/537.36"
}

post = requests.get('http://resume.doska.kg/vacancy/&sortby=new', headers=headers)
postsrc = post.text
POSTSOUD = BeautifulSoup(postsrc, "lxml")
deteil_post_links = []
list_post_links =[]
posts = POSTSOUD.find(class_="mp_last_items_block2").find_all("a")
for k in posts:
    iter_text_ter1 = k.text
    Iten_href1 = 'http://resume.doska.kg' + k.get("href")
    # print(f'{iter_text_ter1}:{Iten_href1}')
    deteil_post_links.append(Iten_href1)
print(len(deteil_post_links))
list_post_links = deteil_post_links[-4]