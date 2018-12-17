#!/usr/local/bin python
# coding=utf-8
# @Time    : 2018/12/17 下午4:29
# @Author  : lifangyi
# @File    : selenium_worker.py
# @Software: PyCharm


# 元素加载的方式 不适用于静态
# 选择webdriver方式
# 慢，易损
# 但动态，不会被针对。


from selenium import webdriver
import pandas as pd
import time

PATH = 'drivers/geckodriver'
global_table = []


def exchange_loader(url):

    fx = webdriver.Firefox(executable_path=PATH)
    fx.get(url)
    fx.refresh()
    fx.maximize_window()
    time.sleep(0.01)
    table = fx.find_element_by_class_name('ivu-table-body')
    # 加载表格
    table.click()
    # 获取每一页的行
    rows = table.find_elements_by_class_name('ivu-table-row')
    for row in rows:
        # 获取每一行的列
        tds = row.find_elements_by_tag_name('td')
        # index=tds[0].text
        # 平台
        platform = tds[1].find_element_by_tag_name('a').text
        # 成交额
        sum = tds[2].find_element_by_tag_name('span').text
        # 对数
        logn = tds[3].find_element_by_tag_name('span').text
        # 地区
        region = tds[4].find_element_by_tag_name('span').text
        types = tds[5].find_elements_by_tag_name('i')
        type_strs = []
        for type in types:
            tcls = str(type.get_attribute('class')).split('-')[1]
            if tcls == 'future':
                type_strs.append('支持期货交易')
            elif tcls == 'spot':
                type_strs.append('支持现货交易')
            elif tcls == 'otc':
                type_strs.append('支持场外交易')
        # 类型
        type = ('/').join(type_strs)
        star_elements = tds[6].find_elements_by_tag_name('i')
        # 评级
        stars = 0
        for se in star_elements:
            sattr = se.get_attribute('class')
            if sattr == 'icon-star-full':
                stars += 1

        followers = tds[7].find_element_by_tag_name('span').text

        global_table.append(
            [platform, sum, logn, region, type, stars, followers])

    fx.close()


def market_loader(url):

    fx = webdriver.Firefox(executable_path=PATH)
    fx.get(url)
    fx.refresh()
    fx.maximize_window()
    time.sleep(0.01)
    table = fx.find_element_by_class_name('ivu-table-body')
    # 加载表格
    table.click()
    # 获取每一页的行
    rows = table.find_elements_by_class_name('ivu-table-row')
    for row in rows:
        # 获取每一行的列
        tds = row.find_elements_by_tag_name('td')
        # 币种
        currency = tds[1].find_element_by_tag_name('span').text
        # 流通市值
        value = tds[2].find_element_by_tag_name('span').text
        # 全球指数
        glog = tds[3].find_element_by_tag_name('span').text
        # 24H成交额
        sum = tds[4].find_element_by_tag_name('span').text
        # 流通数量
        flow = tds[5].find_element_by_tag_name(
            'span').find_element_by_tag_name('span').text
        # 24H涨幅
        trend = tds[6].find_element_by_tag_name('span').text

        global_table.append(
            [currency, value, glog, sum, flow, trend])

    fx.close()


def hot_loader(url):

    fx = webdriver.Firefox(executable_path=PATH)
    fx.get(url)
    fx.refresh()
    fx.maximize_window()
    time.sleep(0.01)
    table = fx.find_element_by_class_name('ivu-table-body')
    # 加载表格
    table.click()
    # 获取每一页的行
    rows = table.find_elements_by_class_name('ivu-table-row')
    for row in rows:
        # 获取每一行的列
        tds = row.find_elements_by_tag_name('td')
        # 币种
        currency = tds[1].find_element_by_tag_name('span').text
        # 流通市值
        value = tds[2].find_element_by_tag_name('span').text
        # 全球指数
        glog = tds[3].find_element_by_tag_name('span').text
        # 24H成交额
        sum = tds[4].find_element_by_tag_name('span').text
        # 流通数量
        flow = tds[5].find_element_by_tag_name('span').text
        # 24H涨幅
        trend = tds[6].find_element_by_tag_name('span').text

        global_table.append(
            [currency, value, glog, sum, flow, trend])

    fx.close()


