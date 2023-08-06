import type { EwoksRFNode, GraphRF, GraphEwoks, GraphNodes } from '../types';
import { toRFEwoksNodes } from '../utils/toRFEwoksNodes';
import { toRFEwoksLinks } from '../utils/toRFEwoksLinks';
import { findAllSubgraphs } from './storeUtils/FindAllSubgraphs';
import existsOrValue from '../utils/existsOrValue';
import { calcCoordinatesFirstNode } from './storeUtils/CalcCoordinatesFirstNode';

const subGraph = (set, get) => ({
  subGraph: {
    graph: { id: '', label: '', input_nodes: [], output_nodes: [] },
    nodes: [],
    links: [],
  } as GraphRF,

  // DOC: takes a GraphEwoks and transform it to graphRF
  setSubGraph: async (subGraph: GraphEwoks) => {
    // 1. input the graphEwoks from server or file-system
    // 2. search for all subgraphs in it (async)

    const prevState = get((prev) => prev);
    const newNodeSubgraphs: GraphEwoks[] = await findAllSubgraphs(
      subGraph,
      prevState.recentGraphs
    );

    // 3. Put the newNodeSubgraphs into recent in their graphRF form (sync)
    newNodeSubgraphs.forEach((gr) => {
      // calculate the rfNodes using the fetched subgraphs
      const rfNodes = toRFEwoksNodes(gr, newNodeSubgraphs, prevState.tasks);

      prevState.setRecentGraphs({
        graph: gr.graph,
        nodes: rfNodes,
        links: toRFEwoksLinks(gr, newNodeSubgraphs, prevState.tasks),
      });
    });
    // 4. Calculate the new graph given the subgraphs
    const grfNodes = toRFEwoksNodes(
      subGraph,
      newNodeSubgraphs,
      prevState.tasks
    );

    const graph = {
      graph: subGraph.graph,
      nodes: grfNodes,
      links: toRFEwoksLinks(subGraph, newNodeSubgraphs, prevState.tasks),
    };
    // Adding a subgraph to an existing workingGraph:
    // save the workingGraph in the recent graphs and add a new graph node to it

    const subToAdd = graph as GraphRF;

    let newNode = {} as EwoksRFNode;
    if (subToAdd) {
      const inputsSub = subToAdd.graph.input_nodes.map((input) => {
        return {
          label: calcLabel(input),
          type: 'data ',
          // positionY: input.uiProps.position.y,
        };
      });
      const outputsSub = subToAdd.graph.output_nodes.map((output) => {
        return {
          label: calcLabel(output),
          type: 'data ',
          // positionY: output.uiProps.position.y,
        };
      });
      let id = 0;
      let graphId = subToAdd.graph.label;
      while (prevState.graphRF.nodes.some((nod) => nod.id === graphId)) {
        graphId += id++;
      }
      newNode = {
        sourcePosition: 'right',
        targetPosition: 'left',
        task_generator: '',
        id: graphId,
        task_type: 'graph',
        task_identifier: subToAdd.graph.id,
        type: 'graph',
        position: calcCoordinatesFirstNode(prevState.graphRF.nodes),
        default_inputs: [],
        inputs_complete: false,
        default_error_node: false,
        default_error_attributes: {
          map_all_data: true,
          data_mapping: [],
        },
        data: {
          exists: true,
          label: subToAdd.graph.label,
          type: 'internal',
          comment: '',
          icon: subToAdd.graph.uiProps && subToAdd.graph.uiProps.icon,
          inputs: inputsSub,
          outputs: outputsSub,
          withImage: true,
          withLabel: true,
        },
      };

      prevState.setRecentGraphs(subToAdd);
    } else {
      prevState.setOpenSnackbar({
        open: true,
        text: 'Couldnt locate the workingGraph in the recent!',
        severity: 'warning',
      });
    }
    const newWorkingGraph = {
      graph: prevState.graphRF.graph,
      nodes: [...prevState.graphRF.nodes, newNode],
      links: prevState.graphRF.links,
    };
    prevState.setGraphRF(newWorkingGraph);
    prevState.setRecentGraphs(newWorkingGraph);
    return graph;
  },
});

function calcLabel(inputOutput: GraphNodes): string {
  return `${
    existsOrValue(inputOutput.uiProps, 'label', inputOutput.id) as string
  }: ${inputOutput.node} ${
    inputOutput.sub_node ? ` -> ${inputOutput.sub_node}` : ''
  }`;
}

export default subGraph;
