import type { Event } from '../types';

// GET /execution/events gets events with filters for nodes, workflows etc
// use this to fetch events for a workflow, a job etc
//
const executedWorkflows = (set) => ({
  executedWorkflows: [] as Event[][],

  setExecutedWorkflows: async (execWorkflow: Event[][]) => {
    set((state) => ({
      ...state,
      executedWorkflows: execWorkflow,
    }));
  },
});

export default executedWorkflows;
