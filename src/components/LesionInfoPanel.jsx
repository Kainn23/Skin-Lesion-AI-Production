import React from 'react';
import { AlertCircle, ChevronRight, Stethoscope } from 'lucide-react';
import lesionInfo from '../data/lesion_info.json';

export default function LesionInfoPanel({ prediction }) {
  if (!prediction) return null;

  const infoKey = Object.keys(lesionInfo).find(key => prediction.includes(key));
  const info = infoKey ? lesionInfo[infoKey] : null;

  if (!info) return null;

  return (
    <div className="glass-panel p-6 mb-6 border-t-4 border-t-accent">
      <div className="flex items-center gap-2 mb-4">
        <Stethoscope size={20} className="text-accent" />
        <h3 className="text-lg font-bold text-text-color tracking-tight">Clinical Information</h3>
      </div>
      
      <div className="space-y-5">
        <div>
          <h4 className="text-[10px] font-bold text-text-color opacity-50 uppercase tracking-widest mb-1.5">Description</h4>
          <p className="text-sm text-text-color opacity-90 leading-relaxed">{info.description}</p>
        </div>

        <div>
          <h4 className="text-[10px] font-bold text-text-color opacity-50 uppercase tracking-widest mb-1.5">Characteristics</h4>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {info.clinical_characteristics.map((char, i) => (
              <li key={i} className="flex items-start gap-1.5 text-sm text-text-color opacity-90">
                <ChevronRight size={16} className="text-accent shrink-0 mt-0.5" />
                <span>{char}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-border-color">
          <h4 className="text-[10px] font-bold text-text-color opacity-50 uppercase tracking-widest mb-1.5">Suggested Action</h4>
          <p className="text-sm font-medium text-text-color opacity-90">{info.suggested_action}</p>
        </div>
      </div>
    </div>
  );
}
