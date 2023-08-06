import type {
  EwoksRFLink,
  EwoksRFNode,
  GraphDetails,
  GraphNodes,
  GraphRF,
} from '../types';
import existsOrValue from './existsOrValue';

// Calculate the ewoks input_nodes and output_nodes within the graph
// from the nodes of the graphRF model with types graphInput, graphOutput
export function calcGraphInputsOutputs(graph: GraphRF): GraphDetails {
  const graph_links = [...graph.links];
  let input_nodes = [];
  let output_nodes = [];

  graph.nodes.forEach((nod) => {
    if (nod.task_type === 'graphInput') {
      input_nodes = [
        ...input_nodes,
        ...calcInOutNodes('graphInput', graph, nod, graph_links),
      ];
    } else if (nod.task_type === 'graphOutput') {
      output_nodes = [
        ...output_nodes,
        ...calcInOutNodes('graphOutput', graph, nod, graph_links),
      ];
    }
  });
  return {
    id: graph.graph.id,
    label: graph.graph.label || graph.graph.id,
    category: graph.graph.category || '',
    input_nodes,
    output_nodes,
    uiProps: graph.graph.uiProps,
  };
}

function calcInOutNodes(
  inputOrOutput: string,
  graph: GraphRF,
  nod: EwoksRFNode,
  graph_links: EwoksRFLink[]
): GraphNodes[] {
  const nodes: GraphNodes[] = [];

  let nodesNamesConnectedTo: string[] = [];
  if (inputOrOutput === 'graphInput') {
    // find those nodes this INPUT node is connected to
    nodesNamesConnectedTo = graph.links
      .filter((link) => link.source === nod.id)
      .map((link) => link.target);
  } else if (inputOrOutput === 'graphOutput') {
    // find those nodes this OUTPUT node is connected to
    nodesNamesConnectedTo = graph.links
      .filter((link) => link.target === nod.id) // !!
      .map((link) => link.source); // !!
  }

  const nodeObjConnectedTo: EwoksRFNode[] = [];
  for (const nodesNames of nodesNamesConnectedTo) {
    nodeObjConnectedTo.push(graph.nodes.find((node) => nodesNames === node.id));
  }

  // iterate the nodes to create the new input_nodes
  nodeObjConnectedTo.forEach((nodConnected) => {
    const link_index =
      inputOrOutput === 'graphOutput'
        ? graph_links.findIndex(
            (lin) => lin.target === nod.id && lin.source === nodConnected.id // !!
          )
        : graph_links.findIndex(
            (lin) => lin.source === nod.id && lin.target === nodConnected.id
          );

    if (nodConnected.task_type === 'graph') {
      // find the link and get the sub_node it is connected to in the graph
      nodes.push(
        calcNodeProps(
          true,
          nod,
          nodConnected,
          graph_links,
          link_index,
          inputOrOutput
        )
      );
    } else {
      nodes.push(
        calcNodeProps(
          false,
          nod,
          nodConnected,
          graph_links,
          link_index,
          inputOrOutput
        )
      );
    }
  });
  return nodes;
}

function calcMarkerEnd(graph_link) {
  return graph_link?.markerEnd ? { type: graph_link?.markerEnd?.type } : '';
}

function calcNodeProps(
  isGraph: boolean,
  nod: EwoksRFNode,
  nodConnected: EwoksRFNode,
  graph_links: EwoksRFLink[],
  link_index: number,
  inputOrOutput: string
): GraphNodes {
  return {
    id: nod.id,
    node: nodConnected.id,

    sub_node: isGraph
      ? (graph_links[link_index] && inputOrOutput === 'graphOutput'
          ? graph_links[link_index].data.sub_source
          : graph_links[link_index].data.sub_target) || // !!
        null
      : null,
    link_attributes: {
      label: existsOrValue(graph_links[link_index], 'label', ''),
      comment: existsOrValue(graph_links[link_index]?.data, 'comment', ''),
      conditions: graph_links[link_index]?.data?.conditions || [],
      data_mapping: graph_links[link_index]?.data?.data_mapping || [],
      map_all_data: graph_links[link_index]?.data?.map_all_data || false,
      on_error: graph_links[link_index]?.data?.on_error || false,
    },
    uiProps: {
      position: nod.position,
      label: nod.data.label,
      linkStyle: graph_links[link_index]?.type || 'default',
      style: {
        stroke: graph_links[link_index]?.style?.stroke || '',
        strokeWidth: '3',
      },
      markerEnd: calcMarkerEnd(graph_links[link_index]),
      animated: graph_links[link_index]?.animated || false,
      withImage: 'withImage' in nod.data ? nod.data.withImage : true,
      withLabel: 'withLabel' in nod.data ? nod.data.withLabel : true,
      colorBorder: nod.data.colorBorder,
      nodeWidth: nod.data.nodeWidth,
    },
  };
}
