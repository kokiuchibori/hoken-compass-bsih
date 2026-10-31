"""共通ヘッダー・フッターを差し込んで静的HTMLを生成する。

使い方: python3 build.py
pages/*.html の本文を編集 → このスクリプトを実行 → ルートに HTML が出力される。
"""
from pathlib import Path

SITE_NAME = "マネー<span>コンパス</span>"
SITE_NAME_TEXT = "マネーコンパス"
ROOT = Path(__file__).parent

# 公開URL（末尾の / まで）。独自ドメインにしたらここを書き換える。
SITE_URL = "https://USERNAME.github.io/REPO/"

# True の間は検索エンジンに登録させない。
# 「要差し替え」「【要記入】」をすべて埋めてから False にすること。
NOINDEX = True

HEADER = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">{robots}
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<div class="ad-notice">当サイトはアフィリエイト広告を利用しています。</div>
<header class="site-header">
  <div class="container">
    <a class="logo" href="index.html">{site}</a>
    <nav class="nav">
      <a href="basics.html">保険の基礎</a>
      <a href="compare.html">無料保険相談の比較</a>
      <a href="simulator.html">必要保障額の試算</a>
      <a href="about.html">運営者情報</a>
    </nav>
  </div>
</header>
"""

FOOTER = """<footer class="site-footer">
  <div class="container">
    <div class="footer-links">
      <a href="about.html">運営者情報</a>
      <a href="disclaimer.html">免責事項・広告について</a>
      <a href="privacy.html">プライバシーポリシー</a>
    </div>
    <p>当サイトは保険募集（保険商品の勧誘・媒介）を行うものではありません。保険の加入・見直しに関する最終判断はご自身の責任で行ってください。</p>
    <p>&copy; 2026 {site_text}</p>
  </div>
</footer>
<script src="js/data.js"></script>
<script src="js/main.js"></script>
</body>
</html>
"""

ROBOTS_META = '\n<meta name="robots" content="noindex, nofollow">' if NOINDEX else ""

urls = []
for src in sorted((ROOT / "pages").glob("*.html")):
    lines = src.read_text(encoding="utf-8").split("\n", 2)
    title = lines[0].removeprefix("title:").strip()
    desc = lines[1].removeprefix("desc:").strip()
    body = lines[2]
    url = SITE_URL + ("" if src.name == "index.html" else src.name)
    urls.append(url)
    html = HEADER.format(title=title, desc=desc, site=SITE_NAME, url=url, robots=ROBOTS_META) + body + FOOTER.format(site_text=SITE_NAME_TEXT)
    (ROOT / src.name).write_text(html, encoding="utf-8")
    print("built", src.name)

# noindex の確認のため、robots.txt ではクロールを止めない
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
    + "</urlset>\n",
    encoding="utf-8",
)
print("built robots.txt, sitemap.xml", "(noindex)" if NOINDEX else "")

leftovers = [f.name for f in (ROOT / "pages").glob("*.html") if "【" in f.read_text(encoding="utf-8")]
if "要差し替え" in (ROOT / "js" / "data.js").read_text(encoding="utf-8"):
    leftovers.append("js/data.js")
if leftovers:
    print("未記入の箇所あり:", ", ".join(sorted(leftovers)))
