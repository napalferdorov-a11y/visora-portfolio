"use client";
import { AnimatePresence, motion } from "framer-motion";
import { useState } from "react";

const QUOTES = [
  {
    text: "VISORA turned our product line into something that finally looks like a premium brand. The films carried our whole launch — and the leads followed.",
    name: "Sample Client",
    role: "Founder, Studio Brand",
    img: "/img/t1.jpg",
  },
  {
    text: "Every frame felt intentional. The attention to detail — colour, pacing, mood — matched our vision perfectly and raised how customers see us.",
    name: "Sample Client",
    role: "Owner, E-commerce Shop",
    img: "/img/t2.jpg",
  },
  {
    text: "One shoot day gave us a month of content. Our engagement has never been higher and it barely took any of my time.",
    name: "Sample Client",
    role: "Director, Café Group",
    img: "/img/t3.jpg",
  },
];

export default function Testimonials() {
  const [i, setI] = useState(0);
  const q = QUOTES[i];
  return (
    <div className="flex flex-col items-center text-center max-w-3xl mx-auto">
      <div className="h-16 w-16 rounded-full overflow-hidden mb-8 ring-2 ring-[var(--accent)]">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={q.img} alt="" className="h-full w-full object-cover" />
      </div>
      <AnimatePresence mode="wait">
        <motion.blockquote
          key={i}
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -14 }}
          transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
          className="text-xl md:text-2xl leading-snug text-[#1a1a1a]"
        >
          “{q.text}”
          <footer className="mt-6 text-base text-[var(--muted)]">
            <span className="font-medium text-[#0c0c0c]">{q.name}</span> — {q.role}
          </footer>
        </motion.blockquote>
      </AnimatePresence>
      <div className="flex gap-2.5 mt-9">
        {QUOTES.map((_, n) => (
          <button
            key={n}
            aria-label={`Go to testimonial ${n + 1}`}
            onClick={() => setI(n)}
            className={`h-2.5 rounded-full transition-all ${
              n === i ? "w-7 bg-[var(--accent)]" : "w-2.5 bg-[#d4d4d4]"
            }`}
          />
        ))}
      </div>
    </div>
  );
}
