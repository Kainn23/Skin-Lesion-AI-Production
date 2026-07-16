import React from 'react';
import { motion } from 'framer-motion';

export default function ABCDEAssessment({ data }) {
  const getRiskDetails = (score) => {
    if (score === null || score === undefined) return { label: 'N/A', color: 'bg-slate-200 dark:bg-slate-700 text-slate-500' };
    if (score <= 30) return { label: 'Low', color: 'bg-emerald-500 text-emerald-600' };
    if (score <= 60) return { label: 'Moderate', color: 'bg-amber-500 text-amber-600' };
    return { label: 'High', color: 'bg-red-500 text-red-600' };
  };

  const metrics = [
    { label: 'A', name: 'Asymmetry', value: data?.asymmetry },
    { label: 'B', name: 'Border Irregularity', value: data?.border_irregularity },
    { label: 'C', name: 'Color Variation', value: data?.color_variation },
    { label: 'D', name: 'Diameter', value: data?.diameter },
  ];

  return (
    <div className="glass-panel p-6 mb-6">
      <h3 className="text-[10px] font-bold text-text-color opacity-50 uppercase tracking-widest mb-4">ABCDE Analysis</h3>
      
      <div className="space-y-4">
        {metrics.map((metric, i) => {
          const risk = getRiskDetails(metric.value);
          
          return (
            <div key={i}>
              <div className="flex justify-between items-center mb-1 text-sm">
                <span className="font-semibold text-text-color opacity-90">{metric.name}</span>
                <span className="font-bold text-text-color opacity-70">
                  {metric.value !== undefined && metric.value !== null ? `${metric.value}%` : '--'}
                </span>
              </div>
              <div className="w-full h-2 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden relative">
                {metric.value !== null && metric.value !== undefined ? (
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${metric.value}%` }}
                    transition={{ duration: 1, delay: i * 0.1, ease: "easeOut" }}
                    className={`h-full rounded-full ${risk.color.split(' ')[0]}`}
                  />
                ) : null}
              </div>
            </div>
          );
        })}

        <div>
          <div className="flex justify-between items-center mb-1 text-sm">
            <span className="font-semibold text-text-color opacity-90">Evolution</span>
          </div>
          <div className="w-full h-8 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-border-color flex items-center px-3">
            <span className="text-xs font-medium text-text-color opacity-60">Requires multiple images over time.</span>
          </div>
        </div>

      </div>
    </div>
  );
}
