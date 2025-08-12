import React, { useState } from 'react';
import './App.css';
import Hero from './components/Hero.jsx';
import SocialLinksContainer from './components/SocialLinksContainer.jsx';
import BalanceUploadContainer from './components/BalanceUploadContainer.jsx';
import { useEffect, useRef } from 'react';


function App() {
  const uploadRef = useRef(null);

  useEffect(() => {
    const btn = document.getElementById('evaluate-risk');
    if (!btn) return;
    const handleClick = (e) => {
      e.preventDefault();
      if (uploadRef.current) {
        uploadRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    };
    btn.addEventListener('click', handleClick);
    return () => btn.removeEventListener('click', handleClick);
  }, []);

  return (
    <>
      <Hero />
      <main>
        <div className="pt-10" />
        <SocialLinksContainer />
        <div ref={uploadRef} className="scroll-mt-24">
          <BalanceUploadContainer />
        </div>
      </main>
    </>
  );
}

export default App;
