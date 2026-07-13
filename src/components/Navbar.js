"use client";
import { useState } from "react";
import Link from "next/link";

const navItem = [
  { name: "Services", path: "/services" },
  { name: "Case Studies", path: "/case-studies" },
  { name: "Industries", path: "/industries" },
  { name: "Blog", path: "/blog" },
  { name: "About", path: "/about" },
  { name: "Contact", path: "/contact" },
];

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="fixed top-0 w-full bg-white/90 backdrop-blur-xl border-b border-gray-100 z-50">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="text-xl font-extrabold tracking-tight">
          <span className="text-primary">Md Kanok Miah</span>
        </Link>
        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-600">
          {navItem.map(item => (
            <Link key={item.name} href={item.path} className="hover:text-primary transition-colors">{item.name}</Link>
          ))}
          <Link href="/contact" className="bg-primary text-white text-sm font-bold px-5 py-2.5 rounded-full hover:bg-primary-dark hover:shadow-lg hover:shadow-primary/25 transition-all">
            Free Audit
          </Link>
        </div>
        <button onClick={() => setMenuOpen(!menuOpen)} className="md:hidden text-2xl text-gray-700" aria-label="Toggle menu">
          {menuOpen ? "✕" : "☰"}
        </button>
      </div>
      {menuOpen && (
        <div className="md:hidden bg-white border-b border-gray-100 px-4 pb-5 flex flex-col gap-3 text-sm font-medium text-gray-600">
          {navItem.map(item => (
            <Link key={item.name} href={item.path} onClick={() => setMenuOpen(false)} className="hover:text-primary transition-colors">
              {item.name}
            </Link>
          ))}
          <Link href="/contact" onClick={() => setMenuOpen(false)} className="bg-primary text-white text-center font-bold px-5 py-2.5 rounded-full">
            Free Audit
          </Link>
        </div>
      )}
    </nav>
  );
}
