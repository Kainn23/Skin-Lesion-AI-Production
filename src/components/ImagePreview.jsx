import React from 'react';
import { Image as ImageIcon } from 'lucide-react';

export default function ImagePreview({ imageUrl }) {
  if (!imageUrl) return null;

  return (
    <div className="glass-panel p-6 mb-6">
      <h3 className="text-[10px] font-bold text-text-color opacity-50 uppercase tracking-widest mb-4">Original Image</h3>
      
      <div className="relative w-full aspect-square rounded-2xl bg-slate-100 dark:bg-slate-900 border border-border-color shadow-inner overflow-hidden">
        <img 
          src={imageUrl} 
          alt="Selected skin lesion" 
          className="absolute inset-0 w-full h-full object-cover"
        />
      </div>
    </div>
  );
}
