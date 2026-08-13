import json, math, os, urllib.parse, urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'generated'; OUT.mkdir(exist_ok=True)
OWNER=os.environ.get('GITHUB_REPOSITORY','').split('/',1)[0]; TOKEN=os.environ.get('GITHUB_TOKEN','')
API='https://api.github.com'

def get(path, default={}):
    try:
        h={'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','User-Agent':'github-profile-rpg'}
        if TOKEN: h['Authorization']=f'Bearer {TOKEN}'
        r=urllib.request.urlopen(urllib.request.Request(API+path,headers=h),timeout=20)
        return json.loads(r.read().decode())
    except Exception as e:
        print('API warning:',e); return default

def esc(v):
    return str(v).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def level(stats):
    xp=stats['activity']*10+stats['repos']*100+stats['stars']*30+stats['followers']*20+stats['prs']*50
    lv=max(1,int(math.sqrt(xp/100))+1); a=(lv-1)**2*100; b=lv**2*100
    return lv,max(0,min(100,int((xp-a)/(b-a)*100))),xp

def main():
    cfg=json.load(open(ROOT/'config.json',encoding='utf8'))
    u=get('/users/'+urllib.parse.quote(OWNER),{})
    repos=get('/users/'+urllib.parse.quote(OWNER)+'/repos?per_page=100&type=owner',[])
    stars=sum(int(x.get('stargazers_count',0)) for x in repos)
    prs=get('/search/issues?q='+urllib.parse.quote(f'is:pr author:{OWNER}')+'&per_page=1',{}).get('total_count',0)
    # Lightweight activity score; see INSTALL.md for exact GraphQL upgrade.
    activity=sum(min(50,max(1,int(x.get('size',0))//100+1)) for x in repos if not x.get('fork'))
    s={'username':OWNER,'name':u.get('name') or OWNER,'repos':int(u.get('public_repos',len(repos))),'stars':stars,'followers':int(u.get('followers',0)),'prs':int(prs),'activity':activity}
    lv,exp,xp=level(s)
    terminal=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="390"><style>text{{font-family:monospace}}.g{{fill:#39ff88}}.t{{fill:#e6edf3}}.m{{fill:#8b949e}}.y{{fill:#ffd166}}</style><rect width="900" height="390" rx="16" fill="#090b10"/><rect x="18" y="18" width="864" height="354" rx="12" fill="#0d1117" stroke="#30363d"/><circle cx="40" cy="40" r="6" fill="#ff5f56"/><circle cx="60" cy="40" r="6" fill="#ffbd2e"/><circle cx="80" cy="40" r="6" fill="#27c93f"/><text x="42" y="78" class="g" font-size="16">root@github:~$ whoami</text><text x="42" y="102" class="t" font-size="16">{esc(cfg['display_name'])} — {esc(cfg['title'])}</text><text x="42" y="138" class="g" font-size="16">root@github:~$ neofetch</text><text x="42" y="162" class="m" font-size="15">USER        : {esc(s['username'])}</text><text x="42" y="186" class="m" font-size="15">REPOSITORIES: {s['repos']}</text><text x="42" y="210" class="m" font-size="15">STARS       : {s['stars']}</text><text x="42" y="234" class="m" font-size="15">FOLLOWERS   : {s['followers']}</text><text x="42" y="258" class="m" font-size="15">PULL REQS   : {s['prs']}</text><text x="42" y="294" class="g" font-size="16">root@github:~$ ./quest</text><text x="42" y="318" class="y" font-size="15">{esc(cfg['current_quest'])}</text><text x="42" y="352" class="g" font-size="15">root@github:~$ _</text></svg>'''
    skills=list(cfg['skills'].items()); skill_svg=''
    for i,(name,val) in enumerate(skills):
        x=45 if i<3 else 470; y=390+(i if i<3 else i-3)*48; w=190; filled=w*max(0,min(100,int(val)))/100
        skill_svg+=f'<text x="{x}" y="{y}" class="t" font-size="15">{esc(name)}</text><rect x="{x+150}" y="{y-14}" width="{w}" height="14" rx="5" fill="#21262d"/><rect x="{x+150}" y="{y-14}" width="{filled:.1f}" height="14" rx="5" fill="'+('#39ff88' if i<3 else '#58a6ff')+f'"/><text x="{x+350}" y="{y}" class="m" font-size="13">{int(val)}/100</text>'
    rpg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="610"><style>text{{font-family:monospace}}.g{{fill:#39ff88}}.t{{fill:#e6edf3}}.m{{fill:#8b949e}}.c{{fill:#58a6ff}}.y{{fill:#ffd166}}</style><rect width="900" height="610" rx="16" fill="#090b10"/><rect x="18" y="18" width="864" height="574" rx="12" fill="#0d1117" stroke="#30363d"/><text x="45" y="58" class="g" font-size="22">DEVELOPER RPG // CHARACTER SHEET</text><text x="45" y="92" class="t" font-size="18">{esc(s['name'])} @ {esc(s['username'])}</text><text x="45" y="120" class="m" font-size="14">{esc(cfg['title'])}</text><rect x="45" y="145" width="250" height="170" rx="10" fill="#161b22" stroke="#30363d"/><text x="72" y="180" class="c" font-size="17">PLAYER</text><text x="72" y="225" class="t" font-size="34">LV. {lv}</text><text x="72" y="253" class="m" font-size="12">XP {xp:,}</text><rect x="72" y="272" width="190" height="12" rx="5" fill="#21262d"/><rect x="72" y="272" width="{190*exp/100:.1f}" height="12" rx="5" fill="#39ff88"/><text x="72" y="302" class="g" font-size="12">NEXT LEVEL {exp}%</text><text x="330" y="180" class="g" font-size="17">GITHUB ATTRIBUTES</text>'''
    y=215
    for label,val in [('REPOSITORIES',s['repos']),('STARS',s['stars']),('FOLLOWERS',s['followers']),('PULL REQUESTS',s['prs']),('ACTIVITY SCORE',s['activity'])]:
        rpg+=f'<text x="330" y="{y}" class="t" font-size="14">{label}</text><text x="620" y="{y}" class="c" font-size="14">{val:,}</text>'; y+=27
    rpg+='<text x="45" y="355" class="g" font-size="18">SKILL TREE</text>'+skill_svg+f'<text x="45" y="545" class="g" font-size="17">CURRENT QUEST</text><text x="210" y="545" class="y" font-size="14">{esc(cfg["current_quest"])}</text><text x="45" y="575" class="m" font-size="12">Generated automatically by GitHub Actions</text></svg>'
    (OUT/'terminal.svg').write_text(terminal,encoding='utf8'); (OUT/'rpg.svg').write_text(rpg,encoding='utf8')
    (OUT/'stats.json').write_text(json.dumps({'generated_at':datetime.now(timezone.utc).isoformat(),**s,'level':lv,'exp':exp,'xp':xp},indent=2),encoding='utf8')

if __name__=='__main__': main()
