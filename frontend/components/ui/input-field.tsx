import type { InputHTMLAttributes, TextareaHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

type InputFieldProps = {
  label: string;
  error?: string;
  hint?: string;
} & InputHTMLAttributes<HTMLInputElement>;

export function InputField({ label, error, hint, className, ...props }: InputFieldProps) {
  return (
    <label className="block space-y-2">
      <span className="text-sm font-medium text-pine">{label}</span>
      <input
        className={cn(
          "w-full rounded-2xl border border-forest/15 bg-white/90 px-4 py-3 text-sm text-pine outline-none transition placeholder:text-pine/35 focus:border-forest focus:ring-2 focus:ring-forest/10",
          className,
        )}
        {...props}
      />
      {hint ? <span className="text-xs text-pine/55">{hint}</span> : null}
      {error ? <span className="text-xs text-red-600">{error}</span> : null}
    </label>
  );
}

type TextareaFieldProps = {
  label: string;
  error?: string;
  hint?: string;
} & TextareaHTMLAttributes<HTMLTextAreaElement>;

export function TextareaField({
  label,
  error,
  hint,
  className,
  ...props
}: TextareaFieldProps) {
  return (
    <label className="block space-y-2">
      <span className="text-sm font-medium text-pine">{label}</span>
      <textarea
        className={cn(
          "min-h-[140px] w-full rounded-[1.5rem] border border-forest/15 bg-white/90 px-4 py-3 text-sm text-pine outline-none transition placeholder:text-pine/35 focus:border-forest focus:ring-2 focus:ring-forest/10",
          className,
        )}
        {...props}
      />
      {hint ? <span className="text-xs text-pine/55">{hint}</span> : null}
      {error ? <span className="text-xs text-red-600">{error}</span> : null}
    </label>
  );
}
