/* ==========================================================================
   VISORA — interactions
   ========================================================================== */
(function () {
  "use strict";

  /* ---------- 1. TYPING ANIMATION ("VISORA") ---------- */
  const words = ["VISORA", "A FILMMAKER", "A COLOURIST", "VISORA"];
  const typed = document.getElementById("typed");
  let w = 0, c = 0, deleting = false;

  function type() {
    if (!typed) return;
    const word = words[w];
    typed.textContent = deleting ? word.slice(0, c--) : word.slice(0, c++);

    if (!deleting && c === word.length + 1) {          // finished typing
      deleting = true;
      return setTimeout(type, 1600);
    }
    if (deleting && c === 0) {                          // finished deleting
      deleting = false;
      w = (w + 1) % words.length;
      return setTimeout(type, 350);
    }
    setTimeout(type, deleting ? 55 : 110);
  }
  type();

  /* ---------- 2. BEFORE / AFTER COLOUR GRADE SLIDER ---------- */
  function initGrade(root) {
    const before  = root.querySelector(".grade__before");
    const divider = root.querySelector(".grade__divider");
    const range   = root.querySelector(".grade__range");
    if (!before || !divider || !range) return;

    function set(pct) {
      pct = Math.max(0, Math.min(100, pct));
      before.style.width = pct + "%";
      divider.style.left = pct + "%";
    }
    range.addEventListener("input", (e) => set(+e.target.value));

    // pointer drag anywhere on the media
    const media = root.querySelector(".grade__media");
    let dragging = false;
    const move = (clientX) => {
      const r = media.getBoundingClientRect();
      const pct = ((clientX - r.left) / r.width) * 100;
      set(pct);
      range.value = pct;
    };
    media.addEventListener("pointerdown", (e) => { dragging = true; move(e.clientX); });
    window.addEventListener("pointermove", (e) => dragging && move(e.clientX));
    window.addEventListener("pointerup", () => (dragging = false));

    set(50);
  }
  document.querySelectorAll(".grade").forEach(initGrade);

  /* ---------- 3. VIDEO SHOWCASE (edit this data) ---------- */
  const films = [
    { title: "Nightfall",        tag: "MUSIC VIDEO",   video: "assets/videos/film1.mp4", poster: "assets/images/film1.jpg" },
    { title: "Golden Hour",      tag: "BRAND FILM",    video: "assets/videos/film2.mp4", poster: "assets/images/film2.jpg" },
    { title: "Concrete Dreams",  tag: "SHORT FILM",    video: "assets/videos/film3.mp4", poster: "assets/images/film3.jpg" },
    { title: "Neon Streets",     tag: "COMMERCIAL",    video: "assets/videos/film4.mp4", poster: "assets/images/film4.jpg" },
    { title: "Portrait Series",  tag: "FASHION",       video: "assets/videos/film5.mp4", poster: "assets/images/film5.jpg" },
    { title: "The Coast",        tag: "TRAVEL",        video: "assets/videos/film6.mp4", poster: "assets/images/film6.jpg" }
  ];

  const grid = document.getElementById("films");
  if (grid) {
    films.forEach((f) => {
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
        <video muted loop playsinline preload="metadata" poster="${f.poster}"
               onerror="this.style.display='none'">
          <source src="${f.video}" type="video/mp4">
        </video>
        <div class="card__play"></div>
        <div class="card__overlay">
          <h3>${f.title}</h3>
          <span>${f.tag}</span>
        </div>`;
      const vid = card.querySelector("video");
      card.addEventListener("mouseenter", () => vid.play().catch(() => {}));
      card.addEventListener("mouseleave", () => { vid.pause(); vid.currentTime = 0; });
      grid.appendChild(card);
    });
  }

  /* ---------- 4. PHOTO GALLERY (edit count / sources) ---------- */
  const photos = [
    "assets/images/photo1.jpg", "assets/images/photo2.jpg", "assets/images/photo3.jpg",
    "assets/images/photo4.jpg", "assets/images/photo5.jpg", "assets/images/photo6.jpg",
    "assets/images/photo7.jpg", "assets/images/photo8.jpg", "assets/images/photo9.jpg"
  ];
  const gallery = document.getElementById("gallery");
  if (gallery) {
    photos.forEach((src, i) => {
      const fig = document.createElement("figure");
      fig.innerHTML = `<img src="${src}" alt="VISORA photography ${i + 1}"
        onerror="this.outerHTML='<div class=&quot;ph&quot;>PHOTO ${i + 1}</div>'">`;
      gallery.appendChild(fig);
    });
  }

  /* ---------- 5. SCROLL REVEAL ---------- */
  const io = new IntersectionObserver(
    (entries) => entries.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
    { threshold: 0.12 }
  );
  document.querySelectorAll(".section__head, .grade, .card, .about, .contact").forEach((el) => {
    el.setAttribute("data-reveal", "");
    io.observe(el);
  });

  /* ---------- 6. YEAR + CONTACT (mailto) ---------- */
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  window.VISORA = {
    sendMail(e) {
      e.preventDefault();
      const f = e.target;
      const subject = encodeURIComponent(`New enquiry from ${f.name.value}`);
      const body = encodeURIComponent(`${f.message.value}\n\n— ${f.name.value} (${f.email.value})`);
      window.location.href = `mailto:hello@visora.com?subject=${subject}&body=${body}`;
      return false;
    }
  };
})();
