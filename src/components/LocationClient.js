"use client";

import { useEffect, useRef } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";

const CITY_NAMES = {
  chittagong: { display: "Chittagong", tagline: "SEO Services in Chittagong" },
  sylhet: { display: "Sylhet", tagline: "SEO Services in Sylhet" },
  khulna: { display: "Khulna", tagline: "SEO Services in Khulna" },
  rajshahi: { display: "Rajshahi", tagline: "SEO Services in Rajshahi" },
  barisal: { display: "Barisal", tagline: "SEO Services in Barisal" },
  rangpur: { display: "Rangpur", tagline: "SEO Services in Rangpur" },
  mymensingh: { display: "Mymensingh", tagline: "SEO Services in Mymensingh" },
  dhaka: { display: "Dhaka", tagline: "SEO Services in Dhaka" },
};

const SERVICES = [
  { icon: "🔍", title: "Local SEO", desc: "Rank on Google Maps & local search results in your city." },
  { icon: "📈", title: "On-Page SEO", desc: "Optimize your website content for higher organic rankings." },
  { icon: "⚙️", title: "Technical SEO", desc: "Fix crawl issues, improve site speed & Core Web Vitals." },
  { icon: "🔗", title: "Link Building", desc: "Build quality backlinks to boost domain authority." },
];

export default function LocationClient({ city }) {
  const info = CITY_NAMES[city] || { display: "Your City", tagline: "SEO Services" };
  const { display, tagline } = info;

  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-white">
        {/* Hero Section */}
        <section className="bg-gradient-to-br from-purple-900 via-purple-800 to-red-800 text-white py-20 px-4">
          <div className="max-w-6xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-extrabold mb-6">
              Best SEO Services in <span className="text-yellow-300">{display}</span>
            </h1>
            <p className="text-xl max-w-3xl mx-auto mb-8">
              Rank #1 on Google & AI Search in {display} with proven SEO strategies. 
              210+ successful projects delivered across Bangladesh.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link href="/contact" className="bg-yellow-400 text-gray-900 px-8 py-3 rounded-full font-bold hover:bg-yellow-300 transition">
                Get a Free SEO Audit
              </Link>
              <Link href="/seo-services" className="border-2 border-white px-8 py-3 rounded-full font-bold hover:bg-white hover:text-purple-900 transition">
                View SEO Services
              </Link>
            </div>
          </div>
        </section>

        {/* SEO Services Grid */}
        <section className="py-16 px-4 max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Our SEO Services in {display}</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {SERVICES.map((svc, i) => (
              <div key={i} className="bg-gray-50 rounded-xl p-6 border border-gray-100 hover:shadow-lg transition">
                <div className="text-3xl mb-4">{svc.icon}</div>
                <h3 className="text-xl font-bold mb-2">{svc.title}</h3>
                <p className="text-gray-600">{svc.desc}</p>
                <Link href={`/services/${svc.title.toLowerCase().replace(/\s+/g, '-')}`} className="text-purple-700 font-semibold mt-3 inline-block hover:underline">
                  Learn More →
                </Link>
              </div>
            ))}
          </div>
        </section>

        {/* Trust & Results Section */}
        <section className="bg-gray-50 py-16 px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">Why Businesses in {display} Trust Kanok Miah</h2>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center p-6">
                <div className="text-4xl mb-4">📍</div>
                <h3 className="text-xl font-bold mb-2">Google Maps Ranking</h3>
                <p className="text-gray-600">Proven strategies to get your business to the top of Google Maps in {display}.</p>
              </div>
              <div className="text-center p-6">
                <div className="text-4xl mb-4">📋</div>
                <h3 className="text-xl font-bold mb-2">GBP Optimization</h3>
                <p className="text-gray-600">Expert Google Business Profile optimization for maximum local visibility in {display}.</p>
              </div>
              <div className="text-center p-6">
                <div className="text-4xl mb-4">🚀</div>
                <h3 className="text-xl font-bold mb-2">210+ Projects</h3>
                <p className="text-gray-600">Successfully delivered 210+ SEO projects for businesses across Bangladesh including {display}.</p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="bg-gradient-to-r from-purple-800 to-red-700 text-white py-16 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl font-bold mb-6">Ready to Rank Higher in {display}?</h2>
            <p className="text-xl mb-8">Get a free SEO analysis for your business in {display} and discover how we can help you dominate local search results.</p>
            <Link href="/contact" className="bg-yellow-400 text-gray-900 px-10 py-4 rounded-full font-bold text-lg hover:bg-yellow-300 transition inline-block">
              Contact Us Today
            </Link>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
