import type { Icon } from '../types';

const allIcons = (set) => ({
  allIcons: [],

  setAllIcons: (icons: [Icon]) => {
    set((state) => ({
      ...state,
      allIcons: icons,
    }));
  },
});

export default allIcons;
