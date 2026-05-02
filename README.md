# pygames
pygame を使ったサンプル集です。

## Linux コマンド

```
cd ..    <== 親ディレクトリに移動
cd 名前  <== 指定したディレクトリに移動 
pwd      <== 現在のディレクトリを表示
ls       <== ファイル一覧を表示
```

## pygame モジュールのインストール
```
pip install pygame
```

## クローン：github のリポジトリ（プロジェクト）を自分の端末にコピーする
```
git clone https://github.com/jcodeorg/pygames
```

## プル：github のリポジトリから最新状態を取得して更新する
```
git pull
```

## スタッシュ＆プル：修正中のファイルをスタッシュ（一旦退避）して、github のリポジトリから最新状態を取得更新し、そして退避したファイルを戻す
```
git stash
git pull
git stash pop
```

## ディレクトリ構成
```
pygames
│      
├─breakout      # ブロック崩し
│      main.py
│      
├─dialogbox     # ダイアログボックス
│      main.py
│      NotoSansJP-Regular.ttf
│      
├─moving        # 上下左右に動かす（シンプル版）
│      main.py
│      
├─moving2       # ２つのオブジェクトを上下左右に動かす
│      main.py
│      
├─platformer    # プラットフォーマー
│      main.py
│      neko.png
│      
├─shooting      # シューティング
│      main.py
│      
├─shooting2     # シューティング2
│      main.py
│      
├─tetris        # テトリス
│      main.py
│      
├─tetris2       # テトリス2
│      main.py
│      
└─text          # 文字の表示
        main.py
```