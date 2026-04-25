type AdminPageHeaderProps = {
  eyebrow: string;
  title: string;
  description: string;
};

export function AdminPageHeader({
  eyebrow,
  title,
  description,
}: AdminPageHeaderProps) {
  return (
    <div>
      <p className="text-xs uppercase tracking-[0.35em] text-forest/60">{eyebrow}</p>
      <h1 className="mt-3 font-serif text-5xl text-pine">{title}</h1>
      <p className="mt-4 max-w-3xl text-sm leading-7 text-pine/70">{description}</p>
    </div>
  );
}
