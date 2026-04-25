import Image from "next/image";
import Link from "next/link";
import { MapPin, Users } from "lucide-react";

import { Button } from "@/components/ui/button";
import { StatusBadge } from "@/components/ui/status-badge";
import { DEFAULT_EXPERIENCE_MESSAGE } from "@/lib/site-content";
import type { Experience, SiteSettingsMap } from "@/lib/types";
import { buildWhatsappLink, formatDateLong, formatStatus } from "@/lib/utils";

type ExperienceCardProps = {
  experience: Experience;
  settings: SiteSettingsMap;
};

export function ExperienceCard({ experience, settings }: ExperienceCardProps) {
  const message =
    experience.whatsapp_message ??
    `${DEFAULT_EXPERIENCE_MESSAGE} Me interesa: ${experience.title}.`;
  const availabilityLabel =
    experience.available_spots > 0
      ? `${experience.available_spots} cupos disponibles`
      : formatStatus(experience.status);

  return (
    <article className="soft-panel overflow-hidden">
      <div className="relative h-64 w-full overflow-hidden">
        {experience.cover_image ? (
          <Image
            alt={experience.title}
            className="h-full w-full object-cover transition duration-500 hover:scale-105"
            fill
            sizes="(max-width: 768px) 100vw, 40vw"
            src={experience.cover_image}
          />
        ) : (
          <div className="grain-overlay h-full w-full bg-[linear-gradient(135deg,rgba(47,93,80,0.76),rgba(163,191,168,0.52))]" />
        )}
      </div>
      <div className="space-y-4 p-6">
        <div className="flex items-center justify-between gap-4">
          <StatusBadge status={experience.status} />
          <p className="text-sm text-pine/60">{formatDateLong(experience.date)}</p>
        </div>
        <div>
          <Link href={`/experiences/${experience.slug}`}>
            <h3 className="font-serif text-3xl text-pine transition hover:text-forest">
              {experience.title}
            </h3>
          </Link>
          <div className="mt-3 flex flex-wrap gap-4 text-sm text-pine/65">
            <span className="inline-flex items-center gap-2">
              <MapPin className="h-4 w-4" />
              {experience.location}
            </span>
            <span className="inline-flex items-center gap-2">
              <Users className="h-4 w-4" />
              {availabilityLabel}
            </span>
          </div>
        </div>
        <p className="text-sm leading-7 text-pine/72">{experience.description}</p>
        <div className="flex flex-col gap-3 sm:flex-row">
          <Button
            href={buildWhatsappLink(message, settings)}
            rel="noreferrer"
            target="_blank"
          >
            Quiero participar
          </Button>
          <Button href={`/experiences/${experience.slug}`} variant="secondary">
            Ver detalle
          </Button>
        </div>
      </div>
    </article>
  );
}
