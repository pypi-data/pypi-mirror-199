import type { EwoksNode, EwoksRFNode } from '../types';

function cleanDefaultInputs(default_inputs) {
  return (
    (default_inputs &&
      default_inputs.map((dIn) => {
        return {
          // eslint-disable-next-line unicorn/prefer-number-properties
          name: !isNaN(dIn.name) ? Number(dIn.name) : dIn.name,
          value:
            dIn.value === 'false'
              ? false
              : dIn.value === 'true'
              ? true
              : dIn.value === 'null'
              ? null
              : dIn.value,
        };
      })) ||
    []
  );
}

// EwoksRFNode --> EwoksNode for saving
export function toEwoksNodes(nodes: EwoksRFNode[]): EwoksNode[] {
  const tempNodes: EwoksRFNode[] = [...nodes].filter(
    (nod) => !['graphInput', 'graphOutput', 'note'].includes(nod.task_type)
  );

  return tempNodes.map(
    ({
      id,
      task_type,
      task_identifier,
      // type, exists in EwoksRFNode but is the same as task_type
      inputs_complete,
      task_generator,
      default_inputs,
      default_error_node,
      default_error_attributes,
      data: {
        nodeWidth,
        node_icon,
        label,
        type,
        icon,
        comment,
        moreHandles,
        withImage,
        withLabel,
        colorBorder,
      },
      position,
    }) => {
      if (task_type !== 'graph') {
        return {
          id: id.toString(),
          label,
          task_type,
          task_identifier,
          inputs_complete,
          task_generator: task_generator || null,
          default_error_node,
          default_error_attributes: default_error_node
            ? default_error_attributes
            : null,
          default_inputs: cleanDefaultInputs(default_inputs),
          uiProps: {
            nodeWidth,
            node_icon,
            type,
            icon,
            comment,
            position,
            moreHandles,
            withImage,
            withLabel,
            colorBorder,
          },
        };
      }
      // graphs separately only if a transformation is needed???
      return {
        id: id.toString(),
        label,
        task_type,
        task_identifier,
        // type: task_type,
        inputs_complete,
        task_generator: task_generator || null,
        default_inputs: cleanDefaultInputs(default_inputs),
        default_error_node,
        ddefault_error_attributes: default_error_node
          ? default_error_attributes
          : null,
        uiProps: {
          label,
          type,
          icon,
          comment,
          position,
          moreHandles,
          colorBorder,
          withImage,
          withLabel,
          nodeWidth,
        },
        // inputs: inputsSub,
        // outputs: outputsSub,
        // inputsFlow,
        // inputs: inputsFlow, // for connecting graphically to different input
      };
    }
  );
}
