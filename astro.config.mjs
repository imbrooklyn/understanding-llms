// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import { BOOK_BASE, BOOK_REPOSITORY, BOOK_SITE } from "./src/config/book.mjs";
import { createSidebar } from "./src/config/sidebar.mjs";

const includeDrafts = process.env.NODE_ENV !== "production";

export default defineConfig({
  site: BOOK_SITE,
  base: BOOK_BASE,
  output: "static",
  trailingSlash: "always",
  integrations: [
    starlight({
      title: {
        en: "Understanding Large Language Models from the Ground Up",
        "zh-CN": "理解大语言模型",
      },
      description:
        "A bilingual, from-the-ground-up guide to modern large language models and reliable LLM systems.",
      defaultLocale: "en",
      locales: {
        en: {
          label: "English",
          lang: "en",
        },
        "zh-hans": {
          label: "简体中文",
          lang: "zh-CN",
        },
      },
      customCss: ["./src/styles/custom.css"],
      favicon: "/favicon.svg",
      editLink: {
        baseUrl: `${BOOK_REPOSITORY}/edit/main/`,
      },
      lastUpdated: true,
      disable404Route: true,
      social: [
        {
          icon: "github",
          label: "GitHub",
          href: BOOK_REPOSITORY,
        },
      ],
      sidebar: createSidebar({ includeDrafts }),
      head: [
        {
          tag: "meta",
          attrs: {
            name: "theme-color",
            content: "#15171a",
          },
        },
        {
          tag: "link",
          attrs: {
            rel: "alternate",
            type: "application/rss+xml",
            title:
              "Understanding Large Language Models from the Ground Up — English",
            href: `${BOOK_BASE}/en/rss.xml`,
          },
        },
        {
          tag: "link",
          attrs: {
            rel: "alternate",
            type: "application/rss+xml",
            title: "理解大语言模型 — 中文",
            href: `${BOOK_BASE}/zh-hans/rss.xml`,
          },
        },
      ],
    }),
  ],
});
