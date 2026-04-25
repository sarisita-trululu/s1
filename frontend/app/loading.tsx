export default function Loading() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6">
      <div className="soft-panel grain-overlay w-full max-w-md p-10 text-center">
        <p className="text-xs font-semibold uppercase tracking-[0.35em] text-forest/70">
          Cargando
        </p>
        <h1 className="mt-4 font-serif text-4xl text-pine">
          Preparando un espacio de calma
        </h1>
        <div className="mx-auto mt-8 h-2 w-32 overflow-hidden rounded-full bg-forest/10">
          <div className="h-full w-1/2 animate-pulse rounded-full bg-forest" />
        </div>
      </div>
    </main>
  );
}
