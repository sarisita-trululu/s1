type ToggleFieldProps = {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  description?: string;
};

export function ToggleField({
  label,
  checked,
  onChange,
  description,
}: ToggleFieldProps) {
  return (
    <button
      className="flex w-full items-center justify-between rounded-[1.5rem] border border-forest/10 bg-white/80 px-4 py-3 text-left transition hover:border-forest/20"
      type="button"
      onClick={() => onChange(!checked)}
    >
      <div>
        <p className="text-sm font-semibold text-pine">{label}</p>
        {description ? (
          <p className="mt-1 text-xs leading-5 text-pine/60">{description}</p>
        ) : null}
      </div>
      <span
        className={`relative inline-flex h-7 w-12 rounded-full transition ${
          checked ? "bg-forest" : "bg-forest/15"
        }`}
      >
        <span
          className={`absolute top-1 h-5 w-5 rounded-full bg-white transition ${
            checked ? "left-6" : "left-1"
          }`}
        />
      </span>
    </button>
  );
}
