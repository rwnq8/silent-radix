# QNFO/QWAV Design System v2.0 — Silent Radix Light Theme

> **Canonical reference:** https://silent-radix-demo.pages.dev/quantum/
> **Adopted:** 2026-06-30
> **Principle:** Simple, clean, light theme with properly rendered tables and MathJax math expressions.

---

## 1. Color Palette

| Token | Value | CSS Variable | Usage |
|:------|:------|:-------------|:------|
| `--bg-primary` | `#FFFFFF` | `rgb(255, 255, 255)` | Page background |
| `--text-primary` | `#363636` | `rgb(54, 54, 54)` | Body text |
| `--text-heading` | `#000000` | `rgb(0, 0, 0)` | All headings (h1-h6) |
| `--text-muted` | `#808080` | `rgb(128, 128, 128)` | Secondary/caption text |
| `--link` | `#0076D1` | `rgb(0, 118, 209)` | Hyperlinks |
| `--link-hover` | `#0056A0` | `rgb(0, 86, 160)` | Hover state |
| `--code-bg` | `#EFEFEF` | `rgb(239, 239, 239)` | Inline code background |
| `--table-border` | `#CCCCCC` | `rgb(204, 204, 204)` | Table borders |

**🚫 NO DARK THEMES.** Light theme only across all QNFO/QWAV properties.

---

## 2. Typography

### 2.1 Font Stack

```css
font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
             Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans",
             "Helvetica Neue", "Segoe UI Emoji", "Apple Color Emoji",
             "Noto Color Emoji", sans-serif;
```

**Code:** `monospace` (system default monospace)

### 2.2 Type Scale

| Element | Size | Weight | Line Height | Color |
|:--------|:-----|:-------|:------------|:------|
| `body` | 16px | 400 | 1.4 (22.4px) | `--text-primary` |
| `h1` | 35.2px (2.2em) | 600 | 1.4 | `--text-heading` |
| `h2` | 24px (1.5em) | 600 | 1.4 | `--text-heading` |
| `h3` | 18.72px (1.17em) | 600 | 1.4 | `--text-heading` |
| `h4` | 16px (1em) | 600 | 1.4 | `--text-heading` |
| `p` | 16px (1em) | 400 | 1.4 | `--text-primary` |
| `code` | 0.9em | 400 | — | inherit |
| `small` | 0.875em | 400 | — | `--text-muted` |

### 2.3 Headings

- **No border-bottom** on h2 (unlike GitHub-style)
- **No extra decoration** — clean, weight-based hierarchy
- **Margin:** 0.83em top/bottom for h1, 0.75em for h2

---

## 3. Layout

```css
body {
  max-width: 800px;
  margin: 20px auto;
  padding: 0 10px;
}
```

- **Max width:** 800px (centered)
- **Margin:** 20px vertical, auto horizontal
- **Padding:** 0 10px (responsive gutter)
- **No sidebar, no navigation clutter**
- **Single-column academic layout**

---

## 4. Components

### 4.1 Links

```css
a {
  color: #0076D1;
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
  color: #0056A0;
}
```

### 4.2 Tables

```css
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}
th, td {
  padding: 6px;
  text-align: left;
  border-bottom: 1px solid #CCCCCC;
}
th {
  font-weight: 600;
}
```

**Key rules:**
- `border-collapse: collapse` for clean rendering
- Simple 6px cell padding
- Bottom borders only (not grid lines)
- Left-aligned text

### 4.3 Code Blocks

```css
pre {
  background: #EFEFEF;
  padding: 12px 16px;
  border-radius: 4px;
  overflow-x: auto;
}
pre code {
  font-family: monospace;
  font-size: 0.9em;
  line-height: 1.4;
}
code {
  font-family: monospace;
  background: #EFEFEF;
  padding: 1px 4px;
  border-radius: 3px;
}
```

### 4.4 Blockquotes

```css
blockquote {
  border-left: 3px solid #CCCCCC;
  margin: 1em 0;
  padding: 0.5em 1em;
  color: #666666;
}
```

### 4.5 MathJax

```css
/* MathJax CHTML — left-aligned display equations */
mjx-container[display="true"] {
  text-align: left !important;
}
```

**MathJax Config:**
```javascript
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    macros: {
      "\\R": "\\mathbb{R}", "\\Q": "\\mathbb{Q}",
      "\\Z": "\\mathbb{Z}", "\\N": "\\mathbb{N}",
      "\\C": "\\mathbb{C}", "\\F": "\\mathbb{F}",
      "\\Qp": "\\mathbb{Q}_p", "\\Zp": "\\mathbb{Z}_p",
      "\\cA": "\\mathcal{A}", "\\cC": "\\mathcal{C}",
      "\\cB": "\\mathcal{B}"
    }
  },
  chtml: { displayAlign: 'left' }
};
```

**CRITICAL: CONFIG MUST BE BEFORE MathJax script tag.**

---

## 5. PDF Specification

PDFs must match the HTML light theme:

| Property | Value |
|:---------|:------|
| Page size | A4 |
| Margins | 1 inch (72pt) all sides |
| Font family | System fonts (DejaVu or Liberation as fallback) |
| Body text | 11pt, 1.4 leading |
| H1 | 18pt bold |
| H2 | 14pt bold |
| H3 | 12pt bold |
| Tables | Collapse borders, 0.5pt lines, 4pt cell padding |
| Math | Rendered via matplotlib mathtext (not fragile LaTeX) |
| Links | Blue (#0076D1), underlined |
| Background | White only |
| Code blocks | Light gray background (#EFEFEF), 9pt monospace |

---

## 6. Anti-Patterns (FORBIDDEN)

| Forbidden | Reason |
|:----------|:-------|
| Dark backgrounds (#1a1a2e, #0d1117, etc.) | User mandate: light theme only |
| Gradient backgrounds | Distracting, non-academic |
| Heavy box-shadows / glass effects | Against simple, clean principle |
| `overflow-wrap: anywhere` on body | Breaks layout |
| Tables with grid borders | Use minimal bottom-border style |
| PDFs with \ufffd rendering failures | Font encoding issue — fix before deploy |
| MathJax config AFTER script tag | Math won't render |
| Missing MathJax macros | Standard macros listed above must be included |
| Non-collapsed tables in PDF | Must use `border-collapse: collapse` |

---

## 7. Deployment Targets

| Property | URL | Current Theme | Action |
|:---------|:----|:--------------|:-------|
| Reference | silent-radix-demo.pages.dev | ✅ Light (pandoc default) | Canonical |
| Hub | hub.qnfo.org | TBD | Audit → Convert |
| Publications | papers.qnfo.org | TBD | Audit → Convert |
| Legal | legal.qnfo.org | TBD | Audit → Convert |
| All MD→PDF outputs | — | TBD | New build script |

---

*QNFO Design System v2.0 — Adopted 2026-06-30. Replaces all previous visual styles.*
