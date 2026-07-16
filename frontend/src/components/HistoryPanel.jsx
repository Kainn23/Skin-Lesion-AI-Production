import React from 'react';
import { History } from 'lucide-react';

export default function HistoryPanel({ history, onSelectHistory }) {
  if (!history || history.length === 0) return null;

  return (
    <div className="mb-8">
      <div className="flex items-center gap-2 mb-4">
        <History size={18} className="text-text-color opacity-50" />
        <h2 className="text-sm font-bold text-text-color opacity-70 uppercase tracking-widest">Prediction History</h2>
      </div>

      <div className="flex gap-4 overflow-x-auto pb-4 custom-scrollbar snap-x">
        {history.map((item, i) => (
          <div 
            key={i}
            onClick={() => onSelectHistory(item)}
            className="snap-start shrink-0 w-48 glass-panel p-3 cursor-pointer group hover:border-primary transition-all flex items-center gap-3"
          >
            <div className="h-12 w-12 rounded-lg bg-slate-200 dark:bg-slate-700 overflow-hidden shrink-0">
              <img src={item.imageUrl} alt="History" className="w-full h-full object-cover" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-bold text-text-color truncate">{item.prediction}</p>
              <div className="flex justify-between items-center mt-1">
                <span className="text-[10px] text-primary font-semibold">{(item.confidence * 100).toFixed(1)}%</span>
                <span className="text-[10px] text-text-color opacity-50">{new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
