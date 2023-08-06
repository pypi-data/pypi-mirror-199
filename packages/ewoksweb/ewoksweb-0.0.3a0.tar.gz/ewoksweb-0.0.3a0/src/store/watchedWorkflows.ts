import type { Event } from '../types';

// These are the workflows that can be examined on the canvas
// They include executing-live and the watched workflows from server

const watchedWorkflows = (set, get) => ({
  watchedWorkflows: [] as Event[][],

  setWatchedWorkflows: async (watchedWorkflows: Event[][]) => {
    set((state) => ({
      ...state,
      watchedWorkflows,
    }));
    get().setOpenSettingsDrawer('close');
  },
});

export default watchedWorkflows;
