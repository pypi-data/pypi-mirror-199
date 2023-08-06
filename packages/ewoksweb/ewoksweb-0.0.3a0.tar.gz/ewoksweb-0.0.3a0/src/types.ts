// import type { Color } from '@material-ui/lab';
import type { Position } from 'react-flow-renderer';

export interface GraphNodes {
  id: string;
  node: string;
  sub_node?: string;
  link_attributes?: InOutLinkAttributes;
  uiProps?: InOutNodesUiProps;
}

// TODO: examine with ewoks if all the following are needed in an InOutLink
export interface InOutLinkAttributes {
  label: string;
  comment: string;
  conditions: Conditions[];
  data_mapping: DataMapping[];
  map_all_data: boolean;
  on_error: boolean;
}

export interface InOutNodesUiProps {
  label?: string;
  position?: CanvasPosition;
  linkStyle?: string;
  style?: LinkStyle;
  animated?: boolean;
  markerEnd?: '' | { type: string };
  // TODO: the following is not used for now
  markerStart?: { type: string };
  targetHandle?: string;
  withImage?: boolean;
  withLabel?: boolean;
  colorBorder?: string;
  nodeWidth?: number;
}

export interface GraphDetails {
  id: string;
  label?: string;
  category?: string;
  input_nodes?: GraphNodes[];
  output_nodes?: GraphNodes[];
  uiProps?: UiPropsGraph;
}

export interface Graph {
  graph?: GraphDetails;
  nodes: EwoksNode[];
  links: EwoksLink[];
}

export interface SnackbarParams {
  open: boolean;
  text: string;
  severity: string;
}

export interface DialogParams {
  open: boolean;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  content: any; // {title: string; graph: }
}

// I need the EVENTS=[{nodeId, start/end, values: {}}] somewhere and the
// execGraphRF = a graph upon graphRF structure that builds the execution-timeline
// this line has what happened and when = state is in execGraphRF
// Not play it from the beggining to view the state in a specific time-instanse
// for a time-instanse we need
// 1. what nodes were being executing and
// 2. the results until now for the executed
// 3. the way things happened in a timely manner?

// to draw them on links we need to know where it came from? Not possible
// so draw them on node input/output
// stop for one is not the start of another which can wait for other inputs!
// so draw on link on each side the events in a timely manner.

export interface ExecutedWorkflowEvent extends Event {
  status: string;
}

export interface ExecutedJobsResponse {
  jobs: Event[][];
}

export interface Event {
  host_name?: string;
  process_id?: string;
  user_name?: string;
  job_id?: string;
  binding?: string;
  context?: string;
  workflow_id?: string;
  type?: string;
  time?: string;
  error?: string;
  error_message?: string;
  error_traceback?: string;
  node_id?: string;
  task_id?: string;
  progress?: string;
  task_uri?: string;
  input_uris?: [];
  output_uris?: [];
  id?: number;
  nodeId: string;
  event_type: string; // start/stop/progress events
  values: {}; // all values entering or exiting a node
  // for now put static executing here
  executing?: string[];
}

export interface ExecutingState {
  executingNodes: [string];
  executed: [NodeExecutionHistory];
  eventId: string; // the point on the timeline of events is the unique id in this entity
}

// For visuaization
export interface NodeExecutionHistory {
  id: string; // the unique number on the graph 1,2,3
  eventId: string; // find the event for that time-point
  // the ExecutingState can be found through the eventId again
}

export interface State {
  currentExecutionEvent?: number;
  setCurrentExecutionEvent?: (index: number) => void;

  executedEvents?: Event[];
  setExecutedEvents?: (execEvent: Event) => void;

  executingEvents?: Event[];
  setExecutingEvents?: (execEvent: Event, live: boolean) => void;

  executedWorkflows?: Event[][];
  setExecutedWorkflows?: (execEvent: Event[][], live?: boolean) => void;

  watchedWorkflows?: Event[][];
  setWatchedWorkflows?: (execEvent: Event[][]) => void;

  inExecutionMode?: boolean;
  setInExecutionMode?: (val: boolean) => void;

  gettingFromServer?: boolean;
  setGettingFromServer?: (val: boolean) => void;

  undoRedo?: Action[];
  setUndoRedo?: (action: Action) => void;

  undoIndex?: number;
  setUndoIndex?: (index: number) => void;

  tutorial_Graph?: GraphRF;
  initializedGraph?: GraphEwoks;
  initializedRFGraph?: GraphRF;
  initializedTask?: Task;

  tasks?: Task[];
  setTasks?: (tasks: Task[]) => void;

  taskCategories?: string[];
  setTaskCategories?: (tasks: string[]) => void;

  openDraggableDialog?: DialogParams;
  setOpenDraggableDialog?: (params: DialogParams) => void;

