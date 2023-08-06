/* eslint-disable unicorn/prefer-number-properties */
import type { EwoksLink, EwoksRFLink } from '../types';

// EwoksRFLinks --> EwoksLinks for saving
export function toEwoksLinks(links): EwoksLink[] {
  const tempLinks: EwoksRFLink[] = [...links].filter((link) => !link.startEnd);
  // if there are some startEnd links with conditions or any other link_attributes
  // then graph.input_nodes and/or graph.output_nodes needs update
  return tempLinks.map(
    ({
      label,
      source,
      sourceHandle,
      target,
      targetHandle,
      data: {
        comment,
        data_mapping,
        sub_target,
        sub_source,
        map_all_data,
        required,
        conditions,
        on_error,
        getAroundProps,
      },
      type,
      markerEnd,
      labelBgStyle,
      labelStyle,
      style,
      animated,
    }) => {
      const link: EwoksLink = {
        source,
        target,
        data_mapping: data_mapping.map((mapping) => {
          return {
            source_output: !isNaN(mapping.source_output as number)
              ? Number(mapping.source_output)
              : mapping.source_output,
            target_input: !isNaN(mapping.target_input as number)
              ? Number(mapping.target_input)
              : mapping.target_input,
          };
        }),
        conditions: conditions.map((con) => {
          if (con.source_output) {
            return {
              ...con,
              value: calcConditionValue(con),
            };
          }
          return {
            source_output: con.id,
            value: calcConditionValue(con),
          };
        }),
        on_error,
        map_all_data,
        required,
        uiProps: {
          label,
          comment,
          type,
          markerEnd,
          labelBgStyle,
          labelStyle,
          style,
          animated,
          sourceHandle,
          targetHandle,
          getAroundProps,
        },
      };
      if (sub_source) {
        link.sub_source = sub_source;
      }
      if (sub_target) {
        link.sub_target = sub_target;
      }
      return link;
    }
  );
}

function calcConditionValue(condition) {
  return condition.value === 'true'
    ? true
    : condition.value === 'false'
    ? false
    : condition.value === 'null'
    ? null
    : condition.value;
}
