"use client"

import React from 'react';
import { useLanguage } from '@/contexts/LanguageContext';

const LanguageSwitcher = () => {
  const { language, toggleLanguage } = useLanguage();

  return (
    <button
      onClick={toggleLanguage}
      className="px-3 py-1.5 rounded-lg border border-border bg-background hover:bg-accent transition-colors flex items-center gap-2"
      title={language === 'zh' ? '切换到英文' : 'Switch to Chinese'}
    >
      <span className="text-sm font-medium">
        {language === 'zh' ? '🇨🇳 中文' : '🇺🇸 English'}
      </span>
    </button>
  );
};

export default LanguageSwitcher;
