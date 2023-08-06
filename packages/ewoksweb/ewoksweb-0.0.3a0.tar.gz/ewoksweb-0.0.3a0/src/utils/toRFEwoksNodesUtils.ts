import type { EwoksRFNode, GraphEwoks, GraphNodes, Task } from '../types';

export function inputsAll(tempGraph: GraphEwoks): string[] {
  return tempGraph.graph?.input_nodes?.map((nod) => nod.node);
}

export function outputsAll(tempGraph: GraphEwoks): string[] {
  return tempGraph.graph?.output_nodes?.map((nod) => nod.node);
}

// calculate if node input and/or output or internal
export function calcNodeType(
  inputsAl: string[],
  outputsAll: string[],
  task_type: string,
  id: string
): string {
  const isInput = inputsAl && inputsAl.includes(id);
  const isOutput = outputsAll && outputsAll.includes(id);
  let nodeType = '';
  if (isInput && isOutput) {
    nodeType = 'input_output';
  } else if (isInput) {
    nodeType = 'input';
  } else if (isOutput) {
    nodeType = 'output';
  } else if (task_type === 'graphInput') {
    nodeType = 'graphInput';
  } else if (task_type === 'graphOutput') {
    nodeType = 'graphOutput';
  } else {
    nodeType = 'internal';
  }
  return nodeType;
}

// locate the task and add required+optional-inputs + outputs
export function calcTask(
  tasks: Task[],
  task_identifier: string,
  task_type: string
): Task {
  let tempTask = tasks.find((tas) => tas.task_identifier === task_identifier);

  tempTask = tempTask
    ? tempTask // if you found the Task return it
    : task_type === 'graph' // if not found check if it is a graph
    ? tempTask // if a graph return it and if not add some default inputs-outputs
    : {
        optional_input_names: [],
        output_names: [],
        required_input_names: [],
      };
  return tempTask;
}

interface calcInOutForSubgraphOutput {
  id: string;
  label: string;
  type: string;
  positionY?: number;
}

export function calcInOutForSubgraph(
  subgraphNode: GraphEwoks
): calcInOutForSubgraphOutput[][] {
  let inputsSub: calcInOutForSubgraphOutput[] = [];
  let outputsSub: calcInOutForSubgraphOutput[] = [];

  if (subgraphNode && subgraphNode.graph?.id) {
    const allOutputsIds = subgraphNode.graph.output_nodes.map((nod) => nod.id);
    const allInputsIds = subgraphNode.graph.input_nodes.map((nod) => nod.id);

    inputsSub = subgraphNode.graph.input_nodes.map((input) => {
      allInputsIds.shift();

      return {
        id: input.id,
        label: calcLabel(input, allInputsIds),
        type: 'data ',
        positionY: input.uiProps?.position?.y || 100,
      };
    });

    outputsSub = subgraphNode.graph.output_nodes.map((output) => {
      allOutputsIds.shift();

      return {
        id: output.id,
        label: calcLabel(output, allOutputsIds),
        type: 'data ',
        positionY: output.uiProps?.position?.y || 100,
      };
    });
  } else {
    inputsSub = [{ id: '', label: 'unknown_input', type: 'data' }];
    outputsSub = [{ id: '', label: 'unknown_output', type: 'data' }];
  }
  return [inputsSub, outputsSub];
}

export function calcLabel(
  inOut: GraphNodes,
  allInOutputsIds: string[]
): string {
  return `${('uiProps' in inOut && inOut.uiProps.label) || inOut.id}${
    allInOutputsIds.includes(inOut.id) ? '_' : ':'
  } ${inOut.node} ${inOut.sub_node ? `  -> ${inOut.sub_node}` : ''}`;
}

export function addNodeProperties(
  task_type: string,
  newNodeSubgraphs: GraphEwoks[],
  task_identifier: string,
  node: EwoksRFNode,
  tasks: Task[],
  task_category: string
): EwoksRFNode {
  let tempNode = { ...node };
  if (task_type === 'graph') {
    const subgraphNode: GraphEwoks = newNodeSubgraphs.find(
      (subGr) => subGr.graph.id === task_identifier
    );

    const [inputsSub, outputsSub] = calcInOutForSubgraph(subgraphNode);

    tempNode = {
      ...tempNode,
      data: {
        ...tempNode.data,
        exists: subgraphNode && !!subgraphNode.graph.id,
        inputs: inputsSub,
        outputs: outputsSub,
      },
    };
  } else {
    // locate the task and add required+optional-inputs + outputs
    const tempTask = calcTask(tasks, task_identifier, task_type);

    tempNode = {
      ...tempNode,
      task_category: task_category || '',
      optional_input_names: tempTask.optional_input_names,
      output_names: tempTask.output_names,
      required_input_names: tempTask.required_input_names,
    };
  }

  return tempNode;
}
