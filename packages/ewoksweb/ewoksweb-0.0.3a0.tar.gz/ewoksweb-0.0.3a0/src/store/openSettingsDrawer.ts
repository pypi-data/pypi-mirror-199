const openSettingsDrawer = (set) => ({
  openSettingsDrawer: '',

  setOpenSettingsDrawer: (openTab) => {
    set((state) => ({
      ...state,
      openSettingsDrawer: openTab,
    }));
  },
});

export default openSettingsDrawer;
