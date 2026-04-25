"use client";

import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";

import type { AuthUser } from "@/lib/types";

type AuthState = {
  token: string | null;
  user: AuthUser | null;
  hydrated: boolean;
  setSession: (token: string, user: AuthUser) => void;
  clearSession: () => void;
  markHydrated: () => void;
  setUser: (user: AuthUser) => void;
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      hydrated: false,
      setSession: (token, user) => set({ token, user }),
      clearSession: () => set({ token: null, user: null }),
      markHydrated: () => set({ hydrated: true }),
      setUser: (user) => set({ user }),
    }),
    {
      name: "nuby-admin-auth",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        token: state.token,
        user: state.user,
      }),
      onRehydrateStorage: () => (state) => {
        state?.markHydrated();
      },
    },
  ),
);
