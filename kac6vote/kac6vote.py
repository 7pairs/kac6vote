#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2017 Jun-ya HASEBA
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

import codecs
import collections
import itertools
import sys
import time

import browsercookie
import bs4
import docopt
import requests


# バージョン番号
VERSION = '1.0.0'

# 投票ページのURL
VOTE_PAGE_URL = 'http://p.eagate.573.jp/game/qma/12/p/qt/setkac.html'

# コンソールの文字コード
CONSOLE_ENCODE = 'shift_jis' if sys.platform == 'win32' else 'utf-8'

# 投票後のウェイト(秒)
WAIT_AFTER_VOTE = 1


# 21世紀になって16年が過ぎたというのにまさかのShift_JIS対応
def windows31j(name):
    """
    Windows-31J用の検索関数。
    厳密には一致しないが、仕方なくShift_JISにマッピングする。

    :param name: コーデック名
    :type name: str
    :return: Windows-31Jが指定された場合はShift_JIS, それ以外の場合はNone
    :rtype: codecs.CodecInfo
    """
    # Windows-31JをShift_JISにマッピングする
    if name.lower() == 'windows-31j':
        return codecs.lookup('shift_jis')
    else:
        return None

# Windows-31J用の検索関数を登録
codecs.register(windows31j)


# 賢闘士の情報を格納するバリューオブジェクト
Player = collections.namedtuple('Player', ['name', 'value'])


def main():
    """
    「QMAジャパンツアー2016 グランドスラムダービー」のすべての組み合わせに投票する。
    スクリプトでは画像認証を突破できないので、ブラウザのCookieを利用してログインする。
    """
    # Cookie取得対象のブラウザを決定する
    args = docopt.docopt(__doc__, version=VERSION)
    if args.get('-b') == 'firefox':
        cookie_jar = browsercookie.firefox()
    else:
        cookie_jar = browsercookie.chrome()

    # 投票ページのHTMLを取得する
    response = requests.get(VOTE_PAGE_URL, cookies=cookie_jar)

    # ログインユーザー名を取得する
    soup = bs4.BeautifulSoup(response.text.encode(response.encoding), 'html.parser')
    player_name_box = soup.find('div', {'class': 'player_name_box'})
    if not player_name_box:
        print u'指定のブラウザでログインしてから実行してください'
        exit()
    player_name = player_name_box.text.strip()

    # 確認メッセージを表示する
    message = player_name + u'さんのアカウントで投票します (Y/n) : '
    if raw_input(message.encode(CONSOLE_ENCODE)).strip().lower() != 'y':
        exit()

    # 賢闘士の情報を取得する
    select = soup.find('select', {'name': 'vote0'})
    options = select.find_all('option')
    players = [Player(name=option.text.strip(), value=option['value'].strip()) for option in options]

    # すべての組み合わせに投票する
    for quinella in itertools.combinations(players, 2):
        print quinella[0].name, '-', quinella[1].name, u'に投票しています...'
        requests.post(VOTE_PAGE_URL, {'vote0': quinella[0].value, 'vote1': quinella[1].value}, cookies=cookie_jar)
        time.sleep(WAIT_AFTER_VOTE)

    # 正常終了
    print u'投票が完了しました！'


# メイン処理を呼び出す
if __name__ == '__main__':
    main()
