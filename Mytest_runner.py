import os,sys
sys.path.append("D:/Users/CRT/PycharmProjects/untitled2")
import HTMLTestRunner_PY3
import sys
import unittest
import requests
from web import testinterface,check_out,config
from web import globalVar as gl
class Test(unittest.TestCase):
    '测试用例结果如下'
    def setUp(self):
        pass
    # 没有实例化类之前，Test不会有begin_rep属性
    def begin_req(self, apidata):
        r = a.send_request(apidata)
        print("请求连接",r.url)
        print("返回状态码", r.status_code,)
        try :
            print("返回内容", r.json())
        except:
            print("返回内容", "返回内容为空")
        print("请求方式",r.request.method)
        print("断言方法",apidata["checkout"])
        print("请求响应时间：",r.elapsed.total_seconds(),"秒")
        for tup in apidata["checkout"]:
            checkout.methods(tup[0], tup, r,apidata)
            print(checkout.methods(tup[0], tup, r,apidata))
    def methods(self):
        return (list(filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(self, m)),
                            dir(self))))
def demo(apidata):
    def tool(self):
        Test.begin_req(self, apidata)
    setattr(tool, '__doc__', u':%s:%s' % (str(apidata['name']),str(apidata['id'])))
    return tool
def testall(apidata):
    namelist = []
    for i in range(len(apidata)):
        name = 'test_' + str(i + 1)
        setattr(Test, name, demo(apidata[i]))
        namelist.append(name)
    return namelist
def suite(Apidata):
    namelist = testall(Apidata)
    suites = unittest.TestSuite()
    for i in namelist:
        suites.addTest(Test(i))
    # suit = unittest.makeSuite(Test)
    return suites
def run(Apidata,excel_name):
    report = 1
    name = excel_name.split('.')[0]
    filepath = 'D:/Users/CRT/PycharmProjects/untitled2/web/report/'+ name + str(report) +'.html'
    while os.path.exists(filepath):
        report += 1
        filepath = 'D:/Users/CRT/PycharmProjects/untitled2/web/report/'+ name + str(report) +'.html'
    fp = open(filepath, 'wb')
    runner = HTMLTestRunner_PY3.HTMLTestRunner(stream=fp, title=u'我是测试报告的标题', description=u'我是测试报告的描述')
    runner.run(suite(Apidata))
    fp.close()
if __name__ == "__main__":
    """Apidata = [[一个excel表的所有接口信息]]"""
    checkout = check_out.Check_out()
    a = gl.globalVar()
    for cof_excel in config.config["excel"]:
        api1 = a.get_inter_info(cof_excel)
        # print(api1)
        run(api1,cof_excel)
        # print(a.get_apil())

