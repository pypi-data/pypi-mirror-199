import type { Task } from '../types';

const selectedTask = (set) => ({
  selectedElement: {} as Task,

  setSelectedTask: (task) => {
    set((state) => ({
      ...state,
      selectedTask: task,
    }));
  },
});

export default selectedTask;
