import create from 'zustand';
import type { GraphEwoks, GraphRF, State, Task } from '../types';

import currentExecutionEvent from './currentExecutionEvent';
import gettingFromServer from './gettingFromServer';
import undoRedo from './undoRedo';
import selectedElement from './selectedElement';
import selectedTask from './selectedTask';
import workingGraph from './workingGraph';
import graphRF from './graphRF';
import allWorkflows from './allWorkflows';
import allCategories from './allCategories';
import allIconNames from './allIconNames';
import allIcons from './allIcons';
import executingEvents from './executingEvents';
import executedEvents from './executedEvents';
import graphOrSubgraph from './graphOrSubgraph';
import inExecutionMode from './inExecutionMode';
import openDraggableDialog from './openDraggableDialog';
import openSettingsDrawer from './openSettingsDrawer';
import openSnackbar from './openSnackbar';
import recentGraphs from './recentGraphs';
import subGraph from './subGraph';
import subgraphsStack from './subgraphsStack';
import taskCategories from './taskCategories';
import tasks from './tasks';
import undoIndex from './undoIndex';
import executedWorkflows from './executedWorkflows';
import watchedWorkflows from './watchedWorkflows';
import canvasGraphChanged from './canvasGraphChanged';

const initializedTask: Task = {
  task_identifier: '',
  task_type: '',
  icon: '',
  category: '',
  optional_input_names: [],
  output_names: [],
  required_input_names: [],
};

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
} as GraphEwoks;

const initializedRFGraph = {
  graph: {
    id: 'newGraph',
    label: 'newGraph',
  },
  nodes: [],
  links: [],
} as GraphRF;

const tutorial_Graph = {
  graph: {
    id: 'tutorial_Graph',
    label: 'tutorial_Graph',
    input_nodes: [],
    output_nodes: [],
    uiProps: {},
  },
  nodes: [],
  links: [],
} as GraphRF;

const state = create<State>((set, get) => ({
  ...allIconNames(set),
  ...allIcons(set),
  ...allWorkflows(set),
  ...allCategories(set),
  ...currentExecutionEvent(set),
  ...executedEvents(set, get),
  ...executingEvents(set, get),
  ...executedWorkflows(set),
  ...watchedWorkflows(set, get),
  ...inExecutionMode(set, get),
  ...gettingFromServer(set),
  ...graphOrSubgraph(set),
  ...graphRF(set, get),
  ...canvasGraphChanged(set),
  ...openDraggableDialog(set),
  ...openSettingsDrawer(set),
  ...openSnackbar(set),
  ...recentGraphs(set, get),
  ...subGraph(set, get),
  ...subgraphsStack(set, get),
  ...taskCategories(set),
  ...tasks(set),
  ...undoIndex(set, get),
  ...undoRedo(set, get),
  ...selectedElement(set, get),
  ...selectedTask(set),
  ...workingGraph(set, get),
  initializedTask,
  initializedGraph,
  initializedRFGraph,
  tutorial_Graph,
}));

// @ts-ignore
if (window.Cypress) {
  // @ts-ignore
  window.__state__ = state;
}

export default state;
