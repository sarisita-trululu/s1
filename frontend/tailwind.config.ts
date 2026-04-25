import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./hooks/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        forest: "#2F5D50",
        moss: "#A3BFA8",
        sand: "#F5F1E8",
        cream: "#FBF8F1",
        pine: "#1F3C35",
        sage: "#D9E4D7",
        ember: "#9D7357",
      },
      fontFamily: {
        serif: ["var(--font-serif)"],
        sans: ["var(--font-sans)"],
      },
      boxShadow: {
        soft: "0 24px 60px rgba(47, 93, 80, 0.12)",
        card: "0 18px 40px rgba(31, 60, 53, 0.08)",
      },
      backgroundImage: {
        dawn: "linear-gradient(135deg, rgba(245,241,232,1) 0%, rgba(234,244,236,1) 50%, rgba(219,235,226,1) 100%)",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-8px)" },
        },
      },
      animation: {
        float: "float 6s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};

export default config;
