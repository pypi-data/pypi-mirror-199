import type { GraphRF } from '../../../types';

function curateGraph(graphRF: GraphRF): GraphRF {
  const graphRFCurrated = { ...graphRF };
  // INFO: change the workflow id when the label is changed
  // graphRFCurrated.graph.id = graphRFCurrated.graph.label;

  for (const nod of graphRFCurrated.nodes) {
    // INFO: Remove empty lines in table for nodes and links
    // TODO: removes only the last not all empty...
    if (
      nod.default_inputs &&
      nod.default_inputs.length > 0 &&
      nod.default_inputs[nod.default_inputs.length - 1].id === ''
    ) {
      nod.default_inputs.pop();
    }
    if (
      nod.default_error_attributes &&
      nod.default_error_attributes.data_mapping &&
      nod.default_error_attributes.data_mapping.length > 0 &&
      nod.default_error_attributes.data_mapping[
        nod.default_error_attributes.data_mapping.length - 1
      ].id === ''
    ) {
      nod.default_error_attributes.data_mapping.pop();
    }
  }
  for (const lin of graphRFCurrated.links) {
    if (
      lin.data.conditions &&
      lin.data.conditions.length > 0 &&
      lin.data.conditions[lin.data.conditions.length - 1].id === ''
    ) {
      lin.data.conditions.pop();
    }
    if (
      lin.data.data_mapping &&
      lin.data.data_mapping.length > 0 &&
      lin.data.data_mapping[lin.data.data_mapping.length - 1].id === ''
    ) {
      lin.data.data_mapping.pop();
    }
  }

  return graphRFCurrated;
}

export default curateGraph;
