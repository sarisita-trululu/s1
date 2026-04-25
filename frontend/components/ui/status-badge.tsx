import type { ExperienceStatus } from "@/lib/types";
import { cn, formatStatus } from "@/lib/utils";

type StatusBadgeProps = {
  status: ExperienceStatus;
};

const styles: Record<ExperienceStatus, string> = {
  proximamente: "bg-sand text-forest",
  cupos_abiertos: "bg-moss/30 text-pine",
  finalizada: "bg-pine/10 text-pine/70",
};

export function StatusBadge({ status }: StatusBadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em]",
        styles[status],
      )}
    >
      {formatStatus(status)}
    </span>
  );
}
