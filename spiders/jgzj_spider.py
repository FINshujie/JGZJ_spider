# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from scrapy.http import Request
from jgzj.items import JgzjbookItem

class JgzjSpiderSpider(scrapy.Spider):
    name = 'jgzj_spider'
    allowed_domains = ['bbs.pinggu.org/']
    start_urls = ['http://bbs.pinggu.org/']

    start_book_urls = ['http://bbs.pinggu.org/forum.php?mod=collection&action=view&ctid=3258&fromop=monthfollownum/']



    def parse(self, response):
        post_nodes=response.xpath('//a[@class = "xst "]/@href').extract()
        for post_node in post_nodes:
            post_url = post_node
            yield Request(url = parse.urljoin(response.url, post_url),callback=self.parse_detail,dont_filter=True)

        next_url = response.xpath('//a[@class = "nxt"]/@href').extract_first("")
        if next_url:
            yield Request(url = parse.urljoin(response.url, next_url),callback=self.parse,dont_filter=True)


    def parse_detail(self, response):
        Book_Item = JgzjbookItem()

        cover_img_url = response.xpath('//ignore_js_op[1]/img/@file').extract_first("")
        title = response.xpath('//td[@class="t_f"]/strong/font/text()').extract_first("")
        read_nums = response.xpath('//td[@class = "plc ptm pbn"]/div/em[1]/text()').extract_first("")
        comment_nums = response.xpath('//td[@class = "plc ptm pbn"]/div/em[2]/text()').extract_first("")

        Book_Item['title'] = title
        Book_Item['cover_img_url'] = [cover_img_url]
        Book_Item['cover_img_url_data'] = cover_img_url
        Book_Item['url'] = response.url
        Book_Item['read_nums'] = read_nums
        Book_Item['comment_nums'] = comment_nums


        yield Book_Item

    def start_requests(self):
        headers = {
            'Host':'bbs.pinggu.org',
            'Referer':'http://bbs.pinggu.org/member.php?mod=logging&action=login',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        # 局部header
        return [scrapy.Request(url='http://bbs.pinggu.org/member.php?mod=logging&action=login',
                               headers=headers,
                               callback= self.Login)]

    def Login(self,response):
        headers = {
            'Host': 'bbs.pinggu.org',
            'Referer': 'http://bbs.pinggu.org/member.php?mod=logging&action=login',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }

        response_text = response.text
        formhash_search = re.search('name="formhash" value="(.*?)"',response_text)
        formhash = ''
        if formhash_search:
            formhash = formhash_search.group(1)
        if formhash:
            post_url = 'http://bbs.pinggu.org/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=L70Wq&inajax=1'
            post_data = {
                'formhash':formhash,
                'username':'yinxingzheng',
                'password':'Wangsy520'
            }
            return [scrapy.FormRequest(
                url=post_url,
                formdata=post_data,
                headers=headers,
                callback=self.check_login,
                dont_filter=True
            )]

    def check_login(self,response):
        if '欢迎' in response.text:
            for url in self.start_book_urls:
                yield scrapy.Request(url=url,  dont_filter=True, callback=self.parse)
