import re,os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
markup=open('../vlogo/markup.txt').read()
def logo(uid): return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 96 1156.01 208" preserveAspectRatio="xMidYMid meet" style="display:block;overflow:visible;width:100%;height:100%">'+markup.replace('__CLIP__','c'+uid).replace('__MASK__','m'+uid)+'</svg>'
def hud(cls=''):
    return f'''<div class="hud {cls}"><i class="c tl"></i><i class="c tr"></i><i class="c bl"></i><i class="c br"></i>
<div class="rec"><b class="dot"></b>REC</div><div class="tc">00:00:00:00</div></div>'''
html=open('template.html').read()
html=html.replace('{{LOGO1}}',logo('1')).replace('{{LOGO2}}',logo('2'))
def card(k):
    y=k*1040
    return (f'<div class="sk" style="top:{y}px"><div class="av"></div><div class="b" style="left:96px;top:12px;width:{260+(k*37)%90}px"></div>'
            f'<div class="b" style="left:96px;top:46px;width:{150+(k*23)%60}px;height:16px"></div><div class="m"></div>'
            f'<div class="b" style="left:0;top:884px;width:{640+(k*53)%180}px"></div><div class="b" style="left:0;top:920px;width:{420+(k*41)%160}px"></div>'
            f'<div class="b" style="left:0;top:956px;width:{220+(k*29)%80}px;height:18px"></div></div>')
html=html.replace('{{FEED}}',''.join(card(k) for k in range(9)))
html=re.sub(r'\{\{HUD(?::([\w-]+))?\}\}',lambda m:hud(m.group(1) or ''),html)
open('ad.html','w').write(html)
print('built',len(html))
