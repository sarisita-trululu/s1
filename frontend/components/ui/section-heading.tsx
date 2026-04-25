import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

type SectionHeadingProps = {
  eyebrow?: string;
  title: string;
  description?: ReactNode;
  align?: "left" | "center";
  className?: string;
};

export function SectionHeading({
  eyebrow,
  title,
  description,
  align = "left",
  className,
}: SectionHeadingProps) {
  return (
    <div className={cn(align === "center" && "mx-auto text-center", className)}>
      {eyebrow ? (
        <p className="mb-3 text-xs font-semibold uppercase tracking-[0.35em] text-forest/70">
          {eyebrow}
        </p>
      ) : null}
      <h2 className="font-serif text-4xl leading-tight text-pine md:text-5xl">
        {title}
      </h2>
      {description ? (
        <div className="mt-4 max-w-2xl text-base leading-7 text-pine/75 md:text-lg">
          {description}
        </div>
      ) : null}
    </div>
  );
}
