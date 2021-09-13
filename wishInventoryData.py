import json
import requests
from urllib import parse

# 请求头伪装浏览器
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46 '
}

# 原神祈愿数据网址构成：https://webstatic.mihoyo.com/hk4e/event/e20190909gacha/index.html? + 个人标识码 + #/log
# 原神祈愿数据源地址构成：https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog? + 个人标识码 + &gacha_type=祈愿类型&page=当前页码&size=每页显示数据条数&end_id=上一页最后一项数据id值
# 祈愿类型gacha_type：200（常驻祈愿），100（新手祈愿），301（角色活动祈愿），302（武器活动祈愿）


# 初始url
url = 'https://webstatic.mihoyo.com/hk4e/event/e20190909gacha/index.html?authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&gacha_id=4ae078b55a1609b395ec8119ac842395292580&timestamp=1630453186&lang=zh-cn&device_type=mobile&ext=%7b%22loc%22%3a%7b%22x%22%3a-3046.083740234375%2c%22y%22%3a248.11520385742188%2c%22z%22%3a-4400.73486328125%7d%2c%22platform%22%3a%22Android%22%7d&game_version=CNRELAndroid2.1.0_R4325476_S4282242_D4302397&region=cn_gf01&authkey=RmXJ4QSlXtRi5vqj5%2ftUAr1f7o08QXAbv6W6BmGY6I4bdKMlYYAAkgAw12e4D6TBwVqLPyTsiOXTw3PiiagKHZZW85nQD7n3FVyOuDqNU1BvH3jOP%2fX%2bnl0vJj%2beJu7%2fLu7fdFlMu7ygsIEO3US4tF6vgvjJlUa04AfuX3UCBmuVpbNzefrWal4Tw3r1PQCeKa8juFehILX%2fmd57pt2UVtDA7MbTs6JKTqLXQIfrrFydv4MVm3Gl1MOgOjazE67IySlbO0KvKoPTvUYAFWuhWsB3MJjXzdBYESQTqoaknAU%2f5mHWvgq813HmEXL5OCtx509qBUhG1pvDcayAbTHZr0PSlcT9wUuRd3VO8G%2fDmu6%2biLn%2fHv7%2fzKIlyLc%2fYGZYuJj3i%2fEhWLJDyGVZJpxl8THaSkInobbtFC%2bDdRbCyJhdrPiQHJsHcZ2spzkKaTW8Uc0T2IHsLsIjpuj%2f5eBBJuS3enKwAFdJAKC9Tjk%2fyqNfN7BjFowis0JN4YCl3vJCgSzabNlA%2bUOVdJg0O4tZKMUtMNzgA8BU%2fZvyqghGLbjqay6XYaCHJMuZh2LmdtYu6KonPM%2bm8DMaybp7finQymLiWhEkOHRc3n%2fVRzNZi%2bzmZ%2fYo8LyO3LuwGxMKN2OiKQyP0b0nAvGshtokce99aeQaf4MJNV%2bTB3J9xKHP2ODLauFjt7XozC6142QEMSMX0uuhjqu0l46YqjUAaMMsJoN3PUf5jifdUNWD%2behJ%2b7QYOsej5doPsGTDNGR02Gdskvr18OyWwQOnw0um%2fpWwJvjyga7O4VGAQNg7%2f4L5yVYvKlIvAQ4%2f3Kb7FH%2fl%2fS4PDjqy8KeyqHoOkiV6uFz%2bEd58Qz1tUUYdc7NSsJ2Wtz8g3JN%2fYwgo2IqiR%2fgZAJpdit%2bLpLrFOjkDDeZJJ7Ogkzfqusw5Xje0CeLzxCBB6LXEyEzjpnoGOd1oDBCCmEtrdNiCKG03g9H4fy4IdlVj2X6WGMDzBZgedYt2X5JufVN%2bMs5u0gsU1qq3ZsRh07VYR%2fdQWC1rZhzUtQACZUpoiIp0iGNKhxk7V8kxzrmjb%2bWi8ykBVez64fNOFFX61pDgGjG3z3wV%2fn%2bNF0PMKt2u7T%2floUtA8ocyqZe8O3DFcKjbTk%2bdsqx0Y%2fkzjSDdoX1SfWeMU06crfdTvxK%2bCka7vmWjwsG%2fItdjmx5mvPBWjwbYtn8IR%2b%2fMiX%2f3%2f5Gv%2fxSUkPCPQmDk6CCBi0wJAeYlJQf7DUMAu1pI1QNUMOiKwqVMdCAa7Dg6aiet48VGNB%2bUv3sDFNGdTeYJtwpmWlaayOatDaMPpRQx0e7oQ2x148XZU7v67aWHy4xWwtGCnTaJ%2fFRG%2bUiPNexZMwQWiz7iug%3d%3d&game_biz=hk4e_cn#/log'
# 祈愿类型
gacha_type = '301'
# 当前页码
page = '1'
# 每页显示数据条数（不超过20）
size = '6'
# 上一页最后一项数据id值（第一页默认为0）
end_id = '0'
# 计数器
sum = 0
params = parse.parse_qs(url.split("?")[1])
params.update({'game_biz': ['hk4e_cn']})
params.update({'gacha_type': [gacha_type]})

# 循环页码
while True:
    params.update({'page': [page]})
    params.update({'size': [size]})
    params.update({'end_id': [end_id]})
    # print(params)

    # 使用get方法请求数据
    response = requests.get("https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog", headers=headers, params=params).text

    # 返回json报文
    # print(response)

    # json转换为dict
    data = json.loads(response)

    # 如果该页数据为空
    if int(len(data['data']['list'])) == 0:
        # 如果该页为首页
        if int(data['data']['page']) == 1:
            print("数据为空，程序执行完毕！")
        else:
            print("合计" + str(int(data['data']['page']) - 1) + "页，共" + str(sum) + "项数据，程序执行完毕！")
        break
    else:
        # 获取列表数据
        print("第" + str(data['data']['page']) + "页，共" + str(len(data['data']['list'])) + "项数据：")
        # 循环读取信息
        for i in range(0, int(len(data['data']['list']))):
            print(data['data']['list'][i])
            sum = sum + 1
            # 获取当前页最后一条数据的id充当下一页的end_id
            end_id = data['data']['list'][int(len(data['data']['list'])) - 1]['id']
        # print(end_id)
        print('\n')

        # 下一查询页码
        page = str(int(page) + 1)
print('\n')
