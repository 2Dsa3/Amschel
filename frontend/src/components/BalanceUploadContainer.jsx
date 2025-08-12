import React, { useState, useEffect, useRef } from 'react';
import BalanceAndInfoUpload from './BalanceUpload/BalanceUpload.jsx';
import { uploadPDFs } from '../services/api';

/**
 * BalanceUploadContainer
 * Manages two PDF uploads (Balance Sheet + General Information) and submits them to backend.
 * - Handles state, validation gating, submit, loading & feedback.
 */
const BalanceUploadContainer = () => {
  const [files, setFiles] = useState({ balanceSheet: null, generalInfo: null });
  const [status, setStatus] = useState('idle'); // idle | uploading | success | error
  const [error, setError] = useState('');
  const [serverResponse, setServerResponse] = useState(null);
    const sectionRef = useRef(null);

  const handleChange = (next) => {
    setFiles(next);
    setError('');
  };

  const canSubmit = !!files.balanceSheet || !!files.generalInfo; // allow at least one

    const handleSubmit = async (e) => {
    e.preventDefault();
    if (!canSubmit || status === 'uploading') return;
    setStatus('uploading');
    setError('');
    setServerResponse(null);
    try {
      const resp = await uploadPDFs(files.balanceSheet, files.generalInfo);
      setServerResponse(resp);
      setStatus('success');
    } catch (err) {
      setError(err.message || 'Upload failed');
      setStatus('error');
    }
  };

    // Scroll into centered view on mount
    useEffect(() => {
        if (sectionRef.current) {
            sectionRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }, []);

return (
        <section
            ref={sectionRef}
            className="min-h-screen flex items-center justify-center py-14 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-gray-50 to-gray-100"
            aria-labelledby="balance-section-title"
        >
            <div className="w-full max-w-5xl flex flex-col items-center">
                <h2 id="balance-section-title" className="text-xl font-semibold text-gray-800 mb-6 tracking-tight text-center">
                    Enterprise Documents
                </h2>
                <form onSubmit={handleSubmit} className="w-full flex flex-col items-center gap-8">
                    <BalanceAndInfoUpload files={files} onChange={handleChange} />
                    <div className="flex items-center gap-4 flex-wrap justify-center">
                        <button
                            type="submit"
                            disabled={!canSubmit || status === 'uploading'}
                            className={`px-6 py-2.5 rounded-md text-sm font-semibold text-white transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 shadow-md ${
                                (!canSubmit || status === 'uploading') ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
                            }`}
                            aria-disabled={!canSubmit || status === 'uploading'}
                        >
                            {status === 'uploading' ? 'Uploading…' : 'Upload PDFs'}
                        </button>
                        {status === 'success' && (
                            <span className="text-sm text-green-600" role="status">Uploaded successfully</span>
                        )}
                        {status === 'error' && (
                            <span className="text-sm text-red-600" role="alert">{error}</span>
                        )}
                    </div>
                    {serverResponse && (
                        <pre className="bg-gray-900 text-gray-100 text-xs p-4 rounded-lg overflow-auto max-h-52 w-full" aria-label="Server response">{JSON.stringify(serverResponse, null, 2)}</pre>
                    )}
                </form>
            </div>
        </section>
);
};

export default BalanceUploadContainer;
