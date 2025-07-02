# きなCスレ アーカイブ

したらば掲示板のdatファイルからHTMLへの変換ツールを使用して、
掲示板ごと消えて見れなくなってしまったきなCスレのアーカイブをGitHub Pagesで公開しています。

## フォルダ構成

```
kinac/
├── src/                        # ソースコード
│   └── dat_to_html.py          # 変換スクリプト
├── data/                       # 入力データ（.gitignoreで除外）
│   └── *.dat                   # したらば掲示板のdatファイル
├── docs/                       # Github Pages公開用
│   ├── index.html              # アーカイブ目次ページ
│   ├── 11188_1716630941.html   # CEOがお風呂上がったらLiella!に誘おうかなと考えていたきな子 ★5.2
│   ├── 11188_1719834146.html   # CEOがお風呂上がったらLiella!に誘おうかなと考えていたきな子 ★5.3
│   ├── 11210_1728179793.html   # CEOがお風呂上がったらLiella!に誘うと決めていたきな子 避難所★5.3
│   └── 11210_1734842930.html   # CEOがお風呂上がったらLiella!に誘うと決めていたきな子 避難所★6
├── .gitignore                  # Git除外設定
└── README.md                   # このファイル
```

## 使用方法

ツールを利用する人はいないと思いますが、残しておきます。

### 基本的な使い方

```bash
python3 src/dat_to_html.py data/your_file.dat
```

### 出力ファイル名を指定

```bash
python3 src/dat_to_html.py data/your_file.dat docs/custom_name.html
```

### 例

```bash
# datファイルを変換（自動ファイル名）
python3 src/dat_to_html.py data/jbbs.livedoor.jp%2Fanime%2F11188_1716630941.dat

# 出力: 11188_1716630941.html
```

## GitHub Pages での公開

生成されたHTMLファイルはGitHub Pagesで直接公開できます：

1. GitHubリポジトリにHTMLファイルをアップロード
2. Settings → Pages で公開設定
3. `https://username.github.io/repository-name/11188_1716630941.html` でアクセス可能

## 必要な環境

- Python 3.6以上
- 標準ライブラリのみ使用（追加インストール不要）

## 更新履歴

- **v1.0.0** - 初回作成
