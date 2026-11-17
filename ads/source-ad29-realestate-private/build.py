import os, math
os.chdir(os.path.dirname(os.path.abspath(__file__)))
markup = open('../vlogo/markup.txt').read()
def logo(uid): return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 96 1156.01 208" preserveAspectRatio="xMidYMid meet" style="display:block;overflow:visible;width:100%;height:100%">'+markup.replace('__CLIP__','c'+uid).replace('__MASK__','m'+uid)+'</svg>'

def spiral(W, target):
    """golden spiral as quarter arcs, carved bottom/right/top/left, shifted so it converges on `target`"""
    phi = (1 + 5 ** .5) / 2
    x, y, w, h = 0.0, 0.0, W, W * phi
    pts = []
    for i in range(12):
        side = ['bottom', 'right', 'top', 'left'][i % 4]
        if side == 'bottom':
            s = w; cx, cy = x, y + h - s; a0, a1 = 90, 0; h -= s
        elif side == 'right':
            s = h; cx, cy = x + w - s, y + s; a0, a1 = 0, -90; w -= s
        elif side == 'top':
            s = w; cx, cy = x + s, y + s; a0, a1 = -90, -180; y += s; h -= s
        else:
            s = h; cx, cy = x + s, y; a0, a1 = 180, 90; x += s; w -= s
        for j in range(25):
            a = math.radians(a0 + (a1 - a0) * j / 24)
            pts.append((cx + s * math.cos(a), cy + s * math.sin(a)))
    ex, ey = pts[-1]
    dx, dy = target[0] - ex, target[1] - ey
    return 'M' + ' L'.join('%.1f,%.1f' % (px + dx, py + dy) for px, py in pts)

holes = ''.join('<i style="left:%dpx;top:%dpx"></i>' % (13 + 60 * k, top) for k in range(18) for top in (12, 574))
html = open('template.html').read()
html = html.replace('{{LOGO1}}', logo('1')).replace('{{LOGO2}}', logo('2'))
html = html.replace('{{SPIRAL}}', spiral(980, (560, 470))).replace('{{SPROCKETS}}', holes)
assert '{{' not in html
open('ad.html', 'w').write(html)
print('built', len(html))