  openSettingsDrawer?: string;
  setOpenSettingsDrawer?: (params: string) => void;

  openSnackbar?: SnackbarParams;
  setOpenSnackbar?: (params: SnackbarParams) => void;

  allIcons?: Icon[];
  setAllIcons?: (icons: Icon[]) => void;

  allIconNames?: string[];
  setAllIconNames?: (icons: string[]) => void;
  // { name: string; svgFile?: string; file?: File }[]

  allCategories?: { label: string }[];
  setAllCategories?: (categories: { label: string }[]) => void;

  allWorkflows?: {
    id?: string;
    label?: string;
    category?: string;
  }[];
  setAllWorkflows?: (
    workflows: {
      id?: string;
      label?: string;
      category?: string;
    }[]
  ) => void;

  recentGraphs?: GraphRF[];
  setRecentGraphs?: (graphRF: GraphRF, reset?: boolean) => void;

  graphOrSubgraph?: boolean;
  setGraphOrSubgraph?: (isItGraph: boolean) => void;

  subgraphsStack?: stackGraph[];
  setSubgraphsStack?: (graphRF: stackGraph) => void;

  graphRF?: GraphRF;
  setGraphRF?: (graphRF: GraphRF, isChangeToCanvasGraph?: boolean) => void;

  canvasGraphChanged?: boolean;
  setCanvasGraphChanged?: (isChanged: boolean) => void;

  selectedElement?: EwoksRFNode | EwoksRFLink | GraphDetails;
  setSelectedElement?: (
    element: EwoksRFNode | EwoksRFLink | GraphDetails,
    from?: string,
    update?: boolean
  ) => void;

  selectedTask?: Task;
  setSelectedTask?: (task: Task) => void;

  subGraph?: GraphRF;
  setSubGraph?: (graph: GraphEwoks) => Promise<GraphRF>;

  workingGraph?: GraphRF;
  setWorkingGraph?: (graph: GraphEwoks, source?: string) => Promise<GraphRF>;
}

export interface Action {
  action: string;
  graph: GraphRF;
}

export interface NodeProps {
  nodeWidth?: number;
  withImage?: boolean;
  withLabel?: boolean;
  moreHandles: boolean;
  isGraph: boolean;
  type: string;
  label: string;
  selected: boolean;
  color?: string;
  colorBorder?: string;
  content: React.ReactNode;
  image?: string;
  comment?: string;
  executing?: boolean;
  details?: boolean;
}

export interface Task {
  task_type?: string;
  task_identifier?: string;
  default_inputs?: Inputs[];
  inputs_complete?: boolean;
  task_generator?: string;
  optional_input_names?: string[];
  output_names?: string[];
  required_input_names?: string[];
  icon?: string;
  category?: string;
}

export interface Inputs {
  id?: string;
  name?: string;
  value?: string | boolean;
}

export interface nodeInputsOutputs {
  optional_input_names?: string[];
  output_names?: string[];
  required_input_names?: string[];
}

export interface stackGraph {
  id: string;
  label: string;
}

export interface UiPropsNodes {
  label?: string;
  type?: string;
  icon?: string;
  comment?: string;
  position?: CanvasPosition;
  style?: LinkStyle;
  withImage: boolean;
  withLabel: boolean;
  colorBorder?: string;
  nodeWidth?: number;
  node_icon?: string;
  task_icon?: string;
  task_category?: string;
}

export interface UiPropsLinks {
  label?: string;
  type?: string;
  comment?: string;
  animated?: boolean;
  markerEnd?: '' | { type: string };
  labelBgStyle?: string;
  labelStyle?: string;
  markerStart?: { type: string };
  sourceHandle?: string;
  targetHandle?: string;
  colorLink?: string;
  style?: LinkStyle;
  getAroundProps?: { x?: number; y?: number };
  withImage?: boolean;
  withLabel?: boolean;
  colorBorder?: string;
  nodeWidth?: number;
}

export interface UiPropsGraph {
  label?: string;
  type?: string;
  comment?: string;
  notes?: Note[];
  style?: LinkStyle;
  source: string;
  icon?: string;
}

export interface LinkStyle {
  stroke?: string;
  strokeWidth?: string;
}

export interface Note {
  id?: string;
  label?: string;
  comment: string;
  position: CanvasPosition;
  nodeWidth: number;
}

export interface CanvasPosition {
  x: number;
  y: number;
}

export interface DataMapping {
  source_output?: string | number;
  target_input?: string | number;
  value?: string | boolean;
  id?: string;
  name?: string;
}

export interface Conditions {
  source_output?: string;
  value?: string | boolean;
  id?: string;
  name?: string;
}

