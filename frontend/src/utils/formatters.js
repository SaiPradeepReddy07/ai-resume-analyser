/**
 * Formatting and score tier utilities
 */

export function formatDate(dateString) {
  if (!dateString) return 'N/A';
  try {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    }).format(date);
  } catch {
    return dateString;
  }
}

export function formatPercent(value) {
  if (value === undefined || value === null) return '0%';
  return `${Math.round(value)}%`;
}

export function getScoreTier(score) {
  if (score >= 90) {
    return {
      tier: 'Excellent Match',
      color: '#10b981', // emerald-500
      bgColor: 'bg-emerald-50',
      textColor: 'text-emerald-700',
      borderColor: 'border-emerald-200',
      badgeClass: 'bg-emerald-100 text-emerald-800 border-emerald-300',
      progressClass: 'stroke-emerald-500',
      summary: 'Exceptional alignment across core skills, domain keywords, and role expectations.',
    };
  }
  if (score >= 75) {
    return {
      tier: 'Strong Match',
      color: '#6366f1', // indigo-500
      bgColor: 'bg-indigo-50',
      textColor: 'text-indigo-700',
      borderColor: 'border-indigo-200',
      badgeClass: 'bg-indigo-100 text-indigo-800 border-indigo-300',
      progressClass: 'stroke-indigo-500',
      summary: 'Strong technical baseline covering the majority of essential job requirements.',
    };
  }
  if (score >= 60) {
    return {
      tier: 'Good Match',
      color: '#0284c7', // sky-600
      bgColor: 'bg-sky-50',
      textColor: 'text-sky-700',
      borderColor: 'border-sky-200',
      badgeClass: 'bg-sky-100 text-sky-800 border-sky-300',
      progressClass: 'stroke-sky-500',
      summary: 'Competent candidate profile with a few targeted technical gaps to address.',
    };
  }
  if (score >= 40) {
    return {
      tier: 'Needs Improvement',
      color: '#f59e0b', // amber-500
      bgColor: 'bg-amber-50',
      textColor: 'text-amber-700',
      borderColor: 'border-amber-200',
      badgeClass: 'bg-amber-100 text-amber-800 border-amber-300',
      progressClass: 'stroke-amber-500',
      summary: 'Moderate alignment; several required technologies are missing or terminology differs.',
    };
  }
  return {
    tier: 'Poor Match',
    color: '#ef4444', // red-500
    bgColor: 'bg-red-50',
    textColor: 'text-red-700',
    borderColor: 'border-red-200',
    badgeClass: 'bg-red-100 text-red-800 border-red-300',
    progressClass: 'stroke-red-500',
    summary: 'Low alignment between resume contents and required position specifications.',
  };
}
