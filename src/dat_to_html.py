#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
したらば掲示板 datファイル to HTML 変換スクリプト
"""

import os
import re
import html
from datetime import datetime
from urllib.parse import unquote, urlparse


class ShitarabaDatParser:
    def __init__(self):
        self.posts = []
        self.thread_title = None
        
    def parse_dat_file(self, file_path):
        """datファイルを解析してポストデータを抽出"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # EUC-JPエンコーディングでデコード
            content = content.decode('euc-jp', errors='ignore')
            
            lines = content.strip().split('\n')
            
            for line in lines:
                if line.strip():
                    post = self.parse_post_line(line)
                    if post:
                        self.posts.append(post)
                        
        except Exception as e:
            print(f"エラー: {e}")
            return False
            
        return True
    
    def parse_post_line(self, line):
        """1行のポストデータを解析"""
        # したらば掲示板のdatファイル形式: 
        # レス番号<>投稿者名<>メール<>投稿日時<>投稿内容<>スレッドタイトル<>投稿者ID
        parts = line.split('<>')
        
        if len(parts) < 6:
            return None
            
        try:
            post = {
                'number': int(parts[0]),
                'name': self.clean_name(parts[1]),
                'mail': parts[2],
                'date': parts[3],
                'content': self.clean_content(parts[4]),
                'user_id': ''
            }
            
            # 7フィールドの場合（スレッドタイトル付き）
            if len(parts) >= 7:
                # 1番目の投稿からスレッドタイトルを抽出
                if post['number'] == 1 and parts[5].strip():
                    self.thread_title = parts[5].strip()
                post['user_id'] = parts[6] if len(parts) > 6 else ''
            # 6フィールドの場合（通常の2ch形式）
            elif len(parts) >= 6:
                post['user_id'] = parts[5]
                
            return post
        except (ValueError, IndexError):
            return None
    
    def clean_name(self, name):
        """投稿者名をクリーンアップ"""
        # HTMLタグを除去
        name = re.sub(r'<[^>]+>', '', name)
        # HTMLエンティティをデコード
        name = html.unescape(name)
        return name.strip()
    
    def clean_content(self, content):
        """投稿内容をクリーンアップ"""
        # /bbs/link.cgi?url= 形式のリンクを直接URLに変換（最初に実行）
        content = re.sub(r'<a href="/bbs/link\.cgi\?url=([^"]+)"([^>]*)>([^<]+)</a>', 
                        r'<a href="\1"\2 class="external-link">\3</a>', content)
        
        # 既存の内部アンカーリンク（<a href="#数字">&gt;&gt;数字</a>）を適切な形式に変換
        content = re.sub(r'<a href="#(\d+)">&gt;&gt;\d+</a>', 
                        lambda m: f'<a href="#post-{m.group(1)}" class="anchor-link">&gt;&gt;{m.group(1)}</a>', content)
        
        # HTMLエンティティをデコード
        content = html.unescape(content)
        
        # プレーンなURLをリンク化（http/httpsで始まるURL）
        content = re.sub(r'(?<!href=")(?<!src=")(https?://[^\s<>"\']+)', 
                        r'<a href="\1" target="_blank" class="external-link">\1</a>', content)
        
        # プレーンな >>数字 パターンを内部リンクに変換（HTMLエンティティデコード後）
        content = re.sub(r'>>(\d+)', r'<a href="#post-\1" class="anchor-link">>>\1</a>', content)
        
        return content.strip()
    
    def extract_images_from_content(self, content):
        """投稿内容から画像URLを抽出（重複を除去）"""
        # 通常の画像ファイル拡張子パターン
        image_pattern1 = r'https?://[^\s<>"]+\.(?:jpg|jpeg|png|gif|webp)(?:\?[^\s<>"]*)?'
        
        # Twitter形式のパターン (?format=jpg など)
        image_pattern2 = r'https?://[^\s<>"]*[?&]format=(?:jpg|jpeg|png|gif|webp)(?:[^\s<>"]*)?'
        
        # 特定の画像ホスティングサイトのパターン
        image_pattern3 = r'https?://(?:pbs\.twimg\.com|imgur\.com)/[^\s<>"]*(?:\?[^\s<>"]*)?'
        
        images = []
        images.extend(re.findall(image_pattern1, content, re.IGNORECASE))
        images.extend(re.findall(image_pattern2, content, re.IGNORECASE))
        images.extend(re.findall(image_pattern3, content, re.IGNORECASE))
        
        # 重複を除去しつつ順序を保持
        unique_images = []
        seen = set()
        for img in images:
            if img not in seen:
                unique_images.append(img)
                seen.add(img)
        return unique_images
    
    def format_date(self, date_str):
        """日付文字列をフォーマット"""
        return date_str
    
    def generate_html(self, title="したらば掲示板スレッド"):
        """HTMLを生成"""
        if not self.posts:
            return "<html><body><h1>投稿が見つかりませんでした</h1></body></html>"
        
        # スレッドタイトルが抽出されている場合はそれを使用
        if self.thread_title:
            title = self.thread_title
        
        html_content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <style>
        body {{
            font-family: 'MS PGothic', 'Hiragino Kaku Gothic Pro', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #ffffee;
            line-height: 1.4;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            border: 1px solid #ccc;
            padding: 20px;
        }}
        h1 {{
            background-color: #ffe0f0;
            margin: -20px -20px 20px -20px;
            padding: 10px 20px;
            border-bottom: 1px solid #999;
            font-size: 16px;
            font-weight: bold;
        }}
        .post {{
            margin-bottom: 15px;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}
        .post-header {{
            font-size: 12px;
            color: #008800;
            margin-bottom: 5px;
        }}
        .post-number {{
            font-weight: bold;
            color: #000088;
        }}
        .post-name {{
            font-weight: bold;
            color: #008800;
        }}
        .post-date {{
            color: #666;
        }}
        .post-id {{
            color: #888;
            font-size: 11px;
        }}
        .post-content {{
            margin-left: 20px;
            font-size: 14px;
            word-break: break-all;
            overflow-wrap: break-word;
        }}
        .post-content a {{
            color: #0000ff;
        }}
        .thread-info {{
            background-color: #f0f0f0;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            font-size: 12px;
        }}
        .anchor-link {{
            color: #0000ff;
            text-decoration: none;
        }}
        .anchor-link:hover {{
            text-decoration: underline;
        }}
        .external-link {{
            word-break: break-all;
            overflow-wrap: break-word;
        }}
        .image-thumbnails {{
            margin-top: 10px;
            padding: 5px 0;
        }}
        .thumbnail {{
            max-width: 150px;
            max-height: 150px;
            margin: 5px;
            border: 1px solid #ccc;
            cursor: pointer;
        }}
        .thumbnail:hover {{
            opacity: 0.8;
        }}
        .image-thumbnails a {{
            text-decoration: none;
        }}
        .image-thumbnails a:hover {{
            text-decoration: none;
        }}
        @media (max-width: 600px) {{
            .container {{
                padding: 10px;
                margin: 0;
            }}
            h1 {{
                margin: -10px -10px 20px -10px;
                padding: 10px;
                font-size: 14px;
            }}
            .post-content {{
                margin-left: 10px;
            }}
            .external-link {{
                word-break: break-all;
                overflow-wrap: anywhere;
                line-height: 1.6;
            }}
            .thumbnail {{
                max-width: 100px;
                max-height: 100px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{html.escape(title)}</h1>
        
        <div class="thread-info">
            <strong>総レス数:</strong> {len(self.posts)}<br>
            <strong>開始日時:</strong> {self.posts[0]['date'] if self.posts else 'N/A'}<br>
            <strong>最終投稿:</strong> {self.posts[-1]['date'] if self.posts else 'N/A'}
        </div>
'''
        
        for post in self.posts:
            name_class = 'sage' if post['mail'] == 'sage' else ''
            
            # 投稿内容から画像URLを抽出
            images = self.extract_images_from_content(post['content'])
            
            html_content += f'''
        <div class="post" id="post-{post['number']}">
            <div class="post-header">
                <span class="post-number">{post['number']}</span>
                <span class="post-name {name_class}">{html.escape(post['name'])}</span>
                <span class="post-date">{html.escape(post['date'])}</span>
                {f'<span class="post-id">ID:{html.escape(post["user_id"])}</span>' if post['user_id'] else ''}
            </div>
            <div class="post-content">
                {post['content']}
            </div>'''
            
            # 画像サムネイルを追加
            if images:
                html_content += '''
            <div class="image-thumbnails">'''
                for img_url in images:
                    html_content += f'''
                <a href="{html.escape(img_url)}" target="_blank">
                    <img src="{html.escape(img_url)}" class="thumbnail" alt="画像" onerror="this.style.display='none'">
                </a>'''
                html_content += '''
            </div>'''
            
            html_content += '''
        </div>'''
        
        html_content += '''
    </div>
</body>
</html>'''
        
        return html_content


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法: python dat_to_html.py <datファイルパス> [出力ファイル名]")
        print("例: python dat_to_html.py thread.dat output.html")
        return
    
    dat_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(dat_file):
        print(f"エラー: ファイル '{dat_file}' が見つかりません")
        return
    
    parser = ShitarabaDatParser()
    
    print(f"datファイルを解析中: {dat_file}")
    
    if parser.parse_dat_file(dat_file):
        print(f"投稿数: {len(parser.posts)}")
        
        # スレッドタイトルを表示（デバッグ用）
        if parser.thread_title:
            print(f"スレッドタイトル: {parser.thread_title}")
        
        # ファイル名からデフォルトタイトルを生成（スレッドタイトルが取得できない場合のバックアップ）
        filename = os.path.basename(dat_file)
        default_title = filename.replace('.dat', '').replace('%2F', '/').replace('%2C', ',')
        default_title = unquote(default_title)
        
        html_content = parser.generate_html(default_title)
        
        if output_file is None:
            # ファイル名から板ID_スレッドID.htmlの形式を生成
            # 例: jbbs.livedoor.jp%2Fanime%2F11188_1716630941.dat -> 11188_1716630941.html
            base_name = filename.replace('.dat', '')
            
            # URLエンコードされたファイル名をデコード
            decoded_name = unquote(base_name)
            
            # anime/11188_1716630941 の形式から 11188_1716630941 を抽出
            if '/' in decoded_name:
                parts = decoded_name.split('/')
                if len(parts) >= 2:
                    # 最後の部分（スレッドID部分）のみを取得
                    # 11188_1716630941 の形式になっているはず
                    thread_part = parts[-1]
                    output_file = f"{thread_part}.html"
                else:
                    output_file = f"{parts[-1]}.html"
            else:
                # フォールバック: 元のファイル名をそのまま使用
                output_file = f"{base_name}.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML出力完了: {output_file}")
    else:
        print("datファイルの解析に失敗しました")


if __name__ == "__main__":
    main()