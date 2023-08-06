import type { WorkflowDescription } from '../types';

const allWorkflows = (set) => ({
  allWorkflows: [] as WorkflowDescription[],

  setAllWorkflows: (workflows: WorkflowDescription[]) => {
    set((state) => ({
      ...state,
      allWorkflows: workflows,
    }));
  },
});

export default allWorkflows;
