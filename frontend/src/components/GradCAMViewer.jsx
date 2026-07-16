import React, { useState } from 'react';
import { Layers, Download } from 'lucide-react';

export default function GradCAMViewer({ originalImage, gradcamImage }) {
  const [opacity, setOpacity] = useState(50);

  if (!originalImage && !gradcamImage) return null;

  return (
    <div className="glass-panel p-6 mb-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-[10px] font-bold text-text-color opacity-50 uppercase tracking-widest">Explainability (GradCAM)</h3>
        {gradcamImage && (
          <a 
            href={gradcamImage} 
            download="gradcam_heatmap.png"
            className="flex items-center gap-1.5 text-xs font-semibold text-secondary hover:text-secondary/80 transition-colors"
          >
            <Download size={14} /> Download
          </a>
        )}
      </div>
      
      <p className="text-xs text-text-color opacity-70 mb-4">
        Highlighted regions represent areas of the image that contributed most strongly to the model prediction.
      </p>

      <div className="relative w-full aspect-square rounded-2xl bg-slate-100 dark:bg-slate-900 overflow-hidden mb-4 border border-border-color shadow-inner">
        {originalImage && (
          <img 
            src={originalImage} 
            alt="Original Lesion" 
            className="absolute inset-0 w-full h-full object-cover"
          />
        )}
        
        {gradcamImage && (
          <img 
            src={gradcamImage} 
            alt="GradCAM Overlay" 
            style={{ opacity: opacity / 100 }}
            className="absolute inset-0 w-full h-full object-cover mix-blend-screen transition-opacity"
          />
        )}
        
        {!originalImage && !gradcamImage && (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-text-color opacity-50">
            <Layers size={32} className="mb-2 opacity-30" />
            <span className="text-sm font-medium">Waiting for analysis...</span>
          </div>
        )}
      </div>

      {gradcamImage && (
        <div className="flex items-center gap-3">
          <span className="text-xs font-semibold text-text-color opacity-50 w-24">Original</span>
          <input 
            type="range" 
            min="0" 
            max="100" 
            value={opacity} 
            onChange={(e) => setOpacity(parseInt(e.target.value))}
            className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-secondary"
          />
          <span className="text-xs font-semibold text-text-color opacity-50 w-24 text-right">Heatmap</span>
        </div>
      )}
    </div>
  );
}
