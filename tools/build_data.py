import json, re, glob, pathlib, sys
from bs4 import BeautifulSoup as B
root=pathlib.Path(__file__).resolve().parents[1]
src=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else root.parent
D={k:json.load(open(glob.glob(str(src/f'*{k}*.json'))[0])) for k in ['hybrid','cooking','enchanting','gathering']}
def soup(k,i):return B(D[k]['pages'][i]['text']['content'],'html.parser')
def txt(n):return n.get_text(' ',strip=True)
def norm(s):return s.replace('’',"'").replace('‘',"'").strip()
def slug(s):return re.sub(r'[^a-z0-9]+','-',norm(s).lower()).strip('-')
def field(s,p):
 m=re.search(p,s,re.I);return m.group(1).strip() if m else None
def num(s,p):
 v=field(s,p);return int(v) if v else None
def mats(s):
 out=[]
 for x in s.split(';'):
  m=re.match(r'\s*(\d+)\s*[×x]\s*(.*?)\s*[.]?$',x.strip());
  if not m:raise ValueError(('material',s,x))
  name=norm(re.sub(r'\s*\(supplemental pantry item\)','',m[2],flags=re.I).rstrip('.'))
  out.append(dict(id=slug(name),name=name,qty=int(m[1])))
 return out
def block(h):
 out=[]
 for n in h.next_siblings:
  if getattr(n,'name',None) in ('h2','h3','hr'):break
  if getattr(n,'name',None):out.append(txt(n))
 return out
def rowdata(k,i):return [[txt(c) for c in tr.find_all('td')] for tr in soup(k,i).find_all('tr') if tr.find('td')]
recipes=[]; resources=[]; materials={}
def addmat(name,category,**kw):
 name=norm(name); id=slug(name);materials[id]=dict(id=id,name=name,category=category,**kw)
 return id
def rec(name,category,rarity,dc,minutes,gp,ingredients,tools,description,**kw):
 assert dc is not None and minutes is not None and gp is not None,(name,dc,minutes,gp)
 recipes.append(dict(id=slug(category+'-'+name),name=norm(name),category=category,rarity=rarity,dc=dc,minutes=minutes,gp=gp,materials=ingredients,tools=norm(tools),description=description,quantity=1,**kw))
for row in rowdata('hybrid',1)[:12]:
 name,rarity,identity,prop=row;id=addmat(name,'Mining',rarity=rarity,description=identity+' — '+prop);dc={'Common':10,'Uncommon':13,'Rare':16,'Very Rare':19}[rarity];resources.append(dict(id=id,name=name,category='Mining',rarity=rarity,searchDC=dc,harvestDC=dc,yieldFormula='1',regrowth=None,attempts=3,description=prop))
