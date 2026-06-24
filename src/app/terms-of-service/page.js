"use client";
import { useEffect } from "react";
import Link from "next/link";

export default function TermsOfServicePage() {
  useEffect(() => {
    document.title = "Terms of Service — Kanok MiahIT";
  }, []);

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white">

      {/* === NAVBAR === */}
      <nav className="fixed top-0 w-full bg-[#0a0a0f]/90 backdrop-blur-xl border-b border-white/5 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-xl font-extrabold tracking-tight">
            <span className="bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent">Kanok Miah</span>
            <span className="text-amber-400">IT</span>
          </Link>
          <Link href="/" className="text-sm text-gray-400 hover:text-cyan-400 transition-colors">← Back to Home</Link>
        </div>
      </nav>

      {/* === HEADER === */}
      <section className="relative pt-32 pb-12 px-4 text-center overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl" />
        <div className="relative max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-white/5 border border-white/10 text-cyan-300 text-xs font-semibold px-5 py-2 rounded-full mb-8 backdrop-blur-sm">
            Legal
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mb-4">
            <span className="bg-gradient-to-r from-cyan-300 to-emerald-300 bg-clip-text text-transparent">
              Terms of Service
            </span>
          </h1>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Last updated: June 24, 2026
          </p>
        </div>
      </section>

      {/* === CONTENT === */}
      <section className="pb-24 px-4">
        <div className="max-w-3xl mx-auto space-y-6">

          <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-white mb-3">1. Acceptance of Terms</h2>
            <p className="text-gray-400 leading-relaxed">
              By accessing or using the Kanok MiahIT website and services, you agree to be bound by 
              these Terms of Service. If you do not agree with any part of these terms, you must not 
              use our website or services.
            </p>
            <p className="text-gray-400 leading-relaxed mt-3">
              These terms apply to all visitors, users, and clients of Kanok MiahIT, a Bangladesh-based 
              SEO agency operating from Dhaka, Bangladesh.
            </p>
          </div>

          <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-white mb-3">2. Services Description</h2>
            <p className="text-gray-400 leading-relaxed">
              Kanok MiahIT provides search engine optimisation (SEO) services including but not limited to:
            </p>
            <ul className="list-disc pl-5 mt-2 space-y-1 text-gray-400 text-sm">
              <li>Local SEO and Google Business Profile optimisation</li>
              <li>On-page SEO (keyword research, content optimisation, meta tags)</li>
              <li>Technical SEO (site speed, Core Web Vitals, crawl optimisation, schema markup)</li>
              <li>Link building and digital PR</li>
              <li>E-commerce SEO</li>
              <li>GEO / AI search optimisation</li>
              <li>SEO consulting and strategy</li>
              <li>Monthly SEO reporting and analytics</li>
            </ul>
            <p className="text-gray-400 leading-relaxed mt-3">
              The specific scope of services will be detailed in your individual service agreement or 
              proposal. Services are provided on a month-to-month or project basis as agreed.
            </p>
          </div>

          <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-white mb-3">3. Client Responsibilities</h2>
            <p className="text-gray-400 leading-relaxed">
              As a client, you agree to:
            </p>
            <ul className="list-disc pl-5 mt-2 space-y-1 text-gray-400 text-sm">
              <li>Provide accurate and complete information about your business</li>
              <li>Grant us necessary access to your website, analytics, and SEO tools</li>
              <li>Respond to communications and requests in a timely manner</li>
              <li>Not engage in any black-hat SEO practices or request unethical tactics</li>
              <li>Ensure you have the legal authority to engage our services for your website</li>
            </ul>
          </div>

          <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-white mb-3">4. Payment Terms</h2>
            <p className="text-gray-400 leading-relaxed">
              Payment terms are as follows:
            </p>
            <ul className="list-disc pl-5 mt-2 space-y-1 text-gray-400 text-sm">
              <li>Fees are outlined in your service agreement or proposal</li>
              <li>Monthly retainers are billed at the beginning of each month</li>
              <li>Project-based fees are invoiced according to the agreed payment schedule</li>
              <li>Payments are due within 15 days of invoice date unless otherwise agreed</li>
              <li>Late payments may incur additional charges or service suspension</li>
              <li>All fees are quoted in BDT or USD as specified in the agreement</li>
            </ul>
          </div>

          <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-white mb-3">5. Intellectual Property</h2>
            <p className="text-gray-400 leading-relaxed">
              All SEO strategies, methodologies, reports, and deliverables produced by Kanok MiahIT 
              remain our intellectual property until full payment is received. Upon full payment, 
              the client receives a license to use the deliverables for their business purposes.
            </p>
            <p className="text-gray-400 leading-relaxed mt-3">
              The client retains all rights to their original website content, brand assets, and 
              business information provided to us.
            </p>
          </div>

          <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-white mb-3">6. Confidentiality</h2>
            <p className="text-gray-400 leading-relaxed">
              Both parties agree to maintain the confidentiality of all proprietary information 
              disclosed during the course of the engagement. This includes business strategies, 
              financial data, customer information, and proprietary methodologies.
            </p>
            <p className="text-gray-400 leading-relaxed mt-3">
              This confidentiality obligation survives the termination of our agreement.
            </p>
          </div>

          <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-white mb-3">7. Limitation of Liability</h2>
            <p className="text-gray-400 leading-relaxed">
              Kanok MiahIT provides SEO services with reasonable skill and care. However, we cannot 
              guarantee specific search engine rankings, traffic levels, or revenue increases, as 
              these are influenced by factors beyond our control including search engine algorithm 
              changes and competitor activity.
            </p>
            <p className="text-gray-400 leading-relaxed mt-3">
              To the fullest extent permitted by law, Kanok MiahIT shall not be liable for any 
              indirect, incidental, special, consequential, or punitive damages arising from your 
              use of our services. Our total liability is limited to the amount paid by you for 
              the specific service giving rise to the claim.
            </p>
          </div>

          <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-white mb-3">8. Term and Termination</h2>
            <p className="text-gray-400 leading-relaxed">
              The initial term of service is specified in your service agreement. Either party may 
              terminate the agreement:
            </p>
            <ul className="list-disc pl-5 mt-2 space-y-1 text-gray-400 text-sm">
              <li>With 30 days written notice for monthly retainers</li>
              <li>Immediately for material breach that remains uncured for 14 days</li>
              <li>By mutual written agreement</li>
            </ul>
            <p className="text-gray-400 leading-relaxed mt-3">
              Upon termination, the client will be invoiced for all services rendered up to the 
              termination date.
            </p>
          </div>

          <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-white mb-3">9. Disclaimer of Warranties</h2>
            <p className="text-gray-400 leading-relaxed">
              Our services are provided &ldquo;as is&rdquo; without any warranty, express or implied. While we 
              strive to deliver high-quality SEO services that follow best practices and search 
              engine guidelines, we do not guarantee specific outcomes.
            </p>
          </div>

          <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-white mb-3">10. Governing Law</h2>
            <p className="text-gray-400 leading-relaxed">
              These Terms of Service shall be governed by and construed in accordance with the laws 
              of Bangladesh. Any disputes arising from these terms shall be resolved in the courts 
              of Dhaka, Bangladesh.
            </p>
          </div>

          <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-white mb-3">11. Changes to Terms</h2>
            <p className="text-gray-400 leading-relaxed">
              We reserve the right to modify these Terms of Service at any time. Changes will be 
              effective immediately upon posting to our website. Your continued use of our services 
              after changes constitutes acceptance of the updated terms.
            </p>
          </div>

          <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-white mb-3">12. Contact Information</h2>
            <p className="text-gray-400 leading-relaxed">
              For questions, concerns, or notices regarding these Terms of Service, please contact us:
            </p>
            <div className="mt-4 space-y-2 text-gray-300 text-sm">
              <p><strong className="text-white">Email:</strong> mdkanokmiah232@gmail.com</p>
              <p><strong className="text-white">Phone:</strong> +880 1313-019160</p>
              <p><strong className="text-white">Address:</strong> Dhaka, Bangladesh</p>
              <p><strong className="text-white">Website:</strong> kanokmiah.com</p>
            </div>
          </div>

        </div>
      </section>

      {/* === FOOTER === */}
      <footer className="py-8 border-t border-white/5 text-center text-sm text-gray-600">
        <p>© 2026 <span className="bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent font-bold">Kanok MiahIT</span> — SEO Agency in Bangladesh. All rights reserved.</p>
        <div className="mt-3 flex items-center justify-center gap-4 text-xs">
          <Link href="/about" className="hover:text-cyan-400 transition-colors">About</Link>
          <Link href="/privacy-policy" className="hover:text-cyan-400 transition-colors">Privacy Policy</Link>
          <Link href="/terms-of-service" className="hover:text-cyan-400 transition-colors">Terms of Service</Link>
        </div>
      </footer>

    </div>
  );
}
