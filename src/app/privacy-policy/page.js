"use client";
import { useEffect } from "react";
import Link from "next/link";

export default function PrivacyPolicyPage() {
  useEffect(() => {
    document.title = "Privacy Policy — Md Kanok Miah";
  }, []);

  return (
    <div className="min-h-screen bg-white text-gray-900">

      {/* === NAVBAR === */}
      <nav className="fixed top-0 w-full bg-white/95 backdrop-blur-xl border-b border-gray-100 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-xl font-extrabold tracking-tight">
            <span className="text-primary">Md Kanok Miah</span>
          </Link>
          <Link href="/" className="text-sm text-gray-600 hover:text-primary transition-colors">← Back to Home</Link>
        </div>
      </nav>

      {/* === HEADER === */}
      <section className="relative pt-32 pb-12 px-4 text-center overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-primary/10 rounded-full blur-3xl" />
        <div className="relative max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-primary-light border border-primary/20 text-primary text-xs font-semibold px-5 py-2 rounded-full mb-8 backdrop-blur-sm">
            Legal
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mb-4">
            <span className="text-primary">
              Privacy Policy
            </span>
          </h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Last updated: June 24, 2026
          </p>
        </div>
      </section>

      {/* === CONTENT === */}
      <section className="pb-24 px-4">
        <div className="max-w-3xl mx-auto space-y-6">

          <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-gray-900 mb-3">1. Introduction</h2>
            <p className="text-gray-600 leading-relaxed">
              Md Kanok Miah (&ldquo;we,&rdquo; &ldquo;our,&rdquo; or &ldquo;us&rdquo;) respects your privacy and is committed to protecting 
              your personal data. This Privacy Policy explains how we collect, use, disclose, and safeguard 
              your information when you visit our website or use our SEO services.
            </p>
            <p className="text-gray-600 leading-relaxed mt-3">
              We are a Bangladesh-based SEO agency. By using our website and services, you agree to the 
              collection and use of information in accordance with this policy.
            </p>
          </div>

          <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-gray-900 mb-3">2. Information We Collect</h2>
            <h3 className="font-semibold text-gray-800 mt-4 mb-2">Personal Data</h3>
            <p className="text-gray-600 leading-relaxed">
              We may collect personally identifiable information such as your name, email address, phone 
              number, company name, and billing information when you:
            </p>
            <ul className="list-disc pl-5 mt-2 space-y-1 text-gray-600 text-sm">
              <li>Fill out a contact or inquiry form</li>
              <li>Request a free SEO audit</li>
              <li>Subscribe to our newsletter</li>
              <li>Engage our SEO services</li>
              <li>Communicate with us via email or phone</li>
            </ul>

            <h3 className="font-semibold text-gray-800 mt-6 mb-2">Usage Data</h3>
            <p className="text-gray-600 leading-relaxed">
              We automatically collect certain information when you visit our website, including your IP 
              address, browser type, operating system, referring URLs, pages viewed, and the dates/times 
              of your visits. This data helps us analyse trends and improve our website.
            </p>

            <h3 className="font-semibold text-gray-800 mt-6 mb-2">Cookies &amp; Tracking Technologies</h3>
            <p className="text-gray-600 leading-relaxed">
              We use cookies and similar tracking technologies to enhance your browsing experience, analyse 
              website traffic, and understand where our visitors come from. You can control cookie preferences 
              through your browser settings.
            </p>
          </div>

          <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-gray-900 mb-3">3. How We Use Your Information</h2>
            <p className="text-gray-600 leading-relaxed">
              We use the information we collect for the following purposes:
            </p>
            <ul className="list-disc pl-5 mt-2 space-y-1 text-gray-600 text-sm">
              <li>To provide and maintain our SEO services</li>
              <li>To respond to your inquiries and support requests</li>
              <li>To send marketing communications (with your consent)</li>
              <li>To improve our website and service offerings</li>
              <li>To process payments and manage billing</li>
              <li>To comply with legal obligations</li>
            </ul>
          </div>

          <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-gray-900 mb-3">4. Third-Party Services</h2>
            <p className="text-gray-600 leading-relaxed">
              We may share your data with trusted third-party service providers who assist us in operating 
              our website and delivering our services, including:
            </p>
            <ul className="list-disc pl-5 mt-2 space-y-1 text-gray-600 text-sm">
              <li>Web analytics providers (e.g., Google Analytics)</li>
              <li>Email marketing platforms</li>
              <li>Payment processors</li>
              <li>Hosting and infrastructure providers</li>
            </ul>
            <p className="text-gray-600 leading-relaxed mt-3">
              These third parties are contractually obligated to protect your data and use it only for the 
              purposes we specify. We do not sell your personal information to third parties.
            </p>
          </div>

          <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-gray-900 mb-3">5. Data Security</h2>
            <p className="text-gray-600 leading-relaxed">
              We implement appropriate technical and organisational measures to protect your personal data 
              against unauthorised access, alteration, disclosure, or destruction. This includes SSL 
              encryption, secure data storage, and restricted access controls.
            </p>
            <p className="text-gray-600 leading-relaxed mt-3">
              However, no method of transmission over the Internet is 100% secure. While we strive to 
              protect your data, we cannot guarantee absolute security.
            </p>
          </div>

          <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-gray-900 mb-3">6. Your Rights (GDPR Compliance)</h2>
            <p className="text-gray-600 leading-relaxed">
              If you are located in the European Economic Area (EEA), you have the following rights under 
              the General Data Protection Regulation (GDPR):
            </p>
            <ul className="list-disc pl-5 mt-2 space-y-1 text-gray-600 text-sm">
              <li><strong className="text-gray-900">Right to Access:</strong> Request copies of your personal data.</li>
              <li><strong className="text-gray-900">Right to Rectification:</strong> Request correction of inaccurate data.</li>
              <li><strong className="text-gray-900">Right to Erasure:</strong> Request deletion of your data where applicable.</li>
              <li><strong className="text-gray-900">Right to Restrict Processing:</strong> Request limitation of data processing.</li>
              <li><strong className="text-gray-900">Right to Data Portability:</strong> Request transfer of your data to another service.</li>
              <li><strong className="text-gray-900">Right to Object:</strong> Object to processing for direct marketing purposes.</li>
            </ul>
            <p className="text-gray-600 leading-relaxed mt-3">
              To exercise any of these rights, please contact us using the details below. We will respond 
              to your request within 30 days.
            </p>
          </div>

          <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-gray-900 mb-3">7. Cookies Policy</h2>
            <p className="text-gray-600 leading-relaxed">
              Our website uses cookies to improve functionality and analyse traffic. Cookies are small text 
              files stored on your device. We use:
            </p>
            <ul className="list-disc pl-5 mt-2 space-y-1 text-gray-600 text-sm">
              <li><strong className="text-gray-900">Essential Cookies:</strong> Required for basic website functionality.</li>
              <li><strong className="text-gray-900">Analytics Cookies:</strong> Help us understand how visitors interact with our site.</li>
              <li><strong className="text-gray-900">Preference Cookies:</strong> Remember your settings and preferences.</li>
            </ul>
            <p className="text-gray-600 leading-relaxed mt-3">
              You can manage or disable cookies through your browser settings. Note that disabling cookies 
              may affect certain website features.
            </p>
          </div>

          <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-gray-900 mb-3">8. Data Retention</h2>
            <p className="text-gray-600 leading-relaxed">
              We retain your personal data only as long as necessary to fulfil the purposes outlined in 
              this policy, or as required by law. When data is no longer needed, we securely delete or 
              anonymise it.
            </p>
          </div>

          <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-gray-900 mb-3">9. Changes to This Policy</h2>
            <p className="text-gray-600 leading-relaxed">
              We may update this Privacy Policy from time to time. Changes will be posted on this page 
              with an updated &ldquo;Last updated&rdquo; date. We encourage you to review this policy periodically.
            </p>
          </div>

          <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7">
            <h2 className="text-xl font-extrabold text-gray-900 mb-3">10. Contact Us</h2>
            <p className="text-gray-600 leading-relaxed">
              If you have any questions, concerns, or requests regarding this Privacy Policy or your 
              personal data, please contact us:
            </p>
            <div className="mt-4 space-y-2 text-gray-600 text-sm">
              <p><strong className="text-gray-900">Email:</strong> mdkanokmiah232@gmail.com</p>
              <p><strong className="text-gray-900">Phone:</strong> +880 1313-019160</p>
              <p><strong className="text-gray-900">Address:</strong> Dhaka, Bangladesh</p>
              <p><strong className="text-gray-900">Website:</strong> kanokmiah.com</p>
            </div>
          </div>

        </div>
      </section>

      {/* === FOOTER === */}
      <footer className="py-8 border-t border-gray-100 text-center text-sm text-gray-500">
        <p>© 2026 <span className="text-primary font-bold">Md Kanok Miah</span> — SEO Agency in Bangladesh. All rights reserved.</p>
        <div className="mt-3 flex items-center justify-center gap-4 text-xs">
          <Link href="/about" className="hover:text-primary transition-colors">About</Link>
          <Link href="/privacy-policy" className="hover:text-primary transition-colors">Privacy Policy</Link>
          <Link href="/terms-of-service" className="hover:text-primary transition-colors">Terms of Service</Link>
        </div>
      </footer>

    </div>
  );
}
