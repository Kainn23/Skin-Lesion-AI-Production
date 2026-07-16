import React from 'react';

export default function ConfidenceChart({ result }) {
  if (!result || !result.top3) {
    return (
      <div className="card">
        <h3 className="text-lg font-bold text-slate-800 mb-4 border-b border-slate-100 pb-2">Confidence Scores</h3>
        <p className="text-slate-400 italic">Upload and analyze an image to see confidence scores.</p>
      </div>
    );
  }

  const colors = ['bg-brand-500', 'bg-slate-400', 'bg-slate-300'];

  return (
    <div className="card">
      <h3 className="text-lg font-bold text-slate-800 mb-4 border-b border-slate-100 pb-2">Confidence Scores</h3>
      <div className="space-y-4 pt-2">
        {result.top3.map((item, idx) => {
          const valPct = (item.confidence * 100).toFixed(1);
          return (
            <div key={idx}>
              <div className="flex justify-between text-sm font-medium text-slate-700 mb-1">
                <span className="uppercase">{item.class}</span>
                <span>{valPct}%</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-3">
                <div 
                  className={`${colors[idx] || 'bg-slate-200'} h-3 rounded-full transition-all duration-500 ease-out`}
                  style={{ width: `${valPct}%` }}
                ></div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  );
}
