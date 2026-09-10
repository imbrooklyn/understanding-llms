// SPDX-License-Identifier: Apache-2.0
import { readFileSync } from "node:fs";
import { workedIllustration } from "./book-illustrations.mjs";

const escape = (value) => String(value).replace(/[&<>"']/g, (c) => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
})[c]);

export function renderFigure(id, locale) {
  if (!/^ch-\d{2}\/[a-z-]+$/.test(id)) throw new Error(`Invalid figure: ${id}`);
  const figure = JSON.parse(readFileSync(new URL(`../assets/${id}.json`, import.meta.url), "utf8"));
  const local = (value) => escape(value[locale]);
  const kinds = { token: ['Text pieces', '文本片段'], id: ['Row number', '行编号'], vector: ['A list of numbers', '一组数字'], parameter: ['Stored model numbers', '模型保存的数值'], state: ['Application record', '应用保存的记录'], external: ['Outside the model', '模型之外'], computation: ['An operation', '处理步骤'] };
  return `<figure class="book-figure" id="figure-${escape(id.replace("/", "-"))}"><div role="img" aria-label="${local(figure.alt)}">${workedIllustration(figure.structure, locale, figure) ?? figure.lanes.map((lane) =>
    `<div class="figure-lane"><strong>${local(lane.label)}</strong><ol>${lane.nodes.map((node) =>
      `<li class="kind-${escape(node.kind)}"><span class="node-kind">${escape(kinds[node.kind]?.[locale === 'en' ? 0 : 1] ?? node.kind)}</span><span>${local(node.text)}</span></li>`
    ).join("")}</ol><p class="figure-flow">${local(lane.flow)}</p></div>`
  ).join("")}</div><figcaption>${local(figure.caption)} <small>${local(figure.credit)}</small></figcaption></figure>`;
}

// Number the source AST, so the body and Starlight TOC share numbers and anchors.
export default function remarkBook() {
  return (tree, file) => {
    const match = String(file.path).replaceAll("\\", "/").match(/\/(en|zh-hans)\/ch-(\d{2})\.md$/);
    if (!match) return;
    const [, locale, chapter] = match;
    const counters = [Number(chapter), 0, 0, 0, 0, 0];
    for (const node of tree.children) {
      if (node.type === "heading") {
        if (node.depth < 2) throw new Error(`${file.path}: body headings must start at ##`);
        const level = node.depth - 1;
        if (level > 1 && counters[level - 1] === 0) throw new Error(`${file.path}: skipped heading level`);
        counters[level]++;
        counters.fill(0, level + 1);
        const number = counters.slice(0, level + 1).join(".");
        node.children.unshift({ type: "text", value: `${number} ` });
        node.data = { ...node.data, hProperties: { ...node.data?.hProperties, id: `s-${number.replaceAll(".", "-")}` } };
      }
      if (node.type === "code" && node.lang === "book-figure") {
        node.type = "html";
        node.value = renderFigure(node.value.trim(), locale);
      }
      if (node.type === "code" && node.lang === "book-lab") {
        throw new Error(`${file.path}: book-lab is unsupported; present complete static examples and results`);
      }
    }
  };
}
