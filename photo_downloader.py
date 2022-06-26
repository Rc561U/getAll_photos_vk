import requests
import json
import time
import os
import re


def get_photo_data(TOKEN, user_id, offset=0, count=200):
    api = requests.get("https://api.vk.com/method/photos.getAll", params={
        "owner_id": user_id,
        "access_token": TOKEN,
        "offset": offset,
        "count": count,
        "photo_sizes": 0,
        "v": 5.103
    })

    return json.loads(api.text)


def get_photo(data):
    # data = get_photo_data()
    count_photo = data["response"]["count"]
    i = 0
    count = 200
    photos = []
    while i <= count_photo:
        if i != 0:
            data = get_photo_data(offset=i, count=count)
        for files in data["response"]["items"]:
            file_url = files["sizes"][-1]["url"]
            # filename = file_url.split("/")[-1]
            filename = (re.search('[\w\.]*jpg', file_url)).group()
            photos.append(filename)
            time.sleep(0.1)
            api = requests.get(file_url)

            dir = os.path.join(os.getcwd(), 'VK_Photos')
            if not os.path.exists(dir):
                os.mkdir(dir)
            with open("VK_Photos/%s" % filename, "wb") as file:
                file.write(api.content)

        print(i)
        i += count
        print(len(photos))


if __name__ == '__main__':
    TOKEN = input('Enter your TOKEN: ')
    user_choose = int(input('If you want to download user photos, press - 1\nIf you want to download group photos, press - 2\n'))
    succsess = 'download completed successfully'
    fail = 'download failed'
    if user_choose == 1:
        user_id = input('Enter your user_id: ')
        try:
            data = get_photo_data(TOKEN, user_id)
            get_photo(data)
            print(succsess)
        except:
            print(fail)
    if user_choose == 2:
        try:
            group_id = '-' + input('Enter your group_id: ')
            data = get_photo_data(TOKEN, group_id)
            get_photo(data)
            print(succsess)
        except:
            print(fail)
            
