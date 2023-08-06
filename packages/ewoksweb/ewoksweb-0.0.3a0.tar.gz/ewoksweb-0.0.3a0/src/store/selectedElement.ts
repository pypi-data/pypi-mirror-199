import type { EwoksRFLink, EwoksRFNode, GraphDetails, GraphRF } from '../types';

const selectedElement = (set, get) => ({
  selectedElement: {} as EwoksRFNode | EwoksRFLink | GraphDetails,

  setSelectedElement: (
    element: EwoksRFNode | EwoksRFLink | GraphDetails,
    from: string
  ) => {
    const prevState = get((prev) => prev);

    const wg = prevState.workingGraph.graph.id;
    const { graph, nodes, links } = prevState.graphRF;

    if (from === 'fromSaveElement') {
      prevState.setCanvasGraphChanged(true);
    }

    if (wg === '0' || wg === graph.id) {
      let tempGraph = {} as GraphRF;
      if ('position' in element) {
        const allOtherNodes = nodes.filter((nod) => nod.id !== element.id);
        tempGraph = {
          graph,
          nodes: [...initializeNodes(allOtherNodes), element],
          links: links.map((link) => {
            return { ...link, selected: false };
          }),
        };
        if (from === 'fromSaveElement') {
          prevState.setUndoRedo({
            action: 'Node details changed',
            graph: tempGraph,
          });
        }
      } else if ('source' in element) {
        tempGraph = {
          graph,
          // setting all node de-selected...
          nodes: initializeNodes(nodes),
          links: [...links.filter((link) => link.id !== element.id), element],
        };
        if (from === 'fromSaveElement') {
          prevState.setUndoRedo({
            action: 'Link details changed',
            graph: tempGraph,
          });
        }
      } else {
        tempGraph = {
          graph: element as GraphDetails,
          nodes: initializeNodes(nodes),
          links: links.map((link) => {
            return { ...link, selected: false }; // TODO: examine this after update
          }),
        };

        if (from === 'fromSaveElement') {
          prevState.setUndoRedo({
            action: 'Graph details changed',
            graph: tempGraph,
          });
        }
      }

      set((state) => ({
        ...state,
        graphRF: tempGraph,
        selectedElement: element,
      }));
    } else {
      set((state) => ({
        ...state,
        selectedElement: element,
      }));
    }
  },
});

function initializeNodes(nodes) {
  return nodes.map((nod) => {
    return {
      ...nod,
      selected: false,
      data: { ...nod.data, details: false },
    };
  });
}

export default selectedElement;
