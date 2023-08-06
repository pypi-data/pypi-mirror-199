const graphOrSubgraph = (set) => ({
  graphOrSubgraph: true as boolean,

  setGraphOrSubgraph: (isItGraph: boolean) => {
    set((state) => ({
      ...state,
      graphOrSubgraph: isItGraph,
    }));
  },
});

export default graphOrSubgraph;
