import React from 'react';
import { useTheme } from '../context/ThemeContext';
import { Moon, Sun, Activity, ShieldCheck } from 'lucide-react';

export default function Header() {
  const { isDarkMode, toggleTheme } = useTheme();

  return (
    <header className="py-6 border-b border-border-color mb-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-primary-dark dark:text-primary mb-1 flex items-center gap-3">
            <ShieldCheck className="text-primary" size={32} />
            AI Skin Lesion Diagnostic Assistant
          </h1>
          <p className="text-sm text-text-color opacity-80">
            Explainable AI for Dermatological Image Analysis
          </p>
        </div>

        <div className="flex flex-col items-end gap-2">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 px-3 py-1.5 rounded-full text-xs font-semibold">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
              Inference API Online
            </div>
            <button 
              onClick={toggleTheme}
              className="p-2 rounded-full bg-card-bg border border-border-color hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors text-text-color"
              aria-label="Toggle Theme"
            >
              {isDarkMode ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>
          <p className="text-[10px] text-text-color opacity-60 text-right max-w-[280px]">
            This application is intended for educational and research purposes only and is not a substitute for professional medical diagnosis.
          </p>
        </div>
      </div>
    </header>
  );
}
