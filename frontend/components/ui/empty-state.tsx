type EmptyStateProps = {
  title: string;
  description: string;
};

export function EmptyState({ title, description }: EmptyStateProps) {
  return (
    <div className="rounded-[2rem] border border-forest/10 bg-white/80 p-8 text-center shadow-card">
      <h3 className="font-serif text-2xl text-pine">{title}</h3>
      <p className="mt-3 text-sm leading-6 text-pine/70">{description}</p>
    </div>
  );
}
