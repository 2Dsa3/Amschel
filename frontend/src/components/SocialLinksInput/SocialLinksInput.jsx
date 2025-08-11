import React, { useMemo } from 'react';
import './SocialLinksInput.css';

// Simple URL validator
function isValidUrl(url) {
    if (!url) return true; // empty allowed until submit
    try { new URL(url); return true; } catch { return false; }
}

/**
 * Controlled SocialLinksInput
 * Props:
 *  - links: string[] (required)
 *  - onChange: (updated: string[]) => void
 */
const SocialLinksInput = ({ links = [], onChange }) => {
    const errors = useMemo(() => links.map(l => (l && !isValidUrl(l) ? 'Invalid URL' : '')), [links]);

    const updateAt = (idx, value) => {
        const next = [...links];
        next[idx] = value;
        onChange && onChange(next);
    };

    const addField = () => {
        onChange && onChange([...links, '']);
    };

    const removeField = (idx) => {
        const next = links.filter((_, i) => i !== idx);
        onChange && onChange(next.length ? next : ['']);
    };

    return (
        <div className="sl-wrapper">
            <div className="sl-header">
                <div className="max-w-md mx-auto text-center">
                    <label className="sl-label">Social Media Links</label>
                    <p className="sl-hint">Add public profiles (Facebook, Instagram, Twitter (X)).</p>
                </div>
            </div>

            <div className="sl-fields">
                {links.map((link, idx) => {
                    const hasError = !!errors[idx];
                    return (
                        <div key={idx} className="sl-row sl-row-animate">
                            <div className="sl-input-wrap">
                                <input
                                    id={`social-link-${idx}`}
                                    type="url"
                                    className={`sl-input ${hasError ? 'sl-input-invalid' : ''}`}
                                    placeholder="https://linkedin.com/in/yourprofile"
                                    value={link}
                                    onChange={(e) => updateAt(idx, e.target.value.trim())}
                                    aria-invalid={hasError}
                                    aria-describedby={hasError ? `social-link-${idx}-error` : undefined}
                                />
                                {links.length > 1 && (
                                    <button
                                        type="button"
                                        aria-label={`Remove link ${idx + 1}`}
                                        className="sl-remove-btn"
                                        onClick={() => removeField(idx)}
                                    >
                                        ×
                                    </button>
                                )}
                            </div>
                            {hasError && (
                                <p id={`social-link-${idx}-error`} className="sl-error">{errors[idx]}</p>
                            )}
                        </div>
                    );
                })}
            </div>

            <div className="sl-actions">
                <button type="button" onClick={addField} className="sl-add-btn">+ Add another link</button>
                {errors.some(e => e) && <span className="sl-error-inline">One or more links are invalid.</span>}
            </div>
        </div>
    );
};

export default SocialLinksInput;
