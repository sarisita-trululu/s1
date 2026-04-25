"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";

import { getAdminMe } from "@/lib/admin-api";
import { useAuthStore } from "@/hooks/use-auth-store";

export function useAdminGuard() {
  const router = useRouter();
  const pathname = usePathname();
  const { token, hydrated, clearSession, setUser, user } = useAuthStore();
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    if (!hydrated) {
      return;
    }

    if (!token) {
      router.replace(`/admin/login?next=${encodeURIComponent(pathname)}`);
      setChecking(false);
      return;
    }

    let isMounted = true;
    getAdminMe(token)
      .then((profile) => {
        if (!isMounted) {
          return;
        }
        setUser(profile);
        setChecking(false);
      })
      .catch(() => {
        clearSession();
        router.replace(`/admin/login?next=${encodeURIComponent(pathname)}`);
      });

    return () => {
      isMounted = false;
    };
  }, [clearSession, hydrated, pathname, router, setUser, token]);

  return { checking, token, user, hydrated };
}
