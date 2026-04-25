import type { ReactNode } from "react";

type StatCardProps = {
  label: string;
  value: string | number;
  icon: ReactNode;
  tone?: "default" | "accent";
};

export function StatCard({
  label,
  value,
  icon,
  tone = "default",
}: StatCardProps) {
  return (
    <article
      className={`rounded-[2rem] p-6 shadow-card ${
        tone === "accent" ? "bg-pine text-white" : "bg-white/80 text-pine"
      }`}
    >
      <div className="flex items-center justify-between">
        <div className="text-sm font-medium">{label}</div>
        <div className={tone === "accent" ? "text-white/70" : "text-forest/70"}>{icon}</div>
      </div>
      <div className="mt-6 font-serif text-5xl">{value}</div>
    </article>
  );
}
