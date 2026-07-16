import React from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, ShieldCheck, Activity } from 'lucide-react';
import lesionInfo from '../data/lesion_info.json';

export default function PredictionCard({ prediction, confidence }) {
  if (!prediction) return null;

  // Find info from JSON mapping
  const infoKey = Object.keys(lesionInfo).find(key => prediction.includes(key));
  const info = infoKey ? lesionInfo[infoKey] : null;
  
  const risk = info?.risk || 'Unknown';
  const fullName = info?.name || prediction;
  const abbreviation = infoKey || prediction;

  const confPercent = (confidence * 100).toFixed(1);

  // Risk styling
  let riskColor = 'text-slate-500 bg-slate-100 dark:bg-slate-800';
  let RiskIcon = Activity;
  if (risk === 'High') {
    riskColor = 'text-red-500 bg-red-50 dark:bg-red-500/10 border-red-200 dark:border-red-500/20';
    RiskIcon = AlertTriangle;
  } else if (risk === 'Moderate') {
    riskColor = 'text-amber-500 bg-amber-50 dark:bg-amber-500/10 border-amber-200 dark:border-amber-500/20';
    RiskIcon = AlertTriangle;
  } else if (risk === 'Low') {
    riskColor = 'text-emerald-500 bg-emerald-50 dark:bg-emerald-500/10 border-emerald-200 dark:border-emerald-500/20';
    RiskIcon = ShieldCheck;
  }

  return (
    <div className="glass-panel p-6 mb-6">
      <h3 className="text-[10px] font-bold text-text-color opacity-50 uppercase tracking-widest mb-4">Primary Prediction</h3>
      
      <div className="flex flex-col gap-6">
        <div>
          <div className="flex items-end gap-3 mb-1">
            <h2 className="text-3xl font-extrabold text-text-color tracking-tight">{fullName}</h2>
            <span className="text-lg font-medium text-text-color opacity-50 mb-1">({abbreviation})</span>
          </div>
          <div className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full border ${riskColor} text-xs font-bold mt-2`}>
            <RiskIcon size={14} />
            {risk} Risk
          </div>
        </div>

        <div>
          <div className="flex justify-between items-end mb-2">
            <span className="text-sm font-semibold text-text-color opacity-80">Confidence Score</span>
            <span className="text-2xl font-bold text-primary">{confPercent}%</span>
          </div>
          <div className="w-full h-3 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
            <motion.div 
              initial={{ width: 0 }}
              animate={{ width: `${confPercent}%` }}
              transition={{ duration: 1, ease: 'easeOut' }}
              className="h-full bg-primary rounded-full"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
