import { HomeView } from "@/components/public/home-view";
import { withFeaturedExperienceFallback } from "@/lib/experience-landings";
import { PublicShell } from "@/components/public/page-shell";
import { buildSettingsMap } from "@/lib/utils";
import { getBlogPosts, getExperiences, getServices, getSiteSettings, getTestimonials } from "@/lib/public-api";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const [services, experiences, blogPosts, testimonials, siteSettings] =
    await Promise.all([
      getServices().catch(() => []),
      getExperiences().catch(() => []),
      getBlogPosts().catch(() => []),
      getTestimonials().catch(() => []),
      getSiteSettings().catch(() => []),
    ]);

  const settingsMap = buildSettingsMap(siteSettings);
  const visibleExperiences = withFeaturedExperienceFallback(experiences);

  return (
    <PublicShell settings={settingsMap}>
      <HomeView
        blogPosts={blogPosts}
        experiences={visibleExperiences}
        services={services}
        settings={settingsMap}
        testimonials={testimonials}
      />
    </PublicShell>
  );
}
