import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { bookParts } from "./book.mjs";

const docsDirectory = fileURLToPath(new URL("../content/docs/", import.meta.url));

const sidebarPartLabels = {
  "part-1": { "zh-hans": "I · 打开黑箱", en: "I · Opening the Black Box" },
  "part-2": { "zh-hans": "II · 必要地基", en: "II · Foundations" },
  "part-3": { "zh-hans": "III · 上下文", en: "III · Context" },
  "part-4": { "zh-hans": "IV · Transformer", en: "IV · The Transformer" },
  "part-5": { "zh-hans": "V · 现代 LLM", en: "V · Modern LLMs" },
  "part-6": { "zh-hans": "VI · 后训练", en: "VI · Post-Training" },
  "part-7": {
    "zh-hans": "VII · 上下文、工具与知识",
    en: "VII · Context, Tools & Knowledge",
  },
  "part-8": {
    "zh-hans": "VIII · Agent 与可靠性",
    en: "VIII · Agents & Reliability",
  },
  "part-9": { "zh-hans": "IX · 生产系统", en: "IX · Production Systems" },
};

function isPublished(locale, id) {
  const source = readFileSync(`${docsDirectory}/${locale}/${id}.md`, "utf8");
  return !/^draft:\s*true\s*$/mu.test(source);
}

export function createSidebar({ includeDrafts = false } = {}) {
  const includeEntry = (id) =>
    includeDrafts || (isPublished("en", id) && isPublished("zh-hans", id));
  const chapterGroups = bookParts
    .map((part) => ({
      label: sidebarPartLabels[part.id]["zh-hans"],
      translations: { en: sidebarPartLabels[part.id].en },
      collapsed: true,
      items: part.chapters
        .filter((chapter) => includeEntry(chapter.id))
        .map((chapter) => ({ slug: chapter.id })),
    }))
    .filter((part) => part.items.length > 0);

  return [
    {
      label: "全书路线图",
      translations: { en: "Book roadmap" },
      slug: "roadmap",
    },
    ...chapterGroups,
    ...(includeEntry("primer-py") || includeEntry("primer-http")
      ? [
          {
            label: "基础补充",
            translations: { en: "Primers" },
            collapsed: true,
            items: ["primer-py", "primer-http"]
              .filter(includeEntry)
              .map((slug) => ({ slug })),
          },
        ]
      : []),
    ...(includeEntry("ext-mm-01")
      ? [
          {
            label: "在线扩展",
            translations: { en: "Extension" },
            collapsed: true,
            items: [{ slug: "ext-mm-01" }],
          },
        ]
      : []),
    {
      label: "参考与维护",
      translations: { en: "Reference" },
      collapsed: true,
      items: [
        { slug: "glossary" },
        { slug: "changelog" },
        { slug: "errata" },
        { slug: "about" },
      ],
    },
    {
      label: "返回 imbrooklyn.dev",
      translations: { en: "Back to imbrooklyn.dev" },
      link: "https://imbrooklyn.dev/",
      attrs: { target: "_self" },
    },
  ];
}
