import type { stackGraph } from '../types';

const subgraphsStack = (set, get) => ({
  subgraphsStack: [] as stackGraph[],

  setSubgraphsStack: (stackGraph: stackGraph) => {
    let stack = [];
    const subStack = get().subgraphsStack;
    const exists: number = subStack.map((gr) => gr.id).indexOf(stackGraph.id);

    if (stackGraph.id === 'initialiase') {
      stack = [];
    } else if (exists === -1) {
      stack = [...subStack, stackGraph];
    } else if (exists === subStack.length - 1) {
      // TODO: if user insert the same 'graph' and is the first then stack is not updated
      // Not applicable so left as is and it just wont be able to doubleClick
      stack = subStack;
    } else {
      // TODO: if the same graph is inserted again lower in the subgraphs this is activated
      // and resets the stack without adding. If it is an addition this stack needs to know it
      // subStack.length = exists + 1;
      // Not applicable so stays as is for now
      stack = subStack.slice(0, exists + 1);
      // stack = ['graph'];
    }
    set((state) => ({
      ...state,
      subgraphsStack: stack,
    }));
  },
});

export default subgraphsStack;
