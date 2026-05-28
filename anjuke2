import csv
import time
import requests
import os
from lxml import etree
from openai import OpenAI
import json

from setuptools.package_index import user_agent


class Spider():
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
            "referer": "https://xa.anjuke.com/"
        }

    def download(self,url,xinxi):
        resp = requests.get(url, headers=self.headers).text
        tree = etree.HTML(resp)
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
            link = div.xpath('.//div[@class="zu-info"]/h3/a/@href')

            xinxi.writerow([fangyuan, huxing, dizhi, tedian, jiaqian, link])

def analyze_houses(csv_file_path):
    #  读取 csv 内容
    # api_key = os.getenv('ARK_API_KEY')
    with open(csv_file_path, "r", encoding="utf-8") as f:
        content = f.read()
        # print(content)
    # 连接豆包 API

    client = OpenAI(
        api_key=key,
        base_url="https://ark.cn-beijing.volces.com/api/v3"
    )

    # 给 AI 发指令
    prompt = f"""
        你是租房分析师，请分析以下房源信息：
        
        要求：
        1. 整理成清晰表格
        2. 标注价格、户型、位置
        3. 按性价比排序，并且将跳转链接也一起放在表格里
        4. 给出最推荐的3个房源，并且说明理由
        
        房源数据：
        {content}
        """

    # 调用大模型
    response = client.chat.completions.create(
        model="doubao-seed-1-8-251228",
        messages=[{"role": "user", "content": prompt}],
    )

    # 返回
    return response.choices[0].message.content
    # 打印JSON
    # result = response.model_dump()
    # print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    with  open("xinxi.csv", "w", encoding="utf-8") as f:
        xinxi = csv.writer(f)
        xinxi.writerow(["房源标题", "户型信息", "详细地址", "房屋特点", "价格信息","跳转链接"])
        spider = Spider()
        user_input = input("请输入要获取的网址：")
        for i in range(1,6):
            if i == 1:
                url = user_input
                print(f"正在爬取第1页")
            else:
                print(f"正在爬取第{i}页")
                url = user_input+f"p{i}/"
            spider.download(url,xinxi)
            time.sleep(2)
        print()
    print("爬取成功，正在调用AI分析...")
    key = input("请输入key:")
    result = analyze_houses("xinxi.csv")
    print("AI 分析结果")
    print(result)
