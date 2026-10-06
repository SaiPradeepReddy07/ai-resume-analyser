import React, { useEffect, useMemo, useState } from 'react';
import { Activity, ArrowUpRight, FileText, Sparkles, TrendingUp } from 'lucide-react';
import { Link } from 'react-router-dom';
import { LineChart, Line, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid } from 'recharts';
import StatCard from '../components/StatCard';
import { fetchDashboardStats } from '../services/analysisService';
import { formatDate } from '../utils/formatters';

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadDashboard() {
      try {
        const data = await fetchDashboardStats();
        setStats(data);
      } catch (err) {
        setError(err?.response?.data?.detail || 'Could not load dashboard data. Please try again later.');
      }
    }

    loadDashboard();
  }, []);

  const trendData = useMemo(() => {
    return stats?.score_history?.map((item) => ({
      ...item,
      label: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    })) || [];
  }, [stats]);

  if (!stats) {
    return (
      <div className="rounded-3xl border border-slate-200 bg-white p-8 text-sm text-slate-500 shadow-sm">
        {error || 'Loading dashboard insights...'}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.14em] text-brand-700">Overview</p>
          <h1 className="mt-2 text-3xl font-black tracking-tight text-slate-900">Dashboard</h1>
        </div>
        <Link
          to="/analyze"
          className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm shadow-brand-500/20 transition hover:bg-brand-700"
        >
          <Sparkles className="h-4 w-4" />
          New Analysis
        </Link>
      </div>

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Total analyses" value={stats.total_analyses} subtitle="Across all roles" icon={FileText} color="brand" />
        <StatCard title="Average score" value={`${stats.average_score}%`} subtitle="Overall fit" icon={TrendingUp} color="indigo" />
        <StatCard title="Highest score" value={`${stats.highest_score}%`} subtitle="Best match" icon={Activity} color="emerald" />
        <StatCard title="Lowest score" value={`${stats.lowest_score}%`} subtitle="Improvement area" icon={ArrowUpRight} color="amber" />
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-5 flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Score trend</p>
              <h2 className="mt-1 text-xl font-bold text-slate-900">Match performance</h2>
            </div>
          </div>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="label" tickLine={false} axisLine={false} fontSize={12} stroke="#64748b" />
                <YAxis domain={[0, 100]} tickLine={false} axisLine={false} fontSize={12} stroke="#64748b" />
                <Tooltip
                  formatter={(value) => [`${value}%`, 'Score']}
                  labelFormatter={(label) => `${label}`}
                  contentStyle={{ borderRadius: 12, border: '1px solid #e2e8f0' }}
                />
                <Line type="monotone" dataKey="score" stroke="#0e8ce9" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Skills to improve</p>
          <h2 className="mt-1 text-xl font-bold text-slate-900">Common gaps</h2>
          <div className="mt-5 space-y-3">
            {stats.most_frequently_missing_skills?.map((skill) => (
              <div key={skill.skill} className="rounded-2xl border border-slate-200 bg-slate-50 p-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-semibold text-slate-800">{skill.skill}</span>
                  <span className="rounded-full bg-amber-100 px-2 py-0.5 text-[10px] font-bold uppercase tracking-[0.12em] text-amber-700">
                    {skill.count}x
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Recent activity</p>
            <h2 className="mt-1 text-xl font-bold text-slate-900">Latest analyses</h2>
          </div>
        </div>

        <div className="space-y-3">
          {stats.recent_analyses?.map((item) => (
            <Link
              key={item.id}
              to={`/analysis/${item.id}`}
              state={{ analysis: item }}
              className="flex flex-col gap-2 rounded-2xl border border-slate-200 bg-slate-50 p-4 transition hover:border-brand-200 hover:bg-brand-50/60 sm:flex-row sm:items-center sm:justify-between"
            >
              <div>
                <div className="text-base font-semibold text-slate-900">{item.job_title}</div>
                <div className="text-sm text-slate-500">{item.company}</div>
              </div>
              <div className="flex items-center gap-4">
                <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-bold text-emerald-700">{item.match_score}%</span>
                <span className="text-xs text-slate-400">{formatDate(item.created_at)}</span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
