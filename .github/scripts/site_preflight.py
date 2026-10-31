#!/usr/bin/env python3
"""Fail-closed release acceptance for the MathewUrsua.com static website.
Run BEFORE any GitHub tree / branch / Pages deployment operation.
"""
from pathlib import Path
import re,json,sys,hashlib,xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2]
errors=[];checks=[]
def check(name,condition,details=''):
 checks.append((name,bool(condition),details))
 if not condition:errors.append(f'{name}: {details}')
 return bool(condition)
canonicals={'index.html':'https://mathewursua.com/','portfolio.html':'https://mathewursua.com/portfolio.html'}
parsed={}
for page,url in canonicals.items():
 src=(ROOT/page).read_text()
 soup=BeautifulSoup(src,'html.parser');parsed[page]=soup
 c=soup.find_all('link',rel=lambda x:x and 'canonical' in x)
 check(page+' canonical exactly once',len(c)==1 and c[0].get('href')==url, str([x.get('href') for x in c]))
 og=soup.find('meta',attrs={'property':'og:url'})
 check(page+' OG URL',og and og.get('content')==url,og.get('content') if og else 'missing')
 robots=soup.find('meta',attrs={'name':'robots'})
 check(page+' is not noindexed',robots is None or 'noindex' not in robots.get('content','').lower())
 scripts=soup.select('script[type="application/ld+json"]')
 try:
  schema=[json.loads(s.string or s.get_text()) for s in scripts]
  check(page+' JSON-LD parse and context',len(schema)==1 and schema[0]['@context']=='https://schema.org')
  if page=='index.html':
   g=schema[0]['@graph'];person=next(x for x in g if x.get('@type')=='Person');profile=next(x for x in g if x.get('@type')=='ProfilePage')
   check('home Person ID',person['@id']=='https://mathewursua.com/#person' and person['name']=='Mathew Ursua')
   check('home Person sameAs',person.get('sameAs')==['https://mathewursua.substack.com/'])
   check('ProfilePage mainEntity',profile.get('mainEntity')=={'@id':person['@id']})
  else:
   check('portfolio is a collection page about same person',schema[0].get('@type')=='CollectionPage' and schema[0].get('about',{}).get('@id')=='https://mathewursua.com/#person')
 except Exception as e:check(page+' JSON-LD parse',False,str(e))
 check(page+' one H1',len(soup.find_all('h1'))==1)
 check(page+' no duplicate HTML ids',len([x.get('id') for x in soup.select('[id]')])==len(set(x.get('id') for x in soup.select('[id]'))))
 check(page+' real favicon',soup.find('link',href='/favicon.ico') is not None)
 check(page+' signature quotation exact',len(soup.select('.mu-signature-lockup .mu-signature-quote'))==1 and soup.select_one('.mu-signature-quote').get_text(strip=True)=='“Infant footsteps to a window on a day that brings rain. I know.”')
 check(page+' all photos have text alternative',not [x for x in soup.find_all('img') if x.get('alt') is None])
 check(page+' signature image exists',soup.select_one('.mu-signature-lockup img').get('src')=='assets/signature-header.png')
 ids={x.get('id') for x in soup.select('[id]')}
 for x in soup.select('[href]'):
  href=x.get('href')
  if href.startswith('http:') or href.startswith('https:') or href.startswith('mailto:'):continue
  if href.startswith('#'):check(page+' fragment '+href,href[1:] in ids)
  elif href.startswith('/#'):check(page+' shared root fragment '+href,href[2:] in {y.get('id') for y in BeautifulSoup((ROOT/'index.html').read_text(),'html.parser').select('[id]')})
  elif href.startswith('/'):
   if href=='/':continue
   if '#' in href:href=href.split('#')[0]
   check(page+' local absolute path '+href,(ROOT/href.lstrip('/')).is_file())
  else:
   clean=href.split('#')[0].split('?')[0]
   if clean:check(page+' local linked file '+clean,(ROOT/clean).is_file(),clean)
 for img in soup.find_all('img'):
  src=img.get('src','')
  if src and not src.startswith('http'):check(page+' image asset '+src,(ROOT/src.lstrip('/')).is_file())
 # Absence of editorial placeholders and internal QA language on public page
 check(page+' no placeholder/review-package prose',not any(x in src.lower() for x in ['playback availability not independently confirmed','two untouched source composites','six panels extracted','review package','mu-book-cover-art']))
# Both headers identical except per-page aria-current on navigation.
a=parsed['index.html'].select_one('header .mast');b=parsed['portfolio.html'].select_one('header .mast')
for mast in [a,b]:
 for el in mast.select('[aria-current]'):el.attrs.pop('aria-current',None)
check('header and navigation markup parity',a.decode()==b.decode(),(a.decode()[:200],b.decode()[:200]))
check('home nav active correct',BeautifulSoup((ROOT/'index.html').read_text(),'html.parser').select_one('nav[aria-label="Main navigation"] a[aria-current="page"]') is not None)
check('book mock removed',not parsed['index.html'].select('.mu-book-cover-art'))
cover=ROOT/'assets/books/comeback-of-the-century-published-cover.jpg'
check('authentic cover is present',cover.is_file())
if cover.is_file():
 from PIL import Image
 with Image.open(cover) as im:
  check('cover dimensions',im.size==(943,1500),str(im.size))
 reference=Path('/mnt/data/71ee5LTgRqL._SL1500_.jpg')
 if reference.exists():check('cover bytes identical to author JPG',hashlib.sha256(reference.read_bytes()).hexdigest()==hashlib.sha256(cover.read_bytes()).hexdigest())
