import React from 'react';
import { useLocation, Link, Navigate } from 'react-router-dom';
import { Sprout, CheckCircle2, AlertTriangle, ArrowLeft, ShieldCheck, HeartPulse } from 'lucide-react';

export default function PredictionPage() {
  const location = useLocation();
  const state = location.state;

  if (!state || !state.prediction) {
    return <Navigate to="/upload" replace />;
  }

  const { prediction, preview } = state;
  const { disease_name, scientific_name, confidence, is_healthy, details } = prediction;

  const sections = [
    { label: 'Description', content: details.description, icon: Sprout },
    { label: 'Symptoms', content: details.symptoms, icon: HeartPulse },
    { label: 'Causes', content: details.causes, icon: AlertTriangle },
    { label: 'Treatment', content: details.treatment, icon: ShieldCheck },
    { label: 'Prevention', content: details.prevention, icon: CheckCircle2 },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Upper navigation */}
      <div>
        <Link 
          to="/upload" 
          className="inline-flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-brand-500 transition-colors"
        >
          <ArrowLeft size={16} />
          <span>Upload Another Image</span>
        </Link>
      </div>

      {/* Hero card diagnosis summary */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-slate-200/50 dark:border-slate-800/80 flex flex-col md:flex-row items-center gap-8">
        {preview && (
          <img 
            src={preview} 
            alt="Foliage scan preview" 
            className="w-full md:w-56 h-56 rounded-2xl object-cover border border-slate-200 dark:border-slate-800"
          />
        )}

        <div className="flex-1 w-full text-center md:text-left space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-center md:justify-start gap-3">
            <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold ${
              is_healthy 
                ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400' 
                : 'bg-rose-500/10 text-rose-600 dark:text-rose-400'
            }`}>
              {is_healthy ? <CheckCircle2 size={12} /> : <AlertTriangle size={12} />}
              <span>{is_healthy ? 'Healthy Vegetation' : 'Infected / Pathology Detected'}</span>
            </span>

            <span className="text-xs font-bold text-slate-400 dark:text-slate-500">
              Confidence score: {Math.round(confidence * 100)}%
            </span>
          </div>

          <div className="space-y-1">
            <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight">
              {disease_name}
            </h1>
            <span className="text-base sm:text-lg italic text-slate-400 dark:text-slate-500 block">
              {scientific_name}
            </span>
          </div>

          <div className="w-full bg-slate-100 dark:bg-slate-800 h-2.5 rounded-full overflow-hidden">
            <div 
              className={`h-full transition-all duration-500 ${is_healthy ? 'bg-emerald-500' : 'bg-rose-500'}`}
              style={{ width: `${confidence * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Pathology Breakdown details */}
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">Pathological Profile</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {sections.map((sec, idx) => {
            const Icon = sec.icon;
            // Skip irrelevant details if crop is healthy
            if (is_healthy && ['Symptoms', 'Causes', 'Treatment'].includes(sec.label)) {
              return null;
            }
            return (
              <div 
                key={idx} 
                className={`
                  glass-panel p-6 rounded-3xl border border-slate-200/50 dark:border-slate-800/80 space-y-3
                  ${sec.label === 'Description' ? 'md:col-span-2' : ''}
                `}
              >
                <div className="flex items-center gap-2 text-brand-600 dark:text-brand-400">
                  <Icon size={18} />
                  <h3 className="font-bold text-sm uppercase tracking-wider">{sec.label}</h3>
                </div>
                <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                  {sec.content || 'No details specified.'}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
