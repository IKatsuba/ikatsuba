module.exports = {
  prefix: '',
  purge: {
    enabled: process.argv.some((str) => str.endsWith(':production')),
    content: ['apps/readme/src/**/*.{html,ts}'],
  },
  darkMode: 'class',
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [require('@tailwindcss/typography')],
};
