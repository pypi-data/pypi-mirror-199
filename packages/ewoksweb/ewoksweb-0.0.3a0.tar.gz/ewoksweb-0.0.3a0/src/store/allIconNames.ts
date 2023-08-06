// import type { Icons } from '../types';

const allIconNames = (set) => ({
  allIconNames: [],

  setAllIconNames: (icons: [string]) => {
    set((state) => ({
      ...state,
      allIconNames: icons,
    }));
  },
});

export default allIconNames;
