import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Sprout, ShieldAlert, BarChart3, Clock, ArrowRight, Sun, Moon } from 'lucide-react';

export default function LandingPage() {
  const { user } = useAuth();

  const features = [
    {
      title: "Instant Diagnosis",
      description: "Upload a single leaf photo and get a detailed diagnosis with crop health details in milliseconds.",
      icon: Sprout,
      color: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
    },
    {
      title: "Actionable Treatments",
      description: "Get detailed descriptions of symptoms, causes, biological treatments, and preventions.",
      icon: ShieldAlert,
      color: "bg-amber-500/10 text-amber-600 dark:text-amber-400"
    },
    {
      title: "Analytics Dashboard",
      description: "Track scan history, analyze disease distributions, monitor confidence levels, and check crop trends.",
      icon: BarChart3,
      color: "bg-blue-500/10 text-blue-600 dark:text-blue-400"
    },
    {
      title: "Historical Audits",
      description: "Keep a record of your scans. Look up diagnoses, search crop categories, and manage old logs.",
      icon: Clock,
      color: "bg-purple-500/10 text-purple-600 dark:text-purple-400"
    }
  ];

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 flex flex-col justify-between transition-colors duration-300">
      {/* Navbar header */}
      <nav className="max-w-7xl mx-auto w-full px-6 py-5 flex items-center justify-between">
        <div className="flex items-center gap-2 font-bold text-xl text-brand-600 dark:text-brand-500 tracking-tight">
          <div className="bg-brand-100 dark:bg-brand-500/10 p-1.5 rounded-xl">
            <Sprout className="text-brand-600 dark:text-brand-500" size={24} />
          </div>
          <span>LeafSense <span className="text-slate-400 font-light">AI</span></span>
        </div>

        <div>
          {user ? (
            <Link 
              to="/dashboard" 
              className="px-5 py-2.5 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-medium glow-button flex items-center gap-2 text-sm"
            >
              <span>Go to Dashboard</span>
              <ArrowRight size={16} />
            </Link>
          ) : (
            <div className="flex items-center gap-4">
              <Link 
                to="/login" 
                className="text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 transition-colors"
              >
                Log In
              </Link>
              <Link 
                to="/register" 
                className="px-5 py-2.5 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-medium glow-button text-sm"
              >
                Get Started
              </Link>
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center text-center max-w-4xl mx-auto px-6 py-12">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-100 dark:bg-brand-500/10 text-brand-700 dark:text-brand-400 text-xs font-semibold tracking-wide uppercase mb-6">
          <span>Production-Ready ML Inference</span>
        </div>
        
        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight mb-6 bg-gradient-to-r from-slate-900 via-brand-700 to-emerald-600 dark:from-white dark:via-brand-400 dark:to-emerald-400 bg-clip-text text-transparent">
          AI-Powered Plant Health Management Platform
        </h1>

        <p className="text-base sm:text-lg text-slate-600 dark:text-slate-400 max-w-2xl mb-8 leading-relaxed">
          LeafSense AI applies deep transfer learning with EfficientNetB0 to diagnose 38 crop categories. Protect your crop health, prevent disease outbreaks, and record scans instantly.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 mb-16">
          {user ? (
            <Link 
              to="/upload" 
              className="px-8 py-3.5 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold glow-button flex items-center justify-center gap-2"
            >
              <span>Scan Leaf Image Now</span>
              <ArrowRight size={18} />
            </Link>
          ) : (
            <>
              <Link 
                to="/register" 
                className="px-8 py-3.5 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold glow-button flex items-center justify-center gap-2"
              >
                <span>Create Free Account</span>
                <ArrowRight size={18} />
              </Link>
              <Link 
                to="/login" 
                className="px-8 py-3.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 font-semibold hover:bg-slate-50 dark:hover:bg-slate-800 transition-all flex items-center justify-center"
              >
                Sign In
              </Link>
            </>
          )}
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 text-left w-full">
          {features.map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <div key={idx} className="glass-panel p-6 rounded-2xl flex gap-4">
                <div className={`p-3 rounded-xl h-fit ${feature.color}`}>
                  <Icon size={20} />
                </div>
                <div>
                  <h3 className="font-semibold text-lg mb-2 text-slate-900 dark:text-white">{feature.title}</h3>
                  <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">{feature.description}</p>
                </div>
              </div>
            );
          })}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200/50 dark:border-slate-900 py-6 text-center text-sm text-slate-400">
        <p>&copy; {new Date().getFullYear()} LeafSense AI. All rights reserved.</p>
      </footer>
    </div>
  );
}
