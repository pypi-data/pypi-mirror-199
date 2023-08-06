import type { GraphRF } from '../types';

const recentGraphs = (set, get) => ({
  recentGraphs: [] as GraphRF[],

  setRecentGraphs: (newGraph: GraphRF, reset = false) => {
    let rec = [];
    if (!reset) {
      rec =
        get().recentGraphs.length > 0
          ? get().recentGraphs.filter((gr) => {
              return gr.graph.id !== newGraph.graph.id;
            })
          : [];
    }
    if (newGraph.graph) {
      set((state) => ({
        ...state,
        recentGraphs: [...rec, newGraph],
      }));
    } else {
      set((state) => ({
        ...state,
        recentGraphs: [...rec],
      }));
    }
  },
});

export default recentGraphs;
