import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { 
  Sprout, 
  Heart, 
  AlertTriangle, 
  Award, 
  PlusCircle, 
  ArrowRight, 
  Loader2 
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  PieChart, 
  Pie, 
  Cell, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  AreaChart, 
  Area, 
  CartesianGrid,
  Legend
} from 'recharts';

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await axios.get('/api/dashboard/stats');
        setStats(res.data);
      } catch (err) {
        console.error("Failed to load dashboard metrics:", err);
        setError("Could not retrieve statistics. Please refresh the page.");
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center gap-3">
        <Loader2 className="animate-spin text-brand-500" size={40} />
        <p className="text-slate-500 dark:text-slate-400 font-medium">Compiling dashboard analytics...</p>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="p-6 rounded-2xl bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20 text-red-700 dark:text-red-400 text-center">
        <p className="font-semibold">{error || "Data load error"}</p>
      </div>
    );
  }

  const { 
    total_predictions, 
    healthy_vs_diseased, 
    most_common_diseases, 
    confidence_distribution, 
    recent_predictions 
  } = stats;

  // Chart data formatting
  const pieData = [
    { name: 'Healthy Crops', value: healthy_vs_diseased.healthy },
    { name: 'Diseased Crops', value: healthy_vs_diseased.diseased }
  ];

  const PIE_COLORS = ['#10b981', '#f43f5e']; // Emerald-500 and Rose-500

  // Calculate healthy scan percentage
  const healthyPercentage = total_predictions > 0 
    ? Math.round((healthy_vs_diseased.healthy / total_predictions) * 100) 
    : 0;

  return (
    <div className="space-y-8">
      {/* Upper header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">Crop Analytics</h1>
          <p className="text-slate-500 dark:text-slate-400">Review real-time crop disease diagnoses and platform logs.</p>
        </div>
        <Link 
          to="/upload" 
          className="px-5 py-3 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold flex items-center gap-2 glow-button text-sm shrink-0"
        >
          <PlusCircle size={18} />
          <span>New Leaf Scan</span>
        </Link>
      </div>

      {/* Grid of Key Metrics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Card 1: Total Scans */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-200/50 dark:border-slate-800/80 flex items-center gap-4">
          <div className="p-3 bg-brand-500/10 text-brand-600 dark:text-brand-400 rounded-2xl">
            <Sprout size={24} />
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider block">Total Scans</span>
            <span className="text-2xl font-bold dark:text-white">{total_predictions}</span>
          </div>
        </div>

        {/* Card 2: Healthy Leaves */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-200/50 dark:border-slate-800/80 flex items-center gap-4">
          <div className="p-3 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 rounded-2xl">
            <Heart size={24} />
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider block">Healthy Crops</span>
            <span className="text-2xl font-bold dark:text-white">{healthy_vs_diseased.healthy}</span>
          </div>
        </div>

        {/* Card 3: Diseased Leaves */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-200/50 dark:border-slate-800/80 flex items-center gap-4">
          <div className="p-3 bg-rose-500/10 text-rose-600 dark:text-rose-400 rounded-2xl">
            <AlertTriangle size={24} />
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider block">Diseased Crops</span>
            <span className="text-2xl font-bold dark:text-white">{healthy_vs_diseased.diseased}</span>
          </div>
        </div>

        {/* Card 4: Health Score */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-200/50 dark:border-slate-800/80 flex items-center gap-4">
          <div className="p-3 bg-blue-500/10 text-blue-600 dark:text-blue-400 rounded-2xl">
            <Award size={24} />
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider block">Health Ratio</span>
            <span className="text-2xl font-bold dark:text-white">{healthyPercentage}%</span>
          </div>
        </div>
      </div>

      {/* Analytics Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chart 1: Pie Distribution of Healthy vs Diseased */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-200/50 dark:border-slate-800/80 flex flex-col justify-between min-h-[350px]">
          <h3 className="font-bold text-lg text-slate-900 dark:text-white mb-4">Crop Health Profile</h3>
          {total_predictions > 0 ? (
            <div className="flex-1 flex flex-col items-center justify-center">
              <div className="w-full h-48">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={80}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip contentStyle={{ borderRadius: '12px' }} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="flex gap-6 mt-4 text-xs font-medium">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-emerald-500" />
                  <span className="text-slate-500">Healthy ({healthy_vs_diseased.healthy})</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-rose-500" />
                  <span className="text-slate-500">Diseased ({healthy_vs_diseased.diseased})</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-slate-400 text-sm">
              No scan records. Scanned leaves will show here.
            </div>
          )}
        </div>

        {/* Chart 2: Common Diseases */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-200/50 dark:border-slate-800/80 flex flex-col justify-between lg:col-span-2 min-h-[350px]">
          <h3 className="font-bold text-lg text-slate-900 dark:text-white mb-4">Most Common Pathologies</h3>
          {most_common_diseases.length > 0 ? (
            <div className="flex-1 w-full h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={most_common_diseases} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" className="dark:hidden" />
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#1E293B" className="hidden dark:block" />
                  <XAxis 
                    dataKey="disease_name" 
                    tick={{ fontSize: 10, fill: '#94A3B8' }}
                    axisLine={false}
                    tickLine={false}
                    interval={0}
                    angle={-15}
                    textAnchor="end"
                  />
                  <YAxis 
                    tick={{ fontSize: 10, fill: '#94A3B8' }} 
                    axisLine={false}
                    tickLine={false}
                  />
                  <Tooltip contentStyle={{ borderRadius: '12px' }} cursor={{ fill: 'transparent' }} />
                  <Bar dataKey="count" fill="#3b82f6" radius={[8, 8, 0, 0]}>
                    {most_common_diseases.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill="#3b82f6" className="fill-brand-500 hover:fill-brand-600 transition-colors" />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-slate-400 text-sm">
              No disease scans recorded. All crops scanned are healthy!
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chart 3: Confidence Distribution */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-200/50 dark:border-slate-800/80 flex flex-col justify-between min-h-[350px] lg:col-span-1">
          <h3 className="font-bold text-lg text-slate-900 dark:text-white mb-4">Confidence Spread</h3>
          {total_predictions > 0 ? (
            <div className="flex-1 w-full h-64">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={confidence_distribution} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorConf" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" className="dark:hidden" />
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#1E293B" className="hidden dark:block" />
                  <XAxis dataKey="range_label" tick={{ fontSize: 9, fill: '#94A3B8' }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fontSize: 9, fill: '#94A3B8' }} axisLine={false} tickLine={false} />
                  <Tooltip contentStyle={{ borderRadius: '12px' }} />
                  <Area type="monotone" dataKey="count" stroke="#10b981" strokeWidth={2} fillOpacity={1} fill="url(#colorConf)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-slate-400 text-sm">
              No scan logs.
            </div>
          )}
        </div>

        {/* Section 4: Recent Predictions */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-200/50 dark:border-slate-800/80 flex flex-col justify-between lg:col-span-2 min-h-[350px]">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-bold text-lg text-slate-900 dark:text-white">Recent Activity</h3>
            {recent_predictions.length > 0 && (
              <Link 
                to="/history" 
                className="text-xs font-semibold text-brand-600 dark:text-brand-400 hover:text-brand-500 transition-colors flex items-center gap-1"
              >
                <span>View Full History</span>
                <ArrowRight size={14} />
              </Link>
            )}
          </div>

          <div className="flex-1 flex flex-col justify-center">
            {recent_predictions.length > 0 ? (
              <div className="space-y-4">
                {recent_predictions.map((item) => (
                  <div 
                    key={item.id} 
                    className="flex items-center justify-between p-3 rounded-2xl bg-slate-50 dark:bg-slate-900/50 border border-slate-100 dark:border-slate-800/40 hover:scale-[1.01] transition-transform duration-200"
                  >
                    <div className="flex items-center gap-3">
                      <img 
                        src={`/${item.image_path}`} 
                        alt="Scanned foliage" 
                        className="w-12 h-12 rounded-xl object-cover border border-slate-200 dark:border-slate-800"
                      />
                      <div>
                        <h4 className="font-bold text-sm text-slate-900 dark:text-white">{item.disease_name}</h4>
                        <span className="text-xs italic text-slate-400 dark:text-slate-500">{item.scientific_name}</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-4 text-right">
                      <div>
                        <span className="text-xs block font-semibold text-slate-400">Match Rate</span>
                        <span className="text-sm font-bold dark:text-white">{Math.round(item.confidence * 100)}%</span>
                      </div>
                      <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                        item.is_healthy 
                          ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400' 
                          : 'bg-rose-500/10 text-rose-600 dark:text-rose-400'
                      }`}>
                        {item.is_healthy ? 'Healthy' : 'Infected'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex items-center justify-center text-slate-400 text-sm">
                No scans registered. Get started by uploading a leaf photo.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
