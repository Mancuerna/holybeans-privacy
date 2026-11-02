#!/usr/bin/env python3
"""Render the bilingual guide with the Python standard library.

Run from any directory. Use --check to verify committed HTML is up to date.
Source HTML fragments are trusted, maintainer-authored content in _guide/.
"""
import argparse
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://holybeans.jacortes.me'
CHAPTERS = json.loads((ROOT / '_guide/chapters.json').read_text())
TEXT = {
    'es': dict(guide='Guía de usuario', home='Inicio', privacy='Privacidad', terms='Condiciones',
        other='English', skip='Ir al contenido', nav='Navegación principal', chapters='Capítulos de la guía',
        menu='Explorar la guía', contents='En esta página', updated='Revisado el 2 de noviembre de 2026',
        prev='Anterior', next='Siguiente', top='Volver arriba', index='Todos los capítulos',
        description='Aprende a registrar cafés y preparaciones, organizar tus existencias y conservar tu diario.',
        intro='Desde tu primera taza hasta las copias de seguridad. Elige lo que quieres hacer y sigue los pasos con la app a mano.',
        start='Empieza por tu primera preparación',
        version='Esta edición cubre funciones incorporadas hasta HolyBeans 1.1.17. La disponibilidad y los nombres pueden variar en versiones anteriores. Las conexiones experimentales se indican en su capítulo.',
        help='¿Algo no funciona?', helptext='Comprueba filtros, conexiones y copias antes de modificar tus datos.',
        helplink='Busca el síntoma y cómo resolverlo',
        exampletitle='Una dosis, un registro', exampletext='Ejemplo ficticio: tienes 250 g disponibles y guardas una preparación de 15 g. Quedan 235 g. Archivar esa preparación conserva el consumo.',
        examplelink='Entiende tus existencias'),
    'en': dict(guide='User guide', home='Home', privacy='Privacy', terms='Terms',
        other='Español', skip='Skip to content', nav='Main navigation', chapters='Guide chapters',
        menu='Explore the guide', contents='On this page', updated='Reviewed November 2, 2026',
        prev='Previous', next='Next', top='Back to top', index='All chapters',
        description='Learn to record coffees and brews, organize your stock and keep your journal safe.',
        intro='From your first cup to your backups. Choose what you want to do and follow the steps with the app at hand.',
        start='Start with your first brew',
        version='This edition covers features introduced through HolyBeans 1.1.17. Availability and labels may differ in earlier versions. Experimental connections are identified in their chapters.',
        help='Something not working?', helptext='Check filters, connections and backups before changing your data.',
        helplink='Find the symptom and how to resolve it',
        exampletitle='One dose, one record', exampletext='Fictional example: you have 250 g available and save a 15 g brew. You have 235 g left. Archiving that brew preserves its consumption.',
        examplelink='Understand your stock'),
}

def guide_url(lang, slug=''):
    return ('/es' if lang == 'es' else '') + '/docs/' + (slug + '/' if slug else '')

def link(url, label, current=False):
    return f'<a href="{url}"' + (' aria-current="page"' if current else '') + f'>{escape(label)}</a>'

