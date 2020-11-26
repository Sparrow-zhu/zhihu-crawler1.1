import get_data
import time
import random
import re
import csv
import json
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

# 全局变量（值不变）。穿插在各个函数，在函数中需要引用global，以改变全局变量的值
## 需要获取/输出的变量
link_id1 = '' # 获取ajxj中网址以及小鹿回答的地址
rank = 1 # 小鹿回答的排名，初始化为第1名，每次爬取完一个时需要再次初始化
totals = 1 # 获取当下话题的总回答数
ans_link = ''
title = ''
final_data = []
comment = []
comments = []
date = ''
followers = ''
looked = ''

## 判断条件变量
flag = 0 # 爬取小鹿排名时，需要flag来判断是否抓取到了小鹿的回答
judge = "" # 判断获取到的网页信息的type

def get_save(data):
    file = open('知乎回答问题数据.csv', mode='a', encoding='utf-8-sig', newline='')
    csv_write = csv.DictWriter(file, fieldnames=['小鹿的发表日期', '话题关注者数量', '话题被浏览量', '话题名称', '小鹿的回答链接', '回答总数量', '回答排名数'])
    csv_write.writeheader()  # 写入表头

    for i in final_data:
        dict_data = {'小鹿的发表日期': i[0], '话题关注者数量': i[1], '话题被浏览量': i[2],
                     '话题名称': i[3], '小鹿的回答链接': i[4], '回答总数量': i[5], '回答排名数': i[6]
                     }
        csv_write.writerow(dict_data)

    file.close()

# 获取某一话题下小鹿的回答的全部数据
def parse_data(html):
    '''
    功能：提取 html 页面信息中的关键信息，并整合一个数组并返回
    参数：html 根据 url 获取到的网页内容
    返回：存储有 html 中提取出的关键信息的数组
    '''
    global rank
    global flag
    global comment
    global comments
    flag = 0
    comments = []

    json_data = json.loads(html)['data']
    #print(json_data)

    for item in json_data:
        comment = []
        comment_xiaolu = [] # 判断是否循环到了小鹿，如果判定是小鹿，则停止循环并且返回rank
        comment_xiaolu.append(item['author']['name'])  # 姓名
        #comment.append(item['author']['gender'])  # 性别
        #comment.append(item['author']['url'])     # 个人主页
        #comment.append(item['voteup_count'])  # 点赞数
        #comment.append(item['comment_count'])  # 评论数
        #comment.append(item['url'])               # 回答链接
        #comments.append(comment)
        print(comment_xiaolu[0])
        if comment_xiaolu[0] == "小鹿" or comment_xiaolu[0] == "å°�é¹¿" or rank > 99: # 如果小鹿回答的排名掉出100名以外变直接返回rank=100
            flag = 1
            #print(rank)
            comment.append(date)
            comment.append(followers)
            comment.append(looked)
            comment.append(title)
            comment.append(ans_link)
            comment.append(totals)
            comment.append(rank)
            comments.append(comment)
            print(comments)
            break
        else: rank += 1

    return comments

# 获取所有话题下小鹿的回答的全部数据
def get_final_data(url):

    global link_id1
    global judge
    global totals
    global rank
    global final_data

    print('====' * 30)

    # get total users number
    html = get_data.get_data(url)
    judge = isinstance(html, str) #判断获取到的网页信息的type是否时str，如果知乎弹出了登录验证，则get_data返回的type是NoType

    if isinstance(html, str) != True:
        comment = []
        comments = []
        comment.append(title)
        comment.append(ans_link)
        comment.append('') # 有多少个其他变量（除了title和ans_link）就要多少个这个命令来占位
        comment.append('')
        comments.append(comment)
        final_data.extend(comments)
        print(comments)
        return

    totals = json.loads(html)['paging']['totals']
    print(f"当下回答总数数量：{totals}")

    ans_page = 0

    while (ans_page <= totals):  # 遍历某话题下的每一条回答(用来获取回答者信息)(第二层循环)

        print("现在是多少页了：" + str(ans_page))
        html = get_data.get_data(url)

        if isinstance(html, str) != True:
            break

        commentsss = parse_data(html)  # 获取小鹿的用户的信息，以及回答的rank

        ans_page += 5          #话题下面每个问题打开自动会加载5条回答

        if (flag != 0): # 如果已经抓取到了小鹿的排名，跳出函数
            break

        url = json.loads(html)['paging']['next']  # 获取某一个话题中的下一页回答（ps：每一页有5个回答，即offset=0，5，10...）

    final_data.extend(commentsss)  # 将所有获得的数据输入一个数组中
    #print(final_data)

    return

