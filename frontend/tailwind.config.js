/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: {
          DEFAULT: '#0e1014',
          subtle: '#14171d',
          surface: '#1a1d24',
          elevated: '#222630',
        },
        border: {
          subtle: '#252932',
          DEFAULT: '#313642',
          strong: '#454c5c',
        },
        foreground: {
          DEFAULT: '#f0f2f5',
          secondary: '#a6adb9',
          muted: '#6f7682',
        },
        technical: {
          green: '#22c55e',
          amber: '#f59e0b',
          red: '#ef4444',
          blue: '#3b82f6',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'SFMono-Regular', 'Consolas', 'monospace'],
      }
    },
  },
  plugins: [],
}
