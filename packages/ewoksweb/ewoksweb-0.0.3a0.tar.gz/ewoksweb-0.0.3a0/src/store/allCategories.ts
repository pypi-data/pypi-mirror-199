const allCategories = (set) => ({
  allCategories: [] as { label: string }[],

  setAllCategories: (categories: [{ label: string }]) => {
    set((state) => ({
      ...state,
      allCategories: categories,
    }));
  },
});

export default allCategories;
