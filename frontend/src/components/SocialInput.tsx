"use client";
import React, { useState, ChangeEvent } from 'react';

interface ValidationResult {
  platform: string | null;
  url: string;
  isValid: boolean;
  reason?: string;
}

// Solo detecta plataforma si es URL válida
function detectPlatformFromURL(u: URL): string | null {
  const h = u.hostname.toLowerCase();
  if (h.includes('twitter.com') || h === 'x.com') return 'twitter';
  if (h.includes('linkedin.com')) return 'linkedin';
  if (h.includes('instagram.com')) return 'instagram';
  if (h.includes('facebook.com')) return 'facebook';
  if (h.includes('tiktok.com')) return 'tiktok';
  return null;
}

function validateUrl(raw: string): ValidationResult | null {
  const trimmed = raw.trim();
  if (!trimmed) return null; // nada que validar aún
  if (!/^https?:\/\//i.test(trimmed)) {
    return { platform: null, url: trimmed, isValid: false, reason: 'Debe iniciar con http:// o https://' };
  }
  try {
    const urlObj = new URL(trimmed);
    if (!urlObj.hostname.includes('.')) {
      return { platform: null, url: trimmed, isValid: false, reason: 'Dominio inválido' };
    }
    const platform = detectPlatformFromURL(urlObj);
    if (!platform) {
      return { platform: null, url: trimmed, isValid: false, reason: 'Dominio no reconocido como red social soportada' };
    }
    return { platform, url: urlObj.toString(), isValid: true };
  } catch {
    return { platform: null, url: trimmed, isValid: false, reason: 'URL inválida' };
  }
}

export default function SocialInput() {
  const [value, setValue] = useState('');
  const [result, setResult] = useState<ValidationResult | null>(null);

  function handleChange(e: ChangeEvent<HTMLInputElement>) {
    const v = e.target.value;
    setValue(v);
    setResult(validateUrl(v));
  }

  function handleSubmit() {
    if (result?.isValid) {
      alert(`Guardado: ${result.url}`);
    }
  }

  return (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-gray-700" htmlFor="socialUrl">URL de red social (solo URLs válidas)</label>
      <input
        id="socialUrl"
        type="url"
        inputMode="url"
        value={value}
        onChange={handleChange}
        placeholder="https://www.red_social.com/company/ejemplo"
        className="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
        aria-invalid={result?.isValid === false}
        aria-describedby="socialUrlHelp"
      />
      <p id="socialUrlHelp" className="text-xs text-gray-500">Acepta el URL de: LinkedIn, Twitter/X, Instagram, Facebook, TikTok. Debe incluir http(s)://</p>
      {result && (
        <div className="text-xs flex flex-col gap-1">
          <div className="flex items-center gap-2">
            <span className="font-medium">Estado:</span>
            {result.isValid ? (
              <span className="text-green-600">Válida</span>
            ) : (
              <span className="text-red-600">Inválida{result.reason ? `: ${result.reason}` : ''}</span>
            )}
          </div>
          <div className="flex items-center gap-2">
            <span className="font-medium">Plataforma:</span>
            <span>{result.platform ?? '—'}</span>
          </div>
        </div>
      )}
      <button
        type="button"
        disabled={!result?.isValid}
        className="inline-flex items-center rounded bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow hover:bg-indigo-500 disabled:cursor-not-allowed disabled:bg-gray-300"
        onClick={handleSubmit}
      >
        Guardar
      </button>
    </div>
  );
}
