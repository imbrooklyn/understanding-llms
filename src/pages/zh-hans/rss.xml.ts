import type { APIRoute } from "astro";
import { createBookFeed } from "../../rss";

export const GET: APIRoute = () =>
  createBookFeed({
    locale: "zh-hans",
    title: "理解大语言模型",
    description: "《理解大语言模型》中文 Web Edition 新章节。",
  });