for i in range(3,15):
 category=['Herbalism','Flowers','Fungi','Wood','Creatures','Aquatic & Planar'][(i-3)//2]
 for h in soup('gathering',i).find_all('h3'):
  name=norm(txt(h));b=block(h);s=b[0];rarity=s.split('|')[0].strip();id=addmat(name,category,rarity=rarity,description='\n'.join(b));resources.append(dict(id=id,name=name,category=category,rarity=rarity,searchDC=num(s,r'Search DC (\d+)'),harvestDC=num(s,r'Harvest DC (\d+)'),yieldFormula=field(s,r'Yield (\d+d\d+|\d+)'),regrowth=None if category=='Creatures' else {'Common':7,'Uncommon':14,'Rare':30,'Very Rare':None}[rarity],attempts=1,description='\n'.join(b),where=field(' '.join(b),r'Where:\s*(.*?)\s*When:') or '',when=field(' '.join(b),r'When:\s*(.*?)\s*How to harvest:') or ''))
for i in range(5,14):
 for row in rowdata('cooking',i):
  name=txt(soup('cooking',i).find_all('tr')[1].find('strong')) if False else None
  # first strong in ingredient row, supplemental name plain
 for tr in soup('cooking',i).find_all('tr'):
  td=tr.find('td');
  if not td:continue
  name=txt(td.find('strong') or td);addmat(name,'Cooking',description=txt(tr))
for i in [4,5,6,10,11,12,17,18,20,21]:
 for h in soup('hybrid',i).find_all('h3'):
  name=field(txt(h),r'^\d+[.\s—–-]+(.+)$');
  if not name:continue
  b=block(h);s=' '.join(b);rarity=field(s,r'Rarity:\s*([^|]+?)\s*\|')
  if i<=12:
   mat=field(s,r'Materials:\s*(.*?)\s*\|\s*Required tools:');tools=field(s,r'Required tools:\s*(.*?)\s*\|\s*Attunement:');time=num(s,r'Time:\s*(\d+)\s*h');gp=num(s,r'Supplies:\s*(\d+)\s*gp');dc=num(s,r'Known Recipe DC:\s*(\d+)');effect=field(s,r'Result:\s*(.*)') or s
  else:
   mat=field(s,r'Materials:\s*(.*?)\s*Crafting:');tools=field(s,r'gp supplies;\s*(.*?)\s*Effect:');time=num(s,r'DC\s*\d+,\s*(\d+)\s*h');gp=num(s,r'(\d+)\s*gp supplies');dc=num(s,r'Crafting:\s*DC\s*(\d+)');effect=field(s,r'Effect:\s*(.*)') or s
  if not all([mat,tools,rarity]):raise ValueError((name,b))
  cat='Runecrafting' if i>=20 else 'Alchemy' if i in [12,17,18] else 'Engineering' if 'Tinker' in tools else 'Jewelcrafting' if 'Jeweler' in tools else 'Blacksmithing'
  att=bool(re.search(r'Attunement:\s*Yes|Attunement to the inscribed item required',s,re.I));target=field(effect,r'Engrave on (.*?)[.]') if cat=='Runecrafting' else None
  rec(name,cat,rarity,dc,time*60,gp,mats(mat),tools,'\n'.join(b),effect=effect,attunement=att,target=target,source=D['hybrid']['pages'][i]['name'])
for i in range(4,12):
 for sec in soup('enchanting',i).find_all('section'):
  h=sec.find('h4');rarity,target=txt(h.find('small')).strip('()').split(' • ');name=field(txt(h),r'^\w\d+ — (.*?)\s*\(');s=txt(sec);mat=field(s,r'Catalysts:\s*(.*?)\s*Check:');tools="Smith's Tools" if i<8 else "Jeweler's Tools" if i<10 else "Woodcarver's Tools or Jeweler's Tools or Smith's Tools";rec(name,'Enchanting',rarity,num(s,r'DC\s*(\d+)'),num(s,r'(\d+) hours')*60,num(s,r'(\d+) gp supplies'),mats(mat),tools,s,effect=field(s,r'Effect:\s*(.*?)\s*Attunement:'),attunement=rarity in ['Rare','Very Rare'],target=target,source=D['enchanting']['pages'][i]['name'])
for i in range(14,26):
 for h in soup('cooking',i).find_all('h3'):
  div=h.parent;s=txt(div);mins=num(s,r'Time:\s*(\d+) min');serv=num(s,r'Servings:\s*(\d+)');dc=num(s,r'Cooking DC:\s*(\d+)');ingredients=mats('; '.join(txt(li) for li in div.find('ul').find_all('li')));benefit=field(s,r'Meal Benefit:\s*(.*?)(?:Optional sides|Recipe is Averis|$)');rec(txt(h),'Cooking','Common',dc,mins,0,ingredients,"Cook's Utensils",s,effect=benefit,servings=serv,source=D['cooking']['pages'][i]['name'])
for r in recipes:
 if r['category'] in ['Blacksmithing','Engineering','Jewelcrafting']:
  m=re.search(r'\((\d+)\)$',r['name']);r['quantity']=int(m[1]) if m else 1
 if r['category']=='Cooking':r['quantity']=r['servings']
 for m in r['materials']:
  if m['id'] not in materials:print('UNMATCHED',r['name'],m['name']);addmat(m['name'],'Unresolved',description='Referenced by recipe; verify with GM.')
assert len(recipes)==267,len(recipes)
assert len(resources)==84,len(resources)
assert len(set(r['id'] for r in recipes))==267
out=dict(recipes=recipes,materials=list(materials.values()),resources=resources,regions=rowdata('gathering',2)[:9])
(root/'data/catalog.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('recipes',len(recipes),'materials',len(materials),'resources',len(resources))
