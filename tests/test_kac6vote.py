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

from mock import patch

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
    assert '7pairs (Jun-ya HASEBA)' in actual
