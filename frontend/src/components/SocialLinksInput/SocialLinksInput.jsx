import React, { useState } from 'react';
import './SocialLinksInput.css';

function isValidUrl(url) {
  try {
    new URL(url);
    return true;
  } catch (_) {
    return false;
  }
}

const SocialLinksInput = ({ links = [], onChange }) => {
  const [socialLinks, setSocialLinks] = useState(links.length ? links : ['']);
  const [errors, setErrors] = useState([]);

  const handleInputChange = (idx, value) => {
    const updatedLinks = [...socialLinks];
    updatedLinks[idx] = value;
    setSocialLinks(updatedLinks);
    if (onChange) onChange(updatedLinks);
    validateLinks(updatedLinks);
  };

  const handleAddField = () => {
    setSocialLinks([...socialLinks, '']);
    setErrors([...errors, '']);
  };

  const handleRemoveField = (idx) => {
    const updatedLinks = socialLinks.filter((_, i) => i !== idx);
    setSocialLinks(updatedLinks);
    setErrors(errors.filter((_, i) => i !== idx));
    if (onChange) onChange(updatedLinks);
  };

  const validateLinks = (linksArr) => {
    const newErrors = linksArr.map(link =>
      link && !isValidUrl(link) ? 'Invalid URL' : ''
    );
    setErrors(newErrors);
  };

  return (
    <div className="social-links-input-container">
      <label className="block text-sm font-medium text-gray-700 mb-2">Social Media Links</label>
      {socialLinks.map((link, idx) => (
        <div key={idx} className="flex items-center mb-2">
          <input
            type="text"
            className={`social-link-input border rounded px-3 py-2 w-full mr-2 ${errors[idx] ? 'border-red-500' : 'border-gray-300'}`}
            placeholder="Enter social media URL"
            value={link}
            onChange={e => handleInputChange(idx, e.target.value)}
            aria-label={`Social media link ${idx + 1}`}
          />
          <button
            type="button"
            className="delete-btn text-red-500 hover:text-red-700 ml-1"
            onClick={() => handleRemoveField(idx)}
            aria-label="Delete link"
            disabled={socialLinks.length === 1}
          >
            &times;
          </button>
        </div>
      ))}
      {errors.some(e => e) && (
        <div className="text-red-500 text-xs mb-2">Please enter valid URLs.</div>
      )}
      <button
        type="button"
        className="add-btn bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        onClick={handleAddField}
      >
        Add
      </button>
    </div>
  );
};

export default SocialLinksInput;
