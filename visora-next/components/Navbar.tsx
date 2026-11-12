"use client";
import { useEffect, useState } from "react";

const LINKS = ["Home", "Work", "Services", "About", "Journal"];

function NavLink({ label }: { label: string }) {
  return (
    <a href="#" className="navlink text-[15px]">
      <span className="a">{label}</span>
      <span className="b" aria-hidden>{label}</span>
    </a>
  );
}

export default function Navbar() {
  const [stuck, setStuck] = useState(false);
  const [open, setOpen] = useState(false);
  useEffect(() => {
    const on = () => setStuck(window.scrollY > 20);
    on();
    window.addEventListener("scroll", on, { passive: true });
    return () => window.removeEventListener("scroll", on);
  }, []);

  // dark text over the light hero at the top; light text once stuck over dark bg
  const light = stuck;           // true => white text on dark bar
  const txt = light ? "text-white" : "text-[#0c0c0c]";
  const bar = light ? "bg-white" : "bg-[#0c0c0c]";

  return (
    <header
      className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${
        stuck ? "bg-[#0c0c0c]/90 backdrop-blur-md py-3" : "py-5"
      }`}
    >
      <div className={`wrap flex items-center justify-between ${txt}`}>
        <a href="#" className="flex items-center gap-2 text-[22px] font-medium tracking-tight">
          VISORA<span className="inline-block w-2 h-2 rounded-full" style={{ background: "var(--accent)" }} />
        </a>

        <nav className="hidden md:flex items-center gap-9">
          {LINKS.map((l) => <NavLink key={l} label={l} />)}
        </nav>

        <div className="hidden md:flex items-center gap-4">
          <span className={`mono text-[13px] ${light ? "text-white/70" : "text-black/50"}`}>EN</span>
          <a href="#contact"
            className={`btn-dark ${light ? "!bg-white !text-[#0c0c0c] !border-white" : "!bg-[#0c0c0c] !text-white !border-[#0c0c0c]"}`}>
            Contact Us <span className="btn-ico">↗</span>
          </a>
        </div>

        <button
          className="md:hidden flex flex-col gap-[5px] p-2"
          aria-label="Menu"
          aria-expanded={open}
          onClick={() => setOpen((v) => !v)}
        >
          <span className={`w-6 h-[2px] ${bar} transition-transform ${open ? "translate-y-[7px] rotate-45" : ""}`} />
          <span className={`w-6 h-[2px] ${bar} transition-opacity ${open ? "opacity-0" : ""}`} />
          <span className={`w-6 h-[2px] ${bar} transition-transform ${open ? "-translate-y-[7px] -rotate-45" : ""}`} />
        </button>
      </div>

      {/* mobile drawer */}
      <div
        className={`md:hidden overflow-hidden transition-[max-height] duration-400 bg-[#0c0c0c] ${
          open ? "max-h-96" : "max-h-0"
        }`}
      >
        <div className="wrap flex flex-col gap-4 py-6 text-white">
          {LINKS.map((l) => (
            <a key={l} href="#" className="text-lg" onClick={() => setOpen(false)}>{l}</a>
          ))}
          <a href="#contact" className="btn-dark !bg-white !text-[#0c0c0c] !border-white w-fit mt-2" onClick={() => setOpen(false)}>
            Contact Us <span className="btn-ico">↗</span>
          </a>
        </div>
      </div>
    </header>
  );
}
