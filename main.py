import zhihu

# 爬虫案例必经步骤
# 1、确定数据所在的url地址
# 2、发送url地址对应的请求（你要的数据/不要的数据）
# 3、解析你要的数据（不要的数据排查出去）
# 4、数据保存
# 5、问题所在：黑色字体，封装在了js中，只能使用正则语言来解析

if __name__ == '__main__':

    start_page = 1
    zhihu.zhihu_ans(start_page)