import type { EwoksNode, GraphEwoks, Task } from '../types';

// find the outputs-inputs from the connected nodes
export function calcTasksForLink(
  tempGraph: GraphEwoks,
  source: string,
  target: string,
  newNodeSubgraphs,
  tasks: Task[]
): Task[] {
  const sourceTmp = tempGraph.nodes.find((nod) => nod.id === source);
  const targetTmp = tempGraph.nodes.find((nod) => nod.id === target);

  let sourceTask = {} as Task;
  let targetTask = {} as Task;

  if (sourceTmp) {
    sourceTask = calcTask('source', sourceTmp, tasks, newNodeSubgraphs);
  }

  if (targetTmp) {
    targetTask = calcTask('target', targetTmp, tasks, newNodeSubgraphs);
  }

  // if not found app does not break, put an empty skeleton
  sourceTask = sourceTask || {
    output_names: [],
  };
  targetTask = targetTask || {
    optional_input_names: [],
    required_input_names: [],
  };

  return [sourceTask, targetTask];
}

function calcTask(
  sourceOrTarget: 'source' | 'target',
  node: EwoksNode,
  tasks: Task[],
  newNodeSubgraphs: GraphEwoks[]
) {
  let task = {} as Task;

  if (node.task_type !== 'graph') {
    task = tasks.find((tas) => tas.task_identifier === node.task_identifier);
  } else {
    const subgraphNodeSource = newNodeSubgraphs.find(
      (subGr) => subGr.graph.id === node.task_identifier
    );

    const outputsOrOutputs = [];

    if (subgraphNodeSource) {
      subgraphNodeSource.graph.output_nodes.forEach((out) =>
        outputsOrOutputs.push(out.id)
      );
    }

    if (sourceOrTarget === 'source') {
      task = {
        task_type: node.task_type,
        task_identifier: node.task_identifier,
        output_names: outputsOrOutputs,
      };
    } else if (sourceOrTarget === 'target') {
      task = {
        task_type: node.task_type,
        task_identifier: node.task_identifier,
        optional_input_names: outputsOrOutputs,
        required_input_names: [],
      };
    }
  }
  return task;
}
