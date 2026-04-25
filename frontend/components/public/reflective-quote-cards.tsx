"use client";

import { motion } from "framer-motion";
import { Leaf, Quote, Sparkles } from "lucide-react";

import { cn } from "@/lib/utils";

export type ReflectiveQuoteItem = {
  type: "quote" | "inspired";
  text: string;
  author?: string;
};

type ReflectiveQuoteCardsProps = {
  className?: string;
  items: ReflectiveQuoteItem[];
};

export function ReflectiveQuoteCards({
  className,
  items,
}: ReflectiveQuoteCardsProps) {
  return (
    <div className={cn("grid gap-5 md:grid-cols-2 xl:grid-cols-4", className)}>
      {items.map((item, index) => {
        const isQuote = item.type === "quote";
        const Icon = isQuote ? Quote : index % 4 === 1 ? Leaf : Sparkles;

        return (
          <motion.article
            key={`${item.type}-${item.text}`}
            className={cn(
              "rounded-[2rem] border p-6 shadow-card backdrop-blur-sm",
              isQuote
                ? "border-forest/10 bg-white/82 text-pine"
                : "border-forest/10 bg-sage/24 text-pine",
              index % 2 === 1 ? "md:mt-10" : "",
            )}
            initial={{ opacity: 0, y: 28 }}
            transition={{
              duration: 0.7,
              delay: index * 0.08,
              ease: [0.22, 1, 0.36, 1],
            }}
            viewport={{ once: true, amount: 0.25 }}
            whileInView={{ opacity: 1, y: 0 }}
          >
            <div
              className={cn(
                "inline-flex rounded-full p-3",
                isQuote ? "bg-sand text-forest" : "bg-white/70 text-forest",
              )}
            >
              <Icon className="h-5 w-5" />
            </div>

            {isQuote ? (
              <blockquote className="mt-5">
                <p className="font-serif text-2xl leading-snug text-pine">
                  “{item.text}”
                </p>
                <footer className="mt-5 text-sm font-medium uppercase tracking-[0.28em] text-forest/62">
                  {item.author}
                </footer>
              </blockquote>
            ) : (
              <div className="mt-5">
                <p className="font-serif text-2xl leading-snug text-pine">
                  {item.text}
                </p>
                <p className="mt-5 text-sm uppercase tracking-[0.28em] text-forest/58">
                  Frase inspirada
                </p>
              </div>
            )}
          </motion.article>
        );
      })}
    </div>
  );
}