check('cover links to exact user Amazon link',parsed['index.html'].select_one('a.mu-book-cover-link').get('href')=='https://a.co/d/0e0VC77t')
check('original publications panel removed', 'Writing, video and fieldwork' not in (ROOT/'index.html').read_text() and not parsed['index.html'].select('.mu-publications'))
for pg in canonicals:
 nav=parsed[pg].select_one('nav.mu-social-links#selected-writing')
 check(pg+' footer social nav exists',nav is not None)
 if nav:
  links=nav.find_all('a')
  check(pg+' footer contains three distinct labelled links',len(links)==3 and len({a.get('href') for a in links})==3 and all(a.get_text(' ',strip=True) for a in links))
  check(pg+' supports platform/account labels',all(a.select_one('.mu-social-platform') and a.select_one('.mu-social-label') for a in links))
  check(pg+' icon assets present',all((ROOT/i['src']).is_file() for i in nav.find_all('img')))
check('footer links match on both pages',str(parsed['index.html'].select_one('nav.mu-social-links'))==str(parsed['portfolio.html'].select_one('nav.mu-social-links')))
check('old publication card CTA removed', 'Writing on Substack ↗' not in (ROOT/'index.html').read_text())
check('book CTA retained',any(a.get('href')=='https://a.co/d/0e0VC77t' for a in parsed['index.html'].select('a.mu-book-buy')))
check('Honolulu video retained',parsed['index.html'].select_one('iframe[src="https://www.youtube-nocookie.com/embed/j6mDC0QaW_s"]') is not None)
check('Mileka article link retained',any(a.get('href')=='https://mathewursua.substack.com/p/why-independent-photographers-must' for a in parsed['index.html'].select('a[href]')))
check('no GA fake measurement ID',not any(re.search(r'G-[A-Z0-9]{6,}',(ROOT/page).read_text()) for page in canonicals))
check('Option C steel gray CSS rules included','Lillian Option C' in (ROOT/'assets/site.css').read_text() and '#68757B' in (ROOT/'assets/site.css').read_text())
# Sitemaps must mention only available canonical pages
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
try:
 urls=[n.text for n in ET.parse(ROOT/'sitemap.xml').findall('.//s:loc',ns)]
 check('sitemap only published canonicals',urls==list(canonicals.values()),str(urls))
except Exception as e:check('sitemap XML parsed',False,str(e))
check('robots sitemap discovery', 'Sitemap: https://mathewursua.com/sitemap.xml' in (ROOT/'robots.txt').read_text())
for path,target in [('assets/index.html','https://mathewursua.com/'),('assets/portfolio.html','https://mathewursua.com/portfolio.html')]:
 s=BeautifulSoup((ROOT/path).read_text(),'html.parser')
 check(path+' legacy noindex',s.find('meta',attrs={'name':'robots'}).get('content')=='noindex,follow')
 check(path+' legacy canonical',s.find('link',attrs={'rel':'canonical'}).get('href')==target)

# RC4 regression: both-page JavaScript, common ribbon, and latest hotfix retained.
for page in canonicals:
 s=parsed[page]
 check(page+' shared JS loads normally',len(s.select('script[src="assets/site.js"][defer]'))==1)
 check(page+' exactly one JSON-LD script',len(s.select('script[type="application/ld+json"]'))==1)
 check(page+' no corrupt script tag', '<script ty<script' not in (ROOT/page).read_text() and '</script>fer=""' not in (ROOT/page).read_text())
 check(page+' no index-only a782 patch',not s.select('#mu-20261031-index-only-adjustments') and not s.select('#mu-20261031-image-fallbacks'))
 check(page+' shared header has authored signature',s.select_one('header .mu-signature-quote') is not None)
css_current=(ROOT/'assets/site.css').read_text()
js_current=(ROOT/'assets/site.js').read_text()
check('ribbon patch exists as common CSS','v1.7.2 RC4' in css_current and 'position: sticky !important' in css_current)
check('charcoal motto retained',parsed['index.html'].select_one('.mu-hero-strap').get_text(' ',strip=True)=='WITNESS. INVESTIGATE. CHALLENGE.' and '#25292b !important' in css_current)
check('shared fallback has hero and signature',all(x in js_current for x in ['.mu-hero-art img','.brand--signature img','raw.githubusercontent.com','mu-art-unavailable','mu-signature-text-fallback']))
check('preflight covers both pages',len(parsed)==2)

# Report
import tempfile
report=Path(tempfile.gettempdir())/'mathewursua-site-preflight-results.txt'
report.write_text('\n'.join(('PASS' if ok else 'FAIL')+' '+name+(' — '+str(info) if info and not ok else '') for name,ok,info in checks)+'\n'+f'\n{sum(x[1] for x in checks)} / {len(checks)} checks passed\n')
print(f'{sum(x[1] for x in checks)} / {len(checks)} checks passed; details: {report}')
for err in errors:print('ERROR',err)
sys.exit(1 if errors else 0)
