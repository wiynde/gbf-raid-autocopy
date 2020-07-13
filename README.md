![demo](images/demo.png) 

# グラブルTwitter救援検索ツール on Command Line

コマンドラインで動くグラブルTwitter救援検索ツール．  
指定したマルチバトルの救援依頼ツイートを取得し，参戦IDを自動でクリップボードにコピーします．  
IDをコピーするためのクリック動作が不要なため，同種の<strong>Webアプリよりクリック1回分早い</strong>です．  
2019.12.29現在，WindowsとmacOSに対応しています．

this repo cloned from <https://github.com/bookii/gbf-rapid-search>

## 使用方法

```
python search.py <level>-<name> [-e] [--help]
python search.py <short_name> -s [-e] [--help]
```
+ `-s, --short`オプションは，[search_ext.json](search_ext.json)の`shorts`に登録したクエストに名前を付け，その名前を指定することで検索を開始します．
    + ゴブロとかgoburoとか登録しておけば楽になるって感じです．
    + 四大天司ＨＬ等のレベル表示がないクエストはlevel=""とします．
        + 例) `"4": { "level":"", "name":"四大天司ＨＬ" }`
+ `-e, --exclude`オプションは，[search_ext.json](search_ext.json)の`excludes`に登録した名前またはスクリーンネームを持つアカウントのツイートをコピー対象から外します．
    + 要するに自分のスクリーンネームを書いておけば，出力には表示されますが，自発したクエストはコピーされないようになります．

### 例

```
python search.py 120-ゴッドガード・ブローディア
python search.py goburo -s
```
+ 取得したツイートがコマンドラインに表示され，同時に参戦IDがクリップボードにコピーされます．
+ 終了するときは`Ctrl+C`を押してください．

## 必要なもの
+ Python3.x

## 準備

### ライブラリのインストール
```
pip install requests_oauthlib
```

### Consumer Keyの取得
1. Twitterにログイン後，https://apps.twitter.com にアクセスして「Create New App」をクリック．
![apps_twitter_1](images/apps_twitter_1.png)  

2. 下のような画面が出てくるので，入力して「Create your Twitter application」をクリック．
![apps_twitter_2](images/apps_twitter_2.png)

   + Name  
   何でも構いませんが，他のアプリケーションと重複しないようにする必要があります．

   + Description  
   認証画面で出てくる説明文．本ツールは認証画面を持たないので適当で大丈夫です．
   
   + Website  
   本ツールはWebアプリではないので適当に．

   + Callback URL  
   空白で大丈夫です．  

3. 「Keys and Access Tokens」タブより「Consumer Key」「Consumer Secret」を取得．さらに「Create my access token」をクリックすると「Access Token」「Access Token Secret」を取得できる．  
![apps_twitter_3](images/apps_twitter_3.png)
これら4つのパラメータを`search.py`内の`consumer_key`以下4つのプレースホルダーと入れ替える．  

+ Permissionについて  
ツイートを取得するだけなのでRead onlyで構いません．
![apps_twitter_4](images/apps_twitter_4.png)

## その他
+ 日本語のみの対応です．
+ 2018年6月20日にUser StreamsなどいくつかのAPIを廃止するという[Twitter社のアナウンス](https://blog.twitter.com/developer/ja_jp/topics/tools/2017/aaa.html)がありましたが，本ツールが使用しているPublic Streamsは存続すると思われます．