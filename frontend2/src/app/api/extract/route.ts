import { NextRequest, NextResponse } from 'next/server';

// Force dynamic (no caching) and ensure node runtime for consistent scraping
export const dynamic = 'force-dynamic';
export const revalidate = 0;
export const runtime = 'nodejs';

// Supported platforms (only instagram implemented for deep data now)
const SUPPORTED = ['linkedin', 'twitter', 'x.com', 'instagram', 'facebook', 'tiktok'];

function detectPlatform(url: string): string {
  const lower = url.toLowerCase();
  for (const p of SUPPORTED) {
    if (lower.includes(p)) return p === 'x.com' ? 'twitter' : p;
  }
  return 'unknown';
}

function normalizeFollowerNumber(raw: string): number | null {
  const cleaned = raw.replace(/,/g, '').trim();
  const m = cleaned.match(/^([0-9]+(?:\.[0-9]+)?)([kKmMbB])?$/);
  if (!m) return parseInt(cleaned, 10) || null;
  const num = parseFloat(m[1]);
  const suffix = m[2]?.toLowerCase();
  switch (suffix) {
    case 'k': return Math.round(num * 1_000);
    case 'm': return Math.round(num * 1_000_000);
    case 'b': return Math.round(num * 1_000_000_000);
    default: return Math.round(num);
  }
}

interface FollowerData {
  follower_count: number | null;
  raw_html_chars: number;
  source: string;
  note?: string;
  debug?: any;
}

function extractUsername(u: string): string | null {
  try {
    const url = new URL(u);
    const parts = url.pathname.split('/').filter(Boolean);
    if (parts.length >= 1) return parts[0];
    return null;
  } catch { return null; }
}

async function fetchInstagramFollowers(url: string): Promise<FollowerData & { username?: string | null }> {
  if (!url.endsWith('/')) url = url + '/';
  try {
    const resp = await fetch(url, {
      cache: 'no-store',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9'
      }
    });
    if (!resp.ok) {
      return { follower_count: null, raw_html_chars: 0, source: 'http_error', note: `status ${resp.status}`, username: extractUsername(url) };
    }
    const html = await resp.text();
    const raw_html_chars = html.length;

  let follower_count: number | null = null;
    let source = 'unknown';
    let note: string | undefined;

    // 1. Meta og:description (multi-language: followers, seguidores, abonnés)
    const ogMetaRegex = /<meta[^>]+property=["']og:description["'][^>]*>/i;
    const ogTag = html.match(ogMetaRegex)?.[0];
    let ogContent: string | undefined;
    if (ogTag) {
      const contentAttr = ogTag.match(/content=["']([^"']+)["']/i);
      ogContent = contentAttr?.[1];
      if (ogContent) {
        const followersPattern = /([0-9][0-9.,]*\s*[kKmMbB]?)(?=\s*(followers|follower|seguidores|seguidoras|abonn[eé]s))/i;
        const match = ogContent.match(followersPattern);
        if (match) {
          follower_count = normalizeFollowerNumber(match[1]);
          source = 'og:description';
          note = `langToken=${match[2]}`;
        }
      }
    }

    // 2. Embedded JSON edge_followed_by
    if (follower_count == null) {
      const jsonEdgeMatch = html.match(/"edge_followed_by":\{"count":(\d+)}/);
      if (jsonEdgeMatch) {
        follower_count = parseInt(jsonEdgeMatch[1], 10);
        source = 'embedded_json';
      }
    }

    // 3. Alternative JSON keys (defensive)
    if (follower_count == null) {
      const altJson = html.match(/"followed_by":\{"count":(\d+)}/);
      if (altJson) {
        follower_count = parseInt(altJson[1], 10);
        source = 'alt_json_followed_by';
      }
    }

    if (follower_count == null) {
      const altJson2 = html.match(/"follower_count":(\d+)/);
      if (altJson2) {
        follower_count = parseInt(altJson2[1], 10);
        source = 'follower_count_key';
      }
    }

    // 4. Fallback: generic pattern with <span> wrappers
    if (follower_count == null) {
      const generic = html.match(/([0-9][0-9.,]*\s*[kKmMbB]?)(?:<\/span>)?\s*(followers|seguidores)/i);
      if (generic) {
        follower_count = normalizeFollowerNumber(generic[1]);
        source = 'generic_pattern';
      }
    }

    const debug = process.env.NODE_ENV !== 'production' ? {
      ogTagFound: !!ogTag,
      ogContentSample: ogContent?.slice(0, 120),
      edgeFollowedByFound: /"edge_followed_by":\{"count":(\d+)}/.test(html),
      altFollowedByFound: /"followed_by":\{"count":(\d+)}/.test(html),
      followerCountKeyFound: /"follower_count":(\d+)/.test(html),
      usedSource: source
    } : undefined;

    return { follower_count, raw_html_chars, source, note, debug, username: extractUsername(url) };
  } catch (e: any) {
    return { follower_count: null, raw_html_chars: 0, source: 'exception', note: e.message, username: extractUsername(url) };
  }
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const raw = (body?.url || '').trim();
    if (!raw) return NextResponse.json({ error: 'url is required' }, { status: 400 });
    if (!/^https?:\/\//i.test(raw)) return NextResponse.json({ error: 'url must start with http(s)://' }, { status: 400 });
    let url: URL;
    try { url = new URL(raw); } catch { return NextResponse.json({ error: 'invalid url' }, { status: 400 }); }
    const platform = detectPlatform(url.toString());

    let followerData: Partial<FollowerData> = {};
    if (platform === 'instagram') {
      followerData = await fetchInstagramFollowers(url.toString());
    }

    return NextResponse.json({
      platform,
      ok: platform !== 'unknown',
      url: url.toString(),
      ...followerData
    });
  } catch (e) {
    return NextResponse.json({ error: 'bad request' }, { status: 400 });
  }
}
