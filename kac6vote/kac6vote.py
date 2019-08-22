#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2017-2019 HASEBA Junya
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Tool for voting on QMA Japan Tour 2016 Grand Slam Derby.

Usage:
  kac6vote [-b <browser>]
  kac6vote -h | --help
  kac6vote -v | --version

Options:
  -b <browser>  chrome or firefox [default: chrome].
  -h --help     print this help message and exit.
  -v --version  print the version number and exit.
"""

from __future__ import print_function
from __future__ import unicode_literals

import codecs
import collections
import itertools
import sys
import time

import browsercookie
import bs4
import docopt
import requests

from . import __version__


# 投票ページのURL
_VOTE_PAGE_URL = 'http://p.eagate.573.jp/game/qma/12/p/qt/setkac.html'

# コンソールの文字コード
_CONSOLE_ENCODE = 'shift_jis' if sys.platform == 'win32' else 'utf-8'

# 投票後のウェイト(秒)
_WAIT_AFTER_VOTE = 1


# 21世紀に入って16年が過ぎたというのにまさかのShift_JIS対応
def _windows_31j(codec_name):
    """
    Windows-31J用の検索関数。
    一番近いと思われるShift_JISにマッピングする。

    :param codec_name: コーデック名
    :type codec_name: str
    :return: Windows-31Jが指定された場合はShift_JIS、それ以外の場合はNone
    :rtype: codecs.CodecInfo
    """
    # Windows-31JをShift_JISにマッピングする
    if codec_name.lower() == 'windows-31j':
        return codecs.lookup('shift_jis')
    else:
        return None

# Windows-31J用の検索関数を登録する
codecs.register(_windows_31j)


# 賢闘士の情報を格納するバリューオブジェクト
Player = collections.namedtuple('Player', ['name', 'value'])


def main():
    """
    「QMAジャパンツアー2016 グランドスラムダービー」のすべての組み合わせに投票する。
    eAMUSEMENTにはブラウザのCookieを利用してログインするため、実行前にブラウザでのログインが必要。
    """
    # CookieJarを取得する
    args = docopt.docopt(__doc__, version=__version__)
    cookie_jar = _get_cookie_jar(args.get('-b'))

    # 投票ページのHTMLを取得する
    vote_page_html = _get_html(_VOTE_PAGE_URL, cookie_jar)

    # ログインユーザー名を取得する
    login_player_name = _get_login_player_name(vote_page_html)
    if not login_player_name:
        print('ブラウザでeAMUSEMENTにログインしてから起動してください。')
        exit()

    # 確認メッセージを表示する
    message = login_player_name + 'さんのアカウントで投票します (y/n) : '
    if input(message.encode(_CONSOLE_ENCODE)).strip().lower() != 'y':
        exit()

    # 賢闘士の情報を取得する
    players = _get_players(vote_page_html)

    # すべての組み合わせに投票する
    _vote(players, _VOTE_PAGE_URL, cookie_jar)

    # 正常終了
    print('投票が完了しました！')


def _get_cookie_jar(browser_name=None):
    """
    指定されたブラウザのCookieJarを取得する。

    :param browser_name: ブラウザ名
    :type browser_name: str
    :return: CookieJar
    :rtype: cookielib.CookieJar
    """
    # 指定されたブラウザのCookieJarを返却する
    if browser_name == 'firefox':
        return browsercookie.firefox()
    else:
        return browsercookie.chrome()


def _get_html(url, cookie_jar=None):
    """
    指定されたURLのHTMLを取得する。

    :param url: URL
    :type url: str
    :param cookie_jar: CookieJar
    :type cookie_jar: cookielib.CookieJar
    :return: HTML
    :rtype: str
    """
    # 指定されたURLのHTMLを返却する
    response = requests.get(url, cookies=cookie_jar)
    return response.text.encode(response.encoding)


def _get_login_player_name(html):
    """
    指定されたHTMLからログインユーザー名を抽出する。

    :param html: 投票ページのHTML
    :type html: str
    :return: ログインユーザー名
    :rtype: str
    """
    # ログインユーザー名を返却する
    soup = bs4.BeautifulSoup(html, 'html.parser')
    player_name_box = soup.find('div', {'class': 'player_name_box'})
    if player_name_box:
        return player_name_box.text.strip()
    else:
        return None


def _get_players(html):
    """
    指定されたHTMLから賢闘士の情報を抽出する。

    :param html: 投票ページのHTML
    :type html: str
    :return: 賢闘士の情報
    :rtype: list
    """
    # 賢闘士の情報を返却する
    soup = bs4.BeautifulSoup(html, 'html.parser')
    select = soup.find('select', {'name': 'vote0'})
    options = select.find_all('option')
    return [Player(name=option.text.strip(), value=option['value'].strip()) for option in options]


def _vote(players, url, cookie_jar=None):
    """
    指定された賢闘士の情報をもとに、すべての組み合わせに投票する。

    :param players: 賢闘士の情報
    :type players: list
    :param url: 投票ページのURL
    :type url: str
    :param cookie_jar: CookieJar
    :type cookie_jar: cookielib.CookieJar
    """
    # すべての組み合わせに投票する
    for quinella in itertools.combinations(players, 2):
        print(quinella[0].name, '-', quinella[1].name, 'に投票しています...')
        requests.post(url, {'vote0': quinella[0].value, 'vote1': quinella[1].value}, cookies=cookie_jar)
        time.sleep(_WAIT_AFTER_VOTE)


# メイン処理を呼び出す
if __name__ == '__main__':
    main()
