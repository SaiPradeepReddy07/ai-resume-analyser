import React from 'react';
import { Check, AlertCircle, HelpCircle } from 'lucide-react';

export default function SkillBadge({ skill, type = 'matching', category, explanation }) {
  const isMatching = type === 'matching';

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium border transition-all ${
        isMatching
          ? 'bg-emerald-50 text-emerald-800 border-emerald-200 hover:bg-emerald-100/70 shadow-xs'
          : 'bg-amber-50 text-amber-800 border-amber-200 hover:bg-amber-100/70 shadow-xs'
      }`}
      title={explanation || (isMatching ? 'Matched in resume' : 'Missing from resume')}
    >
      {isMatching ? (
        <Check className="w-3.5 h-3.5 text-emerald-600 stroke-[2.5]" />
      ) : (
        <AlertCircle className="w-3.5 h-3.5 text-amber-600 stroke-[2.5]" />
      )}
      <span className="font-semibold">{skill}</span>
      {category && (
        <span
          className={`text-[10px] uppercase font-bold px-1.5 py-0.2 rounded ${
            isMatching ? 'bg-emerald-200/60 text-emerald-900' : 'bg-amber-200/60 text-amber-900'
          }`}
        >
          {category}
        </span>
      )}
    </span>
  );
}
