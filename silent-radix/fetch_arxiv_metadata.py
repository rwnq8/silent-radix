#!/usr/bin/env python3
"""Fetch arXiv metadata for all cited papers and generate BibTeX entries."""
import urllib.request, urllib.parse, re, json, time, sys

def get_arxiv_entry(preprint_id):
    url = f'http://export.arxiv.org/api/query?id_list={preprint_id}&max_results=1'
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'DeepChat-Research/1.0')
    try:
        r = urllib.request.urlopen(req, timeout=15)
        xml = r.read().decode('utf-8')
    except Exception as e:
        print(f'  [ERROR] {preprint_id}: {e}', file=sys.stderr)
        return None
    
    entry_match = re.search(r'<entry>(.*?)</entry>', xml, re.DOTALL)
    if not entry_match:
        return None
    entry = entry_match.group(1)
    
    title = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
    authors = re.findall(r'<name>(.*?)</name>', entry)
    published = re.search(r'<published>(.*?)</published>', entry)
    
    # Extract DOI
    doi = ''
    for link in re.findall(r'<link[^>]*>', entry):
        if 'title="doi"' in link or "title='doi'" in link:
            dm = re.search(r'href="([^"]+)"', link)
            if dm:
                doi = dm.group(1).replace('http://dx.doi.org/', '')
    
    return {
        'title': (title.group(1).strip().replace('\n', ' ') if title else ''),
        'authors': authors,
        'year': (published.group(1)[:4] if published else ''),
        'doi': doi,
        'id': preprint_id
    }

def make_bibtex(entry, cite_key=None):
    """Generate BibTeX from arXiv metadata."""
    if not cite_key:
        # Generate citation key from first author + year
        if entry['authors']:
            first_author = entry['authors'][0].split()[-1]  # last name
            cite_key = f"{first_author}{entry['year']}"
        else:
            cite_key = f"anon{entry['year']}"
    
    authors = ' and '.join(entry['authors']) if entry['authors'] else '{[Unknown]}'
    title = entry['title'].replace('{', '\\{').replace('}', '\\}')
    
    lines = [
        f'@misc{{{cite_key},',
        f'  author = {{{authors}}},',
        f'  title = {{{title}}},',
        f'  year = {{{entry["year"]}}},',
        f'  eprint = {{{entry["id"]}}},',
        f'  archiveprefix = {{arXiv}},',
    ]
    if entry['doi']:
        lines.append(f'  doi = {{{entry["doi"]}}},')
    lines.append('}')
    
    return '\n'.join(lines)

# List of all cited papers by category
papers = {
    'core_knapsack': [
        ('Evain2008', '0803.0845'),
        ('Rastaghi2012a', '1210.8375'),
        ('Rastaghi2012b', '1211.6984'),
        ('RizosDraziotis2023', '2303.08973'),
        ('SuLv2008', '0801.4817'),
    ],
    'hidden_subset_sum': [
        ('LuoLiLi2024', '2412.04967'),
        ('LiLuoGini2024', '2409.14260'),
        ('NotarnicolaWiese2021', '2111.05436'),
    ],
    'lattice_ntru': [
        ('PoimenidouDraziotis2025', '2510.26003'),
        ('PoimenidouAdamoudis2023', '2311.17022'),
        ('RastaghiOskouei2012', '1210.7417'),
        ('AdamoudisDraziotis2022', '2203.09620'),
    ],
    'benaloh': [
        ('FousseLafourcade2010', '1008.2991'),
    ],
    'encoding_secret_sharing': [
        ('ChumZhang2009', '0910.3991'),
        ('KantourBouroubi2017', '1711.04642'),
        ('AriffinMandangan2010', '1012.5579'),
    ],
    'quantum_foundations': [
        ('Regev2003', 'cs/0304005'),
        ('BaconChilds2005', 'quant-ph/0501044'),
    ],
}

all_bibtex = []
all_ids = []

for category, entries in papers.items():
    for cite_key, pid in entries:
        all_ids.append(pid)
        if pid not in all_bibtex:
            time.sleep(1.0)
            entry = get_arxiv_entry(pid)
            if entry:
                bibtex = make_bibtex(entry, cite_key)
                all_bibtex.append(bibtex)
                authors = ', '.join(entry['authors'][:3])
                if len(entry['authors']) > 3: authors += ' et al.'
                print(f'  [{pid}] -> {cite_key} | {entry["year"]} | {entry["title"][:80]}')
            else:
                print(f'  [{pid}] -> FAILED (no metadata)')

# Add the Zenodo paper (not on arXiv)
all_bibtex.insert(0, """@misc{QNFO2026,
  author = {{QNFO Research}},
  title = {{The Silent Radix: Positional Notation as Ultrametric Tree and the Calculus of Indications as Remedy}},
  year = {2026},
  doi = {10.5281/zenodo.21134188},
  note = {Available on Zenodo},
}""")

# Write combined BibTeX file
bibtex_output = '\n\n'.join(all_bibtex)
with open('G:/My Drive/DeepChat/silent-radix/references.bib', 'w', encoding='utf-8') as f:
    f.write(bibtex_output)

print(f'\nWrote {len(all_bibtex)} BibTeX entries to silent-radix/references.bib')
