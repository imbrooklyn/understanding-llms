# Web Book 实施方案

## 目标状态

作者只维护书籍正文、示例、图示与配套实践资产。框架、路由、双语映射、导航、搜索、质量检查、主站入口和发布流程均由仓库基础设施承担。

## 仓库与职责

- `imbrooklyn/understanding-llms` 是本书唯一内容源，保持公开，不单独部署。
- `imbrooklyn/imbrooklyn.github.io` 是站点外壳和唯一 GitHub Pages 发布者。
- 主站手动部署时检出书籍仓库，运行 Starlight 构建，并将产物合并到统一 Pages Artifact。
- 不使用 PAT、`repository_dispatch` 或跨仓库 Secret。

## 永久路由

```text
/books/understanding-llms/
/books/understanding-llms/zh-hans/
/books/understanding-llms/zh-hans/ch-01/
/books/understanding-llms/en/
/books/understanding-llms/en/ch-01/
```

书籍根路径固定导向英文版，英文版是技术事实基准。所有章节、词汇表、勘误和变更记录均保留语言前缀。未来其他书籍使用自己的 `/books/<book-slug>/` 命名空间和独立仓库。

## 内容生命周期

1. 所有计划章节预建双语文件与最终 Frontmatter，并默认标记为草稿。
2. 作者只替换正文并完成双语版本，然后移除两个文件的草稿标记，并填写相同的 `published: YYYY-MM-DD` 发布日期。
3. 内容校验确保章节命名、双语配对和发布状态一致。
4. Book 仓库 CI 验证内容与独立构建。
5. 作者手动运行主站 Pages 工作流；主站重新获取公开仓库并统一发布。

## 构建与整合

- Starlight 使用 `site: https://imbrooklyn.dev` 和 `base: /books/understanding-llms`。
- Book 产物输出到自身 `dist/`。
- 主站先构建到自己的 `dist/`，再把 Book 产物复制到 `dist/books/understanding-llms/`。
- 最终只上传一次 Pages Artifact，避免两个项目争用同一自定义域名。
- Book 自带语言切换、Pagefind 搜索、Canonical、Sitemap 和编辑链接。

## 视觉与体验

Starlight 通过 Custom CSS 复用主站的 IBM Plex Mono、蓝色强调色、浅深色变量、边框、圆角与焦点样式。Book 保留更适合长文阅读的正文宽度、左侧章节导航和右侧页内目录，同时提供返回主站与书籍 GitHub 仓库的入口。

## 完成标准

- 两种语言的固定路径可构建且可相互切换。
- 草稿不进入生产产物和搜索索引。
- 主站首页、顶部导航和 `/books/` 索引均可进入本书。
- 独立 Book 构建和主站组合构建均通过。
- GitHub Pages 手动部署成功，线上路径、静态资源、搜索和响应式布局可用。
