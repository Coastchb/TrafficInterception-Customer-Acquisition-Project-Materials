/**
 * NEAGLE GOLF — Cloudflare Worker entry (paired with the static assets in ./dist).
 *
 * Enforces the canonical host + HTTPS with a single 301 redirect:
 *   http://neaglegolf.com/*      -> https://neaglegolf.com/*
 *   http://www.neaglegolf.com/*  -> https://neaglegolf.com/*
 *   https://www.neaglegolf.com/* -> https://neaglegolf.com/*
 *
 * Unknown paths fall back to the custom 404 page (dist/404.html) instead of
 * letting the asset layer return a raw 500/307.
 *
 * workers.dev preview and local dev (wrangler dev) are served as-is.
 */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const host = url.hostname;

    // local dev (wrangler dev) — serve directly
    if (host === 'localhost' || host === '127.0.0.1') {
      return env.ASSETS.fetch(request);
    }

    // enforce canonical host only on the apex/www custom domain
    if (host === 'neaglegolf.com' || host === 'www.neaglegolf.com') {
      if (url.protocol !== 'https:' || host === 'www.neaglegolf.com') {
        const dest = new URL(url);
        dest.protocol = 'https:';
        dest.hostname = 'neaglegolf.com';
        dest.port = '';
        return Response.redirect(dest.toString(), 301);
      }
    }

    // /chatSend, /chatMessages, /profileSave, /profileGet belong to an external
    // Cloud Run proxy (PROXY_BASE), never to this site. Googlebot discovered
    // /chatSend while executing page JS and recorded it as a 404. 410 Gone tells
    // crawlers the URL is permanently gone, which clears it far faster than a 404.
    const NON_PAGE_PATHS = new Set([
      '/chatSend',
      '/chatMessages',
      '/profileSave',
      '/profileGet',
    ]);
    if (NON_PAGE_PATHS.has(url.pathname)) {
      return new Response('410 - Gone', {
        status: 410,
        headers: { 'Content-Type': 'text/plain; charset=utf-8' },
      });
    }

    // workers.dev preview & everything else — serve static assets
    let res;
    try {
      res = await env.ASSETS.fetch(request);
    } catch {
      res = null;
    }
    if (!res || res.status === 404 || res.status >= 500) {
      // serve the custom 404 page (dist/404.html) with a proper 404 status
      try {
        const nf = await env.ASSETS.fetch(
          new Request(new URL('/404.html', url), request)
        );
        if (nf && nf.status === 200) {
          return new Response(nf.body, { status: 404, headers: nf.headers });
        }
      } catch {
        // fall through to plain 404 below
      }
      return new Response('404 - Page Not Found', {
        status: 404,
        headers: { 'Content-Type': 'text/plain; charset=utf-8' },
      });
    }
    return res;
  }
};
