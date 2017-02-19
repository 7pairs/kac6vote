# kac6vote

## 概要

"kac6vote" は [QMAジャパンツアー2016 グランドスラムダービー](http://p.eagate.573.jp/game/qma/12/p/qt/setkac.html) の全組み合わせ120通りを自動で投票するためのツールです。
コナミ様におかれましては、今後はUIの抜本的な見直しを実施していただき、私が来年 "kac7vote" というツールを作る必要がなくなっていることを強く願っています。

## 動作環境

Python2.7での動作を確認しています。OSはMac、Linux、Windows、ブラウザはChrome、Firefoxで動くことになっていますが、Mac＋Chromeの組み合わせでのみ動作を確認しています。

## インストール

同梱の `setup.py` を実行してください。

```console
$ python setup.py install
```

pipを利用して、GitHubから直接インストールすることもできます。

```console
$ pip install git+https://github.com/7pairs/kac6vote.git
```

## 実行方法

### 前準備

ChromeもしくはFirefoxでeAMUSEMENTにログインしてください。

### プログラム起動

```console
$ kac6vote [-b <browser>]
```

`<browser>` には `chrome` もしくは `firefox` を指定します。先ほどログインしたブラウザを指定してください。
`-b` オプションを省略すると `chrome` を指定したことになります。 `-b` オプションに `chrome` 、 `firefox` 以外の文字列を指定しても `chrome` を指定したことになります。

## ライセンス

kac6voteは [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0) にて提供します。
