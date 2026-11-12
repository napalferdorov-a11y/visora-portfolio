import Image from "next/image";
import Navbar from "@/components/Navbar";
import Marquee from "@/components/Marquee";
import Testimonials from "@/components/Testimonials";
import { Reveal, HeadingReveal, CountUp } from "@/components/Reveal";

const STATS = [
  { to: 98, suffix: "%", label: "Client satisfaction rate" },
  { to: 40, suffix: "+", label: "Brands & creators worked with" },
  { to: 500, suffix: "+", label: "Projects delivered" },
  { to: 85, suffix: "%", label: "Repeat clients" },
];

const PROCESS = [
  { n: "01", t: "Discovery & direction", d: "Every project starts with understanding your brand, audience and goals — and the message your visuals need to carry." },
  { n: "02", t: "Concept & planning", d: "I shape the story, shot list and look — from locations to wardrobe — so nothing on the day is left to chance." },
  { n: "03", t: "Shoot day", d: "Direction, lighting and camera handled end to end. You show up and look good; I take care of the rest." },
  { n: "04", t: "Edit & grade", d: "Editing, sound and the cinematic colour grade that makes the final result look genuinely premium." },
];

export default function About() {
  return (
    <main className="bg-white">
      <Navbar />

      {/* ============ BANNER ============ */}
      <section className="pt-40 md:pt-52 pb-20">
        <div className="wrap">
          <Reveal><p className="eyebrow">About VISORA</p></Reveal>
          <HeadingReveal
            text="The eye behind the frame"
            className="display mt-6 text-[clamp(3rem,9vw,7.5rem)] text-[#0c0c0c] max-w-[14ch]"
          />
          <Reveal delay={0.2}>
            <p className="mt-8 max-w-xl text-lg text-[#444] leading-relaxed">
              I&rsquo;m VISORA — a filmmaker and photographer building cinematic
              brand stories that make businesses impossible to ignore. From the
              first frame to the final grade, every project is crafted with intent.
            </p>
          </Reveal>

          <div className="grid grid-cols-1 md:grid-cols-[0.8fr_1.2fr] gap-5 mt-14">
            <Reveal className="group overflow-hidden">
              <div className="relative aspect-[4/5] overflow-hidden">
                <Image src="/img/portrait.jpg" alt="VISORA portrait" fill
                  className="object-cover transition-transform duration-700 group-hover:scale-105" />
              </div>
            </Reveal>
            <Reveal delay={0.12} className="group overflow-hidden">
              <div className="relative aspect-[16/10] overflow-hidden">
                <Image src="/img/photographer.jpg" alt="VISORA on set" fill
                  className="object-cover transition-transform duration-700 group-hover:scale-105" />
              </div>
            </Reveal>
          </div>

          <Reveal delay={0.1}>
            <p className="mono text-sm text-[#888] mt-8">
              FILM&nbsp;&nbsp;//&nbsp;&nbsp;BRAND&nbsp;&nbsp;//&nbsp;&nbsp;PRODUCT&nbsp;&nbsp;//&nbsp;&nbsp;EVENTS
            </p>
          </Reveal>
        </div>
      </section>

      {/* ============ STATS ============ */}
      <section className="py-14">
        <div className="wrap grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-x-10 gap-y-10">
          {STATS.map((s, i) => (
            <Reveal key={s.label} delay={i * 0.08}>
              <div className="border-t border-[#111] pt-4">
                <CountUp to={s.to} suffix={s.suffix}
                  className="display block text-[clamp(2.6rem,5vw,4rem)] text-[#0c0c0c]" />
                <p className="text-[#555] mt-3 text-[15px]">{s.label}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* ============ VISION / PROCESS ============ */}
      <section className="bg-[var(--paper)] py-24 md:py-32 mt-10">
        <div className="wrap">
          <Reveal><p className="eyebrow">My process</p></Reveal>
          <Reveal delay={0.1}>
            <h2 className="display mt-5 text-[clamp(2.2rem,5vw,4rem)] text-[#0c0c0c] max-w-[20ch]">
              Vision behind the work
            </h2>
          </Reveal>

          <div className="mt-16 divide-y divide-[#dcdcd8] border-y border-[#dcdcd8]">
            {PROCESS.map((p, i) => (
              <Reveal key={p.n} delay={i * 0.05}>
                <div className="grid grid-cols-1 md:grid-cols-[120px_1fr] gap-4 md:gap-10 py-8 group">
                  <span className="mono text-sm text-[var(--accent)]">{"{ " + p.n + " }"}</span>
                  <div className="md:flex md:items-baseline md:justify-between md:gap-12">
                    <h3 className="text-2xl md:text-3xl text-[#0c0c0c] font-medium tracking-tight md:w-[34%] transition-transform duration-500 group-hover:translate-x-1">
                      {p.t}
                    </h3>
                    <p className="text-[#555] mt-3 md:mt-0 md:flex-1 leading-relaxed">{p.d}</p>
                  </div>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* ============ TESTIMONIALS ============ */}
      <section className="py-24 md:py-32">
        <div className="wrap">
          <Reveal className="text-center"><p className="eyebrow">Testimonials</p></Reveal>
          <Reveal delay={0.1}>
            <h2 className="display text-center mt-5 mb-16 text-[clamp(2rem,4.5vw,3.5rem)] text-[#0c0c0c]">
              Trusted by growing brands
            </h2>
          </Reveal>
          <Testimonials />
        </div>
      </section>

      {/* ============ MARQUEE ============ */}
      <Marquee />

      {/* ============ FOOTER ============ */}
      <footer id="contact" className="bg-[#0c0c0c] text-white pt-24 overflow-hidden">
        <div className="wrap">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 pb-20 border-b border-white/10">
            <div className="max-w-md">
              <p className="text-white/70 leading-relaxed">
                VISORA — cinematic films &amp; photography for brands that want to
                look as good as they are.
              </p>
              <h3 className="display text-3xl mt-10 mb-5">Be part of the community</h3>
              <form className="flex items-center gap-3 border-b border-white/25 pb-3 max-w-sm">
                <input type="email" placeholder="Email"
                  className="bg-transparent flex-1 outline-none placeholder:text-white/40" />
                <button className="btn-dark !bg-white !text-[#0c0c0c] !border-white !py-2.5">
                  Subscribe <span className="btn-ico">↗</span>
                </button>
              </form>
              <div className="mt-10 space-y-1 text-white/80">
                <p>hello@visora.com</p>
                <p>+1 (000) 000-0000</p>
              </div>
              <div className="flex gap-3 mt-6">
                {["IG", "YT", "TT", "X"].map((s) => (
                  <a key={s} href="#" className="h-10 w-10 grid place-items-center border border-white/20 text-xs text-[var(--accent)] hover:bg-white/5 transition">{s}</a>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-8 lg:justify-items-end">
              <FooterCol title="Explore" items={["Home", "Work", "About"]} />
              <FooterCol title="Services" items={["Film", "Photography", "Social"]} />
              <FooterCol title="Pages" items={["Journal", "Contact", "Pricing"]} />
            </div>
          </div>
        </div>

        {/* Giant wordmark */}
        <div className="relative select-none">
          <h2 className="display text-center text-[var(--accent)] leading-none font-medium
            text-[clamp(5rem,22vw,20rem)] translate-y-[12%] opacity-95">
            VISORA
          </h2>
        </div>
      </footer>
    </main>
  );
}

function FooterCol({ title, items }: { title: string; items: string[] }) {
  return (
    <div>
      <p className="mono text-xs text-white/50 mb-5">{title}</p>
      <ul className="space-y-3">
        {items.map((i) => (
          <li key={i}><a href="#" className="text-white/85 hover:text-[var(--accent)] transition">{i}</a></li>
        ))}
      </ul>
    </div>
  );
}
