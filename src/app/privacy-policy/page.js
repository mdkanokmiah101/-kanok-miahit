import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Privacy Policy — Md Kanok Miah — SEO Expert Dhaka",
  description: "Privacy Policy for Md Kanok Miah — SEO Expert in Dhaka, Bangladesh. Learn how we collect, use, and protect your information.",
  alternates: { canonical: "https://kanokmiah.com.bd/privacy-policy" },
  openGraph: {
    title: "Privacy Policy — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Privacy Policy for Md Kanok Miah — SEO Expert in Dhaka, Bangladesh.",
    url: "https://kanokmiah.com.bd/privacy-policy",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Privacy Policy — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Privacy Policy for Md Kanok Miah — SEO Expert in Dhaka, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

export default function PrivacyPolicyPage() {
  const lastUpdated = "January 1, 2026";

  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Privacy Policy", url: "https://kanokmiah.com.bd/privacy-policy" },
      ])}
      <div className="min-h-screen bg-white text-gray-900">
      <Navbar />
      <main className="pt-32 pb-20 px-4 max-w-4xl mx-auto">
        <h1 className="text-4xl font-extrabold mb-2">Privacy Policy</h1>
        <p className="text-gray-500 text-sm mb-10">Last updated: {lastUpdated}</p>

        <div className="prose prose-gray max-w-none space-y-6">
          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">1. Introduction</h2>
            <p className="text-gray-600 leading-relaxed">
              Md Kanok Miah (&ldquo;we,&rdquo; &ldquo;us,&rdquo; or &ldquo;our&rdquo;) operates kanokmiah.com.bd. This Privacy Policy explains how we collect,
              use, disclose, and safeguard your information when you visit our website.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">2. Information We Collect</h2>
            <p className="text-gray-600 leading-relaxed">We may collect the following types of information:</p>
            <ul className="list-disc pl-6 mt-2 text-gray-600 space-y-2">
              <li><strong>Personal Data:</strong> Name, email address, phone number, and website URL when you fill out our contact form.</li>
              <li><strong>Usage Data:</strong> Pages visited, time spent, browser type, and other analytics data.</li>
              <li><strong>Cookies:</strong> We use cookies to improve your browsing experience and analyze site traffic.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">3. How We Use Your Information</h2>
            <p className="text-gray-600 leading-relaxed">We use the information we collect to:</p>
            <ul className="list-disc pl-6 mt-2 text-gray-600 space-y-2">
              <li>Respond to your inquiries and provide SEO consultation</li>
              <li>Improve our website and services</li>
              <li>Send relevant marketing communications (with your consent)</li>
              <li>Comply with legal obligations</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">4. Data Protection</h2>
            <p className="text-gray-600 leading-relaxed">
              We implement appropriate technical and organizational measures to protect your personal data against unauthorized access,
              alteration, disclosure, or destruction. However, no internet transmission is completely secure.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">5. Third-Party Services</h2>
            <p className="text-gray-600 leading-relaxed">
              We may use third-party services such as Google Analytics, Google Search Console, and email services that collect,
              monitor, and analyze data to help us improve our services. These third parties have their own privacy policies.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">6. Your Rights</h2>
            <p className="text-gray-600 leading-relaxed">You have the right to:</p>
            <ul className="list-disc pl-6 mt-2 text-gray-600 space-y-2">
              <li>Access your personal data held by us</li>
              <li>Request correction or deletion of your data</li>
              <li>Withdraw consent at any time</li>
              <li>Lodge a complaint with a data protection authority</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">7. Contact Us</h2>
            <p className="text-gray-600 leading-relaxed">
              If you have questions about this Privacy Policy, please contact us at:
            </p>
            <div className="mt-2 text-gray-600">
              <p>Email: mdkanokmiah232@gmail.com</p>
              <p>Phone: +880 1712-883101</p>
              <p>Location: Dhaka, Bangladesh</p>
            </div>
          </section>
        </div>
      </main>
      <Footer />
    </div>
    </>
  );
}
