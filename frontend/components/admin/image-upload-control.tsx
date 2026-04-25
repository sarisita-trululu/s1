"use client";

import { LoaderCircle, UploadCloud } from "lucide-react";
import { useState } from "react";

import { uploadImage } from "@/lib/admin-api";

type ImageUploadControlProps = {
  token: string;
  label: string;
  helper?: string;
  multiple?: boolean;
  onUploaded: (urls: string[]) => void;
};

export function ImageUploadControl({
  token,
  label,
  helper,
  multiple = false,
  onUploaded,
}: ImageUploadControlProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  return (
    <div className="block space-y-2">
      <span className="text-sm font-medium text-pine">{label}</span>
      <label className="flex cursor-pointer items-center justify-center gap-3 rounded-[1.5rem] border border-dashed border-forest/25 bg-white/70 px-4 py-5 text-sm text-pine/70 transition hover:border-forest/45 hover:bg-white">
        {loading ? (
          <LoaderCircle className="h-4 w-4 animate-spin" />
        ) : (
          <UploadCloud className="h-4 w-4" />
        )}
        <span>{loading ? "Subiendo..." : "Seleccionar imagen"}</span>
        <input
          className="hidden"
          multiple={multiple}
          type="file"
          accept=".jpg,.jpeg,.png,.webp"
          onChange={async (event) => {
            const files = Array.from(event.target.files ?? []);
            if (!files.length) {
              return;
            }

            setLoading(true);
            setError(null);
            try {
              const urls: string[] = [];
              for (const file of files) {
                const uploaded = await uploadImage(token, file);
                urls.push(uploaded.url);
              }
              onUploaded(urls);
            } catch {
              setError("No fue posible subir la imagen.");
            } finally {
              setLoading(false);
              event.target.value = "";
            }
          }}
        />
      </label>
      {helper ? <p className="text-xs text-pine/55">{helper}</p> : null}
      {error ? <p className="text-xs text-red-600">{error}</p> : null}
    </div>
  );
}
