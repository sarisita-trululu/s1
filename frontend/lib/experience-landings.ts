import type { Experience } from "@/lib/types";

export const EL_LUGAR_DONDE_TODO_EMPEZO_SLUG = "el-lugar-donde-todo-empezo";

export const EL_LUGAR_DONDE_TODO_EMPEZO_WHATSAPP_MESSAGE =
  "Hola, quiero reservar mi lugar para el encuentro El lugar donde todo empezó del 17 de mayo en Laguna la Colorada.";

export const EL_LUGAR_DONDE_TODO_EMPEZO_RESERVE_MESSAGE =
  EL_LUGAR_DONDE_TODO_EMPEZO_WHATSAPP_MESSAGE;

export const EL_LUGAR_DONDE_TODO_EMPEZO_INFO_MESSAGE =
  EL_LUGAR_DONDE_TODO_EMPEZO_WHATSAPP_MESSAGE;

export const EL_LUGAR_DONDE_TODO_EMPEZO_HERO_IMAGE =
  "/experiences/el-lugar-donde-todo-empezo/gallery-10.jpeg";

export const EL_LUGAR_DONDE_TODO_EMPEZO_CTA_IMAGE =
  "/experiences/el-lugar-donde-todo-empezo/gallery-5.jpeg";

export const EL_LUGAR_DONDE_TODO_EMPEZO_GALLERY_IMAGES = [
  "/experiences/el-lugar-donde-todo-empezo/gallery-10.jpeg",
  "/experiences/el-lugar-donde-todo-empezo/gallery-5.jpeg",
  "/experiences/el-lugar-donde-todo-empezo/gallery-2.jpeg",
  "/experiences/el-lugar-donde-todo-empezo/gallery-8.jpeg",
  "/experiences/el-lugar-donde-todo-empezo/gallery-1.jpeg",
  "/experiences/el-lugar-donde-todo-empezo/gallery-6.jpeg",
  "/experiences/el-lugar-donde-todo-empezo/gallery-3.jpeg",
  "/experiences/el-lugar-donde-todo-empezo/gallery-4.jpeg",
];

export function isElLugarDondeTodoEmpezo(experience: Experience) {
  return (
    experience.slug === EL_LUGAR_DONDE_TODO_EMPEZO_SLUG ||
    experience.title.trim().toLowerCase() === "el lugar donde todo empezó" ||
    experience.title.trim().toLowerCase() === "el lugar donde todo empezo"
  );
}

export function getElLugarDondeTodoEmpezoFallbackExperience(): Experience {
  return {
    id: -1,
    title: "El lugar donde todo empezó",
    slug: EL_LUGAR_DONDE_TODO_EMPEZO_SLUG,
    description:
      "Un encuentro para reconectar contigo desde la naturaleza.\n\nHay una parte de ti que no está herida...\nsolo está esperando que regreses.\n\nUn lugar donde aún habita tu versión más libre,\nmás auténtica,\nmás viva.\n\nEn este encuentro no vamos a convertirnos en alguien nuevo...\nvamos a recordar quiénes éramos antes de olvidar.",
    date: "2026-05-17",
    location: "Laguna la Colorada, Sogamoso, Boyacá",
    capacity: 0,
    available_spots: 0,
    status: "cupos_abiertos",
    cover_image: EL_LUGAR_DONDE_TODO_EMPEZO_HERO_IMAGE,
    gallery_images: EL_LUGAR_DONDE_TODO_EMPEZO_GALLERY_IMAGES,
    whatsapp_message: EL_LUGAR_DONDE_TODO_EMPEZO_WHATSAPP_MESSAGE,
    is_published: true,
    created_at: "2026-01-01T00:00:00Z",
    updated_at: "2026-01-01T00:00:00Z",
  };
}

export function getExperienceWithFallback(
  slug: string,
  experience: Experience | null,
) {
  if (experience) {
    return experience;
  }

  if (slug === EL_LUGAR_DONDE_TODO_EMPEZO_SLUG) {
    return getElLugarDondeTodoEmpezoFallbackExperience();
  }

  return null;
}

export function withFeaturedExperienceFallback(experiences: Experience[]) {
  if (experiences.some(isElLugarDondeTodoEmpezo)) {
    return experiences;
  }

  return [getElLugarDondeTodoEmpezoFallbackExperience(), ...experiences];
}
