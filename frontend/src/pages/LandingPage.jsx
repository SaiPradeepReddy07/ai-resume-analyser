import React from 'react';
import { ArrowRight, BarChart3, BrainCircuit, FileText, ShieldCheck, Sparkles, Target } from 'lucide-react';
import { Link } from 'react-router-dom';

const featureCards = [
  {
    title: 'AI-powered Matching',
    description: 'Compare resumes against job requirements using semantic relevance, keyword alignment, and skills coverage.',
    icon: BrainCircuit,
  },
  {
    title: 'Actionable Insights',
    description: 'See the exact gaps, missing tools, and recommended improvements to strengthen your application.',
    icon: Target,
  },
  {
    title: 'Transparent Scoring',
    description: 'Explore match percentages by category and understand why your profile is a strong or weak fit.',
    icon: BarChart3,
  },
];

const metrics = [
  { label: 'Analysis scope', value: '1 : 1', detail: 'A resume compared with a specific role' },
  { label: 'Useful feedback', value: 'Role-specific', detail: 'Matched and missing skills' },
  { label: 'Score dimensions', value: '3', detail: 'Skills, keywords, and semantic fit' },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(14,140,233,0.18),_transparent_35%),radial-gradient(circle_at_bottom_right,_rgba(99,102,241,0.15),_transparent_35%)]" />
        <div className="relative mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8 lg:py-24">
          <div className="grid items-center gap-12 lg:grid-cols-[1.1fr_0.9fr]">
            <div>
              <div className="inline-flex items-center gap-2 rounded-full border border-brand-200 bg-brand-50 px-3 py-1.5 text-xs font-semibold uppercase tracking-[0.12em] text-brand-700">
                <Sparkles className="h-3.5 w-3.5" />
                Intelligent career optimization
              </div>
              <h1 className="mt-6 max-w-xl text-4xl font-black tracking-tight text-slate-900 sm:text-5xl lg:text-6xl">
                Turn your resume into a stronger job match.
              </h1>
              <p className="mt-6 max-w-xl text-lg leading-8 text-slate-600">
                AI Resume Analyzer helps job seekers compare their resume against role requirements, identify missing skills, and improve interview readiness with clear, trusted scoring.
              </p>
              <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                <Link
                  to="/register"
                  className="inline-flex items-center justify-center gap-2 rounded-xl bg-brand-600 px-6 py-3.5 text-base font-semibold text-white shadow-sm shadow-brand-500/20 transition hover:bg-brand-700"
                >
                  Start free
                  <ArrowRight className="h-4 w-4" />
                </Link>
                <Link
                  to="/login"
                  className="inline-flex items-center justify-center rounded-xl border border-slate-300 bg-white px-6 py-3.5 text-base font-semibold text-slate-700 transition hover:border-slate-400 hover:bg-slate-50"
                >
                  Sign in
                </Link>
              </div>
              <div className="mt-10 grid max-w-lg gap-3 sm:grid-cols-3">
                {metrics.map((metric) => (
                  <div key={metric.label} className="rounded-2xl border border-slate-200 bg-white/80 p-4 shadow-sm backdrop-blur-sm">
                    <div className="text-2xl font-extrabold tracking-tight text-slate-900">{metric.value}</div>
                    <div className="mt-1 text-xs font-medium uppercase tracking-[0.12em] text-slate-500">{metric.label}</div>
                    <div className="mt-2 text-[11px] text-slate-400">{metric.detail}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="relative">
              <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-xl shadow-slate-200/70">
              <div className="mb-3 text-[11px] font-semibold uppercase tracking-[0.14em] text-slate-400">
                Example analysis preview
              </div>
              <div className="rounded-2xl bg-slate-900 p-5 text-white">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xs uppercase tracking-[0.2em] text-slate-300">Role fit</p>
                      <div className="mt-3 text-5xl font-black text-white">82%</div>
                    </div>
                    <div className="rounded-2xl bg-emerald-500/15 p-3 text-emerald-300">
                      <ShieldCheck className="h-8 w-8" />
                    </div>
                  </div>
                  <div className="mt-6 rounded-2xl bg-white/5 p-4">
                    <div className="mb-3 flex items-center justify-between text-sm text-slate-200">
                      <span>Skill coverage</span>
                      <span>85%</span>
                    </div>
                    <div className="h-2 w-full overflow-hidden rounded-full bg-white/10">
                      <div className="h-full w-[85%] rounded-full bg-gradient-to-r from-brand-400 to-emerald-400" />
                    </div>
                  </div>
                </div>

                <div className="mt-5 grid gap-3 sm:grid-cols-2">
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <div className="flex items-center gap-2 text-sm font-semibold text-slate-700">
                      <FileText className="h-4 w-4 text-brand-600" />
                      Matching skills
                    </div>
                    <div className="mt-3 flex flex-wrap gap-2 text-[11px]">
                      {['Python', 'FastAPI', 'React', 'SQL'].map((skill) => (
                        <span key={skill} className="rounded-full bg-emerald-50 px-2 py-1 font-medium text-emerald-700">{skill}</span>
                      ))}
                    </div>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <div className="flex items-center gap-2 text-sm font-semibold text-slate-700">
                      <Sparkles className="h-4 w-4 text-amber-500" />
                      Opportunities
                    </div>
                    <div className="mt-3 space-y-2 text-[11px] text-slate-600">
                      <div className="flex items-center justify-between rounded-lg bg-white px-2 py-1.5">
                        <span>Docker</span>
                        <span className="font-semibold text-amber-600">Missing</span>
                      </div>
                      <div className="flex items-center justify-between rounded-lg bg-white px-2 py-1.5">
                        <span>Kubernetes</span>
                        <span className="font-semibold text-amber-600">Missing</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 pb-20 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.16em] text-brand-700">Why it works</p>
          <h2 className="mt-3 text-3xl font-black tracking-tight text-slate-900 sm:text-4xl">Built for transparent, practical career growth.</h2>
        </div>

        <div className="mt-10 grid gap-6 md:grid-cols-3">
          {featureCards.map(({ title, description, icon: Icon }) => (
            <div key={title} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-50 text-brand-600">
                <Icon className="h-6 w-6" />
              </div>
              <h3 className="mt-5 text-xl font-bold text-slate-900">{title}</h3>
              <p className="mt-3 text-sm leading-6 text-slate-600">{description}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
