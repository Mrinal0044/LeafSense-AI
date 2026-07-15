import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Search, Trash2, Calendar, FileText, Loader2, AlertCircle } from 'lucide-react';

export default function HistoryPage() {
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [error, setError] = useState('');

  const fetchHistory = async (query = '') => {
    try {
      const url = query ? `/api/predictions/history?search=${encodeURIComponent(query)}` : '/api/predictions/history';
      const res = await axios.get(url);
      setHistory(res.data);
    } catch (err) {
      console.error("Failed to load scans history:", err);
      setError("Failed to retrieve scan logs.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    setLoading(true);
    fetchHistory(searchQuery);
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation(); // Avoid triggering card click redirect
    if (!window.confirm("Are you sure you want to delete this scan from your history? This will delete the physical file as well.")) {
      return;
    }
    
    try {
      await axios.delete(`/api/predictions/history/${id}`);
      setHistory(history.filter(item => item.id !== id));
    } catch (err) {
      console.error("Failed to delete history item:", err);
      alert("Failed to delete the history item. Please try again.");
    }
  };

  const handleCardClick = async (item) => {
    // We need to fetch detailed disease profiles (symptoms, treatments etc) since list items contain base statistics only
    try {
      setLoading(true);
      // Fetch details from uploads/db if needed, but since we didn't define a GET details endpoint,
      // we can recreate the details using prediction_result formatting by loading the disease_info in python.
      // Wait! The predict function itself maps it, or we can send the local prediction data details to the prediction result page.
      // Wait, where do we get the full details from?
      // Since `disease_info.json` is loaded statically, we can query a predict mock, or we can fetch details from the backend.
      // Wait, is there a details payload inside the list items? No, history items map to PredictionHistoryItem schema:
      // id, class_id, disease_name, scientific_name, confidence, is_healthy, image_path, prediction_date.
      // To get the full detailed dictionary (symptoms, preventions etc.) when they click a card:
      // We can query a simple endpoint or fetch the entire `disease_info.json` or mapping statically in React!
      // Yes! Fetching the details on demand from the static knowledge database is very standard. Or better,
      // since the client can fetch `/ml/saved_model/disease_info.json` (wait, is that exposed?)
      // Let's check: the backend mounts `/uploads`, but it doesn't mount the ml folder.
      // However, we can create a simple route or look up details.
      // Wait! In `HistoryPage`, when they click a card, we can load the disease details statically inside React,
      // OR we can make a query. Let's look up how we can obtain the details.
      // Since the details metadata is a static JSON dictionary, we can bundle a tiny disease metadata map in frontend,
      // or we can request it, or we can just fetch the details dynamically.
      // Wait! Let's check: can we just load the full disease_info.json in the frontend?
      // Yes, we can copy or read the disease details statically in the frontend, or make a backend call.
      // Wait! Let's check if the backend has an endpoint for disease details.
      // No, we didn't add a specific GET `/predictions/{id}` route.
      // But we can add it, or we can just query the static metadata.
      // Actually, since we want a completely self-contained premium layout, let's look up the details by adding a quick detail parser!
      // Wait, we can fetch `/api/predictions/history` which lists the items.
      // If we want the details, we can define a client-side database in React, or just call the predict endpoint again? No, calling predict again writes another row to the database.
      // To do this elegantly and matching standard Repository pattern, we can fetch the `disease_info.json` which has descriptions.
      // Wait, how can we fetch it from frontend?
      // Since the frontend is in the same folder structure, we can just save a copy of `disease_info.json` in the frontend `public` directory,
      // or bundle it in a JSON helper file!
      // Bundling it as `src/data/disease_info.json` or fetching `/disease_info.json` from the frontend public folder is extremely clean.
      // Let's create a copy or fetch it. Actually, we can fetch it or read it. Let's bundle a simplified version or the full database in `src/data/disease_info.json` so the frontend can retrieve details for any scanned card!
      // Let's check: if we copy `ml/saved_model/disease_info.json` to `frontend/public/disease_info.json` (or write it to `frontend/src/data/disease_info.json`), the frontend can import it directly and look up details instantly!
      // This is a beautiful, fast, and completely offline-friendly architectural decision. Let's do that!
      // Let's see: we can fetch the local `disease_info.json` file inside the history detail card view by reading from a JSON helper.
      // Let's write `frontend/src/pages/HistoryPage.jsx` to load this json on card click, then navigate to `/prediction-result`.
      // Let's first make sure we write `frontend/src/pages/HistoryPage.jsx`.
      
      const detailsRes = await axios.get('/api/predictions/history');
      // Let's mock or read the details statically:
      const diseaseDatabase = await import('../data/disease_info.json').then(m => m.default);
      const details = diseaseDatabase[item.class_id] || {
        description: "No description available.",
        symptoms: "N/A",
        causes: "N/A",
        treatment: "N/A",
        prevention: "N/A"
      };

      const fullPrediction = {
        ...item,
        details
      };
      
      navigate('/prediction-result', { state: { prediction: fullPrediction, preview: `/${item.image_path}` } });
    } catch (err) {
      console.error(err);
      alert("Failed to load details for this scan.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">Scan History</h1>
          <p className="text-slate-500 dark:text-slate-400">Manage and inspect your historical crop diagnosis records.</p>
        </div>
      </div>

      {/* Search Input bar */}
      <form onSubmit={handleSearch} className="flex gap-3 max-w-lg">
        <div className="relative flex-1">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
            <Search size={16} />
          </div>
          <input
            type="text"
            placeholder="Search by crop or disease name..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="block w-full pl-10 pr-4 py-3 border border-slate-200 dark:border-slate-800 rounded-xl bg-white dark:bg-slate-900 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 text-sm placeholder-slate-400 dark:text-white transition-all"
          />
        </div>
        <button
          type="submit"
          className="px-5 py-3 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-medium text-sm transition-all shadow-md shadow-brand-500/10 hover:shadow-brand-500/20"
        >
          Search
        </button>
      </form>

      {error && (
        <div className="p-4 rounded-xl bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20 text-red-700 dark:text-red-400 flex items-start gap-3 text-sm">
          <AlertCircle className="shrink-0 mt-0.5" size={16} />
          <span>{error}</span>
        </div>
      )}

      {loading ? (
        <div className="min-h-[40vh] flex flex-col items-center justify-center gap-3">
          <Loader2 className="animate-spin text-brand-500" size={32} />
          <p className="text-slate-500 dark:text-slate-400 text-sm">Loading logs...</p>
        </div>
      ) : history.length > 0 ? (
        /* History Grid Items */
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {history.map((item) => (
            <div
              key={item.id}
              onClick={() => handleCardClick(item)}
              className="glass-panel rounded-3xl border border-slate-200/50 dark:border-slate-800/80 overflow-hidden cursor-pointer hover:shadow-xl hover:scale-[1.01] transition-all duration-300 flex flex-col"
            >
              <div className="relative h-44 w-full bg-slate-100 dark:bg-slate-950">
                <img
                  src={`/${item.image_path}`}
                  alt="Scanned leaf"
                  className="w-full h-full object-cover"
                />
                <span className={`absolute top-4 right-4 px-2.5 py-1 rounded-full text-xs font-semibold shadow-md ${
                  item.is_healthy
                    ? 'bg-emerald-500 text-white'
                    : 'bg-rose-500 text-white'
                }`}>
                  {item.is_healthy ? 'Healthy' : 'Infected'}
                </span>
              </div>

              <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
                <div className="space-y-1">
                  <h3 className="font-bold text-base text-slate-900 dark:text-white line-clamp-1">
                    {item.disease_name}
                  </h3>
                  <span className="text-xs italic text-slate-400 dark:text-slate-500 line-clamp-1">
                    {item.scientific_name}
                  </span>
                </div>

                <div className="flex items-center justify-between border-t border-slate-100 dark:border-slate-800/60 pt-4 text-xs text-slate-400">
                  <div className="flex items-center gap-1.5">
                    <Calendar size={14} />
                    <span>{new Date(item.prediction_date).toLocaleDateString()}</span>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={(e) => handleDelete(item.id, e)}
                      className="p-2 rounded-lg bg-red-50 dark:bg-red-500/10 text-red-600 dark:text-red-400 hover:bg-red-100 dark:hover:bg-red-500/20 transition-colors"
                      title="Delete record"
                    >
                      <Trash2 size={14} />
                    </button>
                    <span className="px-2 py-1 rounded bg-slate-100 dark:bg-slate-800 font-bold">
                      {Math.round(item.confidence * 100)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 glass-panel rounded-3xl border border-slate-200/50 dark:border-slate-800/80">
          <FileText className="mx-auto text-slate-300 dark:text-slate-700 mb-3" size={40} />
          <h3 className="font-bold text-lg text-slate-900 dark:text-white mb-1">No scans found</h3>
          <p className="text-sm text-slate-400 max-w-xs mx-auto">
            Try scanning a leaf image or adjusting your search query filter.
          </p>
        </div>
      )}
    </div>
  );
}
