import { PublicShell } from "@/components/public/page-shell";
import { ServiceCard } from "@/components/public/service-card";
import { EmptyState } from "@/components/ui/empty-state";
import { Reveal } from "@/components/ui/reveal";
import { SectionHeading } from "@/components/ui/section-heading";
import { getServices, getSiteSettings } from "@/lib/public-api";
import { buildSettingsMap } from "@/lib/utils";

export const metadata = {
  title: "Servicios | Nuby Arango Perez",
};

export default async function ServicesPage() {
  const [services, siteSettings] = await Promise.all([
    getServices().catch(() => []),
    getSiteSettings().catch(() => []),
  ]);
  const settingsMap = buildSettingsMap(siteSettings);

  return (
    <PublicShell settings={settingsMap}>
      <section className="page-section">
        <Reveal>
          <SectionHeading
            eyebrow="Servicios"
            title="Acompanamiento para la vida y el trabajo"
            description="Cada proceso esta pensado para abrir un espacio de escucha, orientacion y cuidado emocional con profundidad y calidez."
          />
        </Reveal>
        <div className="mt-10">
          {services.length ? (
            <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
              {services.map((service, index) => (
                <Reveal key={service.id} delay={index * 0.05}>
                  <ServiceCard service={service} />
                </Reveal>
              ))}
            </div>
          ) : (
            <EmptyState
              title="Aun no hay servicios publicados"
              description="Cuando se publiquen nuevos servicios, los veras aqui con toda su informacion."
            />
          )}
        </div>
      </section>
    </PublicShell>
  );
}
