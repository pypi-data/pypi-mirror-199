import type {
  Conditions,
  DataMapping,
  EwoksRFLink,
  GraphEwoks,
  Task,
  UiPropsLinks,
} from '../types';
import { inNodesLinks } from './inNodesLinks';
import { outNodesLinks } from './outNodesLinks';
import { calcTasksForLink } from './calcTasksForLink';
import existsOrValue from './existsOrValue';

// DOC: from GraphEwoks get EwoksRFLinks
// - tempGraph: the graph to transform its links
// - newNodeSubgraphs: the subgraphs located in the supergraph.
export function toRFEwoksLinks(
  tempGraph: GraphEwoks,
  newNodeSubgraphs: GraphEwoks[],
  tasks: Task[]
): EwoksRFLink[] {
  let id = 0;

  // DOC: calculate the links from inputs-outputs of the Ewoks graph
  const inOutTempGraph = calcInOutLinks(tempGraph);

  if (inOutTempGraph.links) {
    return inOutTempGraph.links.map(
      ({
        source,
        target,
        data_mapping = [],
        sub_target,
        sub_source,
        on_error,
        conditions,
        map_all_data,
        required,
        uiProps,
        startEnd,
      }) => {
        const [sourceTask, targetTask] = calcTasksForLink(
          tempGraph,
          source,
          target,
          newNodeSubgraphs,
          tasks
        );
        const color =
          (uiProps && uiProps.style && uiProps.style.stroke) ||
          'rgb(60, 81, 202)';

        return {
          id: `${source}:${
            existsOrValue(uiProps, 'sourceHandle', '') as string
          }->${target}:${
            existsOrValue(uiProps, 'targetHandle', '') as string
          }_${id++}`,
          label: calcLabel(uiProps, conditions, data_mapping),
          source: source.toString(),
          target: target.toString(),
          // TODO: is the following used for inputs-outputs?
          startEnd: startEnd || false,
          targetHandle: calcTargetHandle(uiProps, sub_target),
          sourceHandle: calcSourceHandle(uiProps, sub_source),
          type: (uiProps && uiProps.type) || '',
          markerEnd: existsOrValue(uiProps, 'markerEnd', ''),
          animated: existsOrValue(uiProps, 'animated', false),
          style: {
            stroke:
              (uiProps && uiProps.style && uiProps.style.stroke) || '#96a5f9',
            strokeWidth: '3',
          },
          labelBgStyle: {
            fill: 'rgb(223, 226, 247)',
            fillOpacity: 1,
            strokeWidth: 3,
            stroke: color,
          },
          labelBgPadding: [8, 4],
          labelBgBorderRadius: 4,
          labelStyle: {
            color,
            fill: color,
            fontWeight: 500,
            fontSize: 14,
          },
          data: {
            getAroundProps: (uiProps && uiProps.getAroundProps) || {
              x: 0,
              y: 0,
            },
            // DOC: node optional_input_names are link's optional_output_names
            links_optional_output_names: targetTask.optional_input_names || [],
            // DOC: node required_input_names are link's required_output_names
            links_required_output_names: targetTask.required_input_names || [],
            // DOC: node output_names are link's input_names
            links_input_names: sourceTask.output_names || [],
            data_mapping,
            required: required || false,
            sub_target: sub_target || '',
            sub_source: sub_source || '',
            conditions: conditions || [],
            map_all_data: !!map_all_data,
            on_error: on_error || false,
            comment: existsOrValue(uiProps, 'comment', ''),
          },
        };
      }
    );
  }
  return [] as EwoksRFLink[];
}

function calcLabel(
  uiProps: UiPropsLinks,
  conditions: Conditions[],
  data_mapping: DataMapping[]
): string {
  return uiProps && uiProps.label
    ? uiProps.label
    : conditions && conditions.length > 0
    ? conditions.map((el) => `${el.source_output}->${el.value}`).join(', ')
    : data_mapping && data_mapping.length > 0
    ? data_mapping
        .map((el) => `${el.source_output}->${el.target_input}`)
        .join(', ')
    : '';
}

function calcTargetHandle(uiProps: UiPropsLinks, sub_target: string): string {
  return uiProps?.targetHandle
    ? uiProps.targetHandle
    : sub_target
    ? sub_target
    : 'tl';
}

function calcSourceHandle(uiProps: UiPropsLinks, sub_source: string): string {
  return uiProps && uiProps.sourceHandle
    ? uiProps.sourceHandle
    : sub_source
    ? sub_source
    : 'sr';
}

function calcInOutLinks(tempGraph: GraphEwoks): GraphEwoks {
  // DOC: calculate the links from inputs-outputs of the Ewoks graph
  const inNodeLinks = inNodesLinks(tempGraph);
  const outNodeLinks = outNodesLinks(tempGraph);

  // DOC: accumulate all links inOutTempGraph
  const inOutTempGraph: GraphEwoks = { ...tempGraph };
  if (inNodeLinks.links.length > 0) {
    inOutTempGraph.links = [...inOutTempGraph.links, ...inNodeLinks.links];
  }
  if (outNodeLinks.links.length > 0) {
    inOutTempGraph.links = [...inOutTempGraph.links, ...outNodeLinks.links];
  }

  return inOutTempGraph;
}
