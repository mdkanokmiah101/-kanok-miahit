"use client";
import { useEffect } from "react";
import Navbar from "@/components/Navbar";
import Link from "next/link";

export default function ContactPage() {
  useEffect(() => {
    document.title = "Contact Me — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh";
  }, []);

  return (
    <div className="min-h-screen bg-white text-gray-900">
      {/* Navbar */}
      <Navbar />

      {/* Hero */}
      <section className="relative pt-32 pb-16 px-4 text-center overflow-hidden bg-gradient-to-b from-gray-50 to-white">
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-primary/[0.08] rounded-full blur-3xl" />
        <div className="relative max-w-4xl mx-auto">
          <span className="text-primary text-sm font-semibold tracking-widest uppercase">Get In Touch</span>
          <h1 className="text-4xl md:text-6xl font-extrabold mt-4 mb-6">
            Let&apos;s Grow Your{" "}
            <span className="text-primary">Online Presence</span>
          </h1>
          <p className="text-gray-500 text-lg max-w-2xl mx-auto leading-relaxed">
            Ready to rank higher, attract more customers, and grow your business? 
            Fill out the form or reach out directly — I&apos;ll get back to you within 24 hours.
          </p>
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-12 px-4">
        <div className="max-w-5xl mx-auto grid md:grid-cols-2 gap-10">
          {/* Contact Form */}
          <div className="bg-gray-50 border border-gray-100 rounded-2xl p-8">
            <h2 className="text-xl font-extrabold text-gray-900 mb-6">Send Me a Message</h2>
            <form className="space-y-5" action="https://formsubmit.co/mdkanokmiah101@gmail.com" method="POST">
              <input type="hidden" name="_subject" value="New SEO Lead from Md Kanok Miah Website!" />
              <input type="hidden" name="_captcha" value="false" />
              <input type="hidden" name="_template" value="table" />
              <input type="text" name="_honey" style={{display: "none"}} />
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Your Name *</label>
                <input
                  type="text" name="name" required
                  placeholder="e.g. Md. Rahim"
                  className="w-full bg-white border border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Email Address *</label>
                <input
                  type="email" name="email" required
                  placeholder="your@email.com"
                  className="w-full bg-white border border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Phone Number</label>
                <input
                  type="tel" name="phone"
                  placeholder="01712-883101"
                  className="w-full bg-white border border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Your Website</label>
                <input
                  type="url" name="website"
                  placeholder="https://yourwebsite.com"
                  className="w-full bg-white border border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Tell Me About Your Project *</label>
                <textarea
                  name="message" required rows="5"
                  placeholder="I need SEO for my e-commerce store in Dhaka..."
                  className="w-full bg-white border border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all resize-none"
                ></textarea>
              </div>
              <button
                type="submit"
                className="w-full bg-primary hover:bg-primary-dark text-white font-bold py-3.5 px-6 rounded-xl hover:shadow-lg hover:shadow-primary/20 transition-all"
              >
                Get Free SEO Audit →
              </button>
              <p className="text-xs text-gray-400 text-center">I respect your privacy. No spam, ever.</p>
            </form>
          </div>

          {/* Contact Info */}
          <div className="space-y-6">
            <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7 hover:border-primary/20 transition-all">
              <h3 className="font-bold text-lg mb-4 text-gray-900">📞 Call Me Directly</h3>
              <p className="text-gray-500 text-sm mb-3">Speak directly with me about your SEO needs:</p>
              <a href="tel:+8801712883101" className="text-2xl font-extrabold text-primary hover:text-primary-dark transition-colors">
                +880 1712-883101
              </a>
            </div>

            <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7 hover:border-primary/20 transition-all">
              <h3 className="font-bold text-lg mb-4 text-gray-900">💬 WhatsApp</h3>
              <p className="text-gray-500 text-sm mb-3">Quick response on WhatsApp:</p>
              <a
                href="https://wa.me/8801712883101?text=Hi%20Md%20Kanok%20Miah!%20I%20need%20SEO%20help%20for%20my%20business."
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-700 px-5 py-3 rounded-xl font-semibold hover:bg-emerald-100 transition-all text-sm"
              >
                💬 Chat on WhatsApp → <span className="text-xs text-gray-400">(Fastest Response)</span>
              </a>
            </div>

            <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7 hover:border-primary/20 transition-all">
              <h3 className="font-bold text-lg mb-4 text-gray-900">📍 Other Ways to Reach</h3>
              <div className="space-y-3 text-sm">
                <div className="flex items-center gap-3">
                  <span className="text-xl">📧</span>
                  <a href="mailto:mdkanokmiah232@gmail.com" className="text-gray-600 hover:text-primary transition-colors">
                    mdkanokmiah232@gmail.com
                  </a>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-xl">🌐</span>
                  <a href="https://kanokmiah.com" target="_blank" rel="noopener noreferrer" className="text-gray-600 hover:text-primary transition-colors">
                    kanokmiah.com
                  </a>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-xl">📍</span>
                  <span className="text-gray-600">Dhaka, Bangladesh</span>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-r from-primary to-primary-dark rounded-2xl p-6 text-center text-white">
              <p className="text-lg font-bold mb-1">⭐ Free SEO Audit</p>
              <p className="text-white/80 text-sm">Worth BDT 5,000 — Get a complete analysis of your website. No commitment required.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-gray-100 text-center text-sm text-gray-500">
        <div className="max-w-4xl mx-auto px-4">
          <div className="flex flex-wrap justify-center gap-6 mb-4">
            <Link href="/" className="hover:text-primary transition-colors">Home</Link>
            <Link href="/services" className="hover:text-primary transition-colors">Services</Link>
            <Link href="/industries" className="hover:text-primary transition-colors">Industries</Link>
            <Link href="/blog" className="hover:text-primary transition-colors">Blog</Link>
            <Link href="/about" className="hover:text-primary transition-colors">About</Link>
            <Link href="/contact" className="hover:text-primary transition-colors">Contact</Link>
          </div>
          <p>© 2026 <span className="text-primary font-bold">Md Kanok Miah</span> — SEO Expert in Bangladesh. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
