import Link from "next/link";

const services = [
  { name: "Local SEO", slug: "local-seo" },
  { name: "On-Page SEO", slug: "on-page-seo" },
  { name: "Technical SEO", slug: "technical-seo" },
  { name: "Link Building", slug: "link-building" },
  { name: "Semantic SEO", slug: "semantic-seo" },
  { name: "GEO / AI Search", slug: "geo-ai-search" },
  { name: "E-commerce SEO", slug: "ecommerce-seo" },
];

const industries = [
  { name: "Garments & Textile", path: "/industries/garments-textile" },
  { name: "E-commerce", path: "/industries/ecommerce" },
  { name: "SMM Panel", path: "/industries/smm-panel" },
  { name: "Real Estate", path: "/industries/real-estate" },
  { name: "Cleaning Services", path: "/industries/cleaning" },
  { name: "Spa & Salon", path: "/industries/spa-salon" },
  { name: "Medical & Healthcare", path: "/industries/medical" },
  { name: "Education", path: "/industries/education" },
  { name: "Food & Restaurant", path: "/industries/food-restaurant" },
];

export default function Footer() {
  return (
    <footer className="relative bg-gray-900 text-gray-300 pt-16 pb-0 px-4 overflow-hidden">
      {/* Top decorative gradient line */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-primary via-primary-dark to-primary" />

      <div className="relative max-w-7xl mx-auto">
        {/* Main Footer Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-10 mb-12">

          {/* Column 1 - Brand */}
          <div className="lg:col-span-1">
            <Link href="/" className="text-2xl font-extrabold tracking-tight text-white">
              Md <span className="text-primary">Kanok Miah</span>
            </Link>
            <p className="text-gray-400 text-sm mt-4 leading-relaxed">
              Bangladesh&apos;s trusted SEO expert with 6+ years of experience. Helping local businesses rank higher,
              grow faster, and dominate search results with proven SEO strategies.
            </p>
            {/* Trust Badge */}
            <div className="flex items-center gap-2 mt-5 bg-gray-800/50 rounded-xl px-4 py-3 inline-flex">
              <span className="text-yellow-400 text-lg">⭐</span>
              <span className="text-white text-sm font-semibold">4.9/5</span>
              <span className="text-gray-400 text-xs">(50+ reviews)</span>
            </div>
          </div>

          {/* Column 2 - Quick Links */}
          <div>
            <h4 className="text-white font-bold text-sm uppercase tracking-wider mb-5">Quick Links</h4>
            <ul className="space-y-3 text-sm">
              {[
                { name: "Home", path: "/" },
                { name: "Services", path: "/services" },
                { name: "Industries", path: "/industries" },
                { name: "Blog", path: "/blog" },
                { name: "FAQ", path: "/faq" },
                { name: "Portfolio", path: "/portfolio" },
                { name: "Case Studies", path: "/case-studies" },
                { name: "Locations", path: "/locations/dhaka" },
                { name: "About", path: "/about" },
                { name: "Contact", path: "/contact" },
              ].map((link, i) => (
                <li key={i}>
                  <Link href={link.path} className="text-gray-400 hover:text-primary transition-colors flex items-center gap-2">
                    <span className="text-primary text-xs">▸</span> {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 3 - Services */}
          <div>
            <h4 className="text-white font-bold text-sm uppercase tracking-wider mb-5">SEO Services</h4>
            <ul className="space-y-3 text-sm">
              {services.map((service, i) => (
                <li key={i}>
                  <Link href={`/services/${service.slug}`} className="text-gray-400 hover:text-primary transition-colors flex items-center gap-2">
                    <span className="text-primary text-xs">▸</span> {service.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 4 - Industries */}
          <div>
            <h4 className="text-white font-bold text-sm uppercase tracking-wider mb-5">Industries We Serve</h4>
            <ul className="space-y-3 text-sm">
              {industries.map((ind, i) => (
                <li key={i}>
                  <Link href={ind.path} className="text-gray-400 hover:text-primary transition-colors flex items-center gap-2">
                    <span className="text-primary text-xs">▸</span> {ind.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 5 - Contact */}
          <div>
            <h4 className="text-white font-bold text-sm uppercase tracking-wider mb-5">Contact</h4>
            <ul className="space-y-4 text-sm">
              <li className="flex items-start gap-3">
                <span className="text-primary mt-0.5">📞</span>
                <div>
                  <div className="text-gray-400 text-xs">Phone</div>
                  <a href="tel:+880****9110" className="text-white hover:text-primary transition-colors font-medium">+880 1604-809110</a>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-primary mt-0.5">📧</span>
                <div>
                  <div className="text-gray-400 text-xs">Email</div>
                  <a href="mailto:mdkanokmiah232@gmail.com" className="text-white hover:text-primary transition-colors font-medium">mdkanokmiah232@gmail.com</a>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-primary mt-0.5">📍</span>
                <div>
                  <div className="text-gray-400 text-xs">Location</div>
                  <span className="text-white font-medium">Dhaka, Bangladesh</span>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-primary mt-0.5">💬</span>
                <div>
                  <div className="text-gray-400 text-xs">WhatsApp</div>
                  <a href="https://wa.me/8801604809110" target="_blank" rel="noopener noreferrer" className="text-white hover:text-primary transition-colors font-medium">Chat Now</a>
                </div>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 pt-8 pb-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-gray-500 text-center md:text-left">
            © 2026 <span className="text-primary font-semibold">Md Kanok Miah</span>. All rights reserved.
          </p>
          <div className="flex items-center gap-4 text-sm">
            <span className="text-gray-400 text-xs font-medium">🔥 350+ projects completed</span>
            <span className="text-gray-700">|</span>
            <Link href="/privacy-policy" className="text-gray-500 hover:text-primary transition-colors">Privacy Policy</Link>
            <span className="text-gray-700">|</span>
            <Link href="/terms-of-service" className="text-gray-500 hover:text-primary transition-colors">Terms of Service</Link>
            <span className="text-gray-700">|</span>
            <Link href="/sitemap.xml" className="text-gray-500 hover:text-primary transition-colors">Sitemap</Link>
          </div>
        </div>
      </div>

      {/* Bottom flag line */}
      <div className="bg-gray-950 py-3 text-center">
        <p className="text-xs text-gray-600">🇧🇩 Serving Dhaka, Chittagong, Sylhet & all of Bangladesh</p>
      </div>
    </footer>
  );
}
