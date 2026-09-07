# Contributing

## Chapter contract

Every chapter should contain:

1. A concrete question and its link to the surrounding chapters.
2. A self-contained explanation of the mechanism.
3. A minimal numerical example, diagram, or observable experiment.
4. At least one failure case and a clear applicability boundary.
5. A core-understanding self-check and answers.
6. Sources and further reading.
7. A practical exercise when the topic calls for one.

Start headings inside chapter Markdown at `##`; the page title comes from frontmatter. Keep English and Chinese chapter filenames identical. Both versions must preserve technical meaning, equations, conclusions, risks, and dependencies.

## Publishing a chapter

Draft files are visible during `pnpm dev` but excluded from production. A chapter is publishable only when both language files:

- have real content in place of the placeholder;
- no longer contain `draft: true`;
- contain the same `published: YYYY-MM-DD` release date;
- use the same chapter identifier;
- pass `pnpm ci:build`.

The main website owns production deployment. After pushing book content, manually run its Pages workflow.

## Assets

Put reusable source assets in `src/assets/<chapter-id>/`. Add meaningful alt text to every image and never rely on color alone. Keep source and license information adjacent to third-party assets.

Put notebooks, code, small datasets, and expected outputs in the matching top-level directories. Never commit credentials, restricted data, or unlicensed artifacts.
