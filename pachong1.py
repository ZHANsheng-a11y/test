import csv
from lib2to3.main import diff_texts

import requests
from pprint import pprint
from lxml import etree

 #爬取页面
with  open("xinxi.csv", "w+") as f:
    writer = csv.writer(f)
    writer.writerow(["房源标题", "户型信息", "详细地址", "房屋特点", "价格信息"])
    for i in range(5):
        if i == 0:
            continue
        elif i == 1:
            url = "https://xa.zu.anjuke.com/fangyuan/yantaqu/"
        else:
            url = f"https://xa.zu.anjuke.com/fangyuan/yantaqu/p{i}/"

        headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "referer" : "https://xa.anjuke.com/"
        }
        #获取页面数据
        resp = requests.get(url, headers=headers).text
        tree = etree.HTML(resp)
        #pprint(resp)

        #解析数据
        data = tree.xpath("//div[@class='zu-itemmod clearfix']")
        for div in data:
                fangyuan = div.xpath('.//div[@class="zu-info"]/h3/a/b[@class="strongbox"]/text()')[0]
                h_text = div.xpath('.//p[@class="details-item tag"]//text()')
                huxing = h_text[1] + h_text[2] + h_text[3] + h_text[4] + h_text[6] + h_text[7]
                d_text = div.xpath('.//address[@class="details-item tag"]//text()')
                dizhi = d_text[1] + d_text[2].strip() + d_text[3] + d_text[4] + d_text[5] + d_text[6].strip()
                t_text = div.xpath('.//p[@class="details-item bot-tag"]/span/text()')
                tedian = "-".join(t_text)
                j_text = div.xpath(".//div[@class='zu-side']//text()")
                jiaqian = j_text[1] + j_text[3]
                writer.writerow([fangyuan, huxing, dizhi, tedian, jiaqian])
        print(f"正在爬取第{i}页")
    print("爬取成功")
