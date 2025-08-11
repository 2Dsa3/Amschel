"use client";
import React, { useState } from "react";

// Simple component: user types a social network name and we send it to backend (Python).
// Adjust BACKEND_URL and payload key to match your FastAPI endpoint.

const BACKEND_URL = "http://localhost:8000/"; // change to your endpoint

export default function SocialInput() {
  const [network, setNetwork] = useState("");
  const [loading, setLoading] = useState(false);
  const [serverResp, setServerResp] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const disabled = !network.trim() || loading;

  async function handleSubmit() {
    if (disabled) return;
    setLoading(true);
    setError(null);
    setServerResp(null);
    try {
      const resp = await fetch(BACKEND_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ social_network: network.trim() })
      });
      if (!resp.ok) {
        const data = await resp.json().catch(() => ({}));
        throw new Error(data.detail || "Error en el servidor");
      }
      const data = await resp.json().catch(() => ({}));
      setServerResp(data);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-3">
      <label htmlFor="socialInput" className="block text-sm font-medium text-gray-700">
        Red social
      </label>
      <input
        id="socialInput"
        type="text"
        value={network}
        onChange={(e) => setNetwork(e.target.value)}
        placeholder="Ej: twitter, linkedin, instagram..."
        className="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
      />
      <button
        type="button"
        disabled={disabled}
        onClick={handleSubmit}
        className="inline-flex items-center rounded bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow hover:bg-indigo-500 disabled:cursor-not-allowed disabled:bg-gray-300"
      >
        {loading ? "Enviando..." : "Enviar"}
      </button>
      {error && <div className="text-xs text-red-600">{error}</div>}
      {serverResp && (
        <pre className="mt-2 max-h-60 overflow-auto rounded border border-gray-200 bg-gray-50 p-2 text-xs">
{JSON.stringify(serverResp, null, 2)}
        </pre>
      )}
    </div>
  );
}
