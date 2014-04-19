# -*- coding: utf8 -*-

import requests

from xml.etree import ElementTree as ET

from i3pystatus import IntervalModule
from i3pystatus.core.util import internet, require



class ngb(IntervalModule):

    settings = ('username', 'password')

    required = ("username", "password")

    def init(self):
        self.interval = 30

        self.session = requests.session()

        self.login()


    def login(self):
        """
        log in method for VB"
        """
        url = 'https://ngb.to/login.php?do=login'

        params = {'do': 'login'}
        payload = {'vb_login_username':self.username,
                   'vb_login_password':self.password,
                   'url':"index.php",
                   'do':"login",
                   'vb_login_md5password':"",
                   'vb_login_md5password_utf':"",
                   's':"",
                   'securitytoken':"guest",
                   'cookieuser':"1"}

        self.session.post(url, data=payload, params=params)

    def get_usercp_xml(self,):
        """
        method for getting usercp in xml
        """
        response = self.session.get('https://ngb.to/usercp.php?type=xml')
        return response.text

    def parse_usercp_xml(self):
        """
        parsing usercp xml
        """
        xml = self.get_usercp_xml()
        tree = ET.fromstring(xml)
        parsed = {}

        element = tree.find('subscriptions')
        parsed['new_post_count'] = element.attrib['count']

        element = tree.find('messages')
        parsed['new_pn_count'] = element.attrib['count']

        element = tree.find('friends')
        parsed['new_friends'] = element.attrib['count']

        element = tree.find('subscribedforums/group')
        parsed['new_annos'] = element.attrib['count']

        return parsed

    @require(internet)
    def run(self):
        """
        status infor for ngb new posts in subs etc
        """
        parsed = self.parse_usercp_xml()

        text = ''

        if parsed['new_post_count'] != '0':
            text += 'P:{} '.format(parsed['new_post_count'])

        if parsed['new_pn_count'] != '0':
            text += 'PN:{} '.format(parsed['new_pn_count'])

        if parsed['new_annos'] != '0':
            text += 'AN:{} '.format(parsed['new_annos'])

        if parsed['new_friends'] != '0':
            text += 'FR:{} '.format(parsed['new_friends'])

        if text != '':
            text = 'NGB: ' + text

        self.output  = {'full_text':text.strip(), 'name': 'NGB',}
