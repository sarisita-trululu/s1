"use client";

import { Button } from "@/components/ui/button";

export default function GlobalError({
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html lang="es">
      <body className="bg-dawn">
        <main className="flex min-h-screen items-center justify-center px-6">
          <div className="soft-panel max-w-xl p-10 text-center">
            <p className="text-xs uppercase tracking-[0.35em] text-forest/60">
              Algo necesita aire
            </p>
            <h1 className="mt-4 font-serif text-5xl text-pine">
              No pudimos abrir esta vista
            </h1>
            <p className="mt-4 text-base leading-7 text-pine/70">
              La experiencia no se ha perdido. Puedes volver a intentarlo o
              regresar al inicio.
            </p>
            <div className="mt-8 flex flex-col justify-center gap-4 sm:flex-row">
              <Button onClick={reset} type="button">
                Reintentar
              </Button>
              <Button href="/" variant="secondary">
                Volver al inicio
              </Button>
            </div>
          </div>
        </main>
      </body>
    </html>
  );
}
