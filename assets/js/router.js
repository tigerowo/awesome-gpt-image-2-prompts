const REPOSITORY_ORIGIN = "https://prompt-library.invalid";
const DEFAULT_ROUTE = { path: "README.md" };

export function parseMarkdownRoute(hash) {
  const rawValue = String(hash || "").replace(/^#\/?/, "");

  if (!rawValue) {
    return { ...DEFAULT_ROUTE };
  }

  let value = rawValue;
  try {
    value = decodeURIComponent(rawValue);
  } catch {
    return { ...DEFAULT_ROUTE };
  }

  if (!value.toLowerCase().endsWith(".md")) {
    return { ...DEFAULT_ROUTE };
  }

  const inputSegments = value.replace(/\\/g, "/").split("/");
  if (inputSegments.includes("..")) {
    return { ...DEFAULT_ROUTE };
  }

  let contentUrl;
  try {
    contentUrl = new URL(value.replace(/\\/g, "/"), `${REPOSITORY_ORIGIN}/`);
  } catch {
    return { ...DEFAULT_ROUTE };
  }

  if (contentUrl.origin !== REPOSITORY_ORIGIN) {
    return { ...DEFAULT_ROUTE };
  }

  let path;
  try {
    path = decodeURIComponent(contentUrl.pathname).replace(/^\//, "");
  } catch {
    return { ...DEFAULT_ROUTE };
  }

  if (!path || path.includes("../") || !path.toLowerCase().endsWith(".md")) {
    return { ...DEFAULT_ROUTE };
  }

  return { path };
}

export function resolveContentPath(value, sourcePath) {
  const original = String(value || "");

  if (
    original.startsWith("#") ||
    /^(https?:)?\/\//i.test(original) ||
    /^(mailto|tel):/i.test(original)
  ) {
    return original;
  }

  let resolved;
  try {
    const sourceUrl = new URL(sourcePath, `${REPOSITORY_ORIGIN}/`);
    resolved = new URL(original, sourceUrl);
  } catch {
    return original;
  }

  if (resolved.origin !== REPOSITORY_ORIGIN) {
    return resolved.href;
  }

  let path;
  try {
    path = decodeURIComponent(resolved.pathname).replace(/^\//, "");
  } catch {
    return original;
  }

  if (path.includes("../")) {
    return original;
  }

  return `${path}${resolved.search}${resolved.hash}`;
}
