import requests
from lxml import etree
import json


class SpiderYanZhao:
    # 爬取url

    url = "https://yz.chsi.com.cn/zsml/querySchAction.do?ssdm=44&dwmc=%E5%8D%8E%E5%8D%97%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6&mldm=zyxw&yjxkdm=0854"
    classcode_url = "https://yz.chsi.com.cn/zsml/pages/getZy.jsp"   # 课程代号

    # 课程分类
    type_class = {"01": [],  # 哲学类
                  "02": [],  # 经济类
                  "03": [],  # 法学类
                  "04": [],  # 教育学类
                  "05": [],  # 文学类
                  "06": [],  # 历史学类
                  "07": [],  # 理学类
                  "08": [],  # 工学类
                  "09": [],  # 农学类
                  "10": [],  # 医学类
                  "11": [],  # 军事学
                  "12": [],  # 管理学
                  "13": [],  # 艺术学
                  }

    def create_url(self, school, class_code):
        """
        创建专业页面url
       :param school: 学校名
       :param class_code: 专业代号
       :return:
       """

        url = "https://yz.chsi.com.cn/zsml/querySchAction.do?ssdm=44&dwmc=%s&mldm=zyxw&yjxkdm=%s"% (school,class_code)

        return url

    def major_spider(self, school="广东工业大学", type='01'):
        """获取学校的专业"""

        result = []  # 结果列表




        # 获取课程代号
        code_list = self.type_class[type]

        for code in code_list:

            # 创建爬取url
            url = self.create_url(school, code)
            print("正在爬取url:",url)

            # 获取响应
            response = requests.get(url)

            # 获取html
            html = response.text

            # 解析
            selector = etree.HTML(html)

            # 获取每一行学院学科信息
            tr_list = selector.xpath("//tr")

            if len(tr_list) > 1:  # 如果是该学科有专业
                # 第一行为标题，去掉
                for index in range(1, len(tr_list)):
                    # 详情链接 //td/a[@target="_blank"]/@href
                    href = tr_list[index].xpath('.//td/a[@target="_blank"]/@href')[0]

                    # 院系所
                    college = tr_list[index].xpath('.//td[2]/text()')[0]

                    # 专业
                    major = tr_list[index].xpath('.//td[3]/text()')[0]

                    # 研究方向
                    study = tr_list[index].xpath('.//td[4]/text()')[0]

                    # 将结果构建字典
                    major_dict = {}

                    major_dict["院系所"] = college
                    major_dict["专业"] = major
                    major_dict["研究方向"] = study
                    major_dict["详情链接"] = href

                    # 添加进入结果list
                    print(major_dict)
                    result.append(major_dict)
        print("爬取结束")

        return result

    def classcode_spider(self):
        """获取课程代号"""

        response = requests.get(self.classcode_url)


        # 获取json数据
        code_dict = json.loads(response.text)
        print(code_dict)

        # 将课程代号抽取从json抽取出来  {'mc': '考古学', 'dm': '0601'}
        for d in code_dict:
            if d['mc'] != "":
                cl = d['dm'][0:2]  # 提取出不用代号前两个数字
                self.type_class[cl].append(d["dm"])




    def deatil_spider(self, url):
        """获取详细页面"""
        print(url)
        # 爬取页面
        resp = requests.get("https://yz.chsi.com.cn" + url)

        # 获取html
        html = resp.text

        # 解析
        selector = etree.HTML(html)


        # 拟招人数
        people = selector.xpath('//td[@class="zsml-summary"]/text()')[-1]

        # 学校
        school = selector.xpath('//td[@class="zsml-summary"]/text()')[0]

        # 考试方式
        exam = selector.xpath('//td[@class="zsml-summary"]/text()')[1]

        # 考试科目
        subject_err = selector.xpath('//tbody[@class="zsml-res-items"]//td/text()')
        # 获取的科目格式有问题，去掉空格和换行
        subject = [s.strip() for s in subject_err]

        # 返回字典
        result = {}

        result["拟招人数"] = people
        result["学校"] = school
        result["考试方式"] = exam
        result["考试科目"] = subject


        return result



spide = SpiderYanZhao()
spide.classcode_spider()