def history_loader(url):

    fx = webdriver.Firefox(executable_path=PATH)
    fx.get(url)
    fx.refresh()
    fx.maximize_window()
    time.sleep(0.01)
    table = fx.find_element_by_class_name('ivu-table-body')
    # 加载表格
    table.click()
    # 获取每一页的行
    rows = table.find_elements_by_class_name('ivu-table-row')
    for row in rows:
        # 获取每一行的列
        tds = row.find_elements_by_tag_name('td')
        # 币种
        currency = tds[1].find_element_by_tag_name('span').text
        # 全球指数
        glog = tds[2].find_element_by_tag_name('span').text
        # 历史高位
        high = tds[3].find_element_by_tag_name('span').text
        # 高位时间
        high_time = tds[4].find_element_by_tag_name('span').text
        # 历史低位
        low = tds[5].find_element_by_tag_name('span').text
        # 低位时间
        low_time = tds[6].find_element_by_tag_name('span').text
        # ATH跌幅
        ath_drop = tds[7].find_element_by_tag_name('span').text
        global_table.append(
            [currency, glog, high, high_time, low, low_time, ath_drop])

    fx.close()


def csv_writer(table, filename, columns):
    df = pd.DataFrame(
        table,
        columns=columns)

    df.to_csv(filename, index=False)


def url_gen(base_url, num):
    urls = []
    urls.append(base_url)
    for i in range(2, num + 1):
        url = base_url + '?page={}'.format(i)
        urls.append(url)
    return urls


def currency_url_gen(start_url, num):
    urls = []
    base = 'https://www.feixiaohao.com/'
    urls.append(start_url)
    for i in range(2, num + 1):
        url = base + 'list_{}.html'.format(i)
        urls.append(url)
    return urls


def template_url_gen(base_url, num):
    urls = []
    urls.append(base_url)
    for i in range(2, num + 1):
        url = base_url + 'list_{}.html'.format(i)
        urls.append(url)
    return urls


if __name__ == '__main__':

    交易平台数据
    base_url = 'https://www.feixiaohao.com/exchange/'
    N = 6
    urls = url_gen(base_url, N)
    for url in urls:
        exchange_loader(url)
    filename = 'exchange.csv'
    columns = ['交易平台', '24H成交额', '交易对数量', '国家/地区', '交集类型', '评级', '关注数']
    csv_writer(global_table, filename, columns)
    global_table.clear()

    # 行情 - 货币数据
    base_url = 'https://www.feixiaohao.com/currencies/'
    N = 25
    urls = currency_url_gen(base_url, N)
    for url in urls:
        market_loader(url)
    filename = 'market-currency.csv'
    columns = ['币种', '流通市值', '全球指数', '24H成交额', '流通数量', '24H涨幅']
    csv_writer(global_table, filename, columns)
    global_table.clear()

    # 行情 - 代币数据
    base_url = 'https://www.feixiaohao.com/assets/'
    N = 15
    urls = template_url_gen(base_url, N)
    for url in urls:
        market_loader(url)
    filename = 'market-asset.csv'
    columns = ['币种', '流通市值', '全球指数', '24H成交额', '流通数量', '24H涨幅']
    csv_writer(global_table, filename, columns)
    global_table.clear()

    # 行情 - 热搜数据
    url = 'https://www.feixiaohao.com/hotsearch/'
    hot_loader(url)
    filename = 'market-hotsearch.csv'
    columns = ['币种', '流通市值', '全球指数', '24H成交额', '流通数量', '24H涨幅']
    csv_writer(global_table, filename, columns)
    global_table.clear()

    # 行情 - 历史高位数据
    url = 'https://www.feixiaohao.com/ath/'
    history_loader(url)
    filename = 'market-history.csv'
    columns = ['币种', '全球指数', '历史高位', '高位时间', '历史低位', '低位时间', 'ATH跌幅']
    csv_writer(global_table, filename, columns)
    global_table.clear()
