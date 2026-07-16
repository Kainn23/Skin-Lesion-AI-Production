import React, { useState, useEffect } from 'react';
import { RefreshCw, MousePointerClick, AlertCircle } from 'lucide-react';
import { getRandomExamples } from '../services/api';

export default function ExampleGallery({ onSelectExample }) {
  const [examples, setExamples] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadRandomExamples = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getRandomExamples(8);
      setExamples(data);
    } catch (err) {
      console.error(err);
      setError("Failed to load dataset examples.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRandomExamples();
  }, []);

  const handleDragStart = (e, url) => {
    e.dataTransfer.setData('application/x-example-url', url);
  };

  return (
    <div className="mb-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-bold text-text-color flex items-center gap-2">
          HAM10000 Example Cases
        </h2>
        <button 
          onClick={loadRandomExamples}
          disabled={loading}
          className="flex items-center gap-2 text-xs font-semibold text-primary hover:text-primary-dark transition-colors disabled:opacity-50"
        >
          <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
          Refresh Examples
        </button>
      </div>

      {error ? (
        <div className="p-4 bg-amber-50 dark:bg-amber-900/20 text-amber-600 border border-amber-200 dark:border-amber-700/30 rounded-xl flex items-center gap-2 text-sm">
          <AlertCircle size={16} />
          {error} (Ensure the backend is running)
        </div>
      ) : (
        <div className="flex gap-4 overflow-x-auto pb-4 custom-scrollbar snap-x">
          {examples.map((ex, i) => (
            <div 
              key={`${ex.id}-${i}`}
              draggable
              onDragStart={(e) => handleDragStart(e, ex.url)}
              onClick={() => onSelectExample(ex.url)}
              className="snap-start shrink-0 w-36 h-36 glass-panel overflow-hidden cursor-pointer group hover:border-primary transition-all relative"
            >
              <div className="w-full h-full bg-slate-200 dark:bg-slate-700 relative overflow-hidden">
                <img 
                  src={ex.url} 
                  alt="Example Case" 
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" 
                  crossOrigin="anonymous"
                />
                <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                  <MousePointerClick className="text-white" size={24} />
                </div>
              </div>
            </div>
          ))}
          
          {loading && examples.length === 0 && (
            [...Array(8)].map((_, i) => (
              <div key={i} className="snap-start shrink-0 w-36 h-36 glass-panel overflow-hidden animate-pulse">
                <div className="w-full h-full bg-slate-200 dark:bg-slate-700"></div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
