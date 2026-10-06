import React, { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { Search, SlidersHorizontal } from 'lucide-react';
import { fetchHistory } from '../services/analysisService';
import { formatDate } from '../utils/formatters';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState('date_desc');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadHistory() {
      try {
        const data = await fetchHistory();
        setHistory(data);
      } catch (err) {
        setError(err?.response?.data?.detail || 'Could not load analysis history. Please try again later.');
      } finally {
        setLoading(false);
      }
    }

    loadHistory();
  }, []);

  const filtered = useMemo(() => {
    const query = search.trim().toLowerCase();
    const next = [...history].filter((item) => {
      if (!query) return true;
      const haystack = `${item.job_title || ''} ${item.company || ''}`.toLowerCase();
      return haystack.includes(query);
    });

    next.sort((a, b) => {
      if (sortBy === 'score_desc') return (b.match_score || 0) - (a.match_score || 0);
      if (sortBy === 'score_asc') return (a.match_score || 0) - (b.match_score || 0);
      if (sortBy === 'date_asc') return new Date(a.created_at || 0) - new Date(b.created_at || 0);
      return new Date(b.created_at || 0) - new Date(a.created_at || 0);
    });

    return next;
  }, [history, search, sortBy]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.14em] text-brand-700">History</p>
          <h1 className="mt-2 text-3xl font-black tracking-tight text-slate-900">Previous analyses</h1>
        </div>
        <Link to="/analyze" className="inline-flex items-center rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm shadow-brand-500/20 transition hover:bg-brand-700">
          Run new match
        </Link>
      </div>

      <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div className="relative w-full md:max-w-md">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search by job title or company"
              className="w-full rounded-xl border border-slate-300 bg-slate-50 py-2.5 pl-10 pr-3 text-sm text-slate-900 outline-none transition focus:border-brand-400 focus:bg-white focus:ring-4 focus:ring-brand-50"
            />
          </div>

          <div className="flex items-center gap-2">
            <SlidersHorizontal className="h-4 w-4 text-slate-500" />
            <select
              value={sortBy}
              onChange={(event) => setSortBy(event.target.value)}
              className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-2.5 text-sm text-slate-700 outline-none transition focus:border-brand-400 focus:bg-white focus:ring-4 focus:ring-brand-50"
            >
              <option value="date_desc">Newest first</option>
              <option value="date_asc">Oldest first</option>
              <option value="score_desc">Highest score</option>
              <option value="score_asc">Lowest score</option>
            </select>
          </div>
        </div>
      </div>

      <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
        {error ? (
          <div className="p-8 text-center text-sm text-rose-700">{error}</div>
        ) : loading ? (
          <div className="p-8 text-center text-sm text-slate-500">Loading analysis history...</div>
        ) : filtered.length === 0 ? (
          <div className="p-8 text-center text-sm text-slate-500">No analyses match your current filter.</div>
        ) : (
          <div className="divide-y divide-slate-200">
            {filtered.map((item) => (
              <Link
                key={item.id}
                to={`/analysis/${item.id}`}
                state={{ analysis: item }}
                className="flex flex-col gap-3 p-4 transition hover:bg-slate-50 md:flex-row md:items-center md:justify-between"
              >
                <div>
                  <div className="text-base font-bold text-slate-900">{item.job_title || 'Resume Analysis'}</div>
                  <div className="text-sm text-slate-500">{item.company || 'Target Company'}</div>
                </div>
                <div className="flex items-center gap-4 text-sm">
                  <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-bold text-emerald-700">{item.match_score || 0}%</span>
                  <span className="text-slate-500">{formatDate(item.created_at)}</span>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
