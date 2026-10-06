import React, { useState, useRef } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertCircle, X, Sparkles } from 'lucide-react';

export default function FileUploader({ file, onFileSelect, onRemove, onUseSample }) {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState(null);
  const inputRef = useRef(null);

  const MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024; // 5 MB

  const validateAndSet = (selectedFile) => {
    setError(null);
    if (!selectedFile) return;

    if (!selectedFile.name.toLowerCase().endsWith('.pdf')) {
      setError('Please upload a PDF document (.pdf only).');
      return;
    }

    if (selectedFile.size > MAX_FILE_SIZE_BYTES) {
      setError('File size exceeds the 5MB maximum limit.');
      return;
    }

    onFileSelect(selectedFile);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndSet(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSet(e.target.files[0]);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  return (
    <div className="w-full">
      <input
        ref={inputRef}
        type="file"
        accept="application/pdf,.pdf"
        className="hidden"
        onChange={handleChange}
      />

      {!file ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-200 ${
            isDragging
              ? 'border-brand-500 bg-brand-50/70 scale-[1.01]'
              : 'border-slate-300 hover:border-brand-400 bg-slate-50/60 hover:bg-white'
          }`}
        >
          <div className="w-14 h-14 mx-auto mb-4 rounded-2xl bg-brand-100 text-brand-600 flex items-center justify-center shadow-xs">
            <UploadCloud className="w-7 h-7" />
          </div>

          <h4 className="text-base font-bold text-slate-800">
            Upload your resume PDF
          </h4>
          <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
            Drag and drop your file here, or{' '}
            <span className="text-brand-600 font-semibold underline decoration-brand-300 underline-offset-2">
              browse files
            </span>
          </p>

          <div className="mt-4 flex items-center justify-center gap-3 text-[11px] text-slate-400 font-medium">
            <span>PDF format only</span>
            <span>•</span>
            <span>Max size 5 MB</span>
          </div>

          {onUseSample && (
            <div className="mt-6 pt-5 border-t border-slate-200/80">
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  onUseSample();
                }}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-brand-700 bg-brand-50 hover:bg-brand-100 border border-brand-200 transition-colors"
              >
                <Sparkles className="w-3.5 h-3.5 text-brand-600" />
                Use Sample Junior Python Resume
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="border border-slate-200 bg-white rounded-2xl p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3.5 overflow-hidden">
              <div className="w-11 h-11 rounded-xl bg-brand-50 text-brand-600 flex items-center justify-center shrink-0 border border-brand-100">
                <FileText className="w-6 h-6" />
              </div>
              <div className="overflow-hidden">
                <p className="text-sm font-bold text-slate-800 truncate">
                  {file.name}
                </p>
                <p className="text-xs text-slate-400 flex items-center gap-1 mt-0.5">
                  <span>{formatFileSize(file.size)}</span>
                  <span>•</span>
                  <span className="text-emerald-600 flex items-center gap-0.5 font-medium">
                    <CheckCircle2 className="w-3 h-3" /> Ready for analysis
                  </span>
                </p>
              </div>
            </div>

            <button
              type="button"
              onClick={onRemove}
              className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
              title="Remove file"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}

      {error && (
        <div className="mt-2.5 flex items-center gap-2 p-2.5 rounded-xl bg-rose-50 text-rose-700 text-xs font-medium border border-rose-200">
          <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}
