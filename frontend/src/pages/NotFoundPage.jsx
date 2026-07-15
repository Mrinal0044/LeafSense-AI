import React from 'react';
import { Link } from 'react-router-dom';
import { AlertCircle, Home } from 'lucide-react';

export default function NotFoundPage() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center text-center p-6 space-y-6">
      <div className="p-4 bg-amber-500/10 text-amber-600 dark:text-amber-500 rounded-full">
        <AlertCircle size={48} />
      </div>
      
      <div className="space-y-2">
        <h1 className="text-4xl font-extrabold text-slate-900 dark:text-white">404 - Page Not Found</h1>
        <p className="text-slate-500 dark:text-slate-400 max-w-sm mx-auto leading-relaxed">
          The crop pathway or page you are looking for does not exist or has been removed.
        </p>
      </div>

      <Link
        to="/dashboard"
        className="px-5 py-3 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold flex items-center gap-2 glow-button text-sm"
      >
        <Home size={18} />
        <span>Return to Dashboard</span>
      </Link>
    </div>
  );
}
