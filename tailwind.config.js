/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        'brand': {
          DEFAULT: '#3ECF8E',
          50: '#E6FAF2',
          100: '#CCF5E5',
          200: '#99EBCB',
          300: '#66E0B1',
          400: '#3ECF8E',
          500: '#3ECF8E',
          600: '#32A672',
          700: '#267D56',
          800: '#1A533A',
          900: '#0D2A1D',
        },
        'scale': {
          0: '#18181b',
          50: '#1f1f23',
          100: '#27272a',
          200: '#2e2e33',
          300: '#3a3a3f',
          400: '#52525b',
          500: '#71717a',
          600: '#a1a1aa',
          700: '#d4d4d8',
          800: '#e4e4e7',
          900: '#f4f4f5',
          1000: '#fafafa',
          1100: '#fcfcfc',
          1200: '#ffffff',
        }
      },
      fontFamily: {
        'mono': ['SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', 'monospace'],
      },
      animation: {
        'slide-in': 'slideIn 0.2s ease-out',
        'fade-in': 'fadeIn 0.15s ease-out',
      },
      keyframes: {
        slideIn: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
      boxShadow: {
        'subtle': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'medium': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'large': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      },
    },
  },
  plugins: [
    require('daisyui')
  ],
  daisyui: {
    themes: [
      {
        light: {
          "primary": "#3ECF8E",
          "primary-content": "#ffffff",
          "secondary": "#7c3aed",
          "secondary-content": "#ffffff",
          "accent": "#f59e0b",
          "accent-content": "#ffffff",
          "neutral": "#71717a",
          "neutral-content": "#ffffff",
          "base-100": "#ffffff",
          "base-200": "#fafafa",
          "base-300": "#f4f4f5",
          "base-content": "#18181b",
          "info": "#3b82f6",
          "info-content": "#ffffff",
          "success": "#10b981",
          "success-content": "#ffffff",
          "warning": "#f59e0b",
          "warning-content": "#ffffff",
          "error": "#ef4444",
          "error-content": "#ffffff",
        },
        dark: {
          "primary": "#3ECF8E",
          "primary-content": "#18181b",
          "secondary": "#a78bfa",
          "secondary-content": "#18181b",
          "accent": "#f59e0b",
          "accent-content": "#18181b",
          "neutral": "#52525b",
          "neutral-content": "#fafafa",
          "base-100": "#18181b",
          "base-200": "#1f1f23",
          "base-300": "#27272a",
          "base-content": "#fafafa",
          "info": "#60a5fa",
          "info-content": "#18181b",
          "success": "#34d399",
          "success-content": "#18181b",
          "warning": "#fbbf24",
          "warning-content": "#18181b",
          "error": "#f87171",
          "error-content": "#18181b",
        },
      },
    ],
  },
}