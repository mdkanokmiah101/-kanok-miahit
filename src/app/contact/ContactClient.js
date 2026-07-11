"use client";
import { useState } from "react";
import Navbar from "@/components/Navbar";
import Link from "next/link";

const WHATSAPP_NUMBER = "01604809110";
const WHATSAPP_FULL = "+880****9110";
const WHATSAPP_URL = "https://wa.me/8801604809110?text=Hi%20Md%20Kanok%20Miah!%20I%20need%20SEO%20help%20for%20my%20business.";

export default function ContactClient() {
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const form = e.target;
      const data = new FormData(form);
      const res = await fetch("/api/contact", { method: "POST", body: data });
      const result = await res.json();
      if (result.success) {
        setSubmitted(true);
        form.reset();
      }
    } catch (err) {
      console.error("Form error:", err);
    }
    setSubmitting(false);
  };

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
            Ready to work with the <Link href="/" className="text-primary font-semibold hover:underline">best SEO expert in Dhaka</Link>? Reach out via WhatsApp for the fastest response, or fill out the form below.
          </p>
        </div>
      </section>

      {/* WhatsApp Hero Banner */}
      <section className="-mt-8 px-4 mb-8">
        <div className="max-w-5xl mx-auto">
          <a
            href={WHATSAPP_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="block bg-gradient-to-r from-green-600 to-emerald-500 rounded-2xl p-6 md:p-8 text-white text-center hover:shadow-xl hover:shadow-green-500/25 transition-all group"
          >
            <div className="text-4xl mb-3">💬</div>
            <p className="text-sm font-medium text-green-100 uppercase tracking-wider">Fastest Response — Reply Within Minutes</p>
            <p className="text-3xl md:text-4xl font-extrabold mt-2 group-hover:scale-105 transition-transform inline-block">
              {WHATSAPP_NUMBER}
            </p>
            <p className="text-green-100 text-sm mt-2">Tap to chat on WhatsApp →</p>
          </a>
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-12 px-4">
        <div className="max-w-5xl mx-auto grid md:grid-cols-2 gap-10">
          {/* Contact Form */}
          <div className="bg-gray-50 border border-gray-100 rounded-2xl p-8">
            <h2 className="text-xl font-extrabold text-gray-900 mb-2">Send Me a Message</h2>
            <p className="text-gray-400 text-sm mb-6">
              I&apos;ll get back to you within 24 hours. For immediate help, use{" "}
              <a href={WHATSAPP_URL} target="_blank" rel="noopener noreferrer" className="text-emerald-600 font-semibold hover:underline">
                WhatsApp
              </a>.
            </p>

            {!submitted ? (
              <form className="space-y-5" onSubmit={handleSubmit} method="POST">
                <input type="hidden" name="_subject" value="New SEO Lead from Md Kanok Miah Website!" />
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
                    placeholder="01604-809110"
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
                {/* WhatsApp Option Inside Form */}
                <div className="relative my-2">
                  <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-gray-200"></div></div>
                  <div className="relative flex justify-center text-xs"><span className="bg-white px-2 text-gray-400">OR</span></div>
                </div>
                <a href="https://wa.me/8801604809110?text=Hi%20Md%20Kanok%20Miah!%20I%20need%20SEO%20help%20for%20my%20business." target="_blank"
                  className="flex items-center justify-center gap-2 w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-xl transition-all">
                  💬 Chat on WhatsApp <span className="text-green-100">01604809110</span>
                </a>
                <button
                  type="submit" disabled={submitting}
                  className="w-full bg-primary hover:bg-primary-dark disabled:bg-primary/50 text-white font-bold py-3.5 px-6 rounded-xl hover:shadow-lg hover:shadow-primary/20 transition-all"
                >
                  {submitting ? "Sending..." : "Get Free SEO Audit →"}
                </button>
                <p className="text-xs text-gray-400 text-center">I respect your privacy. No spam, ever.</p>
              </form>
            ) : (
              <div className="text-center py-6 space-y-6">
                <div className="bg-green-50 border border-green-200 text-green-700 rounded-xl px-5 py-4 text-sm text-center font-medium">
                  ✅ Thank you! Your message has been logged. I&apos;ll get back to you within 24 hours.
                </div>

                {/* WhatsApp CTA after submission */}
                <div className="bg-gradient-to-r from-green-600 to-emerald-500 rounded-xl p-6 text-white">
                  <p className="text-lg font-bold mb-1">🚀 Need faster help?</p>
                  <p className="text-white/80 text-sm mb-4">
                    Get an instant response on WhatsApp — I typically reply within minutes.
                  </p>
                  <a
                    href={WHATSAPP_URL}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 bg-white text-emerald-700 px-6 py-3 rounded-xl font-bold hover:bg-green-50 transition-all shadow-lg"
                  >
                    💬 Chat Now on {WHATSAPP_NUMBER}
                  </a>
                </div>

                <button
                  onClick={() => setSubmitted(false)}
                  className="text-gray-500 text-sm hover:text-primary transition-colors underline"
                >
                  ← Send another message
                </button>
              </div>
            )}
          </div>

          {/* Contact Info — WhatsApp first, most prominent */}
          <div className="space-y-6">
            {/* WhatsApp — #1 */}
            <div className="bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200 rounded-2xl p-7 hover:shadow-lg hover:shadow-green-500/10 transition-all">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-2xl">💬</span>
                <h3 className="font-bold text-lg text-gray-900">WhatsApp — Fastest Response</h3>
              </div>
              <p className="text-gray-500 text-sm mb-2">Message me directly for an instant reply:</p>
              <p className="text-3xl font-extrabold text-green-700 mb-3">
                {WHATSAPP_NUMBER}
              </p>
              <a
                href={WHATSAPP_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl font-bold transition-all shadow-md hover:shadow-lg w-full justify-center text-sm"
              >
                💬 Chat on WhatsApp Now
              </a>
              <p className="text-xs text-green-600/70 mt-2 text-center">Usually replies within minutes</p>
            </div>

            {/* Phone */}
            <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7 hover:border-primary/20 transition-all">
              <h3 className="font-bold text-lg mb-4 text-gray-900">📞 Call Me Directly</h3>
              <p className="text-gray-500 text-sm mb-3">Speak directly with me about your SEO needs:</p>
              <a href="tel:+880****9110" className="text-2xl font-extrabold text-primary hover:text-primary-dark transition-colors">
                +880 1604-809110
              </a>
            </div>

            {/* Other Ways to Reach */}
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

            {/* Free SEO Audit CTA */}
            <div className="bg-gradient-to-r from-primary to-primary-dark rounded-2xl p-6 text-center text-white">
              <p className="text-lg font-bold mb-1">⭐ Free SEO Audit</p>
              <p className="text-white/80 text-sm">Worth BDT 5,000 — Get a complete analysis of your website. No commitment required.</p>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              { question: "How quickly do you respond?", answer: "I typically respond to all inquiries within 24 hours. For urgent matters, WhatsApp messages are usually answered within a few hours. I value your time and make prompt communication a priority." },
              { question: "Do you offer free SEO audit?", answer: "Yes! I offer a completely free SEO audit worth BDT 5,000. I'll analyze your website's technical health, on-page optimization, current rankings, and provide a roadmap of opportunities — with no obligation to proceed." },
              { question: "What information do you need to start?", answer: "To get started, I need your website URL, a brief overview of your business goals, target keywords if you have them, and access to your Google Search Console and Analytics accounts if available. Everything else I can gather during the audit." },
              { question: "Can you work with my existing website?", answer: "Absolutely. I can optimize any existing website regardless of its current state — from sites with no SEO foundation to those already ranking but needing improvement. I work with all platforms including WordPress, Shopify, Wix, and custom-built sites." },
              { question: "What payment methods do you accept?", answer: "I accept multiple payment methods including bank transfer (within Bangladesh), bKash, Nagad, and international payments via PayPal. Payment terms are discussed and agreed upon before any work begins." },
            ].map((f, i) => (
              <details key={i} className="py-4 group">
                <summary className="font-semibold text-gray-900 cursor-pointer list-none flex justify-between items-center">
                  {f.question}
                  <span className="text-primary transition-transform group-open:rotate-180">▼</span>
                </summary>
                <p className="text-gray-600 mt-3 pl-2">{f.answer}</p>
              </details>
            ))}
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
