import type {
  EwoksRFLink,
  EwoksRFNode,
  GraphEwoks,
  GraphRF,
  Task,
} from '../types';
import { toRFEwoksNodes } from '../utils/toRFEwoksNodes';
import { toRFEwoksLinks } from '../utils/toRFEwoksLinks';
import { findAllSubgraphs } from './storeUtils/FindAllSubgraphs';
import configData from '../configData.json';
import { getTaskDescription } from '../utils/api';

// TODO: use the initial graph from store
const initializedGraph = {
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

const workingGraph = (set, get) => ({
  workingGraph: initializedGraph,

  setWorkingGraph: async (
    workingGraph: GraphEwoks,
    source: string
  ): Promise<GraphRF> => {
    // 1. if it is a new graph opening initialize
    if (get().tasks.length === 0) {
      try {
        const tasksData = await getTaskDescription();
        const tasks = tasksData.data as { items: Task[] };
        get().setTasks(tasks.items);
      } catch (error) {
        // console.error('The Promise is rejected!', error);
        get().setOpenSnackbar({
          open: true,
          text: error.response?.data?.message || configData.retrieveTasksError,
          severity: 'error',
        });
      }
    }
    get().setSelectedElement({} as EwoksRFNode | EwoksRFLink);
    get().setSubgraphsStack({ id: 'initialiase', label: '' });

    // TODO: examine if the following initialization is needed any more?
    // get().setGraphRF(get().initializedRFGraph);
    // Is the following needed as to not get existing graphs? Better an empty array?
    get().setRecentGraphs({} as GraphRF, true);

    const newNodeSubgraphs = await findAllSubgraphs(
      workingGraph,
      get().recentGraphs
    );

    // 3. Put the newNodeSubgraphs into recent in their graphRF form (sync)
    newNodeSubgraphs.forEach((gr) => {
      // calculate the rfNodes using the fetched subgraphs
      get().setRecentGraphs({
        graph: gr.graph,
        nodes: toRFEwoksNodes(gr, newNodeSubgraphs, get().tasks),
        links: toRFEwoksLinks(gr, newNodeSubgraphs, get().tasks),
      });
    });

    // 4. Calculate the new graph given the subgraphs
    let grfNodes = toRFEwoksNodes(workingGraph, newNodeSubgraphs, get().tasks);

    // 5. Calculate notes nodes
    const notes =
      (workingGraph.graph.uiProps &&
        workingGraph.graph.uiProps.notes &&
        workingGraph.graph.uiProps?.notes?.map((note) => {
          return {
            data: {
              label: note.label,
              comment: note.comment,
              nodeWidth: note.nodeWidth || 180,
            },
            id: note.id,
            task_type: 'note',
            task_identifier: note.id,
            type: 'note',
            position: note.position,
          };
        })) ||
      ([] as EwoksRFNode[]);

    grfNodes = [...grfNodes, ...notes];

    const graph = {
      graph: {
        ...workingGraph.graph,
        uiProps: { ...workingGraph.graph.uiProps, source },
      },
      nodes: grfNodes,
      links: toRFEwoksLinks(workingGraph, newNodeSubgraphs, get().tasks),
    };

    get().setRecentGraphs(graph as GraphRF);

    // set the new graph as the working graph
    get().setGraphRF(graph as GraphRF);
    get().setSelectedElement(graph.graph);
    // add the new graph to the recent graphs if not already there
    get().setRecentGraphs({
      graph: workingGraph.graph,
      nodes: grfNodes,
      links: toRFEwoksLinks(workingGraph, newNodeSubgraphs, get().tasks),
    });
    get().setSubgraphsStack({
      id: workingGraph.graph.id,
      label: workingGraph.graph.label || workingGraph.graph.id,
    });
    set((state) => ({
      ...state,
      workingGraph: graph,
      undoRedo: [{ action: 'Opened new graph', graph }],
      undoIndex: 0,
    }));
    return graph;
  },
});
export default workingGraph;
