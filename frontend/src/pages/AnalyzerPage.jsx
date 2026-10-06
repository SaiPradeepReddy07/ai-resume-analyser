import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AlertCircle, ArrowRight, Sparkles } from 'lucide-react';
import FileUploader from '../components/FileUploader';
import { submitAnalysis } from '../services/analysisService';

export default function AnalyzerPage() {
  const navigate = useNavigate();
  const [resumeFile, setResumeFile] = useState(null);
  const [jobTitle, setJobTitle] = useState('Junior Python Developer');
  const [company, setCompany] = useState('Tech Innovations Inc.');
  const [jobDescription, setJobDescription] = useState(
    'We are seeking a Junior Python Developer proficient with Python, FastAPI, PostgreSQL, Git, and Docker. Experience with REST APIs and React is a strong plus.'
  );
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');

    if (!resumeFile) {
      setError('Please upload a PDF resume before running the analysis.');
      return;
    }

    if (!jobTitle.trim() || !jobDescription.trim()) {
      setError('Please provide both a job title and job description.');
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', resumeFile);
      formData.append('job_title', jobTitle.trim());
      formData.append('company', company.trim() || 'Target Company');
      formData.append('job_description', jobDescription.trim());

      const result = await submitAnalysis(formData);

      navigate(`/analysis/${result.id}`, { state: { analysis: result } });
    } catch (err) {
      setError(err?.response?.data?.detail || err.message || 'We could not complete the analysis. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.14em] text-brand-700">AI resume matcher</p>
        <h1 className="mt-2 text-3xl font-black tracking-tight text-slate-900">Analyze a role fit</h1>
      </div>

      <form onSubmit={handleSubmit} className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-5">
            <h2 className="text-xl font-bold text-slate-900">Resume upload</h2>
          </div>
          <FileUploader
            file={resumeFile}
            onFileSelect={setResumeFile}
            onRemove={() => setResumeFile(null)}
          />
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-5 flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-brand-600" />
            <h2 className="text-xl font-bold text-slate-900">Job details</h2>
          </div>

          <div className="space-y-5">
            <div>
              <label htmlFor="jobTitle" className="mb-2 block text-sm font-medium text-slate-700">Job title</label>
              <input
                id="jobTitle"
                value={jobTitle}
                onChange={(event) => setJobTitle(event.target.value)}
                className="w-full rounded-xl border border-slate-300 bg-slate-50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-brand-400 focus:bg-white focus:ring-4 focus:ring-brand-50"
              />
            </div>

            <div>
              <label htmlFor="company" className="mb-2 block text-sm font-medium text-slate-700">Company</label>
              <input
                id="company"
                value={company}
                onChange={(event) => setCompany(event.target.value)}
                className="w-full rounded-xl border border-slate-300 bg-slate-50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-brand-400 focus:bg-white focus:ring-4 focus:ring-brand-50"
              />
            </div>

            <div>
              <label htmlFor="jobDescription" className="mb-2 block text-sm font-medium text-slate-700">Job description</label>
              <textarea
                id="jobDescription"
                value={jobDescription}
                onChange={(event) => setJobDescription(event.target.value)}
                rows={10}
                className="w-full rounded-xl border border-slate-300 bg-slate-50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-brand-400 focus:bg-white focus:ring-4 focus:ring-brand-50"
              />
            </div>
          </div>

          {error && (
            <div className="mt-5 flex items-start gap-2 rounded-xl border border-rose-200 bg-rose-50 px-3 py-2.5 text-sm text-rose-700">
              <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="mt-5 inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <ArrowRight className="h-4 w-4" />
            {loading ? 'Analyzing resume...' : 'Analyze match'}
          </button>
        </div>
      </form>
    </div>
  );
}
