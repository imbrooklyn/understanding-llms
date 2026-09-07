import type { APIRoute } from "astro";
import { createBookFeed } from "../../rss";

export const GET: APIRoute = () =>
  createBookFeed({
    locale: "en",
    title: "Understanding Large Language Models",
    description: "New chapters from the English Web Edition.",
  });
