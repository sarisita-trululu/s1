"use client";

import { useEffect, useState } from "react";

import { AdminPageHeader } from "@/components/admin/admin-page-header";
import { Button } from "@/components/ui/button";
import { useAuthStore } from "@/hooks/use-auth-store";
import { listContactMessages, updateContactMessage } from "@/lib/admin-api";
import type { ContactMessage } from "@/lib/types";
import { formatDateLong } from "@/lib/utils";

export default function AdminMessagesPage() {
  const { token } = useAuthStore();
  const [items, setItems] = useState<ContactMessage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = async () => {
    if (!token) {
      return;
    }

    setLoading(true);
    try {
      const data = await listContactMessages(token);
      setItems(data);
    } catch {
      setError("No fue posible cargar los mensajes.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refresh();
  }, [token]);

  return (
    <div className="space-y-8">
      <AdminPageHeader
        eyebrow="Mensajes"
        title="Mensajes de contacto"
        description="Revisa los mensajes que llegan desde el formulario publico y marca los ya atendidos."
      />

      <section className="soft-panel overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="border-b border-forest/10 bg-white/70 text-pine/70">
              <tr>
                <th className="px-6 py-4 font-medium">Nombre</th>
                <th className="px-6 py-4 font-medium">Correo</th>
                <th className="px-6 py-4 font-medium">Motivo</th>
                <th className="px-6 py-4 font-medium">Mensaje</th>
                <th className="px-6 py-4 font-medium">Fecha</th>
                <th className="px-6 py-4 font-medium">Estado</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td className="px-6 py-6 text-pine/65" colSpan={6}>
                    Cargando mensajes...
                  </td>
                </tr>
              ) : items.length ? (
                items.map((item) => (
                  <tr key={item.id} className="border-b border-forest/8 bg-white/65 align-top">
                    <td className="px-6 py-5 font-medium text-pine">{item.full_name}</td>
                    <td className="px-6 py-5 text-pine/70">{item.email}</td>
                    <td className="px-6 py-5 text-pine/70">{item.reason}</td>
                    <td className="max-w-sm px-6 py-5 text-pine/72">{item.message}</td>
                    <td className="px-6 py-5 text-pine/60">{formatDateLong(item.created_at)}</td>
                    <td className="px-6 py-5">
                      <Button
                        onClick={async () => {
                          if (!token) {
                            return;
                          }
                          await updateContactMessage(token, item.id, {
                            is_read: !item.is_read,
                          });
                          await refresh();
                        }}
                        type="button"
                        variant={item.is_read ? "ghost" : "secondary"}
                      >
                        {item.is_read ? "Leido" : "Marcar leido"}
                      </Button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td className="px-6 py-6 text-pine/65" colSpan={6}>
                    Todavia no hay mensajes registrados.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      {error ? (
        <p className="rounded-2xl bg-red-100 px-4 py-3 text-sm text-red-700">
          {error}
        </p>
      ) : null}
    </div>
  );
}
