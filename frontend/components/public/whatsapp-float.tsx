import { MessageCircleHeart } from "lucide-react";

import { DEFAULT_CONTACT_MESSAGE } from "@/lib/site-content";
import type { SiteSettingsMap } from "@/lib/types";
import { buildWhatsappLink } from "@/lib/utils";

type WhatsappFloatProps = {
  settings: SiteSettingsMap;
  message?: string;
};

export function WhatsappFloat({
  settings,
  message = DEFAULT_CONTACT_MESSAGE,
}: WhatsappFloatProps) {
  return (
    <a
      className="fixed bottom-24 right-4 z-40 inline-flex h-14 w-14 items-center justify-center rounded-full bg-forest text-white shadow-soft transition hover:scale-105 hover:bg-pine md:bottom-5 md:right-5"
      href={buildWhatsappLink(message, settings)}
      target="_blank"
      rel="noreferrer"
      aria-label="Escribir por WhatsApp"
    >
      <MessageCircleHeart className="h-6 w-6" />
    </a>
  );
}
