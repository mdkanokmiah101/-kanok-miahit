// Comprehensive Schema Generator for all page types

export function OrganizationSchema() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "Md Kanok Miah",
    url: "https://kanokmiah.com.bd",
    logo: "https://kanokmiah.com.bd/favicon.ico",
    description:
      "Bangladesh-focused SEO expert. Local SEO, technical SEO, link building, semantic SEO, and GEO optimization.",
    address: {
      "@type": "PostalAddress",
      addressLocality: "Dhaka",
      addressCountry: "BD",
    },
    contactPoint: {
      "@type": "ContactPoint",
      telephone: "+880-1712-883101",
      contactType: "customer service",
      availableLanguage: ["English", "Bengali"],
    },
    sameAs: [
      "https://kanokmiah.com",
      "https://www.facebook.com/mdkanokmiahweb",
      "https://bd.linkedin.com/in/kanok-miah",
      "https://www.youtube.com/@kanokmiah",
      "https://www.pinterest.com/mdkanokmiah",
      "https://www.instagram.com/kanokmiahbd",
      "https://www.tiktok.com/@kanokmiahbd",
      "https://wa.me/8801712883101",
    ],
    foundingDate: "2020",
    founder: {
      "@type": "Person",
      name: "Md Kanok Miah",
    },
    knowsAbout: [
      "Search Engine Optimization",
      "Local SEO",
      "Technical SEO",
      "Link Building",
      "Semantic SEO",
      "GEO / AI Search Optimization",
      "E-commerce SEO",
      "Content Marketing",
      "Google Business Profile Optimization",
      "Generative Engine Optimization",
    ],
  };
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

export function LocalBusinessSchema() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    name: "Md Kanok Miah — SEO Expert",
    url: "https://kanokmiah.com.bd",
    telephone: "+880-1712-883101",
    email: "mdkanokmiah232@gmail.com",
    description:
      "Best SEO expert in Dhaka, Bangladesh. Specializing in Local SEO, Technical SEO, Link Building, and GEO optimization.",
    image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
    address: {
      "@type": "PostalAddress",
      addressLocality: "Dhaka",
      addressCountry: "BD",
    },
    geo: {
      "@type": "GeoCoordinates",
      latitude: "23.8103",
      longitude: "90.4125",
    },
    priceRange: "$$",
    areaServed: ["Dhaka", "Mirpur", "Gulshan", "Banani", "Uttara", "Dhanmondi", "Chittagong", "Sylhet", "Bangladesh"],
    hasOfferCatalog: {
      "@type": "OfferCatalog",
      name: "SEO Services",
      itemListElement: [
        { "@type": "Offer", itemOffered: { "@type": "Service", name: "Local SEO" } },
        { "@type": "Offer", itemOffered: { "@type": "Service", name: "On-Page SEO" } },
        { "@type": "Offer", itemOffered: { "@type": "Service", name: "Technical SEO" } },
        { "@type": "Offer", itemOffered: { "@type": "Service", name: "Link Building" } },
        { "@type": "Offer", itemOffered: { "@type": "Service", name: "Semantic SEO" } },
        { "@type": "Offer", itemOffered: { "@type": "Service", name: "GEO / AI Search" } },
        { "@type": "Offer", itemOffered: { "@type": "Service", name: "E-commerce SEO" } },
      ],
    },
    aggregateRating: {
      "@type": "AggregateRating",
      ratingValue: "4.9",
      bestRating: "5",
      ratingCount: "50",
    },
  };
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

export function WebSiteSchema() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "Md Kanok Miah",
    url: "https://kanokmiah.com.bd",
    description:
      "Best SEO expert in Dhaka, Bangladesh. Get higher rankings, more traffic, and qualified leads with proven SEO strategies.",
    inLanguage: ["en", "bn"],
    potentialAction: {
      "@type": "SearchAction",
      target: {
        "@type": "EntryPoint",
        urlTemplate: "https://kanokmiah.com.bd/blog?q={search_term_string}",
      },
      "query-input": "required name=search_term_string",
    },
  };
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

export function BreadcrumbSchema(items) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  };
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

export function PersonSchema() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Person",
    name: "Md Kanok Miah",
    alternateName: "Kanok Miah",
    givenName: "Kanok",
    familyName: "Miah",
    url: "https://kanokmiah.com.bd",
    sameAs: [
      "https://kanokmiah.com",
      "https://www.facebook.com/mdkanokmiahweb",
      "https://bd.linkedin.com/in/kanok-miah",
      "https://www.youtube.com/@kanokmiah",
      "https://www.pinterest.com/mdkanokmiah",
      "https://www.instagram.com/kanokmiahbd",
      "https://www.tiktok.com/@kanokmiahbd",
    ],
    jobTitle: "SEO Expert & Digital Marketing Specialist",
    worksFor: {
      "@type": "Organization",
      name: "Md Kanok Miah",
    },
    knowsAbout: [
      "Search Engine Optimization",
      "Local SEO",
      "Technical SEO",
      "Link Building",
      "GEO / AI Search Optimization",
    ],
    description:
      "Best SEO expert in Dhaka, Bangladesh with 6+ years of experience. Specializing in local SEO, technical SEO, link building, and GEO optimization.",
  };
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

export function ServiceSchema(service) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Service",
    name: service.title,
    description: service.desc,
    provider: {
      "@type": "Person",
      name: "Md Kanok Miah",
    },
    areaServed: ["Dhaka", "Chittagong", "Sylhet", "Bangladesh"],
    serviceType: service.title,
    offers: {
      "@type": "Offer",
      priceSpecification: {
        "@type": "PriceSpecification",
        priceCurrency: "BDT",
        description: "Custom pricing based on project scope",
      },
    },
  };
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

export function FAQSchema({ faqs }) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: faqs.map((faq) => ({
      "@type": "Question",
      name: faq.question,
      acceptedAnswer: {
        "@type": "Answer",
        text: faq.answer,
      },
    })),
  };
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

export function ArticleSchema(post) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: post.title,
    description: post.excerpt || post.desc,
    author: {
      "@type": "Person",
      name: "Md Kanok Miah",
      url: "https://kanokmiah.com.bd/about",
    },
    publisher: {
      "@type": "Organization",
      name: "Md Kanok Miah",
      logo: {
        "@type": "ImageObject",
        url: "https://kanokmiah.com.bd/favicon.ico",
      },
    },
    datePublished: post.date || new Date().toISOString(),
    dateModified: new Date().toISOString(),
    mainEntityOfPage: {
      "@type": "WebPage",
      "@id": `https://kanokmiah.com.bd/blog/${post.slug}`,
    },
    image: post.image || "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  };
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}