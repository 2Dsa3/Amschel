import React from 'react';
import './Hero.css';
import { TrendingUp, Shield, Users, CheckCircle2 } from 'lucide-react';

// Landing page hero section for anschel.ai (two-column layout + feature cards)
const Hero = () => {
  return (
    <header className="hero" role="banner">
      <div className="hero__bg" aria-hidden="true" />
      <div className="hero__inner hero__grid">
        {/* Left Column: Copy */}
        <div className="hero__col hero__col--content">
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
            <button  id='evaluate-risk' className="btn btn--primary" aria-label="Begin evaluating business risk">Evaluate Enterprise's Risk</button>
            <a href="https://github.com/2Dsa3/PymeRisk" className="btn btn--secondary" aria-label="Learn how the platform works">How It Works</a>
          </div>
        </div>

        {/* Right Column: Feature Cards + Checklist */}
        <div className="hero__col hero__col--features" aria-label="Key platform features">
          <ul className="feature-cards" role="list">
            <li className="feature-card">
              <div className="feature-card__icon" aria-hidden="true"><TrendingUp size={28} strokeWidth={2.2} /></div>
              <div className="feature-card__body">
                <h3 className="feature-card__title">Alternative Data Analysis</h3>
                <p className="feature-card__desc">Evaluate creditworthiness using behavioral patterns, digital footprint, and operational signals</p>
              </div>
            </li>
            <li className="feature-card">
              <div className="feature-card__icon" aria-hidden="true"><Shield size={28} strokeWidth={2.2} /></div>
              <div className="feature-card__body">
                <h3 className="feature-card__title">Transparent Risk Assessment</h3>
                <p className="feature-card__desc">Fair, explainable AI-driven evaluations that promote financial inclusion</p>
              </div>
            </li>
            <li className="feature-card">
              <div className="feature-card__icon" aria-hidden="true"><Users size={28} strokeWidth={2.2} /></div>
              <div className="feature-card__body">
                <h3 className="feature-card__title">SME Focused</h3>
                <p className="feature-card__desc">Designed for small & medium enterprises in emerging markets</p>
              </div>
            </li>
          </ul>
          <ul className="hero__checklist" role="list" aria-label="Platform assurances">
            <li><CheckCircle2 aria-hidden="true" /> Regulatory compliant</li>
            <li><CheckCircle2 aria-hidden="true" /> GDPR & data privacy focused</li>
            <li><CheckCircle2 aria-hidden="true" /> Real-time decision making</li>
          </ul>
        </div>
      </div>
    </header>
  );
};

export default Hero;
