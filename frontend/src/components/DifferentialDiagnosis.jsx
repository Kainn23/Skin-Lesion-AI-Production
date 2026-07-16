import React from 'react';
import { motion } from 'framer-motion';
import lesionInfo from '../data/lesion_info.json';

export default function DifferentialDiagnosis({ probabilities }) {
  if (!probabilities || Object.keys(probabilities).length === 0) return null;

  // Get top 3 predictions
  const top3 = Object.entries(probabilities)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 3)
    .map(([key, value]) => {
      // Clean up key if it has formatting (e.g., "1_MEL")
      const cleanKey = key.split('_').pop();
      const info = lesionInfo[cleanKey];
      return {
        key: cleanKey,
        name: info ? info.name : cleanKey,
        value: value * 100
      };
    });

  // Colors based on rank (1st, 2nd, 3rd)
  const colors = [
    'bg-primary',
    'bg-secondary',
    'bg-accent'
  ];

  return (
    <div className="glass-panel p-6 mb-6">
      <h3 className="text-[10px] font-bold text-text-color opacity-50 uppercase tracking-widest mb-4">Differential Diagnosis</h3>
      
      <div className="space-y-4">
        {top3.map((item, index) => (
          <div key={index} className="w-full">
            <div className="flex justify-between items-end mb-1.5 text-sm">
              <span className="font-semibold text-text-color opacity-90">{item.name}</span>
              <span className="font-bold text-text-color opacity-70">{item.value.toFixed(1)}%</span>
            </div>
            <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: `${item.value}%` }}
                transition={{ duration: 1, delay: index * 0.1, ease: 'easeOut' }}
                className={`h-full rounded-full ${colors[index]}`}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
