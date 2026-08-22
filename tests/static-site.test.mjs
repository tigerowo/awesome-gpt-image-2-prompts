import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { test } from "node:test";

const routerModule = fileURLToPath(new URL("../assets/js/router.js", import.meta.url));

test("hash routes are limited to repository Markdown files", async () => {
  assert.ok(existsSync(routerModule), "static site router module is missing");
  const { parseMarkdownRoute } = await import(new URL("../assets/js/router.js", import.meta.url));

  assert.deepEqual(parseMarkdownRoute(""), { path: "README.md" });
  assert.deepEqual(parseMarkdownRoute("#cases/ecommerce.md"), {
    path: "cases/ecommerce.md",
  });
  assert.deepEqual(parseMarkdownRoute("#/README_zh-TW.md"), {
    path: "README_zh-TW.md",
  });
  assert.deepEqual(parseMarkdownRoute("#../secret.md"), { path: "README.md" });
  assert.deepEqual(parseMarkdownRoute("#%2e%2e/secret.md"), { path: "README.md" });
  assert.deepEqual(parseMarkdownRoute("#https://example.com/README.md"), {
    path: "README.md",
  });
});

test("relative assets resolve against the loaded Markdown file", async () => {
  assert.ok(existsSync(routerModule), "static site router module is missing");
  const { resolveContentPath } = await import(new URL("../assets/js/router.js", import.meta.url));

  assert.equal(resolveContentPath("../images/example.jpg", "cases/ui.md"), "images/example.jpg");
  assert.equal(resolveContentPath("portrait.md", "cases/ui.md"), "cases/portrait.md");
  assert.equal(resolveContentPath("#section", "README.md"), "#section");
  assert.equal(resolveContentPath("https://example.com", "README.md"), "https://example.com");
});

test("local development server serves JavaScript modules with a browser-safe MIME type", () => {
  const pkg = JSON.parse(readFileSync(new URL("../package.json", import.meta.url), "utf8"));
  assert.match(
    pkg.scripts.start,
    /mimetypes\.add_type\(["']text\/javascript["'], ["']\.js["']\)/,
  );
});
test("Render deployment has a root-level static entry", () => {
  assert.ok(existsSync(new URL("../index.html", import.meta.url)), "index.html is missing");
  assert.ok(existsSync(new URL("../render.yaml", import.meta.url)), "render.yaml is missing");
});
