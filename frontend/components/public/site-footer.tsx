import Link from "next/link";

import {
  DEFAULT_EMAIL,
  DEFAULT_INSTAGRAM,
  DEFAULT_WHATSAPP_DISPLAY,
  FALLBACK_SITE_SETTINGS,
} from "@/lib/site-content";
import type { SiteSettingsMap } from "@/lib/types";

type SiteFooterProps = {
  settings: SiteSettingsMap;
};

const links = [
  { href: "/", label: "Inicio" },
  { href: "/services", label: "Servicios" },
  { href: "/experiences", label: "Experiencias" },
  { href: "/blog", label: "Blog" },
  { href: "/contact", label: "Contacto" },
];

export function SiteFooter({ settings }: SiteFooterProps) {
  return (
    <footer className="border-t border-forest/10 bg-pine text-white">
      <div className="mx-auto grid max-w-7xl gap-10 px-5 py-14 md:grid-cols-[1.2fr_0.8fr_0.8fr] md:px-8">
        <div>
          <h3 className="font-serif text-3xl">Nuby Arango Perez</h3>
          <p className="mt-3 max-w-md text-sm leading-7 text-white/75">
            {settings.footer_phrase ?? FALLBACK_SITE_SETTINGS.footer_phrase}
          </p>
        </div>

        <div>
          <p className="text-xs uppercase tracking-[0.35em] text-white/50">
            Links rapidos
          </p>
          <div className="mt-4 flex flex-col gap-3">
            {links.map((link) => (
              <Link
                key={link.href}
                className="text-sm text-white/75 hover:text-white"
                href={link.href}
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>

        <div>
          <p className="text-xs uppercase tracking-[0.35em] text-white/50">
            Contacto
          </p>
          <div className="mt-4 space-y-3 text-sm text-white/75">
            <p>{settings.contact_phone ?? DEFAULT_WHATSAPP_DISPLAY}</p>
            <p>{settings.contact_email ?? DEFAULT_EMAIL}</p>
            <p>{settings.instagram ?? DEFAULT_INSTAGRAM}</p>
          </div>
        </div>
      </div>
    </footer>
  );
}
