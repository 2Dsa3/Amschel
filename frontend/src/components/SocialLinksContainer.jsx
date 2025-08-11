import React, { useCallback, useMemo, useState } from 'react';
import SocialLinksInput from './SocialLinksInput/SocialLinksInput.jsx';
import { scrapeInstagram } from '../services/api';

/**
 * SocialLinksContainer
 * Manages social links state, triggers Instagram scraping, and displays results.
 */
const SocialLinksContainer = () => {
  const [socialLinks, setSocialLinks] = useState(['']);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null); // { followers, followees }

  // Update handler passed to SocialLinksInput
  const handleLinksChange = useCallback((links) => {
    setSocialLinks(links);
  }, []);

  // Extract the first Instagram username from provided links
  const instagramUsername = useMemo(() => {
    for (const link of socialLinks) {
      if (!link) continue;
      try {
        const url = new URL(link);
        if (url.hostname.includes('instagram.com')) {
          // Path may end with slash or include extra segments
            const segments = url.pathname.split('/').filter(Boolean);
            if (segments.length) {
              // Basic username validation: letters, numbers, underscores, periods
              const candidate = segments[0];
              if (/^[A-Za-z0-9._]+$/.test(candidate)) {
                return candidate;
              }
            }
        }
      } catch (_) {
        // ignore invalid URL parse errors
      }
    }
    return '';
  }, [socialLinks]);

  const canScrape = instagramUsername && !loading;

  const handleScrape = async () => {
    if (!instagramUsername) return;
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const data = await scrapeInstagram(instagramUsername);
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="social-links-container" style={{ maxWidth: '640px', margin: '2rem auto', padding: '0 1rem' }}>
      <SocialLinksInput links={socialLinks} onChange={handleLinksChange} />
      <div style={{ marginTop: '1rem' }}>
        <button
          type="button"
          onClick={handleScrape}
          disabled={!canScrape}
          className={`scrape-btn ${!canScrape ? 'scrape-btn--disabled' : ''}`}
          aria-disabled={!canScrape}
        >
          {loading ? 'Scraping...' : 'Scrape Instagram'}
        </button>
        {!instagramUsername && (
          <p style={{ color: '#6B7280', fontSize: '0.85rem', marginTop: '0.5rem' }}>
            Add a valid Instagram URL (e.g., https://instagram.com/your_user/) to enable scraping.
          </p>
        )}
        {error && (
          <p style={{ color: '#DC2626', fontSize: '0.9rem', marginTop: '0.5rem' }} role="alert">
            {error}
          </p>
        )}
        {result && (
          <div style={{ marginTop: '0.75rem', background: '#F3F6FA', padding: '0.75rem 1rem', borderRadius: '0.5rem' }}>
            <p style={{ margin: 0, color: '#1F2937', fontWeight: 500 }}>Username: <span style={{ fontWeight: 600 }}>{instagramUsername}</span></p>
            <p style={{ margin: '0.25rem 0 0', color: '#1F2937' }}>Followers: <strong>{result.followers}</strong></p>
            <p style={{ margin: '0.15rem 0 0', color: '#1F2937' }}>Following: <strong>{result.followees}</strong></p>
          </div>
        )}
      </div>
      <style>{`
        .scrape-btn { background:#1D4ED8; color:#fff; border:none; padding:0.85rem 1.3rem; font-size:0.95rem; font-weight:600; border-radius:0.65rem; cursor:pointer; transition:background .25s, opacity .25s; }
        .scrape-btn:hover:not(:disabled) { background:#1E40AF; }
        .scrape-btn:disabled, .scrape-btn.scrape-btn--disabled { background:#93A5BF; cursor:not-allowed; opacity:0.85; }
        .scrape-btn:focus-visible { outline:3px solid #93C5FD; outline-offset:2px; }
      `}</style>
    </div>
  );
};

export default SocialLinksContainer;
