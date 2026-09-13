import { readFileSync } from "node:fs";
import { assertPublicationState } from "./publication-state.mjs";
import { fileURLToPath } from "node:url";
import { BOOK_LOCALES, chapterLabel, plannedChapters } from "../src/config/book.mjs";

const repositoryRoot = fileURLToPath(new URL("../", import.meta.url));
const docsRoot = `${repositoryRoot}src/content/docs`;
const supportingLessons = ["primer-py", "primer-http", "ext-mm-01"];
const requiredPublishedPages = [
  "index",
  "roadmap",
  "glossary",
  "changelog",
  "errata",
  "about",
];
const errors = [];

function readPage(locale, id) {
  const pathname = `${docsRoot}/${locale}/${id}.md`;
  let source;

  try {
    source = readFileSync(pathname, "utf8");
  } catch {
    errors.push(`Missing ${locale}/${id}.md`);
    return null;
  }

  const match = source.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/u);
  if (!match) {
    errors.push(`${locale}/${id}.md must contain YAML frontmatter.`);
    return null;
  }

  const [, frontmatter, body] = match;
  const title = frontmatter.match(/^title:\s*(.+)$/mu)?.[1]?.trim();
  const description = frontmatter
    .match(/^description:\s*(.+)$/mu)?.[1]
    ?.trim();
  const draft = /^draft:\s*true\s*$/mu.test(frontmatter);
  const published = frontmatter.match(/^published:\s*(\d{4}-\d{2}-\d{2})\s*$/mu)?.[1];
  if (plannedChapters.some((entry) => entry.id === id) || supportingLessons.includes(id)) {
    try { assertPublicationState(frontmatter, `${locale}/${id}.md`); }
    catch (error) { errors.push(error.message); }
  }

  if (!title) errors.push(`${locale}/${id}.md is missing title.`);
  const chapter = plannedChapters.find((entry) => entry.id === id);
  if (chapter && title !== JSON.stringify(`${chapterLabel(id, locale)} ${chapter.title[locale]}`)) {
    errors.push(`${locale}/${id}.md must use the localized chapter label and configured title.`);
  }
  if (/\bCH-\d{2}\b/u.test(body)) {
    errors.push(`${locale}/${id}.md must use reader-facing chapter names in prose.`);
  }
  if (!description) errors.push(`${locale}/${id}.md is missing description.`);
  if (/^#\s+/mu.test(body)) {
    errors.push(`${locale}/${id}.md must start body headings at level 2.`);
  }

  return { body, draft, published };
}

for (const id of [...plannedChapters.map((chapter) => chapter.id), ...supportingLessons]) {
  const pages = Object.fromEntries(
    BOOK_LOCALES.map((locale) => [locale, readPage(locale, id)]),
  );

  if (pages.en && pages["zh-hans"] && pages.en.draft !== pages["zh-hans"].draft) {
    errors.push(`${id} must have the same draft status in both languages.`);
  }

  if (pages.en && pages["zh-hans"] && pages.en.published !== pages["zh-hans"].published) {
    errors.push(`${id} must have the same publication date in both languages.`);
  }

  for (const [locale, page] of Object.entries(pages)) {
    if (!page || page.draft) continue;
    if (!page.published) {
      errors.push(`${locale}/${id}.md requires published: YYYY-MM-DD.`);
    }
    if (/visible only in local development|仅在本地开发模式可见/u.test(page.body)) {
      errors.push(`${locale}/${id}.md still contains the draft placeholder.`);
    }
    if (page.body.trim().length < 300) {
      errors.push(`${locale}/${id}.md is too short to publish.`);
    }
  }
}

for (const id of requiredPublishedPages) {
  for (const locale of BOOK_LOCALES) {
    const page = readPage(locale, id);
    if (page?.draft) errors.push(`${locale}/${id}.md must not be a draft.`);
  }
}

if (errors.length > 0) {
  console.error("Book content validation failed:\n");
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(
  `Validated ${plannedChapters.length} bilingual chapter pairs and supporting pages.`,
);