export interface DefaultErrorAttributes {
  map_all_data?: boolean;
  data_mapping?: DataMapping[];
}

export interface EwoksNode {
  id: string;
  label?: string;
  category?: string;
  task_type?: string;
  task_identifier?: string;
  default_inputs?: Inputs[];
  inputs_complete?: boolean;
  task_generator?: string;
  default_error_node?: boolean;
  default_error_attributes?: DefaultErrorAttributes;
  uiProps?: UiPropsNodes;
}

export interface EwoksLink {
  id?: string;
  source: string;
  target: string;
  map_all_data: boolean;
  required?: boolean;
  data_mapping?: DataMapping[];
  conditions?: Conditions[];
  on_error?: boolean;
  sub_target?: string;
  sub_source?: string;
  startEnd?: boolean;
  uiProps?: UiPropsLinks;
}

export interface outputsInputsSub {
  label: string;
  type: string;
}

export interface EwoksRFNode {
  id?: string;
  label?: string;
  category?: string;
  task_type?: string;
  type?: string;
  task_identifier?: string;
  task_icon?: string;
  task_category?: string;
  default_inputs?: Inputs[];
  inputs_complete?: boolean;
  task_generator?: string;
  default_error_node?: boolean;
  default_error_attributes?: DefaultErrorAttributes;
  data?: {
    nodeWidth?: number;
    node_icon?: string;
    executing?: boolean;
    exists?: boolean;
    label?: string;
    type?: string;
    inputs?: outputsInputsSub[]; // ?
    outputs?: outputsInputsSub[]; // ?
    icon?: string;
    comment?: string;
    moreHandles?: boolean;
    details?: boolean;
    withImage?: boolean;
    withLabel?: boolean;
    colorBorder?: string;
    map_all_data?: boolean;
  };
  selected?: boolean;
  sourcePosition?: string;
  targetPosition?: string;
  position?: CanvasPosition;
  optional_input_names?: string[];
  output_names?: string[];
  required_input_names?: string[];
  uiProps?: UiPropsNodes;
}

export interface EditableTableRow {
  id: number;
  name: string;
  value: never; // string | number | null | undefined,
  isEditMode: boolean;
  type: string;
}

export interface CustomTableCellProps {
  index: number;
  row: EditableTableRow;
  name: string;
  type: string;
  typeOfValues: string[];
  onChange(e: never, row: EditableTableRow, index: number): void;
}

export interface EwoksRFLink {
  id?: string;
  source: string;
  target: string;
  label?: string;
  data?: {
    label?: string;
    data_mapping?: DataMapping[];
    type?: string;
    comment?: string;
    conditions?: Conditions[];
    on_error?: boolean;
    map_all_data?: boolean;
    required?: boolean;
    sub_target?: string;
    sub_target_attributes?: {};
    sub_source?: string;
    colorLine?: string;
    getAroundProps?: { x?: number; y?: number };
    links_input_names?: string[];
    links_required_output_names?: string[];
    links_optional_output_names?: string[];
  };
  // TODO: see if used and give type to the following
  labelStyle;
  labelBgStyle;
  labelBgPadding;
  labelBgBorderRadius;
  style;
  startEnd?: boolean;
  subtarget?: string;
  subsource?: string;
  uiProps?: UiPropsLinks;
  type?: string;
  markerEnd?: '' | { type: string };
  markerStart?: string;
  animated?: boolean;
  sourceHandle?: string;
  targetHandle?: string;
}

export interface RFLink {
  id?: string;
  source: string;
  target: string;
  label?: string;
  data?: {
    data_mapping?: DataMapping;
    type?: string;
    comment?: string;
    conditions?: Conditions[];
    on_error?: Inputs;
  };
  subtarget?: string;
  subsource?: string;
  uiProps?: UiPropsLinks;
}

export interface RFNode {
  id: string;
  label?: string;
  task_type?: string;
  task_identifier?: string;
  default_inputs?: Inputs[];
  inputs_complete?: boolean;
  task_generator?: string;
  data?: {
    label?: string;
    type?: string;
    inputs?: [string]; // ?
    outputs?: [string]; // ?
    icon?: string;
    comment?: string;
  };
  sourcePosition?: Position;
  targetPosition?: Position;
  position?: CanvasPosition;
}

export interface GraphRF {
  graph?: GraphDetails;
  nodes?: EwoksRFNode[];
  links?: EwoksRFLink[];
}

export interface GraphEwoks {
  graph?: GraphDetails;
  nodes?: EwoksNode[];
  links?: EwoksLink[];
}

export interface IconsNames {
  identifiers: [string];
}

export interface Icon {
  name: string;
  type?: string;
  image?: { data_url?: string };
}

export interface WorkflowDescription {
  id: string;
  label?: string;
  category?: string;
}
