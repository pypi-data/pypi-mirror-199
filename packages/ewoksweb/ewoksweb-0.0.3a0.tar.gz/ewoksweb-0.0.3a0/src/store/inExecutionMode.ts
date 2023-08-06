// DOC: when UI in execution mode
const inExecutionMode = (set, get) => ({
  inExecutionMode: false,

  setInExecutionMode: (val: boolean) => {
    const prevState = get((prev) => prev);

    set((state) => ({
      ...state,
      inExecutionMode: val,
    }));

    // when execution stops by user the execution nodes are removed from the graph
    if (!val) {
      set((state) => ({
        ...state,
        // only for testing set graphRF
        graphRF: {
          ...prevState.graphRF,
          nodes: prevState.graphRF.nodes.filter(
            (nod) => nod.type !== 'executionSteps'
          ),
        },
        executingEvents: [],
      }));
    } else {
      // when execution starts
    }
  },
});

export default inExecutionMode;
