import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Sparkles,
  History,
  User,
  ShieldCheck,
  FileCheck2,
} from 'lucide-react';

export default function Sidebar() {
  const links = [
    { name: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
    { name: 'Analyze Resume', to: '/analyze', icon: Sparkles, highlight: true },
    { name: 'My Analyses', to: '/history', icon: History },
    { name: 'My Profile', to: '/profile', icon: User },
  ];

  return (
    <aside className="w-64 bg-white border-r border-slate-200 hidden lg:flex flex-col justify-between p-4 shrink-0">
      <div>
        <div className="px-3 py-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
          Navigation
        </div>
        <nav className="mt-2 space-y-1">
          {links.map((link) => {
            const Icon = link.icon;
            return (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-brand-50 text-brand-700 font-semibold shadow-xs'
                      : link.highlight
                      ? 'text-brand-600 hover:bg-brand-50/50'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'
                  }`
                }
              >
                <Icon className="w-4 h-4 shrink-0" />
                {link.name}
                {link.highlight && (
                  <span className="ml-auto text-[10px] uppercase font-bold bg-brand-100 text-brand-700 px-1.5 py-0.5 rounded-full">
                    New
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Helpful ATS Tip Card in Sidebar */}
      <div className="bg-gradient-to-br from-slate-900 to-indigo-950 text-white p-4 rounded-2xl shadow-sm">
        <div className="flex items-center gap-2 text-brand-300 text-xs font-semibold uppercase tracking-wider mb-1.5">
          <ShieldCheck className="w-4 h-4 text-brand-400" />
          Pro Tip
        </div>
        <p className="text-xs text-slate-300 leading-relaxed mb-3">
          Mirror standard industry keywords accurately to clear automated Applicant Tracking System filters.
        </p>
        <div className="flex items-center gap-1.5 text-[11px] font-medium text-brand-200">
          <FileCheck2 className="w-3.5 h-3.5" />
          <span>Transparent Scoring</span>
        </div>
      </div>
    </aside>
  );
}
