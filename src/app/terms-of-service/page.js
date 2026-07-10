import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Terms of Service — Md Kanok Miah — SEO Expert Dhaka",
  description: "Terms of Service for Md Kanok Miah — SEO Expert in Dhaka, Bangladesh. Please read these terms carefully before using our services.",
  alternates: { canonical: "https://kanokmiah.com.bd/terms-of-service" },
  openGraph: {
    title: "Terms of Service — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Terms of Service for Md Kanok Miah — SEO Expert in Dhaka, Bangladesh.",
    url: "https://kanokmiah.com.bd/terms-of-service",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Terms of Service — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Terms of Service for Md Kanok Miah — SEO Expert in Dhaka, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

export default function TermsOfServicePage() {
  const lastUpdated = "January 1, 2026";

  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Terms of Service", url: "https://kanokmiah.com.bd/terms-of-service" },
      ])}
      <div className="min-h-screen bg-white text-gray-900">
      <Navbar />
      <main className="pt-32 pb-20 px-4 max-w-4xl mx-auto">
        <h1 className="text-4xl font-extrabold mb-2">Terms of Service</h1>
        <p className="text-gray-500 text-sm mb-10">Last updated: {lastUpdated}</p>

        <div className="prose prose-gray max-w-none space-y-6">
          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">1. Acceptance of Terms</h2>
            <p className="text-gray-600 leading-relaxed">
              By accessing or using kanokmiah.com.bd (&ldquo;the Website&rdquo;), you agree to be bound by these Terms of Service.
              If you do not agree with any part of these terms, you must not use our services.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">2. Services</h2>
            <p className="text-gray-600 leading-relaxed">
              Md Kanok Miah provides SEO consulting and digital marketing services including but not limited to:
              Local SEO, On-Page SEO, Technical SEO, Link Building, Semantic SEO, GEO/AI Search Optimization,
              and E-commerce SEO. All services are provided on a best-effort basis with the goal of improving
              search engine rankings and online visibility.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">3. Payment Terms</h2>
            <p className="text-gray-600 leading-relaxed">
              Payment terms are agreed upon before the commencement of any project. Payments are due as per the
              agreed schedule. Late payments may result in service suspension. All fees are non-refundable unless
              otherwise stated in the service agreement.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">4. No Guarantee of Specific Results</h2>
            <p className="text-gray-600 leading-relaxed">
              While we strive to improve your search engine rankings and online presence, we cannot guarantee
              specific rankings, traffic numbers, or revenue. Search engine algorithms change frequently, and
              results depend on many factors beyond our control, including competitor activities and search
              engine policy updates.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">5. Client Responsibilities</h2>
            <p className="text-gray-600 leading-relaxed">As a client, you agree to:</p>
            <ul className="list-disc pl-6 mt-2 text-gray-600 space-y-2">
              <li>Provide accurate information and timely access to your website and analytics</li>
              <li>Not engage in any activity that violates search engine guidelines</li>
              <li>Maintain website ownership and hosting throughout the engagement</li>
              <li>Communicate promptly regarding approvals and feedback</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">6. Intellectual Property</h2>
            <p className="text-gray-600 leading-relaxed">
              All content, strategies, and materials created during the engagement remain the intellectual property
              of Md Kanok Miah until full payment is received. Upon payment, clients receive full rights to the
              deliverables created specifically for them.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">7. Limitation of Liability</h2>
            <p className="text-gray-600 leading-relaxed">
              Md Kanok Miah shall not be liable for any indirect, incidental, special, consequential, or punitive
              damages resulting from your use of our services. Our total liability is limited to the amount paid
              by you for the services in question.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">8. Termination</h2>
            <p className="text-gray-600 leading-relaxed">
              Either party may terminate the service agreement with 30 days written notice. Upon termination,
              you are responsible for payment for all services rendered up to the termination date.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">9. Changes to Terms</h2>
            <p className="text-gray-600 leading-relaxed">
              We reserve the right to modify these terms at any time. Changes will be posted on this page,
              and continued use of our services after changes constitutes acceptance of the new terms.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mt-8 mb-3">10. Contact</h2>
            <p className="text-gray-600 leading-relaxed">
              For questions about these Terms of Service, contact us:
            </p>
            <div className="mt-2 text-gray-600">
              <p>Email: mdkanokmiah232@gmail.com</p>
              <p>Phone: +880 1712-883101</p>
              <p>Website: https://kanokmiah.com.bd</p>
            </div>
          </section>
        </div>
      </main>
      <Footer />
    </div>
    </>
  );
}
