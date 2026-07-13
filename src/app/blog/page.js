import BlogListClient from "./BlogListClient";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { BreadcrumbSchema, FAQSchema, CollectionPageSchema } from "@/components/Schema";

// ISR: regenerate every hour so new blog posts appear automatically
export const revalidate = 3600;

// Using ISR instead of SSG to keep blog listings fresh
// Cache is revalidated hourly; stale-while-revalidate for responsiveness

export const metadata = {
  title: "SEO Blog — Tips & Guides for Bangladesh | Md Kanok Miah",
  description:
    "Expert SEO tips and guides for Bangladesh businesses. Learn local SEO, technical SEO, e-commerce SEO, and GEO optimization from Md Kanok Miah.",
  alternates: { canonical: "https://kanokmiah.com.bd/blog" },
  openGraph: {
    title: "SEO Blog — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description:
      "Expert SEO tips, guides, and strategies for Bangladesh businesses. Learn local SEO, technical SEO, e-commerce SEO, GEO optimization, and more.",
    url: "https://kanokmiah.com.bd/blog",
    siteName: "Md Kanok Miah",
    images: [
      {
        url: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
        width: 400,
        height: 400,
        alt: "Md Kanok Miah — SEO Expert Dhaka",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "SEO Blog — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description:
      "Expert SEO tips, guides, and strategies for Bangladesh businesses from Md Kanok Miah.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

export default function BlogPage() {
  return (
    <>
      {CollectionPageSchema({
        name: "SEO Blog | Bangladesh Digital Marketing Tips",
        description: "Expert SEO tips, guides, and strategies for Bangladesh businesses. Learn local SEO, technical SEO, e-commerce SEO, GEO optimization, and more.",
        url: "https://kanokmiah.com.bd/blog",
      })}
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Blog", url: "https://kanokmiah.com.bd/blog" },
      ])}
      <Navbar />
      <BlogListClient />
      {/* FAQ */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <FAQSchema
            faqs={[
              {
                question: "How often do you publish new blog posts?",
                answer:
                  "I publish new blog posts regularly, typically 2–4 times per month. Each post is carefully researched and written to provide valuable SEO insights specifically for Bangladeshi businesses and website owners.",
              },
              {
                question: "Can I suggest a blog topic?",
                answer:
                  "Absolutely! I welcome topic suggestions from readers. If there's an SEO topic you'd like me to cover, please contact me through the website and I'll consider it for a future post.",
              },
              {
                question: "Are the blog posts available in Bangla?",
                answer:
                  "Currently, most blog posts are published in English. However, I'm planning to introduce Bangla-language content to better serve Bangladeshi business owners who prefer reading in their native language.",
              },
              {
                question: "Can I share your blog content?",
                answer:
                  "Yes, you're welcome to share my blog posts on social media, with your colleagues, or on your website as long as you provide proper attribution and a link back to the original post.",
              },
            ]}
          />
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              {
                question: "How often do you publish new blog posts?",
                answer:
                  "I publish new blog posts regularly, typically 2–4 times per month. Each post is carefully researched and written to provide valuable SEO insights specifically for Bangladeshi businesses and website owners.",
              },
              {
                question: "Can I suggest a blog topic?",
                answer:
                  "Absolutely! I welcome topic suggestions from readers. If there's an SEO topic you'd like me to cover, please contact me through the website and I'll consider it for a future post.",
              },
              {
                question: "Are the blog posts available in Bangla?",
                answer:
                  "Currently, most blog posts are published in English. However, I'm planning to introduce Bangla-language content to better serve Bangladeshi business owners who prefer reading in their native language.",
              },
              {
                question: "Can I share your blog content?",
                answer:
                  "Yes, you're welcome to share my blog posts on social media, with your colleagues, or on your website as long as you provide proper attribution and a link back to the original post.",
              },
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

      {/* CTA */}
      <section className="relative py-20 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-primary-dark" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-extrabold mb-3 text-white">
            Want to <span className="text-amber-300">Dominate</span> Search?
          </h2>
          <p className="text-white/80 mb-7 text-base">
            Get a free SEO audit for your Bangladesh business.
          </p>
          <a
            href="/contact"
            className="group inline-flex items-center gap-2 bg-white text-primary-dark px-8 py-3.5 rounded-xl font-bold transition-all hover:shadow-xl hover:-translate-y-0.5"
          >
            Get Your Free Audit
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </a>
        </div>
      </section>

      <Footer />
    </>
  );
}
