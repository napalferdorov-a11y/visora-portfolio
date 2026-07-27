# VISORA — Cinematic Portfolio

A dark, cinematic portfolio website for films & photography, featuring:

- **Hero** with your cut-out portrait, a cosmic/purple nebula backdrop, a big
  `VISORA` watermark behind you, and a **typing animation** on the headline.
- **Before / After colour-grade comparison** — drag the slider to reveal raw
  footage vs. the final graded look. This works with **video** or a still image.
- **Video showcase grid** (hover to preview).
- **Photography gallery** (masonry).
- **About** and a working **contact** form (opens the visitor's mail app).

Everything is plain HTML/CSS/JS — no build step, no framework. Open
`index.html` in a browser and it just works.

---

## 1. Add your own media

Drop your files into `assets/` using these exact names (or edit the paths in
`js/main.js`):

| What | Put it here | Notes |
|------|-------------|-------|
| **Your photo** (the cut-out) | `assets/images/portrait.png` | Use a **transparent PNG** (background removed) so it blends into the scene. Used in the hero + About. |
| **Before/After clip** | `assets/videos/showreel.mp4` | One clip is enough — the "before" side is auto-flattened to look ungraded. |
| Before/After still (optional) | `assets/images/after-poster.jpg` | Shown until/if the video loads. Replace with a frame from your clip. |
| Showcase videos | `assets/videos/film1.mp4` … `film6.mp4` | Titles/tags are set in `js/main.js`. |
| Video thumbnails | `assets/images/film1.jpg` … `film6.jpg` | Poster frame shown before hover. |
| Gallery photos | `assets/images/photo1.jpg` … `photo9.jpg` | Add/remove in the `photos` array in `js/main.js`. |

> **Tip — get a transparent cut-out:** upload your photo to a background
> remover (e.g. remove.bg) and export as PNG. That's what makes the portrait
> sit *inside* the purple glow like the reference design.

The current files are **placeholders** so the site looks complete out of the
box. Replace them with your real work.

## 2. True A/B before & after (optional)

By default the "before" side reuses your one clip and flattens it with a CSS
filter (low saturation/contrast) to fake the ungraded look. If you have a
**real ungraded export**, use two separate videos:

1. Put the raw clip at `assets/videos/showreel-before.mp4`.
2. In `index.html`, inside `.grade__before`, point the `<source>` to that file
   and remove the `grade__before video { filter: ... }` rule in `css/style.css`.

## 3. Edit text & links

- **Headline typing words:** `words` array at the top of `js/main.js`.
- **Taglines, section copy, social links:** directly in `index.html`.
- **Contact email:** search `hello@visora.com` in `index.html` / `js/main.js`.
- **Colours:** the `:root` variables at the top of `css/style.css`
  (`--violet`, `--magenta`, backgrounds).

## 4. Preview locally

```bash
# from this folder
python3 -m http.server 8000
# then open http://localhost:8000
```

## 5. Publish it (free)

**GitHub Pages**
1. Push this repo to GitHub.
2. Settings → Pages → Source: `Deploy from a branch` → pick your branch, `/root`.
3. Your site goes live at `https://<username>.github.io/<repo>/`.

**Netlify / Vercel** — drag-and-drop this folder, or connect the repo. No build
command needed; it's a static site.

---

Made for **VISORA** — cinematic films, commercial photography & creative direction.
