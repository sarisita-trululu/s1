import Image from "next/image";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import type { BlogPost } from "@/lib/types";
import { formatDateLong, truncateText } from "@/lib/utils";

type BlogCardProps = {
  post: BlogPost;
};

export function BlogCard({ post }: BlogCardProps) {
  return (
    <article className="soft-panel overflow-hidden">
      <div className="relative h-60 w-full overflow-hidden">
        {post.cover_image ? (
          <Image
            alt={post.title}
            className="h-full w-full object-cover transition duration-500 hover:scale-105"
            fill
            sizes="(max-width: 768px) 100vw, 33vw"
            src={post.cover_image}
          />
        ) : (
          <div className="grain-overlay h-full w-full bg-[linear-gradient(135deg,rgba(245,241,232,0.92),rgba(163,191,168,0.4))]" />
        )}
      </div>
      <div className="space-y-4 p-6">
        <div className="flex items-center gap-3 text-xs uppercase tracking-[0.2em] text-forest/65">
          <span>{post.category}</span>
          <span className="h-1 w-1 rounded-full bg-forest/35" />
          <span>{formatDateLong(post.published_at ?? post.created_at)}</span>
        </div>
        <Link href={`/blog/${post.slug}`}>
          <h3 className="font-serif text-3xl leading-tight text-pine transition hover:text-forest">
            {post.title}
          </h3>
        </Link>
        <p className="text-sm leading-7 text-pine/72">{truncateText(post.excerpt, 150)}</p>
        <Button href={`/blog/${post.slug}`} variant="secondary">
          Leer articulo
        </Button>
      </div>
    </article>
  );
}
