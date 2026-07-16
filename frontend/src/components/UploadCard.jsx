import React, { useCallback } from 'react';

export default function UploadCard({ onImageSelect }) {
  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file) => {
    if (!file.type.startsWith('image/')) return;
    
    const previewUrl = URL.createObjectURL(file);
    onImageSelect({ file, previewUrl });
  };

  return (
    <div className="w-full">
      <label 
        className="block border-2 border-dashed border-brand-500 bg-brand-50 rounded-2xl p-12 text-center transition-all hover:bg-brand-100 hover:border-brand-600 cursor-pointer"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <input 
          type="file" 
          accept="image/*" 
          className="hidden" 
          onChange={handleChange}
        />
        <svg className="mx-auto h-16 w-16 text-brand-500 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
        </svg>
        <h3 className="text-xl font-semibold text-slate-900 mb-1">Upload Dermoscopic Image</h3>
        <p className="text-slate-500">Drag and drop or click to browse</p>
      </label>
    </div>
  );
}
