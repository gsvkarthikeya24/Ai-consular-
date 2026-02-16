/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                // Dark Space Theme
                background: '#020617', // Deep Navy
                surface: '#0f172a', // Slate 900
                'surface-light': '#1e293b', // Slate 800

                // Primary Accents (Neon Cyan/Blue)
                primary: {
                    DEFAULT: '#06b6d4', // Cyan 500
                    glow: '#22d3ee', // Cyan 400
                    dim: '#0891b2', // Cyan 600
                    dark: '#164e63', // Cyan 900
                },

                // Secondary Accents (Neon Purple/Magenta)
                secondary: {
                    DEFAULT: '#a855f7', // Purple 500
                    glow: '#c084fc', // Purple 400
                    dim: '#9333ea', // Purple 600
                },

                // Text
                text: {
                    primary: '#f8fafc', // Slate 50
                    secondary: '#cbd5e1', // Slate 300
                    muted: '#64748b', // Slate 500
                }
            },
            fontFamily: {
                sans: ['Outfit', 'Inter', 'system-ui', 'sans-serif'],
                heading: ['Space Grotesk', 'Outfit', 'sans-serif'],
            },
            boxShadow: {
                'neon-blue': '0 0 10px rgba(6, 182, 212, 0.5), 0 0 20px rgba(6, 182, 212, 0.3)',
                'neon-purple': '0 0 10px rgba(168, 85, 247, 0.5), 0 0 20px rgba(168, 85, 247, 0.3)',
                'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.15)',
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'hero-glow': 'conic-gradient(from 180deg at 50% 50%, #164e63 0deg, #020617 180deg, #164e63 360deg)',
            },
            animation: {
                'float': 'float 6s ease-in-out infinite',
                'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'spin-slow': 'spin 12s linear infinite',
            },
            keyframes: {
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-20px)' },
                }
            }
        },
    },
    plugins: [],
}
