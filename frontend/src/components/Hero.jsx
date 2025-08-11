import React from 'react';
import './Hero.css';

// Landing page hero section for anschel.ai
const Hero = () => {
  return (
    <header className="hero" role="banner">
      <div className="hero__bg" aria-hidden="true" />
      <div className="hero__inner">
        <p className="hero__eyebrow">Democratizing credit access in Ecuador</p>
        <h1 className="hero__title">
          AI-powered risk intelligence for <span className="hero__highlight">SMEs</span>
        </h1>
        <p className="hero__subtitle">
          anschel.ai combats financial exclusion by analyzing alternative data—behavioral patterns, digital reputation, operational signals, and context—to deliver transparent, fair, and actionable risk evaluations for small & medium enterprises without traditional credit history.
        </p>
        <p className="hero__impact">
          Enabling equitable lending decisions, accelerating growth, and fostering inclusive economic development across underserved regions.
        </p>
        <div className="hero__actions" role="group" aria-label="Primary actions">
          <button className="btn btn--primary" aria-label="Begin evaluating business risk">Evaluate My Risk</button>
          <button className="btn btn--secondary" aria-label="Learn how the platform works">How It Works</button>
        </div>
      </div>
    </header>
  );
};

export default Hero;