# 获取第一层循环数据（小鹿回答过的全部问题以及问题的名字+id1），获取第二层循环的地址（由第一层循环中获取的id1构造第二层循环的地址链接）
def get_answer(text):

    global link_id1
    global rank
    global ans_link
    global title
    global comment
    global comments
    global date
    global followers
    global looked

    result_list = re.findall('\{"suggestEdit":.*?"question","id":.*?\}', text)
    for data in result_list:

        information = []
        title = re.findall('"title":"(.*?)"', data)[1]  # 回答话题名称
        # link = re.findall('"url":"(.*?)",', data)[1].encode().decode('unicode_escape')
        link_id1 = re.findall('"type":"question","id":(.*?)\}', data)[0]
        link_id2 = re.findall('"id":(.*?),', data)[0]
        ques_link = 'https://www.zhihu.com/question/' + link_id1  # 话题总链接

#        linklink = json.loads(html_data)['paging']['previous']
#        final_link_id = re.findall('https://(.*?)offset=', linklink)[0]
#        final_link = 'httpst://' + str(final_link_id) + "offset=" + "0" + "&platform=desktop&sort_by=default"
        ans_link = 'https://www.zhihu.com/question/' + link_id1 + '/answer/' + link_id2  # 小鹿回答链接
#        voteupCount = re.findall('"voteupCount":(.*?),', result_list[0])[0] # 回答投票数量

        #comment.append(title)
        #comment.append(ans_link)

        rank = 1 #重新初始化rank

        start_url = 'https://www.zhihu.com/api/v4/questions/' + str(
            link_id1) + '/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics%3Bsettings.table_of_content.enabled%3B&limit=5&offset=0&platform=desktop&sort_by=default'

        html_ans_link = get_data.get_data(ans_link)
        soup = BeautifulSoup(html_ans_link, 'lxml')

        doc = pq(html_ans_link)
        date = doc('.ContentItem-time').text()
        followers = soup.find_all('strong', class_="NumberBoard-itemValue")[0].get_text()
        looked = soup.find_all('strong', class_="NumberBoard-itemValue")[1].get_text()

        get_final_data(start_url)



    return

# 主函数，构造第一层循环
def zhihu_ans(page):

    print(f"======知乎关注的问题爬取第{page}页======")

    # 1、确定数据所在的url地址
    link = 'https://www.zhihu.com/people/you-wu-jun-77/answers?page={}'.format(str(page))

    # 2、发送url地址对应的请求（你要的数据/不要的数据）
    html_data = get_data.get_data(link) #返回的就是response.text

    # 3、解析你要的数据（不要的数据排查出去）
    ## {"author":{"avatarUrlTemplate":"https:\u002F\u002Fpic1.zhimg.com\u002F85d2fe422c461502ced66225564ab9f4.jpg?source=c8b7c179","badge":[],"name":"apin","url":"http:\u002F\u002Fwww.zhihu.com\u002Fapi\u002Fv4\u002Fpeople\u002Fbc51b4f9dcb0d1a2c7bc45264f487d36","gender":1,"userType":"people","urlToken":"apin","isAdvertiser":false,"avatarUrl":"https:\u002F\u002Fpic4.zhimg.com\u002F85d2fe422c461502ced66225564ab9f4_l.jpg?source=c8b7c179","isOrg":false,"headline":"产品设计师","type":"people","id":"bc51b4f9dcb0d1a2c7bc45264f487d36"},"url":"http:\u002F\u002Fwww.zhihu.com\u002Fapi\u002Fv4\u002Fquestions\u002F19932946","title":"对于“无UI是UI设计的最高境界”这句话你怎么看？","answerCount":44,"created":1322297069,"questionType":"normal","followerCount":112,"updatedTime":1322297069,"type":"question","id":19932946}
    get_answer(html_data)

    ## 循环小鹿的回答，每一页中含有20条小鹿的回答
    soup = BeautifulSoup(html_data, 'lxml')
    next_link = soup.find_all('button', class_="Button PaginationButton PaginationButton--current Button--plain")
    if len(next_link) != 0:
        print("第" + str(page) + "页数据爬取完毕！")
        page += 1
        time.sleep(random.randint(1, 2))
        zhihu_ans(page)
    else:
        print("所有数据爬取完毕！")

    # 4、数据保存，此时直接使用final_data即可，因为是全局变量，而且已经在get_final_data中已经获得到了数据
    get_save(final_data)

    return