import unittest
from web import sql
import json
class Check_out(unittest.TestCase):
    sq = sql.Server()
    def setUp(self):
        pass
    # def status_code_200(self,r):
    #     return self.assertEqual(r.status_code,200,msg="状态码不对")
    def _assertEqual(self,tup,r,apidata):
        arg = self.Analy_params(tup,r,apidata)
        return "断言验证",self.assertEqual(arg[0],arg[1]),arg
    def _assertIn(self,tup,r,apidata):
        arg = self.Analy_params(tup, r, apidata)
        # self.assertIn(arg[0],arg[1])
        # self.assertNotEqual()
        return "断言验证", self.assertIn(arg[0], arg[1]), arg
    def methods(self, your_meth ,tup,r,apidata):

        meth = list(filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(self, m)),
                           dir(self)))
        if your_meth in meth:
            return getattr(self, your_meth)(tup,r,apidata)
        else:
            return your_meth,meth
    def Analy_params(self,tup,r,apidata):
        par = []
        if tup[1] == "req":
            par = self.Analy_req(tup,r,apidata)
        if tup[1] == "sql":
            par_0 = self.sq.methods(tup[2])
            if par_0 in apidata["params"].keys():
                par.append(apidata["params"][par_0])
            else:
                par.append(par_0)
            sl_com = self.compound_sql(tup[3],apidata)
            par.append(self.sq.ExecQuery(sl_com,1))
            # par.append(sl_com)
        return par
    def compound_sql(self,s,apidata):
        sl = ""
        for i in s:
            if i in apidata["params"].keys():
                sl = sl+'\''+str(apidata["params"][i])+'\''
            else:
                sl = sl + i
        return sl
    def Analy_req(self,tup,r,apidata):
        par = []
        if tup[3] == "status_code":
            par.append(int(tup[2]))
            par.append(r.status_code)
        if tup[3] == "msg_val":
            par.append(tup[2])
            par.append(r.json().values())
        if tup[3] == "msg_key":
            par.append(tup[2])
            par.append(r.json().keys())
        return par





