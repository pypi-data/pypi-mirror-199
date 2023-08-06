// @ts-ignore
// import dagre from 'dagre';
import type {
  EwoksRFNode,
  GraphEwoks,
  GraphRF,
  WorkflowDescription,
} from './types';
import axios from 'axios';
import { calcGraphInputsOutputs } from './utils/CalcGraphInputsOutputs';
import { toEwoksLinks } from './utils/toEwoksLinks';
import { toEwoksNodes } from './utils/toEwoksNodes';
import { calcNoteNodes } from './utils/calcNoteNodes';
import { getWorkflowsDescriptions, getWorkflow } from './utils/api';

// const { GraphDagre } = dagre.graphlib;
// const NODE_SIZE = { width: 270, height: 36 };

export const ewoksNetwork = {};

export async function getWorkflows(): Promise<WorkflowDescription[]> {
  let res = [];
  try {
    const workflows = await getWorkflowsDescriptions();
    if (workflows && workflows.data) {
      const workf = workflows.data as {
        items: WorkflowDescription[];
      };
      res = workf.items;
      // .sort((a, b) => a.localeCompare(b))
      // .map((work) => {
      //   return { ...work, title: work.label };
      // });
    }
  } catch (error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      // Keep logging in console for debugging when talking with a user
      /* eslint-disable no-console */
      console.log(
        error.response.data,
        error.response.status,
        error.response.headers
      );
    } else if (error.request) {
      // The request was made but no response was received
      /* eslint-disable no-console */
      console.log(error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      /* eslint-disable no-console */
      console.log('Error', error.message);
    }
    /* eslint-disable no-console */
    console.log(error.config);
    res = [{ label: 'network error', category: error?.response?.status }];
  }
  return res;
}

const id = 'graph';
export function createGraph() {
  // server returns the basic structure of a graph
  return {
    graph: {
      id: `${id}1`,
      label: 'newGraph',
      input_nodes: [],
      output_nodes: [],
    },
    nodes: [],
    links: [],
  };
}

export async function getSubgraphs(
  graph: GraphEwoks | GraphRF,
  recentGraphs: GraphRF[]
): Promise<GraphEwoks[]> {
  const nodes: EwoksRFNode[] = [...graph.nodes];
  const existingNodeSubgraphs = nodes.filter(
    (nod) => nod.task_type === 'graph'
  );
  let results = [] as GraphEwoks[];
  if (existingNodeSubgraphs.length > 0) {
    // there are subgraphs -> first search in the recentGraphs for them
    const notInRecent = [];
    existingNodeSubgraphs.forEach((graph) => {
      if (
        recentGraphs.filter((gr) => gr.graph.id === graph.task_identifier)
          .length === 0
      ) {
        // add them in an array to request them from the server
        notInRecent.push(graph.task_identifier);
      }
    });
    // For those that are not in recent get them from the server
    results = await axios
      .all(notInRecent.map((id: string) => getWorkflow(id)))
      .then(
        axios.spread((...res) => {
          // all requests are now complete in an array
          // if there is a null means the subgraph was not found
          // and it should show up in red
          const resCln = res.filter((result) => result.data !== null);
          return resCln.map((result) => result.data) as GraphEwoks[];
        })
      )
      // Uncomment
      .catch((error) => {
        // remove after handling the error
        console.log('AXIOS ERROR', id, error);
        return [];
      });
  }
  return results ? results : [];
}

export function rfToEwoks(tempGraph: GraphRF): GraphEwoks {
  // calculate input_nodes-output_nodes nodes from graphInput-graphOutput
  const graph = calcGraphInputsOutputs(tempGraph);
  const noteNodes = calcNoteNodes(tempGraph);
  graph.uiProps.notes = noteNodes;

  console.log(toEwoksNodes(tempGraph.nodes));

  return {
    graph,
    nodes: toEwoksNodes(tempGraph.nodes),
    links: toEwoksLinks(tempGraph.links),
  };
}

// function getNodeType(isSource: boolean, isTarget: boolean): string {
//   return isSource ? (isTarget ? 'internal' : 'input') : 'output';
// }

// export function positionNodes(nodes: Node[], edges: Edge[]): Node[] {
//   const graph = new GraphDagre();
//   graph.setDefaultEdgeLabel(() => ({}));
//   graph.setGraph({ rankdir: 'LR' });

//   const sourceNodes = new Set();
//   const targetNodes = new Set();

//   edges.forEach((e) => {
//     sourceNodes.add(e.source);
//     targetNodes.add(e.target);
//     graph.setEdge(e.source, e.target);
//   });

//   nodes.forEach((n) => graph.setNode(n.id, { ...NODE_SIZE }));

//   dagre.layout(graph);

//   return nodes.map<Node>((node) => {
//     const { id } = node;
//     const { x, y } = graph.node(id);

//     return {
//       ...node,
//       type: getNodeType(sourceNodes.has(id), targetNodes.has(id)),
//       position: {
//         x: x - NODE_SIZE.width / 2,
//         y: y - NODE_SIZE.height / 2,
//       },
//     };
//   });
// }
