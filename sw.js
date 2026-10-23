/* Keeps the app shell available offline for a fast start; the data always comes live from Versile OS.
   Also shows "new work" alerts on the phone, even when the app is closed. */
var CACHE = 'versile-shell-v9';
var API = 'https://dbilaugtfkeeiuflzqtd.supabase.co/functions/v1/versile';
var FILES = ['./', 'index.html', 'manifest.json', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png'];
self.addEventListener('install', function (e) { e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(FILES); })); self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(caches.keys().then(function (ks) { return Promise.all(ks.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); })); })); self.clients.claim(); });
self.addEventListener('fetch', function (e) {
  var u = new URL(e.request.url);
  if (u.origin !== location.origin) return;           // the app itself (Google) is never cached
  e.respondWith(fetch(e.request).then(function (r) { var c = r.clone(); caches.open(CACHE).then(function (k) { k.put(e.request, c); }); return r; })
    .catch(function () { return caches.match(e.request).then(function (r) { return r || caches.match('./'); }); }));
});
self.addEventListener('push', function (e) {
  e.waitUntil(self.registration.pushManager.getSubscription().then(function (sub) {
    return fetch(API, { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify({ app: 2, endpoint: sub ? sub.endpoint : '' }) })
      .then(function (r) { return r.json(); }).catch(function () { return {}; });
  }).then(function (j) {
    return self.registration.showNotification('Versile OS · new work', { body: (j && j.text) || 'You have new work', icon: 'icon-192.png', badge: 'icon-192.png', tag: 'vos-work', renotify: true, vibrate: [200, 100, 200] });
  }));
});
self.addEventListener('notificationclick', function (e) {
  e.notification.close();
  e.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (cs) {
    for (var i = 0; i < cs.length; i++) if ('focus' in cs[i]) return cs[i].focus();
    return self.clients.openWindow('./');
  }));
});
