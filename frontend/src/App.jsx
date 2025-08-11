import React from 'react';
import './App.css';
import Hero from './components/Hero.jsx';
import SocialLinksContainer from './components/SocialLinksContainer.jsx';

function App() {
  return (
    <>
      <Hero />
      <main>
        <SocialLinksContainer />
      </main>
    </>
  );
}

export default App;
