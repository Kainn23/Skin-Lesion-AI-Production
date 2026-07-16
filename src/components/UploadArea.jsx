import React, { useRef, useState } from 'react';
import { UploadCloud, FileImage, CheckCircle2 } from 'lucide-react';

export default function UploadArea({ onFileSelect, selectedFile, previewUrl, isAnalyzing }) {
  const fileInputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFile = (file) => {
    if (file && (file.type === 'image/jpeg' || file.type === 'image/png')) {
      onFileSelect(file);
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    // Check if it's a dragged URL from the gallery using custom type
    const customUri = e.dataTransfer.getData('application/x-example-url');
    if (customUri) {
      fetch(customUri).then(r => r.blob()).then(blob => {
        const file = new File([blob], "example.jpg", { type: "image/jpeg" });
        handleFile(file);
      });
      return;
    }

    // Fallback: check standard text/uri-list or text/plain
    const textUri = e.dataTransfer.getData('text/uri-list') || e.dataTransfer.getData('text/plain');
    if (textUri && textUri.includes('/api/examples/image/')) {
      fetch(textUri).then(r => r.blob()).then(blob => {
        const file = new File([blob], "example.jpg", { type: "image/jpeg" });
        handleFile(file);
      });
      return;
    }

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="mb-8">
      <div 
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={onDrop}
        onClick={() => !isAnalyzing && fileInputRef.current.click()}
        className={`glass-panel border-2 border-dashed p-8 text-center cursor-pointer transition-all duration-300
          ${isDragging ? 'border-primary bg-primary/5' : 'border-border-color hover:border-primary/50'}
          ${isAnalyzing ? 'opacity-50 pointer-events-none' : ''}
        `}
      >
        <input 
          type="file" 
          className="hidden" 
          ref={fileInputRef} 
          accept=".jpg,.jpeg,.png"
          onChange={(e) => handleFile(e.target.files[0])}
        />
        
        {previewUrl ? (
          <div className="flex flex-col items-center gap-4">
            <div className="w-24 h-24 rounded-2xl overflow-hidden shadow-lg border-2 border-white dark:border-slate-700">
              <img src={previewUrl} alt="Preview" className="w-full h-full object-cover" />
            </div>
            <div className="flex items-center gap-2 text-primary font-semibold">
              <CheckCircle2 size={18} />
              <span>{selectedFile?.name || 'Example Image Loaded'}</span>
            </div>
            <span className="text-xs text-text-color opacity-60">Ready for analysis</span>
          </div>
        ) : (
          <div className="flex flex-col items-center py-6">
            <div className="w-16 h-16 bg-primary/10 text-primary rounded-full flex items-center justify-center mb-4">
              <UploadCloud size={32} />
            </div>
            <h3 className="text-lg font-bold text-text-color mb-2">Upload Dermoscopic Image</h3>
            <p className="text-sm text-text-color opacity-60 max-w-md mx-auto mb-4">
              Drag and drop an image file here, or click to browse. You can also drag an example from the gallery above.
            </p>
            <div className="flex gap-3 text-xs text-text-color opacity-50 font-medium">
              <span className="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded"><FileImage size={12}/> JPG</span>
              <span className="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded"><FileImage size={12}/> JPEG</span>
              <span className="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded"><FileImage size={12}/> PNG</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
