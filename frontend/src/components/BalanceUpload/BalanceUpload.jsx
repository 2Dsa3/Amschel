import React, { useCallback, useRef, useState } from 'react';
import PropTypes from 'prop-types';
import { UploadCloud, FileText, X } from 'lucide-react';

const formatSize = (bytes) => {
  if (!bytes && bytes !== 0) return '';
  const units = ['B','KB','MB','GB'];
  let i = 0; let val = bytes;
  while (val >= 1024 && i < units.length - 1) { val /= 1024; i++; }
  return `${val.toFixed(val < 10 && i>0 ? 1 : 0)} ${units[i]}`;
};

const PDFDropzone = ({ label, file, onFileChange, inputId }) => {
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  const validateAndSet = useCallback(
    (f) => {
      if (!f) return;
      const isPdf = /\.pdf$/i.test(f.name) && f.type === 'application/pdf';
      if (!isPdf) {
        setError('Only PDF files are allowed.');
        return;
      }
      setError('');
      onFileChange(f);
    },
    [onFileChange]
  );

  const handleFiles = (files) => {
    if (!files || !files.length) return;
    validateAndSet(files[0]);
  };

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

  const openDialog = (e) => {
    e?.preventDefault();
    e?.stopPropagation();
    inputRef.current?.click();
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      e.stopPropagation();
      openDialog(e);
    }
  };

  const handleClick = (e) => {
    // Only handle if not triggered by keyboard
    if (e.detail === 0) return; // Keyboard triggered click has detail = 0
    openDialog(e);
  };

  const id = inputId || `${label.replace(/\s+/g, '-').toLowerCase()}-input`;

  return (
    <div className="bu-dropzone-wrapper">
      <div
        role="button"
        tabIndex={0}
        onClick={handleClick}
        onKeyDown={handleKeyDown}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        aria-describedby={error ? `${id}-error` : undefined}
        aria-label={label}
        className={`bu-dropzone ${dragActive ? 'bu-dropzone--active' : ''} ${file ? 'bu-dropzone--has-file' : ''}`}
      >
        <input
          id={id}
          ref={inputRef}
          type="file"
          accept="application/pdf,.pdf"
          className="hidden"
          onChange={onInputChange}
          aria-invalid={!!error}
        />
        <div className="bu-dz-icon">
          {file ? <FileText size={24} /> : <UploadCloud size={24} />}
        </div>
        <div className="bu-dz-text-main">{file ? 'Replace PDF' : 'Click or drag & drop PDF'}</div>
        <div className="bu-dz-text-sub">{label}</div>
        <div className="bu-dz-meta">PDF only</div>
        {file && (
          <div className="bu-file-info">
            <p className="bu-file-name" title={file.name}>{file.name}</p>
            <div className="bu-file-meta">
              <span>{formatSize(file.size)}</span>
              <span className="sep">•</span>
              <button
                type="button"
                onClick={(e) => { e.stopPropagation(); onFileChange(null); }}
                className="bu-remove-btn"
                aria-label="Remove file"
              >
                <X size={12} />
                <span className="txt">Remove</span>
              </button>
            </div>
          </div>
        )}
      </div>
      {error && <p id={`${id}-error`} className="bu-error" role="alert">{error}</p>}
    </div>
  );
};

PDFDropzone.propTypes = {
  label: PropTypes.string.isRequired,
  file: PropTypes.instanceOf(File),
  onFileChange: PropTypes.func.isRequired,
  inputId: PropTypes.string,
};

const BalanceAndInfoUpload = ({ files, onChange }) => {
  const handleFileChange = (key, file) => {
    onChange({ ...files, [key]: file });
  };

  return (
    <div className="bu-wrapper">
      <div className="bu-header">
        <h2 className="bu-title">Financial Documents</h2>
        <p className="bu-hint">Upload the Balance Sheet and a General Information PDF.</p>
      </div>
      <div className="bu-grid">
        <PDFDropzone
          label="Balance Sheet"
          file={files.balanceSheet}
          onFileChange={(f) => handleFileChange('balanceSheet', f)}
        />
        <PDFDropzone
          label="General Information"
          file={files.generalInfo}
          onFileChange={(f) => handleFileChange('generalInfo', f)}
        />
      </div>
    </div>
  );
};

BalanceAndInfoUpload.propTypes = {
  files: PropTypes.shape({
    balanceSheet: PropTypes.instanceOf(File),
    generalInfo: PropTypes.instanceOf(File),
  }).isRequired,
  onChange: PropTypes.func.isRequired,
};

export default BalanceAndInfoUpload;
