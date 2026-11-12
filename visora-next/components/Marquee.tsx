const BRANDS = ["AURORA", "NORTHSIDE", "VERTEX", "BLOOM", "KODE", "MAISON"];

export default function Marquee() {
  const row = [...BRANDS, ...BRANDS];
  return (
    <div className="bg-[var(--accent)] text-white py-5 overflow-hidden">
      <div className="marquee">
        {row.map((b, i) => (
          <div key={i} className="flex items-center shrink-0">
            <span className="text-2xl md:text-3xl font-medium tracking-tight px-8">{b}</span>
            <span className="opacity-60 text-xl">✦</span>
          </div>
        ))}
      </div>
    </div>
  );
}
