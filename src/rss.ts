import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import { BOOK_BASE, BOOK_SITE } from "./config/book.mjs";

interface FeedCopy {
  description: string;
  locale: "en" | "zh-hans";
  title: string;
}

export async function createBookFeed(copy: FeedCopy) {
  const prefix = `${copy.locale}/`;
  const chapters = (
    await getCollection(
      "docs",
      ({ data, id }) =>
        id.startsWith(prefix) &&
        /^ch-\d{2}$/u.test(id.slice(prefix.length)) &&
        !data.draft &&
        Boolean(data.published),
    )
  ).sort(
    (left, right) =>
      (right.data.published?.getTime() ?? 0) -
      (left.data.published?.getTime() ?? 0),
  );

  return rss({
    title: copy.title,
    description: copy.description,
    site: new URL(`${BOOK_BASE}/${copy.locale}/`, BOOK_SITE),
    items: chapters.map((chapter) => ({
      title: chapter.data.title,
      description: chapter.data.description,
      pubDate: chapter.data.published,
      link: `${chapter.id.slice(prefix.length)}/`,
    })),
    customData: `<language>${copy.locale === "en" ? "en" : "zh-CN"}</language>`,
  });
}
