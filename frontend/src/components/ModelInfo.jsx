import React from 'react';
import { Cpu, Database, Activity, GitBranch } from 'lucide-react';

export default function ModelInfo() {
  return (
    <div className="glass-panel p-6 mb-8">
      <h3 className="text-[10px] font-bold text-text-color opacity-50 uppercase tracking-widest mb-4">Model Details</h3>
      
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="flex flex-col gap-1">
          <span className="flex items-center gap-1.5 text-xs text-text-color opacity-60 font-semibold">
            <Cpu size={14} /> Architecture
          </span>
          <span className="text-sm font-bold text-text-color opacity-90">EfficientNet-B0</span>
        </div>
        
        <div className="flex flex-col gap-1">
          <span className="flex items-center gap-1.5 text-xs text-text-color opacity-60 font-semibold">
            <Database size={14} /> Training Data
          </span>
          <span className="text-sm font-bold text-text-color opacity-90">HAM10000</span>
        </div>

        <div className="flex flex-col gap-1">
          <span className="flex items-center gap-1.5 text-xs text-text-color opacity-60 font-semibold">
            <Activity size={14} /> Val Accuracy
          </span>
          <span className="text-sm font-bold text-primary">87.8%</span>
        </div>

        <div className="flex flex-col gap-1">
          <span className="flex items-center gap-1.5 text-xs text-text-color opacity-60 font-semibold">
            <Activity size={14} /> Macro F1
          </span>
          <span className="text-sm font-bold text-primary">0.806</span>
        </div>

        <div className="flex flex-col gap-1">
          <span className="flex items-center gap-1.5 text-xs text-text-color opacity-60 font-semibold">
            <GitBranch size={14} /> Version
          </span>
          <span className="text-sm font-bold text-text-color opacity-90">v1.0.0</span>
        </div>
      </div>
    </div>
  );
}
