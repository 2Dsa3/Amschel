import React, { useCallback, useRef, useState } from 'react';
import PropTypes from 'prop-types';

/**
 * BalanceUpload
 * Upload component for a company's balance sheet (PDF only) supporting drag & drop and click.
 * Props:
 *  - file: File | null
 *  - onChange: (file: File|null) => void
 */
const BalanceUpload = ({ file, onChange }) => {
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  const validateAndSet = useCallback((f) => {
    if (!f) return; // ignore null
    const isPdf = /\.pdf$/i.test(f.name) && f.type === 'application/pdf';
    if (!isPdf) {
      setError('Only PDF files are allowed.');
      return;
    }
    setError('');
    onChange && onChange(f);
  }, [onChange]);

  const handleFiles = useCallback((files) => {
    if (!files || !files.length) return;
    validateAndSet(files[0]);
  }, [validateAndSet]);

  const onInputChange = (e) => {
    handleFiles(e.target.files);
  };

  const onDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!dragActive) setDragActive(true);
  };

  const onDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    // only reset when leaving the container
    if (e.currentTarget.contains(e.relatedTarget)) return;
    setDragActive(false);
  };

  const onDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const openDialog = () => {
    inputRef.current?.click();
  };

  return (
    <div className="w-full max-w-xl">
      <label className="block mb-1 text-sm font-semibold text-gray-700" htmlFor="balance-upload-input">
        Balance Sheet (PDF)
      </label>
      <div
        role="button"
        tabIndex={0}
        onClick={openDialog}
        onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openDialog(); } }}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        aria-describedby={error ? 'balance-upload-error' : undefined}
        className={`group relative flex flex-col items-center justify-center rounded-lg border-2 border-dashed transition-colors cursor-pointer focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 px-4 py-8 text-center select-none
          ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-gray-50 hover:bg-gray-100'}
        `}
      >
        <input
          id="balance-upload-input"
          ref={inputRef}
          type="file"
          accept="application/pdf,.pdf"
          className="hidden"
          onChange={onInputChange}
          aria-invalid={!!error}
        />
        <div className="text-sm text-gray-700 font-medium">
          {file ? 'Replace file' : 'Click or drag & drop to upload'}
        </div>
        <div className="mt-1 text-xs text-gray-500">
          PDF only (max 1 file)
        </div>
        {file && (
          <p className="mt-3 text-xs text-gray-600 truncate w-full" title={file.name}>
            Selected: <span className="font-semibold">{file.name}</span>
          </p>
        )}
      </div>
      {error && (
        <p id="balance-upload-error" className="mt-2 text-xs text-red-600" role="alert">{error}</p>
      )}
    </div>
  );
};

BalanceUpload.propTypes = {
  file: PropTypes.instanceOf(File),
  onChange: PropTypes.func,
};

export default BalanceUpload;
