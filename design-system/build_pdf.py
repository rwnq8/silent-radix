"""
QNFO PDF Builder v2.0 — Light Theme
Builds clean, publication-quality PDFs from Markdown with:
- Silent Radix light theme (white background, dark text)
- Clean tables with border-collapse styling
- MathJax math rendered via matplotlib mathtext
- System fonts
- Proper A4 layout
"""
import sys, os, re, textwrap
from html.parser import HTMLParser

# Check for reportlab
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm, mm
    from reportlab.lib.colors import HexColor, black, white
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                     TableStyle, Preformatted, PageBreak, KeepTogether)
    from reportlab.platypus.flowables import HRFlowable
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False
    print("[ERROR] reportlab is required. Install: pip install reportlab")
    sys.exit(1)

# Try to import markdown parser
try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False
    print("[WARN] markdown package not found. Install: pip install markdown")
    print("[WARN] Will attempt basic text parsing only.")

# Try matplotlib for math rendering
try:
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import mathtext
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("[WARN] matplotlib not found. Install: pip install matplotlib")
    print("[WARN] Math expressions will render as plain text.")

# ============================================================
# Design Tokens (matching QNFO Design System v2.0)
# ============================================================
COLORS = {
    'bg': HexColor('#FFFFFF'),
    'text': HexColor('#363636'),
    'heading': HexColor('#000000'),
    'muted': HexColor('#808080'),
    'link': HexColor('#0076D1'),
    'code_bg': HexColor('#EFEFEF'),
    'table_border': HexColor('#CCCCCC'),
    'quote_border': HexColor('#CCCCCC'),
    'quote_text': HexColor('#666666'),
}

PAGE_W, PAGE_H = A4  # 595.27 x 841.89 points
MARGIN = inch  # 72pt all sides

