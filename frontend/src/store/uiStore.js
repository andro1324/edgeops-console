import { create } from 'zustand';

export const useUIStore = create((set) => ({
  sidebarOpen: false,
  density: 'comfortable',
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  closeSidebar: () => set({ sidebarOpen: false }),
  setDensity: (density) => set({ density }),
}));