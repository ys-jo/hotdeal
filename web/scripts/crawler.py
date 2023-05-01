from bs4 import BeautifulSoup
import requests
import telegram
import asyncio
from hotdeal.models import Deal
from datetime import datetime, timedelta


BOT_TOKEN = "5915137382:AAETw2YzBsIx09L6_YS120AE-PnR_tx0XQ4"
bot = telegram.Bot(token=BOT_TOKEN)

response = requests.get("https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu")
# print(f"statue : {response.status_code}")
soup = BeautifulSoup(response.text, features="html.parser")

#for item in soup.find_all("font", class_="list_title"): # font태그에서 class가 list_title인 걸 긁어오기
#    print(item.text)

def run():

    # 3일이 지난 DB 삭제
    row, _ = Deal.objects.filter(created_at__lte=datetime.now() - timedelta(days=3)).delete()

    # print(row, "deals deleted")

    #  뽐뿌에서 link, image, title, 추천 ,댓글 수
    for item in soup.find_all("tr", {'class': ["list1", "list0"]}): # tr 태그에서 class가 list1 list0인 걸 긁어오기
        try:
            image = item.find("img", class_="thumb_border").get("src")[2:]
            image = "http://" + image
            title = item.find("font", class_="list_title").text
            title = title.strip()
            link = item.find("font", class_="list_title").parent.get("href")
            link = "https://www.ppomppu.co.kr" + link
            reply_count = int(item.find("span", class_="list_comment2").text)
            up_count = item.find_all("td")[-2].text
            up_count = up_count.split("-")[0]
            up_count = int(up_count)
            if up_count >= 5:
                # id 알아내는 법
                # url에서 api.telegram.org/bot{BOT_TOKEN}/getUpdates 로 진행
                if (Deal.objects.filter(link__iexact=link).count() == 0):
                    Deal(image_url = image, title=title, link=link, reply_count=reply_count, up_count=up_count).save()
                    asyncio.run(bot.send_message(-1001985596883, '{} {}'.format(title, link)))
        except Exception as e:
            continue
