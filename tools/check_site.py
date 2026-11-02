#!/usr/bin/env python3
"""Check local links, anchors, semantics and bilingual guide completeness."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT=Path(__file__).resolve().parents[1]
ORIGIN='https://holybeans.jacortes.me'

class Page(HTMLParser):
    def __init__(self,path):
        super().__init__(convert_charrefs=True)
        self.path=path
        self.ids=[]; self.links=[]; self.resources=[]; self.headings=[]; self.lang=None
        self.alternates={}; self.canonical=None; self.mains=0
        self.feed(path.read_text())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='html':self.lang=a.get('lang')
        if tag=='main':self.mains+=1
        if tag in ('h1','h2','h3','h4','h5','h6'):self.headings.append(int(tag[1]))
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag=='link':
            self.links.append(a.get('href',''))
            if a.get('rel')=='alternate':self.alternates[a.get('hreflang')]=a['href']
            if a.get('rel')=='canonical':self.canonical=a['href']
            if a.get('rel')=='stylesheet':self.resources.append(a['href'])
        if tag in ('script','img','iframe','source') and a.get('src'):self.resources.append(a['src'])

def route(path):
    return '/'+str(path.relative_to(ROOT)).removesuffix('index.html')

def main():
    pages={p:Page(p) for p in ROOT.rglob('*.html') if not any(x.startswith('.') for x in p.relative_to(ROOT).parts)}
    errors=[]; links=0
    for path,p in pages.items():
        label=str(path.relative_to(ROOT))
        if len(p.ids)!=len(set(p.ids)):errors.append(label+': duplicate IDs')
        if p.headings.count(1)!=1 or p.mains!=1:errors.append(label+': expected one h1/main')
        if p.lang not in ('en','es'):errors.append(label+': language missing')
        if p.canonical!=ORIGIN+route(path):errors.append(label+': incorrect canonical URL')
        for before,after in zip(p.headings,p.headings[1:]):
            if after>before+1:errors.append(label+': skipped heading level')
        for href in p.links+p.resources:
            target=urlsplit(urljoin(ORIGIN+route(path),href))
            if target.netloc!='holybeans.jacortes.me':continue
            dest=ROOT/unquote(target.path).lstrip('/')
            if target.path.endswith('/'):dest=dest/'index.html'
            links+=1
            if not dest.is_file():errors.append(label+': broken link '+href)
            elif target.fragment and dest in pages and unquote(target.fragment) not in pages[dest].ids:errors.append(label+': missing anchor '+href)
        for resource in p.resources:
            if urlsplit(resource).netloc:errors.append(label+': unexpected external resource '+resource)
        if '/docs/' in route(path):
            other='en' if p.lang=='es' else 'es'
            expected=route(path).removeprefix('/es') if other=='en' else '/es'+route(path)
            if p.alternates.get(other)!=ORIGIN+expected:errors.append(label+': incorrect language counterpart')
    chapters=json.loads((ROOT/'_guide/chapters.json').read_text())
    for c in chapters:
        if [s['id'] for s in c['es']['sections']]!=[s['id'] for s in c['en']['sections']]:errors.append(c['slug']+': different translated sections')
    if errors:raise SystemExit('\n'.join(errors))
    print(f'{len(pages)} pages, {links} local links/resources and all anchors valid; ES/EN chapters aligned.')

if __name__=='__main__':main()
