#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2017-2019 Jun-ya HASEBA
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

from __future__ import unicode_literals

import gzip
import os

from mock import patch
import requests

from kac6vote import kac6vote


def test_windows_31j_should_return_shift_jis_codec_when_codec_name_is_windows_31j():
    """
    コーデック名に'windows-31j'を指定したとき、_windows_31j()がShift_JISのコーデックを返却すること。
    """
    actual = kac6vote._windows_31j('windows-31j')
    assert actual.name == 'shift_jis'


def test_windows_31j_should_return_none_when_codec_name_is_utf_8():
    """
    コーデック名に'utf-8'を指定したとき、_windows_31j()がNoneを返却すること。
    """
    actual = kac6vote._windows_31j('utf-8')
    assert actual is None


@patch('browsercookie.firefox')
def test_get_cookie_jar_should_return_firefox_cookie_jar_when_browser_name_is_firefox(mock_firefox):
    """
    ブラウザ名に'firefox'を指定したとき、_get_cookie_jar()がFirefoxのCookieJarを返却すること。
    """
    mock_firefox.return_value = 'firefox_cookie_jar'
    actual = kac6vote._get_cookie_jar('firefox')
    assert actual == 'firefox_cookie_jar'


@patch('browsercookie.chrome')
def test_get_cookie_jar_should_return_chrome_cookie_jar_when_browser_name_is_chrome(mock_chrome):
    """
    ブラウザ名に'chrome'を指定したとき、_get_cookie_jar()がChromeのCookieJarを返却すること。
    """
    mock_chrome.return_value = 'chrome_cookie_jar'
    actual = kac6vote._get_cookie_jar('chrome')
    assert actual == 'chrome_cookie_jar'


@patch('browsercookie.chrome')
def test_get_cookie_jar_should_return_chrome_cookie_jar_when_browser_name_is_safari(mock_chrome):
    """
    ブラウザ名に'safari'を指定したとき、_get_cookie_jar()がChromeのCookieJarを返却すること。
    """
    mock_chrome.return_value = 'chrome_cookie_jar'
    actual = kac6vote._get_cookie_jar('safari')
    assert actual == 'chrome_cookie_jar'


@patch('browsercookie.chrome')
def test_get_cookie_jar_should_return_chrome_cookie_jar_when_browser_name_is_none(mock_chrome):
    """
    ブラウザ名を指定しなかったとき、_get_cookie_jar()がChromeのCookieJarを返却すること。
    """
    mock_chrome.return_value = 'chrome_cookie_jar'
    actual = kac6vote._get_cookie_jar()
    assert actual == 'chrome_cookie_jar'


def test_get_html_should_return_github_html_when_url_is_github_url():
    """
    GitHubのURLを指定したとき、_get_html()がGitHubのHTMLを返却すること。
    """
    actual = kac6vote._get_html('https://github.com/7pairs')
    assert b'7pairs (Jun-ya HASEBA)' in actual


def test_get_login_player_name_should_return_player_name_when_html_is_vote_page():
    """
    投票ページのHTMLを指定したとき、_get_login_player_name()がプレイヤー名を返却すること。
    """
    actual = kac6vote._get_login_player_name(_get_vote_page_html())
    assert actual == 'ＤＨシアンフロこ'


def test_get_login_player_name_should_return_none_when_html_is_github_page():
    """
    GitHubのHTMLを指定したとき、_get_login_player_name()がNoneを返却すること。
    """
    response = requests.get('https://github.com/7pairs')
    github_html = response.text.encode(response.encoding)
    actual = kac6vote._get_login_player_name(github_html)
    assert actual is None


def test_get_players_should_return_player_value_objects_when_html_is_vote_page():
    """
    投票ページのHTMLを指定したとき、_get_players()が賢闘士情報のバリューオブジェクトを返却すること。
    """
    actual = kac6vote._get_players(_get_vote_page_html())
    assert len(actual) == 16
    assert actual[0] == kac6vote.Player('ウエスト', '1')
    assert actual[1] == kac6vote.Player('ザキヤマ', '2')
    assert actual[2] == kac6vote.Player('リゾットカーン', '3')
    assert actual[3] == kac6vote.Player('チョーネンテン', '4')
    assert actual[4] == kac6vote.Player('カムカム', '5')
    assert actual[5] == kac6vote.Player('あいあんメィデア', '6')
    assert actual[6] == kac6vote.Player('ぼーしぱん', '7')
    assert actual[7] == kac6vote.Player('パーシヴァル', '8')
    assert actual[8] == kac6vote.Player('いせノウミ', '9')
    assert actual[9] == kac6vote.Player('うさまどれーぬ', '10')
    assert actual[10] == kac6vote.Player('イズミ', '11')
    assert actual[11] == kac6vote.Player('むつきとおこ', '12')
    assert actual[12] == kac6vote.Player('きたがわＫこ', '13')
    assert actual[13] == kac6vote.Player('すやあ', '14')
    assert actual[14] == kac6vote.Player('にゃる', '15')
    assert actual[15] == kac6vote.Player('ＰＡＲＡＮＯＩＡ', '16')


@patch('requests.post')
@patch('time.sleep')
def _test_vote_should_call_post_120_times_when_players_size_is_16(mock_post, mock_sleep):
    """
    16人ぶんの賢闘士情報を指定したとき、_vote()内でPOST処理が120回実行されること。
    """
    kac6vote._vote([kac6vote.Player('プレイヤー%02d' % i, str(i)) for i in range(16)], kac6vote._VOTE_PAGE_URL)
    assert mock_post.call_count == 120
    assert mock_sleep.call_args == (kac6vote._WAIT_AFTER_VOTE,)


def _get_vote_page_html():
    """
    テスト用の投票ページのHTMLを取得する。

    :return: 投票ページのHTML
    :rtype: str
    """
    # テスト用の投票ページのHTMLを返却する
    with gzip.open(os.path.join(os.path.dirname(__file__), 'vote_page.html.gz'), 'rb') as f:
        return f.read()
