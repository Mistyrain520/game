# python3+requests实现灵活参数的接口自动化

  
## 环境要求   
python3、requests、xlrd、unittest

## 基本功能  
参数灵活性：可以根据配置取数据库；可以取自上文接口返回信息；可以重新调用指定接口拿新的返回信息来保证用例的独立，不与先前接口产生关联  
断言灵活：有通用的基本断言，也可以写方法做精准断言；  
报告生成、支持多excel；  
优势：可以随时运行于不同服务器；用例单元化可以做回归；用例独立化可以做压测模拟玩家操作；报告详细，有接口相应时间、内容等信息；
## 灵活参数对应
"goods_id":"get_goods"；调用方法从数据库取出数据来用；
"consultant_id":"#['通用接口+2+1','id',]"；如果是#开头，就直接去拿上面已经执行过的接口的返回信息,通过切割方式来拿到对应的value，返回一个字符串；  
如果是@开头，会重新去自动请求一下对应标记的接口信息，并拿到相应的value值，比如你填写@['通用接口+2+1','id',]，id就是key，结果就是Key对应的value；  
如果是*开头，则通过无限遍历的方式从上面的返回信息中随机取出一个符合key值的value,适用于返回值数据不大（过大的数据会运行较慢）  
如果是&开头，就直接去拿上面已经执行过的接口的返回信息,通过切割方式来拿到对应的value，返回一个列表。  
当然你可以二次开发加上你想要的功能

## 灵活断言
建议二次开发实现自己想要的  
目前支持：  
断言返回状态码；断言用简单的一句SQL；  
例子一：断言状态码200，断言5da7dfeb5d11a700019f88de存在于***（数据库查询的结果"select *** from ** where subject_id=","subject_code",）subject_code是请求参数的key  
[("_assertEqual","req","200","status_code"),("_assertIn","sql","5da7dfeb5d11a700019f88de",["select *** from ** where subject_id=","subject_code",])]  
例子二：断言返回数据中有某个key值  
[("_assertEqual","req","200","status_code"),("_assertIn","req","teacher_list","msg_key"),]  
也可以和参数一样写方法做精准断言  
  
目前随便加的

##其他功能 报告生成等，不一一说。  
![image](https://github.com/Mistyrain520/game/blob/master/report_test.png)
