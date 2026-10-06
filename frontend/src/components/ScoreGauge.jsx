import React from 'react';
import { getScoreTier } from '../utils/formatters';

export default function ScoreGauge({ score = 0, size = 180, strokeWidth = 14, showTier = true }) {
  const boundedScore = Math.max(0, Math.min(100, Math.round(score)));
  const tierInfo = getScoreTier(boundedScore);

  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  // Offset formula for stroke-dashoffset: 0% is full offset, 100% is 0 offset
  const strokeDashoffset = circumference - (boundedScore / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center text-center">
      <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
        <svg
          width={size}
          height={size}
          className="transform -rotate-90 origin-center transition-all duration-700 ease-out"
        >
          {/* Background Track Circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#f1f5f9"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Animated Progress Circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={tierInfo.color}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            style={{
              transition: 'stroke-dashoffset 1s ease-out, stroke 0.5s ease',
            }}
          />
        </svg>

        {/* Inner Score Number */}
        <div className="absolute flex flex-col items-center justify-center">
          <span className="text-4xl font-extrabold tracking-tight text-slate-900">
            {boundedScore}%
          </span>
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 mt-0.5">
            Match Score
          </span>
        </div>
      </div>

      {showTier && (
        <div className="mt-3 flex flex-col items-center">
          <span
            className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold border tracking-wide ${tierInfo.badgeClass}`}
          >
            {tierInfo.tier}
          </span>
          <p className="text-xs text-slate-500 max-w-[260px] text-center mt-2 leading-relaxed">
            {tierInfo.summary}
          </p>
        </div>
      )}
    </div>
  );
}
