import React, { useState } from 'react';
import './App.css';
import Hero from './components/Hero.jsx';
import SocialLinksContainer from './components/SocialLinksContainer.jsx';
import { useEffect, useRef } from 'react';


function App() {
    const mainRef = useRef(null);

  useEffect(() => {
    const btn = document.getElementById('evaluate-risk');
    if (!btn) return;
    const handleClick = (e) => {
      e.preventDefault();
      if (mainRef.current) {
        mainRef.current.scrollIntoView({ behavior: 'smooth' });
      }
    };
    btn.addEventListener('click', handleClick);
    return () => btn.removeEventListener('click', handleClick);
  }, []);

  return (
    <>
      <Hero />
      <main ref={mainRef}>
      
        <SocialLinksContainer />
        <

      </main>
    </>
  );
}

export default App;
