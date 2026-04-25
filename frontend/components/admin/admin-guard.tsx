"use client";

import type { ReactNode } from "react";

import { useAdminGuard } from "@/hooks/use-admin-guard";

type AdminGuardProps = {
  children: ReactNode;
};

export function AdminGuard({ children }: AdminGuardProps) {
  const { checking } = useAdminGuard();

  if (checking) {
    return (
      <div className="flex min-h-screen items-center justify-center px-6">
        <div className="soft-panel w-full max-w-md p-10 text-center">
          <p className="text-xs uppercase tracking-[0.35em] text-forest/60">
            Panel privado
          </p>
          <h1 className="mt-4 font-serif text-4xl text-pine">
            Verificando acceso
          </h1>
          <div className="mx-auto mt-8 h-2 w-32 overflow-hidden rounded-full bg-forest/10">
            <div className="h-full w-1/2 animate-pulse rounded-full bg-forest" />
          </div>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
