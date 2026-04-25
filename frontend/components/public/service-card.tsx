import { HeartHandshake, Leaf, Mountain, Presentation, Sparkles, Users, Video } from "lucide-react";

import type { Service } from "@/lib/types";

const icons = {
  video: Video,
  user: Sparkles,
  heart: HeartHandshake,
  "graduation-cap": Presentation,
  building: Users,
  briefcase: Mountain,
  leaf: Leaf,
} as const;

type ServiceCardProps = {
  service: Service;
};

export function ServiceCard({ service }: ServiceCardProps) {
  const Icon = icons[service.icon as keyof typeof icons] ?? Leaf;

  return (
    <article className="soft-panel h-full p-6 transition duration-300 hover:-translate-y-1 hover:shadow-soft">
      <div className="flex h-14 w-14 items-center justify-center rounded-[1.5rem] bg-forest/10 text-forest">
        <Icon className="h-6 w-6" />
      </div>
      <h3 className="mt-5 font-serif text-3xl text-pine">{service.title}</h3>
      <p className="mt-4 text-sm leading-7 text-pine/70">{service.description}</p>
      <ul className="mt-5 space-y-2">
        {service.items.slice(0, 5).map((item) => (
          <li key={item} className="flex items-start gap-3 text-sm text-pine/80">
            <span className="mt-2 h-1.5 w-1.5 rounded-full bg-forest" />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </article>
  );
}
