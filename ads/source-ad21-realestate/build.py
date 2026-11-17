import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
markup = open('../vlogo/markup.txt').read()
def logo(uid): return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 96 1156.01 208" preserveAspectRatio="xMidYMid meet" style="display:block;overflow:visible;width:100%;height:100%">'+markup.replace('__CLIP__','c'+uid).replace('__MASK__','m'+uid)+'</svg>'
# 6 x 10 blueprint cells that fill diagonally from the bottom-left corner
cells = ''.join('<i style="left:%dpx;top:%dpx" data-d="%.3f"></i>' % (c * 180 - 1, r * 192 - 1, ((9 - r) + c) * 0.022) for r in range(10) for c in range(6))
html = open('template.html').read()
html = html.replace('{{LOGO1}}', logo('1')).replace('{{LOGO2}}', logo('2')).replace('{{CELLS}}', cells)
assert '{{' not in html
open('ad.html', 'w').write(html)
print('built', len(html))
