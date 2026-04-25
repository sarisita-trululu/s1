import { redirect } from "next/navigation";

type ExperienciaAliasDetailPageProps = {
  params: Promise<{ slug: string }>;
};

export default async function ExperienciaAliasDetailPage({
  params,
}: ExperienciaAliasDetailPageProps) {
  const { slug } = await params;
  redirect(`/experiences/${slug}`);
}
