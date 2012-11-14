#对URL进行分割
# XXG 2012-10-23

url=raw_input("input the url:")
if(url[0:4] == 'http'):
    domain=url[11:-4]
elif(url[0:3] == 'www'):
    domain=url[4:-4]

print "Domain name :" + domain

#思考： 如：http://www.xxxx.edu.cn
#         https://xxx.cn /com.cn 怎么处理 split('.')
