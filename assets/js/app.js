import { parseMarkdownRoute, resolveContentPath } from "./router.js";

function isExternalHref(value) {
  return /^(https?:)?\/\//i.test(value);
}

function normalizeRenderedContent(root, sourcePath) {
  root.querySelectorAll("img[src]").forEach((image) => {
    const source = image.getAttribute("src");
    image.src = resolveContentPath(source, sourcePath);
    image.loading = "lazy";
    image.decoding = "async";
  });

  root.querySelectorAll("a[href]").forEach((anchor) => {
    const href = anchor.getAttribute("href");
    const resolved = resolveContentPath(href, sourcePath);

    if (isExternalHref(resolved)) {
      anchor.target = "_blank";
      anchor.rel = "noopener noreferrer";
      anchor.href = resolved;
    } else if (resolved.toLowerCase().endsWith(".md")) {
      anchor.href = `#${resolved}`;
    } else {
      anchor.href = resolved;
    }
  });
}

async function renderRoute() {
  const content = document.querySelector("#content");
  const route = parseMarkdownRoute(window.location.hash);

  content.setAttribute("aria-busy", "true");
  content.innerHTML = "<p class=\"loading\">正在加载…</p>";

  try {
    const response = await fetch(route.path);
    if (!response.ok) {
      throw new Error(`${response.status} ${response.statusText}`);
    }

    const markdown = await response.text();
    content.innerHTML = window.DOMPurify.sanitize(window.marked.parse(markdown), {
      ADD_ATTR: ["rel", "target", "width"],
    });
    normalizeRenderedContent(content, route.path);

    const heading = content.querySelector("h1");
    document.title = heading
      ? `${heading.textContent.trim()} - Awesome GPT Image 2 Prompts`
      : "Awesome GPT Image 2 Prompts";
  } catch {
    content.innerHTML = [
      "<section class=\"error\">",
      "<h1>内容暂时无法加载</h1>",
      "<p>请确认网络连接后重试。</p>",
      "<button type=\"button\" data-retry>重试</button>",
      "</section>",
    ].join("");
  } finally {
    content.removeAttribute("aria-busy");
  }
}

document.addEventListener("click", (event) => {
  if (event.target.closest("[data-retry]")) {
    renderRoute();
  }
});

document.querySelector("#language")?.addEventListener("change", (event) => {
  window.location.hash = `#${event.target.value}`;
});

window.addEventListener("hashchange", renderRoute);
renderRoute();
