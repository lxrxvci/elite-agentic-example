/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/widgets/**/*.{js,ts,jsx,tsx,mdx}',
    './src/features/**/*.{js,ts,jsx,tsx,mdx}',
    './src/entities/**/*.{js,ts,jsx,tsx,mdx}',
    './src/shared/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        elite: {
          // Global palette
          black: '#000000',
          white: '#ffffff',
          'gray-100': '#f3f4f6',
          'gray-500': '#6b7280',
          'gray-900': '#111827',
          'blue-600': '#2563eb',
          'red-600': '#dc2626',
          // Semantic
          'text-primary': '#111827',
          'text-secondary': '#6b7280',
          background: '#ffffff',
          surface: '#f3f4f6',
          interactive: '#2563eb',
          danger: '#dc2626',
          success: '#16a34a',
          warning: '#d97706',
          border: '#e5e7eb',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        sm: '0.875rem',
        base: '1rem',
        lg: '1.125rem',
        xl: '1.25rem',
        '2xl': '1.5rem',
      },
      borderRadius: {
        sm: '0.25rem',
        md: '0.375rem',
        lg: '0.5rem',
      },
      spacing: {
        '01': '0.25rem',
        '02': '0.5rem',
        '03': '0.75rem',
        '04': '1rem',
        '05': '1.25rem',
        '06': '1.5rem',
        '08': '2rem',
        '10': '2.5rem',
        '12': '3rem',
      },
      boxShadow: {
        card: '0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)',
        modal: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
      },
    },
  },
  plugins: [],
}
