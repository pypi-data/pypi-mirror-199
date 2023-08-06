import type { EwoksLink, EwoksNode, GraphEwoks, GraphNodes } from '../types';
import existsOrValue from './existsOrValue';

function calcMarkerEnd(inNod: GraphNodes): '' | { type: string } {
  let type: '' | { type: string };
  if (
    typeof inNod.uiProps?.markerEnd === 'object' &&
    'type' in inNod.uiProps.markerEnd
  ) {
    type = { type: inNod.uiProps.markerEnd.type };
  } else {
    type = '';
  }
  return type;
}

// TODO: merge with outNodesLinks if possible when stable
// DOC: calc the input nodes and links that need to be added to the graph from
// the input_nodes in the Ewoks json
export function inNodesLinks(
  graph: GraphEwoks
): { nodes: EwoksNode[]; links: EwoksLink[] } {
  const inputs: { nodes: EwoksNode[]; links: EwoksLink[] } = {
    nodes: [],
    links: [],
  };
  if (
    graph.graph &&
    graph.graph.input_nodes &&
    graph.graph.input_nodes.length > 0
  ) {
    const inNodesInputed = [];
    graph.graph.input_nodes.forEach((inNod) => {
      const nodeTarget = graph.nodes.find((no) => no.id === inNod.node);
      if (nodeTarget) {
        const temPosition = existsOrValue(inNod.uiProps, 'position', {
          x: 50,
          y: 50,
        });

        if (!inNodesInputed.includes(inNod.id)) {
          inputs.nodes.push({
            id: inNod.id,
            label: existsOrValue(inNod.uiProps, 'label', inNod.id),
            task_type: 'graphInput',
            task_identifier: 'Start-End',
            uiProps: {
              type: 'input',
              position: temPosition,
              icon: 'graphInput',
              withImage: existsOrValue(inNod.uiProps, 'withImage', true),
              withLabel: existsOrValue(inNod.uiProps, 'withLabel', true),
              colorBorder: existsOrValue(inNod.uiProps, 'colorBorder', ''),
              nodeWidth: existsOrValue(inNod.uiProps, 'nodeWidth', 110),
            },
          });
          inNodesInputed.push(inNod.id);
        }

        inputs.links.push({
          startEnd: true,
          source: inNod.id,
          target: inNod.node,
          sub_target: nodeTarget.task_type !== 'graph' ? '' : inNod.sub_node,
          conditions: existsOrValue(inNod.link_attributes, 'conditions', []),
          data_mapping: existsOrValue(
            inNod.link_attributes,
            'data_mapping',
            []
          ),
          on_error: existsOrValue(inNod.link_attributes, 'on_error', false),
          map_all_data: existsOrValue(
            inNod.link_attributes,
            'map_all_data',
            false
          ),
          uiProps: {
            label: existsOrValue(inNod.link_attributes, 'label', ''),
            comment: existsOrValue(inNod.link_attributes, 'comment', ''),
            style: {
              stroke: existsOrValue(inNod.uiProps?.style, 'stroke', ''),
            },
            type: existsOrValue(inNod.uiProps, 'linkStyle', 'default'),
            markerEnd: calcMarkerEnd(inNod),
            animated: existsOrValue(inNod.uiProps, 'animated', false),
            withImage: existsOrValue(inNod.uiProps, 'withImage', true),
            withLabel: existsOrValue(inNod.uiProps, 'withLabel', true),
            colorBorder: existsOrValue(inNod.uiProps, 'colorBorder', ''),
            nodeWidth: existsOrValue(inNod.uiProps, 'nodeWidth', 110),
          },
        });
      }
    });
  }
  return inputs;
}
