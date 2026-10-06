import React, { useEffect, useMemo, useState } from 'react';
import { Link, useLocation, useParams } from 'react-router-dom';
import { AlertCircle, ArrowLeft, ArrowRight, CheckCircle2, Lightbulb, Target } from 'lucide-react';
import ScoreGauge from '../components/ScoreGauge';
import SkillBadge from '../components/SkillBadge';
import { fetchAnalysis } from '../services/analysisService';

export default function AnalysisResultsPage() {
  const { id } = useParams();
  const location = useLocation();
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    const routeAnalysis = location.state?.analysis;

    setError('');
    if (
      routeAnalysis &&
      String(routeAnalysis.id) === id &&
      typeof routeAnalysis.skill_score === 'number'
    ) {
      setAnalysis(routeAnalysis);
      setLoading(false);
      return () => {
        cancelled = true;
      };
    }

    setAnalysis(null);
    setLoading(true);
    fetchAnalysis(id)
      .then((result) => {
        if (!cancelled) setAnalysis(result);
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err?.response?.data?.detail || 'Could not load this analysis. Please try again later.');
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [id, location.state]);

  const categoryBreakdown = useMemo(() => Object.entries(analysis?.category_breakdown || {}), [analysis]);

  if (!analysis) {
    return (
      <div className="rounded-3xl border border-slate-200 bg-white p-8 text-sm text-slate-500 shadow-sm">
        {error ? (
          <div className="flex items-center gap-2 text-rose-700">
            <AlertCircle className="h-4 w-4 shrink-0" />
            {error}
          </div>
        ) : loading ? 'Loading analysis...' : 'Analysis is unavailable.'}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Link to="/history" className="inline-flex items-center gap-2 text-sm font-semibold text-brand-700">
          <ArrowLeft className="h-4 w-4" />
          Back to history
        </Link>
      </div>

      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Analysis results</p>
            <h1 className="mt-2 text-3xl font-black tracking-tight text-slate-900">{analysis.job_title || 'Resume Match'} </h1>
            <p className="mt-2 text-sm text-slate-500">{analysis.company || 'Target Company'}</p>
          </div>
          <div className="rounded-2xl border border-brand-100 bg-brand-50 px-4 py-3 text-sm text-brand-800">
            Created {new Date(analysis.created_at || Date.now()).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
          </div>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <ScoreGauge score={analysis.match_score || 0} />
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-5 flex items-center gap-2">
            <Target className="h-5 w-5 text-brand-600" />
            <h2 className="text-xl font-bold text-slate-900">Match breakdown</h2>
          </div>

          <div className="space-y-4">
            {[
              { label: 'Skill score', value: analysis.skill_score || 0 },
              { label: 'Keyword score', value: analysis.keyword_score || 0 },
              { label: 'Semantic score', value: analysis.semantic_score || 0 },
            ].map((item) => (
              <div key={item.label}>
                <div className="mb-1.5 flex items-center justify-between text-sm font-medium text-slate-600">
                  <span>{item.label}</span>
                  <span>{item.value}%</span>
                </div>
                <div className="h-2.5 overflow-hidden rounded-full bg-slate-100">
                  <div className="h-full rounded-full bg-gradient-to-r from-brand-500 to-indigo-500" style={{ width: `${item.value}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center gap-2">
            <CheckCircle2 className="h-5 w-5 text-emerald-600" />
            <h2 className="text-xl font-bold text-slate-900">Matching skills</h2>
          </div>

          <div className="flex flex-wrap gap-2">
            {(analysis.matching_skills || []).map((skill, index) => (
              <SkillBadge key={`${skill}-${index}`} skill={skill} type="matching" explanation="Detected in resume" />
            ))}
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center gap-2">
            <Lightbulb className="h-5 w-5 text-amber-600" />
            <h2 className="text-xl font-bold text-slate-900">Missing skills</h2>
          </div>

          <div className="flex flex-wrap gap-2">
            {(analysis.missing_skills || []).map((skillItem, index) => (
              <SkillBadge key={`${skillItem.skill}-${index}`} skill={skillItem.skill} type="missing" category={skillItem.category} explanation={skillItem.explanation} />
            ))}
          </div>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-bold text-slate-900">Category overview</h2>
          <div className="mt-5 space-y-4">
            {categoryBreakdown.map(([category, values]) => (
              <div key={category}>
                <div className="mb-1.5 flex items-center justify-between text-sm text-slate-600">
                  <span className="font-medium">{category}</span>
                  <span>{values.resume}/{values.job}</span>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <div className="mb-1 text-[10px] uppercase tracking-[0.14em] text-slate-400">Resume</div>
                    <div className="h-2.5 overflow-hidden rounded-full bg-slate-100">
                      <div className="h-full rounded-full bg-emerald-500" style={{ width: `${Math.min((values.resume / Math.max(values.job, 1)) * 100, 100)}%` }} />
                    </div>
                  </div>
                  <div>
                    <div className="mb-1 text-[10px] uppercase tracking-[0.14em] text-slate-400">Role</div>
                    <div className="h-2.5 overflow-hidden rounded-full bg-slate-100">
                      <div className="h-full rounded-full bg-brand-500" style={{ width: `${Math.min((values.job / Math.max(values.job, 1)) * 100, 100)}%` }} />
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center gap-2">
            <Target className="h-5 w-5 text-brand-600" />
            <h2 className="text-xl font-bold text-slate-900">Recommendations</h2>
          </div>

          <div className="space-y-3">
            {(analysis.recommendations || []).map((recommendation, index) => (
              <div key={`${recommendation.title}-${index}`} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <div className="text-sm font-bold text-slate-900">{recommendation.title}</div>
                <p className="mt-2 text-sm leading-6 text-slate-600">{recommendation.detail}</p>
              </div>
            ))}
          </div>

          <Link to="/analyze" className="mt-6 inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm shadow-brand-500/20 transition hover:bg-brand-700">
            Analyze another role
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </div>
    </div>
  );
}
