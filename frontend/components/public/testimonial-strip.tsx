import type { Testimonial } from "@/lib/types";

type TestimonialStripProps = {
  testimonials: Testimonial[];
};

export function TestimonialStrip({ testimonials }: TestimonialStripProps) {
  return (
    <div className="grid gap-5 md:grid-cols-3">
      {testimonials.map((testimonial) => (
        <article
          key={testimonial.id}
          className="soft-panel h-full bg-white/70 p-6"
        >
          <p className="text-sm leading-7 text-pine/75">“{testimonial.text}”</p>
          <div className="mt-6">
            <p className="font-serif text-2xl text-pine">{testimonial.name}</p>
            <p className="text-xs uppercase tracking-[0.25em] text-forest/60">
              {testimonial.service_type}
            </p>
          </div>
        </article>
      ))}
    </div>
  );
}
