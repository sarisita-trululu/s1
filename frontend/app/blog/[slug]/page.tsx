import Image from "next/image";
import { notFound } from "next/navigation";

import { PublicShell } from "@/components/public/page-shell";
import { getBlogPostBySlug, getSiteSettings } from "@/lib/public-api";
import { buildSettingsMap, formatDateLong } from "@/lib/utils";

type BlogDetailPageProps = {
  params: Promise<{ slug: string }>;
};

export async function generateMetadata({ params }: BlogDetailPageProps) {
  const { slug } = await params;
  const post = await getBlogPostBySlug(slug).catch(() => null);
  if (!post) {
    return { title: "Blog | Nuby Arango Perez" };
  }
  return {
    title: `${post.title} | Nuby Arango Perez`,
    description: post.excerpt,
  };
}

export default async function BlogDetailPage({ params }: BlogDetailPageProps) {
  const { slug } = await params;
  const [post, siteSettings] = await Promise.all([
    getBlogPostBySlug(slug).catch(() => null),
    getSiteSettings().catch(() => []),
  ]);

  if (!post) {
    notFound();
  }

  const settingsMap = buildSettingsMap(siteSettings);
  const paragraphs = post.content.split(/\n{2,}/).filter(Boolean);

  return (
    <PublicShell settings={settingsMap}>
      <article className="page-section">
        <div className="mx-auto max-w-4xl">
          <p className="text-xs uppercase tracking-[0.32em] text-forest/60">
            {post.category}
          </p>
          <h1 className="mt-4 font-serif text-5xl leading-tight text-pine md:text-6xl">
            {post.title}
          </h1>
          <p className="mt-4 text-sm text-pine/55">
            {formatDateLong(post.published_at ?? post.created_at)}
          </p>
          {post.cover_image ? (
            <div className="relative mt-10 h-[22rem] overflow-hidden rounded-[2.2rem] md:h-[30rem]">
              <Image
                alt={post.title}
                className="h-full w-full object-cover"
                fill
                priority
                sizes="100vw"
                src={post.cover_image}
              />
            </div>
          ) : null}
          <div className="soft-panel mt-10 p-8 md:p-10">
            <p className="text-lg leading-8 text-pine/80">{post.excerpt}</p>
            <div className="mt-8 space-y-6 text-base leading-8 text-pine/78">
              {paragraphs.map((paragraph, index) => (
                <p key={`${index}-${paragraph.slice(0, 24)}`}>{paragraph}</p>
              ))}
            </div>
          </div>
        </div>
      </article>
    </PublicShell>
  );
}
