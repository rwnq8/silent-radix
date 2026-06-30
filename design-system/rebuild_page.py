"""
QNFO Page Rebuilder v2 — Converts QNFO HTML pages to Silent Radix Light Theme.
"""
import re, sys, os, urllib.request, ssl

CANONICAL_CSS_PATH = os.path.join(os.path.dirname(__file__), 'qnfo-light.css')

MATHJAX_BLOCK = '''
  <!-- MathJax v3 — config MUST come before script -->
  <script>
  window.MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
      displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
      macros: {
        "\\\\R": "\\\\mathbb{R}", "\\\\Q": "\\\\mathbb{Q}",
        "\\\\Z": "\\\\mathbb{Z}", "\\\\N": "\\\\mathbb{N}",
        "\\\\C": "\\\\mathbb{C}", "\\\\F": "\\\\mathbb{F}",
        "\\\\Qp": "\\\\mathbb{Q}_p", "\\\\Zp": "\\\\mathbb{Z}_p",
        "\\\\cA": "\\\\mathcal{A}", "\\\\cC": "\\\\mathcal{C}",
        "\\\\cB": "\\\\mathcal{B}", "\\\\cU": "\\\\mathcal{U}",
        "\\\\bT": "\\\\mathbb{T}", "\\\\bP": "\\\\mathbb{P}",
        "\\\\bK": "\\\\mathbb{K}", "\\\\bB": "\\\\mathbb{B}",
        "\\\\bM": "\\\\mathbb{M}",
        "\\\\GL": "\\\\mathrm{GL}", "\\\\Gal": "\\\\mathrm{Gal}",
        "\\\\Aut": "\\\\mathrm{Aut}", "\\\\End": "\\\\mathrm{End}",
        "\\\\Hom": "\\\\mathrm{Hom}", "\\\\Spec": "\\\\mathrm{Spec}",
        "\\\\Proj": "\\\\mathrm{Proj}", "\\\\id": "\\\\mathrm{id}",
        "\\\\im": "\\\\mathrm{im}", "\\\\ker": "\\\\ker",
        "\\\\Tr": "\\\\mathrm{Tr}", "\\\\vol": "\\\\mathrm{vol}"
      }
    },
    options: { ignoreHtmlClass: 'no-mathjax', processHtmlClass: 'mathjax-process' },
    chtml: { displayAlign: 'left' }
  };
  </script>
  <script id="MathJax-script" async
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
  </script>
'''

def load_css():
    if os.path.exists(CANONICAL_CSS_PATH):
        with open(CANONICAL_CSS_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request('https://qnfo.org/design-system/qnfo-light.css',
            headers={'User-Agent': 'Mozilla/5.0'})
        return urllib.request.urlopen(req, timeout=10, context=ctx).read().decode('utf-8')
    except:
        print("[WARN] Cannot load canonical CSS")
        return ''

def clean_html(html):
    """Remove all dark theme elements from HTML."""
    # Remove ALL <style> blocks
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    # Remove inline :root CSS variable blocks (dark theme vars)
    html = re.sub(r':root\s*\{[^}]*\}', '', html)
    # Remove old MathJax
    html = re.sub(r'<script[^>]*>[\s\S]*?MathJax[\s\S]*?</script>', '', html, flags=re.DOTALL)
    # Fix meta theme-color
    html = re.sub(r'<meta[^>]*theme-color[^>]*content="[^"]*"[^>]*>', 
                  '<meta name="theme-color" content="#FFFFFF">', html)
    # Fix any remaining inline dark styles
    replacements = {
        'background:#0a0a0f': 'background:#FFFFFF',
        'background:#0d1117': 'background:#FFFFFF',
        'background:#12121a': 'background:#FFFFFF',
        'color:#e0e0e0': 'color:#363636',
        'color:#00cec9': 'color:#0076D1',
        'color:#6c5ce7': 'color:#000000',
        'color:#a29bfe': 'color:#000000',
        'color:#fdcb6e': 'color:#363636',
        'color:#e4e4ed': 'color:#363636',
        'color:#8b8b9e': 'color:#808080',
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    return html

def inject_css_and_mathjax(html, css):
    """Inject canonical CSS and MathJax before </head>."""
    css_block = '\n  <!-- QNFO Design System v2.0 — Silent Radix Light Theme -->\n  <style>\n' + css + '\n  </style>\n'
    injection = css_block + MATHJAX_BLOCK
    # Inject right before </head> (only once)
    html = html.replace('</head>', injection + '</head>', 1)
    return html

def rebuild_page(input_html, output_path=None):
    """Full rebuild pipeline."""
    if os.path.exists(input_html):
        with open(input_html, 'r', encoding='utf-8') as f:
            html = f.read()
    else:
        html = input_html

    css = load_css()
    html = clean_html(html)
    html = inject_css_and_mathjax(html, css)

    if output_path:
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"[OK] Rebuilt: {output_path} ({len(html)} chars)")

    return html

def fetch_and_rebuild(url, output_path):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req, timeout=15, context=ctx).read().decode('utf-8', errors='replace')
    return rebuild_page(html, output_path)

if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == '--fetch':
        fetch_and_rebuild(sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 2:
        rebuild_page(sys.argv[1], sys.argv[2] if len(sys.argv) >= 3 else None)
    else:
        print("Usage: python rebuild_page.py [--fetch] <input> [output]")
