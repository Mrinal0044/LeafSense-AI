import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { UploadCloud, Image as ImageIcon, X, AlertCircle, Loader2 } from 'lucide-react';

export default function UploadPage() {
  const navigate = useNavigate();
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const processFile = (file) => {
    setError('');
    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
      setError('Unsupported file type. Please select a JPG, PNG, or WEBP image.');
      return;
    }
    
    // Check file size (e.g. max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      setError('File size too large. Please select an image under 5MB.');
      return;
    }

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
  };

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    setLoading(true);
    setError('');
    
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const res = await axios.post('/api/predictions/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      // Redirect to prediction detail page, passing diagnostic report state
      navigate('/prediction-result', { state: { prediction: res.data, preview: previewUrl } });
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail || 
        'Failed to complete diagnosis. Please ensure the server is active and try again.'
      );
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">Plant Diagnosis</h1>
        <p className="text-slate-500 dark:text-slate-400">Upload a high-quality photo of a single leaf to run AI disease diagnosis.</p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20 text-red-700 dark:text-red-400 flex items-start gap-3 text-sm">
          <AlertCircle className="shrink-0 mt-0.5" size={16} />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {!previewUrl ? (
          /* Drag and Drop Zone */
          <div
            onDragEnter={handleDrag}
            onDragOver={handleDrag}
            onDragLeave={handleDrag}
            onDrop={handleDrop}
            className={`
              border-2 border-dashed rounded-3xl p-10 flex flex-col items-center justify-center min-h-[300px] text-center transition-all cursor-pointer relative group
              ${dragActive 
                ? 'border-brand-500 bg-brand-50/50 dark:bg-brand-500/5' 
                : 'border-slate-300 dark:border-slate-800 hover:border-brand-500 dark:hover:border-brand-500/40 hover:bg-slate-50 dark:hover:bg-slate-900/10'}
            `}
          >
            <input
              type="file"
              id="file-upload"
              multiple={false}
              onChange={handleChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
            
            <div className="p-4 bg-brand-100 dark:bg-brand-500/10 text-brand-600 dark:text-brand-500 rounded-full group-hover:scale-110 transition-transform mb-4">
              <UploadCloud size={32} />
            </div>
            
            <h3 className="font-bold text-lg text-slate-900 dark:text-white mb-1">
              Drag & drop leaf photo here
            </h3>
            <p className="text-sm text-slate-500 dark:text-slate-400 mb-4 max-w-sm">
              Supports JPEG, PNG or WEBP up to 5MB. Make sure the leaf is in focus and centered.
            </p>
            <span className="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-semibold text-slate-600 dark:text-slate-300 group-hover:bg-brand-500 group-hover:text-white transition-colors">
              Browse Files
            </span>
          </div>
        ) : (
          /* Image Preview and Confirmation */
          <div className="glass-panel p-6 rounded-3xl border border-slate-200/50 dark:border-slate-800/80 relative">
            <button
              type="button"
              onClick={handleClear}
              disabled={loading}
              className="absolute top-4 right-4 p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500 dark:text-slate-400 transition-colors disabled:opacity-50"
              title="Remove image"
            >
              <X size={16} />
            </button>
            
            <div className="flex flex-col sm:flex-row items-center gap-6">
              <img 
                src={previewUrl} 
                alt="Selected foliage" 
                className="w-full sm:w-48 h-48 rounded-2xl object-cover border border-slate-200 dark:border-slate-800"
              />
              
              <div className="flex-1 w-full text-center sm:text-left space-y-2">
                <div className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500">
                  <ImageIcon size={14} />
                  <span>Ready for analysis</span>
                </div>
                <h3 className="font-bold text-lg text-slate-900 dark:text-white truncate max-w-xs sm:max-w-md">
                  {selectedFile?.name}
                </h3>
                <span className="text-xs text-slate-400 block">
                  File Size: {Math.round(selectedFile?.size / 1024)} KB
                </span>
                
                <div className="pt-4 flex gap-4">
                  <button
                    type="submit"
                    disabled={loading}
                    className="flex-1 sm:flex-none px-6 py-3 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold flex items-center justify-center gap-2 glow-button text-sm disabled:opacity-50"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="animate-spin" size={18} />
                        <span>Analyzing with AI...</span>
                      </>
                    ) : (
                      <span>Run Health Scan</span>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </form>
    </div>
  );
}
