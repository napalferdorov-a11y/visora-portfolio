import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
m=open('../vlogo/markup.txt').read()
def logo(u): return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 96 1156.01 208" preserveAspectRatio="xMidYMid meet" style="display:block;overflow:visible;width:100%;height:100%">'+m.replace('__CLIP__','c'+u).replace('__MASK__','m'+u)+'</svg>'
h=open('template.html').read().replace('{{LOGO_S}}',logo('s')).replace('{{LOGO_L}}',logo('l'))
open('reel.html','w').write(h); print('built')
