import type { EwoksRFNode, GraphEwoks, Task } from '../types';
import { inNodesLinks } from './inNodesLinks';
import { outNodesLinks } from './outNodesLinks';
import existsOrValue from './existsOrValue';
import {
  inputsAll,
  outputsAll,
  calcNodeType,
  addNodeProperties,
} from './toRFEwoksNodesUtils';

// Accepts a GraphEwoks and returns an EwoksRFNode[]
export function toRFEwoksNodes(
  tempGraph: GraphEwoks,
  newNodeSubgraphs: GraphEwoks[],
  tasks: Task[]
): EwoksRFNode[] {
  // Find input and output nodes of the graph
  const inputsAl = inputsAll(tempGraph);

  const outputsAl = outputsAll(tempGraph);

  const inNodeLinks = inNodesLinks(tempGraph);
  const outNodeLinks = outNodesLinks(tempGraph);

  const inOutTempGraph = { ...tempGraph };

  if (inNodeLinks.nodes.length > 0) {
    inOutTempGraph.nodes = [...inOutTempGraph.nodes, ...inNodeLinks.nodes];
  }

  if (outNodeLinks.nodes.length > 0) {
    inOutTempGraph.nodes = [...inOutTempGraph.nodes, ...outNodeLinks.nodes];
  }

  if (inOutTempGraph.nodes) {
    return inOutTempGraph.nodes.map(
      ({
        id,
        task_type,
        task_identifier,
        label,
        default_inputs,
        inputs_complete,
        default_error_node,
        default_error_attributes,
        task_generator,
        uiProps,
      }) => {
        const nodeType = calcNodeType(inputsAl, outputsAl, task_type, id);

        const node: EwoksRFNode = {
          id: id.toString(),
          task_type,
          task_identifier,
          type: task_type,
          inputs_complete: inputs_complete || false,
          default_error_node: default_error_node || false,
          default_error_attributes: default_error_attributes || {
            map_all_data: true,
            data_mapping: [],
          },
          task_generator: task_generator || '',
          task_icon: uiProps.task_icon || '',
          default_inputs: default_inputs || [],
          data: {
            label: label
              ? label
              : uiProps && uiProps.label
              ? uiProps.label
              : task_identifier,
            type: nodeType,
            nodeWidth: existsOrValue(uiProps, 'nodeWidth', 120),
            icon: uiProps.node_icon
              ? uiProps.node_icon
              : existsOrValue(uiProps, 'icon', ''),
            comment: existsOrValue(uiProps, 'comment', ''),
            moreHandles: existsOrValue(uiProps, 'moreHandles', false),
            details: existsOrValue(uiProps, 'details', false),
            executing: false,
            withImage: existsOrValue(uiProps, 'withImage', true),
            withLabel: existsOrValue(uiProps, 'withLabel', true),
            colorBorder: existsOrValue(uiProps, 'colorBorder', ''),
          },
          position: existsOrValue(uiProps, 'position', { x: 100, y: 100 }),
        };

        return addNodeProperties(
          task_type,
          newNodeSubgraphs,
          task_identifier,
          node,
          tasks,
          uiProps.task_category
        );
      }
    );
  }

  return [] as EwoksRFNode[];
}
