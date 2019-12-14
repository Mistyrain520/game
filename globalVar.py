import xlrd
from web import config
import requests,json
import random,re
from web import sql,authorization
class globalVar:
    def __init__(self):
        self.choiceserver = {
            "测试服": "",
            "预发布服": "",
            "开发服": "",
        }
        self.yourserver = config.config["yourserver"]
        self._global_dict = []
        self.original_api = []

        self.sq = sql.Server()
    def set_global_dict(self, key, param, value):
        for i in self._global_dict:
            if i["id"] == key:
                i[param] = value
                return True

    def get_global_dict(self, key_id,key,):
        for i in self._global_dict:
            if i["id"] == key_id:
                return i[key]
    #返回更新后的全局接口信息
    def get_apil(self):
        return self._global_dict
    def get_original_api(self):
        return self.original_api
    def get_inter_info(self,excel):
        info = []
        workbook = xlrd.open_workbook(excel)
        for sheet in workbook.sheets():
#           如果这个sheet只有一行，那么直接continue
            if sheet.nrows == 1:
                continue
            head = sheet.row_values(0)
            execute_index = head.index("是否执行")
            url_index = head.index("url")
            reqway_index = head.index("请求方式")
            header_index = head.index("请求头")
            params_format = head.index("格式")
            name_index = head.index("接口说明")
            for i in range(1, sheet.nrows):
#                如果execute为0，不记录
                if sheet.cell_value(i, name_index) == "":
                    continue
#先判断是否执行这一列是否为空，避免为空的时候来判断是否等于1会出错
                if sheet.cell_value(i, execute_index) =="":
                    continue
                if int(sheet.cell_value(i, execute_index)) != 1:
                    continue
                if i >= sheet.nrows:
                    break
                for j in range(1,20):
                    p = "请求参数"+str(j)
                    if p not in head:
                        continue
                    params_index = head.index(p)
                    if sheet.cell_value(i,params_index) == '':
                        continue
                    url_dict = {}
                    url_dict["name"] = str(sheet.cell_value(i, name_index))
                    url_dict["execute"] = int(sheet.cell_value(i, execute_index))
                    url_dict["url"] = self.choiceserver[self.yourserver] + str(sheet.cell_value(i, url_index))
                    url_dict["reqway"] = str(sheet.cell_value(i, reqway_index))
                    url_dict["headers"] = eval(sheet.cell_value(i, header_index))
                    url_dict["params"] = eval(sheet.cell_value(i, params_index))
                    url_dict['checkout'] = eval(sheet.cell_value(i, params_index + 1))
                    url_dict["params_format"] = str(sheet.cell_value(i, params_format))
                    url_dict["id"] = str(sheet.name) + "+" + str(i+1) + "+" + str(j)
                    url_dict["response"] = ''
                    info.append(url_dict)
        self._global_dict = info
        self.original_api = info
        return info
    def send_request(self,apiinfo):
        s = requests.Session()
        url = apiinfo["url"]
        params = apiinfo["params"]
        params_format = apiinfo["params_format"]
        headers = apiinfo["headers"]
        headers["authorization"] = authorization.authorization
        reqway = apiinfo["reqway"]
        print(params, "转换前的参数", type(params))
        params = self.deal_parm(params,apiinfo["id"])
        print(params, "转换后的数值")
        if params_format == "json":
            data = json.dumps(params)
            if reqway == "post":
                r = s.post(url, data=data, headers=headers,timeout = 10)
        elif params_format == "string":
            if reqway == "get":
                if params == "None":
                    r = s.get(url, headers=headers,timeout = 10)
                else:
                    r = s.get(url, params=params, headers=headers,timeout = 10)
        # 更新全局变量
        self.set_global_dict(apiinfo["id"], "params", params)
        try:
            self.set_global_dict(apiinfo["id"], "response", r.json())
        except:
            self.set_global_dict(apiinfo["id"], "response", "没有返回值")
        return r




    # 处理params的参数传递
    def deal_parm(self, params,api_id):
        if params == None:
            return params
        #获取全局接口信息（可供更改的字段）
        apil = self.get_apil()
        for key, value in params.items():
            #如果是@开头，会去自动请求一下标记的接口信息，并拿到相应的值，比如返回值中的信息
            if str(value).startswith("@"):
                #将@['sheet1+1+1','key']拆开成@,'sheet1+1+1','key'
                kkk = re.split(r'\[|\,|\]', str(value))
                for i in apil:
                    if i["id"] == kkk[1][1:-1]:
                        new_r = self.send_request(i)
                        params[key] = self.get_value_char(eval(str(value)[1:])[1],new_r.json())
            #如果是#开头，就直接去拿上面已经执行过的接口的返回信息,通过切割方式来拿到对应的value，返回一个字符串
            elif str(value).startswith("#"):
                for i in apil:
                    if i["id"] == eval(str(value)[1:])[0]:
                        params[key] = self.get_value_char(eval(str(value)[1:])[1],i["response"])
            #如果是*开头，则通过无限遍历的方式从上面的返回信息中随机取出一个符合key值的value,适用于返回值数据不大（过大的数据会运行较慢）
            elif str(value).startswith("*"):
                for i in apil:
                    if i["id"] == eval(str(value)[1:])[0]:
                        # str(value)[1:]这个会去掉*号，取出的值用eval就能得到列表,eval(str(value)[1:])[1]就是需要分析的value)
                        print(self.dict_get(eval(str(value)[1:])[1],i["response"],tmp_list=[]),"最终返回了什么")
                        params[key] = random.choice(self.dict_get(eval(str(value)[1:])[1],i["response"],tmp_list=[]))
            # 如果是&开头，就直接去拿上面已经执行过的接口的返回信息,通过切割方式来拿到对应的value，返回一个列表
            elif str(value).startswith("&"):
                for i in apil:
                    if i["id"] == eval(str(value)[1:])[0]:
                        params[key] = [self.get_value_char(eval(str(value)[1:])[1], i["response"])]
            else:
                params[key] = self.sq.methods(value)
        return params
    #根据关键词在返回请求中拿到对应的value
    @staticmethod
    def dict_get(key, url_response, tmp_list=[]):
        if type(url_response) == list:
            url_response = {"XXX":url_response}
        if type(url_response) != dict:
            return tmp_list
        if key in url_response.keys():
            tmp_list.append(url_response[key])
        else:
            for val in url_response.values():
                if type(val) == dict:
                    globalVar.dict_get(key, val, tmp_list)
                elif type(val) == list:
                    globalVar.list_get(key, val, tmp_list)
        if len(tmp_list)==0:
            return tmp_list
        return tmp_list
    @staticmethod
    def list_get(key, val, default):
        for _val in val:
            if type(_val) == list:
                globalVar.list_get(key, _val, default)
            elif type(_val) == dict:
                globalVar.dict_get(key, _val, default)
        # return default
    @staticmethod
    def get_value_char(key,url_response):
        #接收的key不带引号，但是返回值key都是有单引号的（确认过是单引号），因此切割规则要加上引号
        rule = '\''+str(key)+'\''+':'
        value = str(url_response).split(rule,1)
        value[1] = value[1].strip()
        if value[1].startswith('\''):
            result = re.match(r'\'.*?\'',value[1]).group()
            result = result.replace('\'','')
            return result
        else:
            result = re.match(r'.*?[,}]', value[1],).group()
            return int(result[:-1])
#测试用
# a = globalVar()
# print(a.get_inter_info())