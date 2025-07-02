# 使用方法ガイド

## 基本的な使い方

### 1. datファイルの準備

したらば掲示板のdatファイルを`data/`フォルダに配置します。

### 2. 変換実行

```bash
# 基本的な変換
python3 src/dat_to_html.py data/your_file.dat

# 出力ファイル名を指定
python3 src/dat_to_html.py data/your_file.dat output/custom_name.html
```

### 3. 結果の確認

生成されたHTMLファイルが`output/`フォルダまたは指定した場所に保存されます。

## 高度な使用方法

### GitHub Pages での公開

1. GitHubリポジトリを作成
2. 生成されたHTMLファイルをアップロード
3. Settings → Pages で公開設定
4. URLでアクセス可能

### バッチ処理

複数のdatファイルを一括変換する場合：

```bash
#!/bin/bash
for file in data/*.dat; do
    python3 src/dat_to_html.py "$file"
done
```

## トラブルシューティング

### よくある問題

**Q: 文字化けが発生する**
A: datファイルがEUC-JP以外のエンコーディングの可能性があります。

**Q: 画像が表示されない**
A: 画像URLが無効、またはサーバーがアクセスを制限している可能性があります。

**Q: アンカーリンクが動作しない**
A: JavaScriptが無効になっているか、ブラウザの制限による可能性があります。