print('hi')
import requests
from bs4 import BeautifulSoup

url = "https://doska.kg/cat/"
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.673 Yowser/2.5 Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text
# print(src)

# with open("oskon/index.html","w") as file:
#     file.write(src)

with open("oskon/index.html") as file:
    src = file.read()
SOUD = BeautifulSoup(src, "lxml")

find_all_spans_in_user_info = SOUD.find(class_="doska-category-block").find_all("a")
# print(find_all_spans_in_user_info)
list_category=[]
for item in find_all_spans_in_user_info:
    iter_text_ter = item.text
    Iten_href = 'https://doska.kg/'+item.get("href")
    print(f'{iter_text_ter}:{Iten_href}')
    list_category.append(Iten_href)
list_category.pop()
list_category.pop(-1)
######################

# for i in list_category:
sub = requests.get(list_category[1], headers=headers)
subsrc = sub.text
SUBSOUD = BeautifulSoup(subsrc, "lxml")
# print(SUBSOUD.text)
subcategory=SUBSOUD.find(class_="doska-category-block").find_all("a")
post_list=[]
print('==============')
for i in subcategory:

    iter_text_subcategory = i.text
    if not iter_text_subcategory.startswith('+'):
        Iten_href_subcategory = 'https://doska.kg'+i.get("href")
        print(f'{iter_text_subcategory}:{Iten_href_subcategory}')
        post_list.append(Iten_href_subcategory)
###################
# for i in post_list:
post = requests.get(post_list[0], headers=headers)
postsrc = post.text
POSTSOUD = BeautifulSoup(postsrc, "lxml")
deteil_post=[]
posts = POSTSOUD.find(class_="doska_last_items_list").find_all("a")
for k in posts:
    iter_text_ter1 = k.text
    Iten_href1 = 'https://doska.kg' + k.get("href")
    print(f'{iter_text_ter1}:{Iten_href1}')
    deteil_post.append(Iten_href1)
 #   #############
print(deteil_post[0],'___________')
deteil_post_list = requests.get(deteil_post[0], headers=headers)
deteil_post_src = deteil_post_list.text
DETEIL_POST=  BeautifulSoup(deteil_post_src, "lxml")

detei_posts = DETEIL_POST.find(class_="item_title")
print(detei_posts.text)
print(deteil_post[0],'---------')
s=DETEIL_POST.get('img')
print(s)
img_tags = DETEIL_POST.find_all('img')

urls = [img['src'] for img in img_tags]


for url in urls:
    print("https:"+url)

# for i in image:
#     print(i)
    # t = i.text
    # I = 'https://doska.kg' + i.get("href")



# for i in image:
#     iter_text_ter2 = i.text
#     Iten_href2 = 'https://doska.kg' + i.get("img")
#     print(f'{iter_text_ter2}:{Iten_href2}')



















