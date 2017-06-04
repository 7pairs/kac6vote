# kac6vote

[![Build Status](https://travis-ci.org/7pairs/kac6vote.svg?branch=master)](https://travis-ci.org/7pairs/kac6vote)
[![Coverage Status](https://coveralls.io/repos/github/7pairs/kac6vote/badge.svg?branch=master)](https://coveralls.io/github/7pairs/kac6vote?branch=master)

## 概要

"kac6vote" は [QMAジャパンツアー2016 グランドスラムダービー](http://p.eagate.573.jp/game/qma/12/p/qt/setkac.html) の全組み合わせ120通りを自動で投票するツールです。
株式会社コナミアミューズメント様におかれましては、今後はユーザーインターフェイスを抜本的に見直していただき、来年は "kac7vote" といったツールを作る必要がなくなっていることを強く願っています。

## 動作環境

Python2.7での動作を確認しています。
OSはmacOS、Linux、Windows、ブラウザはChrome、Firefoxで動作すると思われますが、開発環境の都合によりmacOS + Chromeの組み合わせのみテストを実施しています。

## インストール

同梱の `setup.py` を実行してください。

```console
$ python setup.py install
```

pipを利用して、GitHubから直接インストールすることもできます。

```console
$ pip install git+https://github.com/7pairs/kac6vote.git
```

## 実行

### 前準備

ChromeもしくはFirefoxで[eAMUSEMENT](http://p.eagate.573.jp/)にログインしてください。

### 起動

```console
$ kac6vote [-b <browser>]
```

`<browser>` には `chrome` もしくは `firefox` を指定します。
前準備でログインに使用したブラウザを指定してください。
`-b` オプションを省略すると `chrome` を指定したものと見なします。
`-b` オプションに `chrome` 、 `firefox` 以外の文字列を指定しても `chrome` を指定したものと見なします。
打ち間違いにご注意ください。

## ライブラリ

kac6voteでは下記のライブラリを利用しています。

- [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4)
- [browsercookie](https://pypi.python.org/pypi/browsercookie)
- [docopt](https://pypi.python.org/pypi/docopt)
- [mock](https://pypi.python.org/pypi/mock)
- [pytest](https://pypi.python.org/pypi/pytest)
- [requests](https://pypi.python.org/pypi/requests)

## ライセンス

kac6voteは [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0) にて提供します。
