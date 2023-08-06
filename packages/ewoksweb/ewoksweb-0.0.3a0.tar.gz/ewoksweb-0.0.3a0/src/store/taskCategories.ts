const taskCategories = (set) => ({
  taskCategories: ['EwoksCore'],
  setTaskCategories: (taskCategories) => {
    set((state) => ({
      ...state,
      taskCategories: [...new Set(taskCategories)],
    }));
  },
});

export default taskCategories;
