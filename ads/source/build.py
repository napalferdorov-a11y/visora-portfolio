import re,os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
markup=open('../vlogo/markup.txt').read()
def logo(uid): return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 96 1156.01 208" preserveAspectRatio="xMidYMid meet" style="display:block;overflow:visible;width:100%;height:100%">'+markup.replace('__CLIP__','c'+uid).replace('__MASK__','m'+uid)+'</svg>'
def hud(cls=''):
    return f'''<div class="hud {cls}"><i class="c tl"></i><i class="c tr"></i><i class="c bl"></i><i class="c br"></i>
<div class="rec"><b class="dot"></b>REC</div><div class="tc">00:00:00:00</div></div>'''
html=open('template.html').read()
html=html.replace('{{LOGO1}}',logo('1')).replace('{{LOGO2}}',logo('2'))
html=re.sub(r'\{\{HUD(?::([\w-]+))?\}\}',lambda m:hud(m.group(1) or ''),html)
open('ad.html','w').write(html)
print('built',len(html))
