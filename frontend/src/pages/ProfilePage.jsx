import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { User, Mail, Calendar, Upload, Heart, ShieldAlert, Loader2, AlertCircle } from 'lucide-react';

export default function ProfilePage() {
  const { user } = useAuth();
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await axios.get('/api/profile/me');
        setProfileData(res.data);
      } catch (err) {
        console.error("Failed to load user profile statistics:", err);
        setError("Could not retrieve profile statistics.");
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center gap-3">
        <Loader2 className="animate-spin text-brand-500" size={32} />
        <p className="text-slate-500 dark:text-slate-400 text-sm">Loading profile profile...</p>
      </div>
    );
  }

  if (error || !profileData) {
    return (
      <div className="p-6 rounded-2xl bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20 text-red-700 dark:text-red-400 text-center">
        <p className="font-semibold">{error || "Data load error"}</p>
      </div>
    );
  }

  const { upload_count, statistics, created_at } = profileData;

  const cards = [
    { label: "Total Uploads", value: upload_count, icon: Upload, color: "bg-brand-500/10 text-brand-600 dark:text-brand-400" },
    { label: "Healthy Scans", value: statistics.healthy_scans, icon: Heart, color: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400" },
    { label: "Infected Scans", value: statistics.diseased_scans, icon: ShieldAlert, color: "bg-rose-500/10 text-rose-600 dark:text-rose-400" }
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">Account Profile</h1>
        <p className="text-slate-500 dark:text-slate-400">Manage account preferences and review leaf scans metrics.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* User Card Information */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-200/50 dark:border-slate-800/80 md:col-span-1 space-y-6">
          <div className="flex flex-col items-center text-center">
            <div className="bg-gradient-to-tr from-brand-600 to-emerald-500 text-white w-20 h-20 rounded-2xl flex items-center justify-center font-extrabold text-3xl shadow-xl shadow-brand-500/10 mb-4">
              {user?.username.charAt(0).toUpperCase()}
            </div>
            <h2 className="font-bold text-xl text-slate-900 dark:text-white">{user?.username}</h2>
            <span className="text-xs font-semibold text-brand-600 dark:text-brand-500 bg-brand-50 dark:bg-brand-500/10 px-2.5 py-1 rounded-full mt-1.5 uppercase">
              Agronomist
            </span>
          </div>

          <div className="border-t border-slate-100 dark:border-slate-800/80 pt-6 space-y-4 text-sm">
            <div className="flex items-center gap-3 text-slate-600 dark:text-slate-300">
              <Mail size={16} className="text-slate-400" />
              <span className="truncate">{user?.email}</span>
            </div>
            <div className="flex items-center gap-3 text-slate-600 dark:text-slate-300">
              <Calendar size={16} className="text-slate-400" />
              <span>Joined {new Date(created_at).toLocaleDateString()}</span>
            </div>
          </div>
        </div>

        {/* Statistics breakdown Grid */}
        <div className="md:col-span-2 space-y-6">
          <div className="glass-panel p-6 rounded-3xl border border-slate-200/50 dark:border-slate-800/80">
            <h3 className="font-bold text-lg text-slate-900 dark:text-white mb-6">Scan Performance Metrics</h3>
            
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              {cards.map((card, idx) => {
                const Icon = card.icon;
                return (
                  <div key={idx} className="p-5 rounded-2xl bg-slate-50 dark:bg-slate-900/50 border border-slate-100 dark:border-slate-800/40 flex flex-col items-center text-center space-y-3">
                    <div className={`p-2.5 rounded-xl ${card.color}`}>
                      <Icon size={20} />
                    </div>
                    <div>
                      <span className="text-xs font-semibold text-slate-400 block mb-1">{card.label}</span>
                      <span className="text-2xl font-bold dark:text-white">{card.value}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="glass-panel p-6 rounded-3xl border border-slate-200/50 dark:border-slate-800/80">
            <h3 className="font-bold text-lg text-slate-900 dark:text-white mb-4 font-semibold">User Role & Authority</h3>
            <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
              This account holds administrative rights to scan leaf foliage. Uploaded files are matched against the local Keras convolutional network and logged in history.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