def render(lang, chapter=None):
    t=TEXT[lang]
    slug=chapter['slug'] if chapter else ''
    content=chapter[lang] if chapter else dict(title=t['guide'],description=t['description'])
    prefix='/es' if lang=='es' else ''
    other='en' if lang=='es' else 'es'
    url=guide_url(lang,slug)
    navigation='\n'.join('<li>'+link(guide_url(lang,p['slug']),p[lang]['title'],p['slug']==slug)+'</li>' for p in CHAPTERS)
    navigation='<ul><li>'+link(guide_url(lang),t['index'],not slug)+'</li>'+navigation+'</ul>'
    if chapter:
        sections=content['sections']
        toc='<nav class="page-contents" aria-label="'+t['contents']+'"><p>'+t['contents']+'</p><ul>'+''.join('<li>'+link('#'+s['id'],s['title'])+'</li>' for s in sections)+'</ul></nav>'
        body=toc+'\n'+ '\n'.join(f'<section id="{s["id"]}"><h2>{escape(s["title"])}</h2>{s["body"]}</section>' for s in sections)
        i=CHAPTERS.index(chapter)
        previous=CHAPTERS[i-1] if i else None
        following=CHAPTERS[i+1] if i+1<len(CHAPTERS) else None
        body+='<nav class="chapter-pagination" aria-label="'+t['chapters']+'">'
        body+='<div><span>'+t['prev']+'</span>'+link(guide_url(lang,previous['slug'] if previous else ''),previous[lang]['title'] if previous else t['index'])+'</div>'
        if following:
            body+='<div><span>'+t['next']+'</span>'+link(guide_url(lang,following['slug']),following[lang]['title'])+'</div>'
        body+='</nav>'
    else:
        body='<p class="guide-start">'+link(guide_url(lang,'getting-started'),t['start'])+'</p>'
        body+='<div class="guide-chapters">'+''.join('<section><h2>'+link(guide_url(lang,p['slug']),p[lang]['title'])+'</h2><p>'+escape(p[lang]['description'])+'</p></section>' for p in CHAPTERS)+'</div>'
        body+='<section class="worked-example"><h2>'+t['exampletitle']+'</h2><p>'+t['exampletext']+'</p><p>'+link(guide_url(lang,'beans'),t['examplelink'])+'</p></section>'
        body+='<section><h2>'+t['help']+'</h2><p>'+t['helptext']+'</p><p>'+link(guide_url(lang,'troubleshooting'),t['helplink'])+'</p></section>'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#f7f2ec">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>{escape(content['title'])} · HolyBeans</title>
  <meta name="description" content="{escape(content['description'],quote=True)}">
  <link rel="canonical" href="{ORIGIN}{url}">
  <link rel="alternate" hreflang="{lang}" href="{ORIGIN}{url}">
  <link rel="alternate" hreflang="{other}" href="{ORIGIN}{guide_url(other,slug)}">
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="/guide.css">
</head>
<body class="guide-site" id="top">
  <a class="skip" href="#content">{t['skip']}</a>
  <div class="wrap">
    <header class="site-header">
      <a class="brand" href="{prefix}/home/"><span class="bean" aria-hidden="true"><span class="halo"></span></span>HolyBeans</a>
      <nav aria-label="{t['nav']}">{link(prefix+'/home/',t['home'])}{link(guide_url(lang),t['guide'],not slug)}{link(prefix+'/',t['privacy'])}{link(prefix+'/terms/',t['terms'])}<a href="{guide_url(other,slug)}" lang="{other}" hreflang="{other}">{t['other']}</a></nav>
    </header>
    <details class="mobile-guide-menu"><summary>{t['menu']}</summary><nav aria-label="{t['chapters']}">{navigation}</nav></details>
    <div class="guide-layout">
      <aside class="guide-sidebar"><nav aria-label="{t['chapters']}"><p>{t['guide']}</p>{navigation}</nav></aside>
      <main id="content" tabindex="-1">
        <article>
          <header class="guide-heading"><h1>{escape(content['title'])}</h1><p class="lead">{escape(content['description'] if chapter else t['intro'])}</p></header>
          {body}
          <div class="guide-edition"><p>{t['updated']}</p><p>{t['version']}</p><a href="#top">{t['top']}</a></div>
        </article>
      </main>
    </div>
    <footer><p>© 2026 HolyBeans · CaffeinatedDev</p><p>{link(prefix+'/home/',t['home'])} · {link(guide_url(lang),t['guide'])} · {link(prefix+'/',t['privacy'])} · {link(prefix+'/terms/',t['terms'])}</p></footer>
  </div>
</body>
</html>
'''

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    stale=[]
    for lang in TEXT:
        for chapter in [None,*CHAPTERS]:
            slug=chapter['slug'] if chapter else ''
            path=ROOT / guide_url(lang,slug).lstrip('/') / 'index.html'
            html=render(lang,chapter)
            if args.check:
                if not path.exists() or path.read_text()!=html: stale.append(str(path.relative_to(ROOT)))
            else:
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_text(html)
    if stale:
        raise SystemExit('Guide needs rebuilding: '+', '.join(stale))
    print(('Checked' if args.check else 'Built')+' 22 guide pages (ES/EN).')

if __name__=='__main__':main()
