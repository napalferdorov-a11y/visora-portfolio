# VISORA — About (Next.js)

An animated **About** page for VISORA, built in a modern editorial style
(big Geist display type, mono `{ }` labels, light theme + violet accent, scroll
reveals, count-up stats, numbered process, testimonial slider, logo marquee, and
a giant footer wordmark).

> Design language and interaction patterns were studied from a reference site;
> **all content, copy, imagery and branding here are original to VISORA**. The
> images in `public/img/` are abstract placeholders — swap them for your own work.

## Stack
- Next.js 14 (App Router) · React · TypeScript
- Tailwind CSS
- Framer Motion (scroll reveals, word-by-word heading, count-up, slider)
- Geist / Geist Mono (via the `geist` package)

## Run locally
```bash
cd visora-next
npm install
npm run dev        # http://localhost:3000
```

## Where to edit
- Page composition & copy: `app/page.tsx`
- Nav links: `components/Navbar.tsx`
- Testimonials: `components/Testimonials.tsx`
- Marquee brands: `components/Marquee.tsx`
- Motion helpers: `components/Reveal.tsx`
- Colors / type tokens: `app/globals.css` (`:root`)
- Images: `public/img/` (replace the placeholders)

## Build
```bash
npm run build && npm run start
```
