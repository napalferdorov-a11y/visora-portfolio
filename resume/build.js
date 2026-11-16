const { chromium } = require('playwright');
const path = require('path');

const T = {
  fr: {
    file: 'CV-Nizar-Zouhri-Videaste-Photographe-FR.pdf',
    title: 'Vidéaste & Photographe — Production de contenu pour marques',
    loc: 'Rabat, Maroc · Expérience internationale · Disponible en déplacement',
    profileH: 'Profil',
    profile: "Fondateur de VISORA Production, studio de production créative au Maroc. Je réalise des films de marque, des publicités et du contenu mensuel pour les entreprises, du script jusqu'aux fichiers finaux. Je dirige une équipe de monteurs et de créateurs de contenu, ce qui me permet de livrer vite et en volume. Je travaille en direct avec les marques et en marque blanche pour les agences de communication.",
    expH: 'Expérience',
    intl: ['Vidéaste & photographe — projets internationaux', 'Russie · Bali (Indonésie) · Thaïlande', 'Projets récents', "Tournages photo et vidéo à l'étranger pour des marques et des clients privés, de la préparation au montage final."],
    role: 'Fondateur, vidéaste & photographe',
    co: 'VISORA Production · Maroc',
    dates: 'Indépendant',
    bullets: [
      "Films de marque de 60 à 120 s pour sites web, LinkedIn et présentations investisseurs.",
      "Spots publicitaires de 15 à 30 s pour Meta, YouTube et TV, construits autour d'une offre et d'un appel à l'action.",
      "Contenu mensuel : 8 à 12 vidéos courtes par mois pour Reels, TikTok et LinkedIn, planifiées avec l'équipe marketing du client.",
      "Portraits de dirigeants, photos d'équipe et interviews pour rapports, presse et recrutement.",
      "Photos produit en studio et vidéos courtes pour catalogues, e-commerce et publicités.",
      "Couverture d'événements, lancements et salons, avec un clip résumé livré le jour même.",
      "Direction d'une équipe de monteurs et de créateurs de contenu : montage, déclinaisons de formats et contenu réseaux sociaux.",
      "Production en marque blanche pour agences, sous NDA, dans le respect de leurs délais.",
    ],
    secH: 'Domaines',
    sectors: ['Marques & publicité', 'Immobilier', 'Shootings privés', 'Courts-métrages', 'Contenu réseaux sociaux', 'Événements'],
    skillsH: 'Compétences',
    skills: [
      'Écriture de script et liste de plans',
      'Tournage caméra cinéma',
      'Prise de son sans fil',
      'Montage et étalonnage',
      'Création de contenu réseaux sociaux',
      "Direction d'équipe de montage",
      'Sous-titres arabe et français',
      'Formats 16:9, 9:16 et 1:1',
      'Photo portrait, produit et événement',
    ],
    methodH: 'Méthode de travail',
    method: [
      ['Devis', 'prix fixe sous 24 h'],
      ['Premier montage', '5 à 7 jours après le tournage'],
      ['Révisions', '2 tours inclus'],
      ['Projet complet', '2 à 3 semaines'],
    ],
    langH: 'Langues',
    langs: ['Arabe', 'Français', 'Anglais'],
    lookH: 'Recherche',
    look: "Missions freelance, collaborations régulières avec agences et postes de vidéaste/photographe à Rabat et dans la région Rabat-Salé-Kénitra.",
    port: 'Portfolio',
    phone: 'Téléphone',
  },
  en: {
    file: 'CV-Nizar-Zouhri-Videographer-Photographer-EN.pdf',
    title: 'Videographer & Photographer — Brand content production',
    loc: 'Rabat, Morocco · International experience · Available for travel',
    profileH: 'Profile',
    profile: "Founder of VISORA Production, a creative production studio in Morocco. I make brand films, ads and monthly content for companies, from the script to the final files. I lead a team of editors and content creators, so projects are delivered fast and at volume. I work directly with brands and as a white-label partner for advertising agencies.",
    expH: 'Experience',
    intl: ['International videographer & photographer', 'Russia · Bali (Indonesia) · Thailand', 'Latest projects', 'Photo and video shoots abroad for brands and private clients, from preparation to the final edit.'],
    role: 'Founder, videographer & photographer',
    co: 'VISORA Production · Morocco',
    dates: 'Freelance',
    bullets: [
      "60 to 120 second brand films for websites, LinkedIn and investor meetings.",
      "15 to 30 second ads for Meta, YouTube and TV, written around one offer and one call to action.",
      "Monthly content: 8 to 12 short videos a month for Reels, TikTok and LinkedIn, planned with the client's marketing team.",
      "Leadership portraits, team photos and interview videos for reports, press and recruitment.",
      "Studio product photos and short product videos for catalogues, e-commerce and ads.",
      "Conferences, openings and trade shows, with a highlight clip delivered the same day.",
      "Lead a team of editors and content creators covering editing, format versions and social media content.",
      "White-label production for agencies, under NDA, delivered to their schedule.",
    ],
    secH: 'What I do',
    sectors: ['Brands & advertising', 'Real estate', 'Private shoots', 'Short films', 'Social media content', 'Events'],
    skillsH: 'Skills',
    skills: [
      'Scriptwriting and shot lists',
      'Cinema camera operation',
      'Wireless sound recording',
      'Editing and colour grading',
      'Social media content creation',
      'Leading an editing team',
      'Arabic and French subtitles',
      '16:9, 9:16 and 1:1 delivery',
      'Portrait, product and event photography',
    ],
    methodH: 'How I work',
    method: [
      ['Quote', 'fixed price within 24 h'],
      ['First cut', '5 to 7 days after the shoot'],
      ['Revisions', '2 rounds included'],
      ['Full project', '2 to 3 weeks'],
    ],
    langH: 'Languages',
    langs: ['Arabic', 'French', 'English'],
    lookH: 'Looking for',
    look: "Freelance projects, ongoing agency partnerships and videographer/photographer roles in Rabat and the Rabat-Salé-Kénitra region.",
    port: 'Portfolio',
    phone: 'Phone',
  },
};

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

