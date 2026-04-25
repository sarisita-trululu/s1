"use client";

import type { ReactNode } from "react";

import type { SiteSettingsMap } from "@/lib/types";
import { SiteFooter } from "@/components/public/site-footer";
import { SiteHeader } from "@/components/public/site-header";
import { WhatsappFloat } from "@/components/public/whatsapp-float";

type PublicShellProps = {
  children: ReactNode;
  settings: SiteSettingsMap;
  whatsappMessage?: string;
};

export function PublicShell({
  children,
  settings,
  whatsappMessage,
}: PublicShellProps) {
  return (
    <div className="relative min-h-screen">
      <SiteHeader settings={settings} />
      <main>{children}</main>
      <SiteFooter settings={settings} />
      <WhatsappFloat message={whatsappMessage} settings={settings} />
    </div>
  );
}
