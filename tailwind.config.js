/** @type {import('tailwindcss').Config} */
import defaultTheme from "tailwindcss/defaultTheme"

export default {
  content: [
    "./templates/**/*.html", // all Flask templates
    "./static/**/*.js",      // any JS files using Tailwind classes
  ],
  theme: {
    extend: {
      // You can add custom colors, spacing, fonts, etc.
      colors: {
        "custom-blue": "#1E40AF",
        ...defaultTheme.colors
      },
    },
  },
  safelist: [
    // **Colors**
    { pattern: /^text-/ },
    { pattern: /^bg-/ },
    { pattern: /^border-/ },
    { pattern: /^ring-/ },
    
    // **Display & Flex/Grid**
    { pattern: /^flex/ },
    { pattern: /^grid/ },
    { pattern: /^block/ },
    { pattern: /^inline-/ },
    { pattern: /^hidden$/ },

    // **Responsive prefixes**
    { pattern: /^(sm|md|lg|xl|2xl):/ },

    // **Shadows**
    { pattern: /^shadow/ },

    // **Other main utilities you may need**
    { pattern: /^p-/, },   // padding
    { pattern: /^m-/, },   // margin
    { pattern: /^w-/, },   // width
    { pattern: /^h-/, },   // height
    { pattern: /^rounded/ },
    { pattern: /^overflow/ },
    { pattern: /^opacity/ },
    { pattern: /^z-/ },
  ],
  plugins: [],
};