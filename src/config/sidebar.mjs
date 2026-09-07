import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { bookParts } from "./book.mjs";

const docsDirectory = fileURLToPath(new URL("../content/docs/", import.meta.url));

function isPublished(locale, id) {
  const source = readFileSync(`${docsDirectory}/${locale}/${id}.md`, "utf8");
  return !/^draft:\s*true\s*$/mu.test(source);
}

export function createSidebar({ includeDrafts = false } = {}) {
  const includeEntry = (id) =>
    includeDrafts || (isPublished("en", id) && isPublished("zh-hans", id));
  const chapterGroups = bookParts
    .map((part) => ({
      label: part.label["zh-hans"],
      translations: { en: part.label.en },
      collapsed: part.id !== "part-1",
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
            label: "基础补充资源",
            translations: { en: "Foundation primers" },
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
            label: "在线选修",
            translations: { en: "Online extension" },
            collapsed: true,
            items: [{ slug: "ext-mm-01" }],
          },
        ]
      : []),
    {
      label: "参考与维护",
      translations: { en: "Reference and maintenance" },
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
