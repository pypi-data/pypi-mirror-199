const tasks = (set) => ({
  tasks: [],
  setTasks: (tasks) => {
    set((state) => ({
      ...state,
      tasks,
    }));
  },
});

export default tasks;
