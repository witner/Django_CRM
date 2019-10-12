#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入系统模块

# 第三方模块

# 导入自定义模块

# 设置环境变量


class Pagination(object):
    def __init__(self, page, url_base, url_params, data_count, entries=10, show_pages=5):
        """
        分页初始化
        :param page: 当前页码
        :param url_base: 请求的URL基础部分
        :param url_params: 请求的URL参数部分
        :param data_count: 请求的数据总条数
        :param entries: 每页显示的记录条目数
        :param show_pages: 页码显示的页码，正负操作
        """
        self.url_base = url_base
        try:
            self.page = int(page)
            # 如果页码数小于等于0，取1
            if self.page <= 0:
                raise Exception()
        except Exception as e:
            self.page = 1
        self.url_params = url_params
        self.page = page  # 页码第X页
        self.entries = entries  # 每页显示条目数量

        self.page_count, r = divmod(data_count, entries)  # 页码的总数，根据记录总数和每页显示条目计算得出, 如果余数不为0，需增加一页
        if r != 0:
            self.page_count += 1

        self.show_pages = show_pages

        # 根据当前页码，计算页码起始，如果当前页 - 页面范围 小于0 起始为1 ，否则为差值
        self.page_index_start = self.page - self.show_pages if self.page > self.show_pages else 1
        # 根据当前页码，计算页码结束，如果当前页码 + 页面范围 小于 页面总数，则取加值，否则取 页面总数
        self.page_index_end = self.page + self.show_pages if (self.page + self.show_pages) < self.page_count else self.page_count

    @property
    def data_index_start(self):
        """
        数据获取值起始索引
        :return:
        """
        return (self.page - 1) * self.entries

    @property
    def data_index_end(self):
        """
        数据获取值结束索引
        :return:
        """
        return self.page * self.entries

    def get_page_index_html(self, page_num, page_type='default'):

        self.url_params['page'] = page_num

        if page_type == 'default':
            if self.page == page_num:
                page_index_html = '<li class="active"><a href="%s?%s">%s</a></li>' \
                                  % (self.url_base, self.url_params.urlencode(), page_num)
            else:
                page_index_html = '<li><a href="%s?%s">%s</a></li>' \
                                  % (self.url_base, self.url_params.urlencode(), page_num)
        else:
            if page_type == 'first':
                icon = 'fa-step-backward'
            elif page_type == 'prev':
                icon = 'fa-angle-double-left'
            elif page_type == 'next':
                icon = 'fa-angle-double-right'
            elif page_type == 'last':
                icon = 'fa-step-forward'
            else:
                icon = ''
            page_index_html = '<li><a href="%s?%s"><i class="fa %s" aria-hidden="true"></i></a></li>' \
                              % (self.url_base, self.url_params.urlencode(), icon)

        return page_index_html

    def get_page_html(self):
        """
        生成分页的HTML页码
        效果 [
        每页数量 | 第一页  前一页  1 2 3 4 5 6 7 8 9  后一页  最后页
        |<<  <  11 12 13 14 15 16 17 18 19 20 21 >  >>|
        ]
        :return:
        """
        page_index_first = self.get_page_index_html(page_type='first', page_num=1)
        page_index_last = self.get_page_index_html(page_type='last', page_num=self.page_count)

        # 前一页，后一页设置
        if self.page <= 1:
            # 如果请求当前页码，小于等于 1，那么前一页的链接地址为当前页
            page_index_prev = self.get_page_index_html(page_type='prev', page_num=1)
            page_index_next = self.get_page_index_html(page_type='next', page_num=self.page + 1)
        elif self.page >= self.page_count:
            # 如果请求当前页码，是最后一页，那么下一页的链接地址为#
            page_index_prev = self.get_page_index_html(page_type='prev', page_num=self.page - 1)
            page_index_next = self.get_page_index_html(page_type='next', page_num=self.page_count)
        else:
            # 其他
            # 如果请求当前页码，大于1 ，那么前一页的前进地址为，当前页码-1，并将url参数带上
            page_index_prev = self.get_page_index_html(page_type='prev', page_num=self.page - 1)
            page_index_next = self.get_page_index_html(page_type='next', page_num=self.page + 1)

        #
        page_index_list = []
        page_index_list.extend([page_index_first, page_index_prev])

        for i in range(self.page_index_start, self.page_index_end + 1):
            page_index_t = self.get_page_index_html(page_num=i)
            page_index_list.append(page_index_t)

        page_index_list.extend([page_index_next, page_index_last])

        page_html_str = "".join(page_index_list)
        return page_html_str