function html(t) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>
  @page { size: A4; margin: 0; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: "Helvetica Neue", Arial, sans-serif; color: #1c1c1a; font-size: 9.6pt; line-height: 1.4; }
  .page { width: 210mm; height: 296.5mm; overflow: hidden; display: grid; grid-template-columns: 64mm 1fr; }
  aside { background: #121211; color: #e9e6df; padding: 13mm 8mm 12mm 10mm; }
  main { padding: 13mm 13mm 12mm 11mm; }
  .brand { font-size: 8pt; letter-spacing: .22em; color: #9aa38c; font-weight: 700; margin-bottom: 4mm; }
  h1 { font-size: 23pt; line-height: 1.05; letter-spacing: -.01em; margin-bottom: 3mm; }
  .title { font-size: 11.5pt; font-weight: 600; color: #4f5844; margin-bottom: 1.5mm; }
  .loc { font-size: 9pt; color: #6b6b66; margin-bottom: 4mm; }
  h2 { font-size: 8pt; letter-spacing: .18em; text-transform: uppercase; font-weight: 700; color: #78816c; margin: 4.8mm 0 2.2mm; }
  aside h2 { color: #9aa38c; margin-top: 7mm; }
  aside h2:first-of-type { margin-top: 0; }
  .contact div { margin-bottom: 2mm; font-size: 9pt; word-break: break-word; }
  .contact b { display: block; font-size: 7pt; letter-spacing: .14em; color: #8c8a83; font-weight: 600; }
  aside ul { list-style: none; }
  aside li { font-size: 9pt; margin-bottom: 1.6mm; padding-left: 3.5mm; position: relative; }
  aside li::before { content: ""; position: absolute; left: 0; top: 1.9mm; width: 1.4mm; height: 1.4mm; background: #78816c; border-radius: 50%; }
  p { margin-bottom: 2mm; }
  .role { display: flex; justify-content: space-between; align-items: baseline; }
  .role strong { font-size: 11pt; }
  .role span { font-size: 8.5pt; color: #6b6b66; white-space: nowrap; padding-left: 3mm; }
  .intl { margin-bottom: 3.5mm; }
  .co { color: #4f5844; font-weight: 600; font-size: 9.5pt; margin-bottom: 2.5mm; }
  main ul { padding-left: 4.5mm; }
  main li { margin-bottom: 1.1mm; }
  main ul.cols { columns: 2; column-gap: 6mm; }
  main ul.cols li { break-inside: avoid; font-weight: 600; }
  .method { display: grid; grid-template-columns: 1fr 1fr; gap: 2mm; }
  .method div { background: #f3f0ea; border-radius: 2mm; padding: 2mm 3mm; }
  .method b { display: block; font-size: 9pt; }
  .method span { font-size: 8.5pt; color: #55554f; }
  </style></head><body><div class="page">
  <aside>
    <h2>Contact</h2>
    <div class="contact">
      <div><b>${t.phone.toUpperCase()}</b>+212 7 19 07 93 14</div>
      <div><b>WHATSAPP</b>+66 65 870 5616</div>
      <div><b>EMAIL</b>support@visoraprod.com</div>
      <div><b>INSTAGRAM</b>@visoraprod</div>
      <div><b>${t.port.toUpperCase()}</b>visoraprod.com</div>
    </div>
    <h2>${t.skillsH}</h2>
    <ul>${t.skills.map((s) => `<li>${esc(s)}</li>`).join('')}</ul>
    <h2>${t.langH}</h2>
    <ul>${t.langs.map((s) => `<li>${esc(s)}</li>`).join('')}</ul>
  </aside>
  <main>
    <div class="brand">VISORA PRODUCTION</div>
    <h1>Nizar Zouhri</h1>
    <div class="title">${esc(t.title)}</div>
    <div class="loc">${esc(t.loc)}</div>
    <h2>${t.profileH}</h2>
    <p>${esc(t.profile)}</p>
    <h2>${t.expH}</h2>
    <div class="role"><strong>${esc(t.intl[0])}</strong><span>${esc(t.intl[2])}</span></div>
    <div class="co">${esc(t.intl[1])}</div>
    <p class="intl">${esc(t.intl[3])}</p>
    <div class="role"><strong>${esc(t.role)}</strong><span>${esc(t.dates)}</span></div>
    <div class="co">${esc(t.co)}</div>
    <ul>${t.bullets.map((b) => `<li>${esc(b)}</li>`).join('')}</ul>
    <h2>${t.secH}</h2>
    <ul class="cols">${t.sectors.map((s) => `<li>${esc(s)}</li>`).join('')}</ul>
    <h2>${t.lookH}</h2>
    <p>${esc(t.look)}</p>
  </main>
  </div></body></html>`;
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  for (const t of Object.values(T)) {
    await page.setContent(html(t), { waitUntil: 'load' });
    await page.pdf({ path: path.join(__dirname, t.file), format: 'A4', printBackground: true });
    await page.screenshot({ path: path.join(__dirname, t.file.replace('.pdf', '.png')), fullPage: true });
  }
  await browser.close();
})();
