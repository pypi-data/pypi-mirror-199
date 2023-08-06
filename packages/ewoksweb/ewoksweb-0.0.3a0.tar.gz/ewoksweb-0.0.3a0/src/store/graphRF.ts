import type { GraphRF } from '../types';

const tutorialGraph = {
  graph: {
    id: 'newGraph',
    label: 'newGraph',
    input_nodes: [],
    output_nodes: [],
    uiProps: {},
  },
  nodes: [],
  links: [],
} as GraphRF;

const graphRF = (set, get) => ({
  graphRF: tutorialGraph,

  setGraphRF: (graphRF, isChangeToCanvasGraph) => {
    if (isChangeToCanvasGraph && !get().inExecutionMode) {
      get().setCanvasGraphChanged(true);
    } else if (isChangeToCanvasGraph === false) {
      get().setCanvasGraphChanged(false);
    }

    // If missing uiProps or other fill it here
    if (!graphRF.graph.uiProps) {
      graphRF.graph.uiProps = {};
    }
    set((state) => ({
      ...state,
      graphRF,
    }));
  },
});

export default graphRF;
