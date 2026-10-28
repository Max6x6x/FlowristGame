// Offline support for Növényismeret. Bump SHELL only when this file's logic changes; app code updates arrive via network-first.
const SHELL = "flowrist-shell-v1";
const IMG = "flowrist-img";
const SHELL_FILES = ["./", "index.html", "latin.json", "data.json"];

self.addEventListener("install", e => e.waitUntil(caches.open(SHELL).then(c => c.addAll(SHELL_FILES)).then(() => self.skipWaiting())));
self.addEventListener("activate", e => e.waitUntil(
  caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("flowrist-shell") && k !== SHELL).map(k => caches.delete(k))))
    .then(() => self.clients.claim())));

self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET") return;
  // pages and data: network first (so updates arrive), cache when offline; query string ignored (?v= cache-busters)
  if (u.origin === location.origin && /(\/|index\.html|data\.json|latin\.json)$/.test(u.pathname)) {
    const key = u.origin + u.pathname;
    e.respondWith(fetch(e.request).then(r => {
      if (r.ok) caches.open(SHELL).then(c => c.put(key, r.clone()));
      return r;
    }).catch(() => caches.match(key)));
    return;
  }
  // photos, same-origin or hotlinked: cache first; opaque (no-cors) responses are cached too
  if (e.request.destination === "image") {
    e.respondWith(caches.open(IMG).then(c => c.match(e.request.url).then(hit => hit || fetch(e.request).then(r => {
      if (r.ok || r.type === "opaque") c.put(e.request.url, r.clone());
      return r;
    }))));
  }
});