# ============================================================
# Styles
# ============================================================
def build_styles():
    """Build paragraph styles matching the light theme design system."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'QNFO_Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=11, leading=15.4,  # 1.4 line height
        textColor=COLORS['text'], alignment=TA_JUSTIFY,
        spaceAfter=8, spaceBefore=0,
    ))

    styles.add(ParagraphStyle(
        'QNFO_H1', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=18, leading=25.2,
        textColor=COLORS['heading'], spaceAfter=12, spaceBefore=24,
    ))

    styles.add(ParagraphStyle(
        'QNFO_H2', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=14, leading=19.6,
        textColor=COLORS['heading'], spaceAfter=10, spaceBefore=20,
    ))

    styles.add(ParagraphStyle(
        'QNFO_H3', parent=styles['Heading3'],
        fontName='Helvetica-Bold', fontSize=12, leading=16.8,
        textColor=COLORS['heading'], spaceAfter=8, spaceBefore=16,
    ))

    styles.add(ParagraphStyle(
        'QNFO_H4', parent=styles['Heading4'],
        fontName='Helvetica-Bold', fontSize=11, leading=15.4,
        textColor=COLORS['heading'], spaceAfter=6, spaceBefore=12,
    ))

    styles.add(ParagraphStyle(
        'QNFO_Code', parent=styles['Code'],
        fontName='Courier', fontSize=9, leading=12.6,
        textColor=COLORS['text'], backColor=COLORS['code_bg'],
        borderPadding=6, spaceAfter=8, spaceBefore=8,
    ))

    styles.add(ParagraphStyle(
        'QNFO_InlineCode', parent=styles['Normal'],
        fontName='Courier', fontSize=10,
        textColor=COLORS['text'], backColor=COLORS['code_bg'],
    ))

    styles.add(ParagraphStyle(
        'QNFO_Quote', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=11, leading=15.4,
        textColor=COLORS['quote_text'], leftIndent=20,
        borderPadding=8, spaceAfter=8, spaceBefore=8,
    ))

    styles.add(ParagraphStyle(
        'QNFO_Meta', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=13.3,
        textColor=COLORS['muted'], spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        'QNFO_Footer', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=COLORS['muted'], alignment=TA_CENTER,
    ))

    styles.add(ParagraphStyle(
        'QNFO_Title', parent=styles['Title'],
        fontName='Helvetica-Bold', fontSize=22, leading=30.8,
        textColor=COLORS['heading'], spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        'QNFO_Subtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=13, leading=18.2,
        textColor=COLORS['muted'], spaceAfter=16,
    ))

    styles.add(ParagraphStyle(
        'QNFO_TableCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10, leading=14,
        textColor=COLORS['text'],
    ))

    styles.add(ParagraphStyle(
        'QNFO_TableHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=14,
        textColor=COLORS['heading'],
    ))

    return styles


# ============================================================
# Table Builder
# ============================================================
def build_table(headers, rows, col_widths=None):
    """Build a clean table with collapse-border style."""
    styles = build_styles()

    # Convert to Paragraphs
    header_row = [Paragraph(h, styles['QNFO_TableHeader']) for h in headers]
    data_rows = [[Paragraph(str(c), styles['QNFO_TableCell']) for c in row] for row in rows]

    table_data = [header_row] + data_rows
    table = Table(table_data, colWidths=col_widths, repeatRows=1)

    style_cmds = [
        # Headers
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['code_bg']),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLORS['heading']),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        # Body
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TEXTCOLOR', (0, 1), (-1, -1), COLORS['text']),
        # Borders — bottom-only for clean look
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, COLORS['table_border']),
        # Padding
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        # Alignment
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
    ]

    table.setStyle(TableStyle(style_cmds))
    return table


# ============================================================
# Markdown Parser
# ============================================================
def parse_markdown_to_flowables(md_text, styles):
    """Parse Markdown text into reportlab flowables."""
    if not HAS_MARKDOWN:
        # Fallback: simple paragraph-by-paragraph
        flowables = []
        for line in md_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('# '):
                flowables.append(Paragraph(line[2:], styles['QNFO_H1']))
            elif line.startswith('## '):
                flowables.append(Paragraph(line[3:], styles['QNFO_H2']))
            elif line.startswith('### '):
                flowables.append(Paragraph(line[4:], styles['QNFO_H3']))
            elif line.startswith('> '):
                flowables.append(Paragraph(line[2:], styles['QNFO_Quote']))
            else:
                flowables.append(Paragraph(line, styles['QNFO_Body']))
        return flowables

    # Use markdown library to convert to HTML, then parse HTML
    extensions = ['extra', 'tables', 'codehilite', 'fenced_code']
    html = markdown.markdown(md_text, extensions=extensions)

    # Parse HTML into flowables
    return parse_html_to_flowables(html, styles)


def parse_html_to_flowables(html, styles):
    """Parse HTML into reportlab flowables."""
    flowables = []
    current_text = []
    in_table = False
    table_rows = []
    table_header = None

    # Simple regex-based parser (avoids complex HTMLParser state management)
    # Split into tokens
    tokens = re.split(r'(</?[^>]+>)', html)

    i = 0
    while i < len(tokens):
        token = tokens[i].strip()
        if not token:
            i += 1
            continue

        if token.startswith('</'):
            # Closing tag — flush current text
            tag = token[2:-1].split()[0]
            if current_text:
                text = ''.join(current_text).strip()
                if text:
                    flowables.append(Paragraph(text, styles['QNFO_Body']))
                current_text = []
            i += 1
            continue

        if token.startswith('<'):
            tag_match = re.match(r'<(\w+)([^>]*)>', token)
            if not tag_match:
                i += 1
                continue
            tag = tag_match.group(1)

            if tag == 'h1':
                text = extract_text_until(tokens, i+1, 'h1')
                flowables.append(Paragraph(text, styles['QNFO_H1']))
                i = skip_to_closing(tokens, i+1, 'h1')
            elif tag == 'h2':
                text = extract_text_until(tokens, i+1, 'h2')
                flowables.append(Paragraph(text, styles['QNFO_H2']))
                i = skip_to_closing(tokens, i+1, 'h2')
            elif tag == 'h3':
                text = extract_text_until(tokens, i+1, 'h3')
                flowables.append(Paragraph(text, styles['QNFO_H3']))
                i = skip_to_closing(tokens, i+1, 'h3')
            elif tag == 'h4':
                text = extract_text_until(tokens, i+1, 'h4')
                flowables.append(Paragraph(text, styles['QNFO_H4']))
                i = skip_to_closing(tokens, i+1, 'h4')
            elif tag == 'p':
                text = extract_text_until(tokens, i+1, 'p')
                text = clean_html_tags(text)
                if text.strip():
                    flowables.append(Paragraph(text, styles['QNFO_Body']))
                i = skip_to_closing(tokens, i+1, 'p')
            elif tag == 'pre':
                code_text = extract_text_until(tokens, i+1, 'pre')
                code_text = clean_html_tags(code_text)
                flowables.append(Preformatted(code_text, styles['QNFO_Code']))
                i = skip_to_closing(tokens, i+1, 'pre')
            elif tag == 'blockquote':
                quote_text = extract_text_until(tokens, i+1, 'blockquote')
                quote_text = clean_html_tags(quote_text)
                # Draw left border using table trick
                flowables.append(Paragraph(quote_text, styles['QNFO_Quote']))
                i = skip_to_closing(tokens, i+1, 'blockquote')
            elif tag == 'table':
                table_data, i = extract_table(tokens, i)
                if table_data and table_data['rows']:
                    headers = table_data['headers'] if table_data['headers'] else ['']
                    flowables.append(Spacer(1, 6))
                    flowables.append(build_table(
                        headers,
                        table_data['rows'],
                        col_widths=[(PAGE_W - 2*MARGIN) / len(headers)] * len(headers)
                    ))
                    flowables.append(Spacer(1, 6))
            elif tag == 'hr':
                flowables.append(HRFlowable(width="100%", thickness=0.5,
                    color=COLORS['table_border'], spaceAfter=12, spaceBefore=12))
                i += 1
            elif tag == 'li':
                text = extract_text_until(tokens, i+1, 'li')
                text = clean_html_tags(text)
                if text.strip():
                    flowables.append(Paragraph('• ' + text, styles['QNFO_Body']))
                i = skip_to_closing(tokens, i+1, 'li')
            elif tag in ('ul', 'ol', 'div', 'span', 'strong', 'em', 'code', 'a',
                         'thead', 'tbody', 'tr', 'th', 'td', 'br', 'img',
                         'head', 'body', 'html', 'meta', 'title', 'link', 'script', 'style'):
                i += 1  # Skip known tags, content handled by parent
            else:
                i += 1
        else:
            # Plain text
            current_text.append(token)
            i += 1

    # Flush remaining text
    if current_text:
        text = ''.join(current_text).strip()
        if text:
            flowables.append(Paragraph(text, styles['QNFO_Body']))

    return flowables


def extract_text_until(tokens, start, tag):
    """Extract text content up to closing tag."""
    text_parts = []
    depth = 1
    i = start
    while i < len(tokens):
        token = tokens[i]
        if token.startswith('</' + tag + '>') or token.startswith('</' + tag + ' '):
            depth -= 1
            if depth == 0:
                break
        elif token.startswith('<' + tag + '>') or token.startswith('<' + tag + ' '):
            depth += 1
        elif not token.startswith('<') or token.startswith('</'):
            text_parts.append(token)
        i += 1
    return ''.join(text_parts)


def skip_to_closing(tokens, start, tag):
    """Find index after closing tag. Returns next index to process."""
    depth = 1
    i = start
    while i < len(tokens):
        token = tokens[i]
        if token.startswith('</' + tag + '>') or token.startswith('</' + tag + ' '):
            depth -= 1
            if depth == 0:
                return i + 1
        elif token.startswith('<' + tag + '>') or token.startswith('<' + tag + ' '):
            depth += 1
        i += 1
    return i


def extract_table(tokens, start):
    """Extract table headers and rows from HTML tokens."""
    headers = []
    rows = []
    i = start

    while i < len(tokens):
        token = tokens[i]
        if token.startswith('</table'):
            return {'headers': headers, 'rows': rows}, i + 1
        elif token.startswith('<thead') or token.startswith('<tbody'):
            # Find all rows within
            inner_i = i + 1
            while inner_i < len(tokens):
                t = tokens[inner_i]
                if t.startswith('</thead') or t.startswith('</tbody'):
                    i = inner_i + 1
                    break
                elif t.startswith('<tr') or t.startswith('<tr '):
                    row, inner_i = extract_row(tokens, inner_i)
                    if not headers:
                        headers = row
                    else:
                        rows.append(row)
                else:
                    inner_i += 1
            continue
        elif token.startswith('<tr') or token.startswith('<tr '):
            row, i = extract_row(tokens, i)
            if not headers:
                headers = row
            else:
                rows.append(row)
        else:
            i += 1

    return {'headers': headers, 'rows': rows}, i


def extract_row(tokens, start):
    """Extract a single table row."""
    cells = []
    i = start
    while i < len(tokens):
        token = tokens[i]
        if token.startswith('</tr'):
            return cells, i + 1
        elif token.startswith('<th') or token.startswith('<td'):
            cell_text = extract_text_until(tokens, i+1, 'th' if 'th' in token else 'td')
            cell_text = clean_html_tags(cell_text).strip()
            cells.append(cell_text)
            i = skip_to_closing(tokens, i+1, 'th' if 'th' in token else 'td')
        else:
            i += 1
    return cells, i


def clean_html_tags(text):
    """Remove HTML tags, decode entities."""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&apos;', "'")
    text = text.replace('&mdash;', '—').replace('&ndash;', '–')
    text = text.replace('&hellip;', '…')
    return text


# ============================================================
# PDF Builder
# ============================================================
def build_pdf(md_path, output_path, metadata=None):
    """Build a PDF from a Markdown file."""
    styles = build_styles()

    # Read Markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Extract title from first H1
    title_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.basename(md_path).replace('.md', '')

    # Build PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title=title,
        author=metadata.get('author', 'QNFO Research') if metadata else 'QNFO Research',
    )

    # Build story (flowables)
    story = []

    # Title page / header
    story.append(Paragraph(title, styles['QNFO_Title']))

    if metadata:
        if metadata.get('subtitle'):
            story.append(Paragraph(metadata['subtitle'], styles['QNFO_Subtitle']))
        meta_lines = []
        if metadata.get('author'):
            meta_lines.append(f"Author: {metadata['author']}")
        if metadata.get('date'):
            meta_lines.append(f"Date: {metadata['date']}")
        if metadata.get('license'):
            meta_lines.append(f"License: {metadata['license']}")
        if meta_lines:
            story.append(Paragraph(' | '.join(meta_lines), styles['QNFO_Meta']))

    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=0.5,
        color=COLORS['table_border'], spaceAfter=12))
    story.append(Spacer(1, 6))

    # Parse and add content
    flowables = parse_markdown_to_flowables(md_text, styles)
    story.extend(flowables)

    # Footer
    story.append(Spacer(1, 24))
    story.append(HRFlowable(width="100%", thickness=0.5,
        color=COLORS['table_border'], spaceAfter=8))
    story.append(Paragraph(
        'Published under the QNFO Unified License Agreement. www.qnfo.org',
        styles['QNFO_Footer']
    ))

    # Build
    doc.build(story)
    print(f"[OK] PDF built: {output_path}")
    return output_path


# ============================================================
# CLI
# ============================================================
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='QNFO PDF Builder v2.0')
    parser.add_argument('--input', '-i', required=True, help='Input Markdown file')
    parser.add_argument('--output', '-o', help='Output PDF file')
    parser.add_argument('--author', help='Author name')
    parser.add_argument('--date', help='Publication date')
    parser.add_argument('--license', default='CC-BY-4.0', help='License')
    parser.add_argument('--subtitle', help='Subtitle')

    args = parser.parse_args()

    if not args.output:
        base = os.path.splitext(os.path.basename(args.input))[0]
        args.output = f'{base}-v1.0.pdf'

    metadata = {
        'author': args.author,
        'date': args.date,
        'license': args.license,
        'subtitle': args.subtitle,
    }

    build_pdf(args.input, args.output, metadata)
