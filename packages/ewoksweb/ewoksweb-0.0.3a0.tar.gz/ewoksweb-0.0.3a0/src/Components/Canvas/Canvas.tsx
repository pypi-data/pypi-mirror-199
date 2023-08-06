/* eslint-disable unicorn/consistent-function-scoping */
/* eslint-disable consistent-return */
import React, { useEffect, useState, useCallback, useRef } from 'react';
import ReactFlow, {
  Controls,
  MiniMap,
  Node,
  Edge,
  Background,
  Connection,
  useReactFlow,
  applyNodeChanges,
  applyEdgeChanges,
  useUpdateNodeInternals,
} from 'react-flow-renderer';
import { makeStyles, createStyles } from '@material-ui/core/styles';
import bendingText from 'CustomEdges/BendingTextEdge';
import multilineText from 'CustomEdges/MultilineTextEdge';
import getAround from 'CustomEdges/GetAroundEdge';

import FunctionNode from 'CustomNodes/FunctionNode';
import NoteNode from 'CustomNodes/NoteNode';
import ExecutionStepsNode from 'CustomNodes/ExecutionStepsNode';
import DataNode from 'CustomNodes/DataNode';
import type { GraphRF, EwoksRFNode, EwoksRFLink } from 'types';
import state from 'store/state';
import { calcNewId } from 'utils/calcNewId';
import isValidLink from 'utils/IsValidLink';

const useStyles = makeStyles(() =>
  createStyles({
    root: {
      flexGrow: 1,
    },
  })
);

const edgeTypes = {
  bendingText,
  multilineText,
  getAround,
};

const nodeTypes = {
  executionSteps: ExecutionStepsNode,
  note: NoteNode,
  graph: FunctionNode,
  method: DataNode,
  ppfmethod: DataNode,
  graphInput: DataNode,
  graphOutput: DataNode,
  class: DataNode,
};

function trimLabel(label) {
  if (label.length <= 20) {
    return label;
  }

  return label.split('.').pop();
}

function Canvas() {
  const classes = useStyles();

  const [rfInstance, setRfInstance] = useState(null);
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [prevGraphId, setPrevGraphId] = useState('');

  const reactFlowWrapper = useRef(null);

  const graphRF = state((state) => state.graphRF);
  const setGraphRF = state((state) => state.setGraphRF);
  const setSubgraphsStack = state((state) => state.setSubgraphsStack);
  const subgraphsStack = state((state) => state.subgraphsStack);
  const setRecentGraphs = state((state) => state.setRecentGraphs);
  const setUndoRedo = state((state) => state.setUndoRedo);
  const setSelectedElement = state((state) => state.setSelectedElement);
  const selectedElement = state((state) => state.selectedElement);
  const setSelectedTask = state((state) => state.setSelectedTask);
  const tasks = state((state) => state.tasks);
  const recentGraphs = state((state) => state.recentGraphs);
  const workingGraph = state((state) => state.workingGraph);
  const setOpenSnackbar = state((state) => state.setOpenSnackbar);
  const updateNodeInternals = useUpdateNodeInternals();

  const { fitView, getZoom, zoomTo } = useReactFlow();
  // TODO: when selecting a node-link selected fires the re-render
  // since graphRF changes. We need to not rerender
  // Accosiated edges titles flicker when selecting a node and then select graph
  useEffect(() => {
    setNodes(graphRF.nodes);
    setEdges(graphRF.links);
  }, [graphRF.nodes, graphRF.links]);

  useEffect(() => {
    if ('position' in selectedElement) {
      const timeoutPosition = setTimeout(() => {
        updateNodeInternals(selectedElement.id);
      }, 400);
      return () => clearTimeout(timeoutPosition);
    }
  }, [selectedElement, updateNodeInternals]);

  useEffect(() => {
    if (subgraphsStack[subgraphsStack.length - 1]) {
      setPrevGraphId(subgraphsStack[subgraphsStack.length - 1].id);
    }
  }, [subgraphsStack]);

  useEffect(() => {
    if (prevGraphId !== graphRF.graph.id) {
      setTimeout(() => {
        // DOC: Define a zoom level for small graphs to not show very-big nodes
        if (graphRF.nodes.length > 0 && graphRF.nodes.length < 6) {
          zoomTo(0.6);
        } else if (graphRF.nodes.length > 0) {
          fitView();
        }
        // DOC: the value of the delay is important to fitview even the execution
        // that takes up to 4secs. Possibly rerender after the call to get the workflow??
      }, 1000);
      // DOC: if I clear the timeout for memory leaks the setTImeout never runs fitview???
      // return () => clearTimeout(timer);
    }
  }, [
    graphRF.graph.id,
    fitView,
    getZoom,
    zoomTo,
    graphRF.nodes.length,
    prevGraphId,
  ]);

  const onElementsRemove = useCallback(
    (elementsToRemove) => {
      let newGraph = {} as GraphRF;
      const [el] = elementsToRemove;
      if (el.position) {
        const nodesLinks = graphRF.links.filter(
          (link) => !(link.source === el.id || link.target === el.id)
        );

        newGraph = {
          ...graphRF,
          nodes: graphRF.nodes.filter((nod) => nod.id !== el.id),
          links: nodesLinks,
        };
        setUndoRedo({ action: 'Removed a Node', graph: newGraph });
      } else if (el.source) {
        newGraph = {
          ...graphRF,
          links: graphRF.links.filter((link) => link.id !== el.id),
        };
        setUndoRedo({ action: 'Removed a Link', graph: newGraph });
      }
      setGraphRF(newGraph, true);
    },
    [graphRF, setGraphRF, setUndoRedo]
  );

  const onNodesChange = useCallback(
    (changes) => {
      const node = [...graphRF.nodes].find((el) => el.id === changes[0].id);
      // TODO: nodes are updated only on rf canvas and not on graphRF
      // if we update graphRF we have a loop so we update on setSelectedElement
      // where we set every other selected to false... SOLUTION

      setNodes((ns) => {
        return applyNodeChanges(changes, ns);
      });

      if (changes[0].type === 'remove') {
        onElementsRemove([node]);
      }
    },
    [onElementsRemove, graphRF.nodes]
  );

  const onEdgesChange = useCallback(
    (changes) => {
      const edgeToRemove = graphRF.links.find((el) => el.id === changes[0].id);

      if (changes[0].type === 'remove') {
        onElementsRemove([edgeToRemove]);
      }
      setEdges((es) => applyEdgeChanges(changes, es));
    },
    [onElementsRemove, graphRF.links]
  );

  const onPaneClick = () => {
    setSelectedElement(graphRF.graph);
  };

  const onNodeClick = (event, element?: Node) => {
    const graphElement: EwoksRFNode = nodes.find((el) => el.id === element.id);

    if (
      !(
        graphElement.task_type === 'executionSteps' &&
        graphElement.type === 'executionSteps'
      )
    ) {
      setSelectedElement(graphElement);
    }
  };

  const onEdgeClick = (event, element?: Edge) => {
    const graphElement: EwoksRFLink = edges.find((el) => el.id === element.id);
    setSelectedElement(graphElement);
  };

  const onInit = useCallback((instance) => {
    setRfInstance(instance);
  }, []);

  const onDragOver = (event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  };

  const onDrop = (event) => {
    event.preventDefault();

    if (graphRF.graph.id === '0') {
      setSubgraphsStack({
        id: graphRF.graph.id,
        label: graphRF.graph.label,
      });
    }

    if (workingGraph.graph.id === graphRF.graph.id) {
      const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
      const task_identifier = event.dataTransfer.getData('task_identifier');
      const task_type = event.dataTransfer.getData('task_type');
      const icon = event.dataTransfer.getData('icon');
      const position = rfInstance.project({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });

      let tempTask = tasks.find(
        (tas) => tas.task_identifier === task_identifier
      );
      tempTask = tempTask
        ? tempTask // if you found the Task return it
        : task_type === 'graph' // if not found check if it is a graph ???
        ? tempTask // if a graph return it and if not add some default inputs-outputs
        : {
            optional_input_names: [],
            output_names: [],
            required_input_names: [],
          };

      const newNode = {
        id:
          task_type === 'graphInput'
            ? calcNewId('In', graphRF.nodes)
            : task_type === 'graphOutput'
            ? calcNewId('Out', graphRF.nodes)
            : task_type === 'note'
            ? calcNewId('Note', graphRF.nodes)
            : calcNewId(task_identifier || 'Node', graphRF.nodes),
        // TODO not dublicate label
        label: trimLabel(task_identifier),
        task_type,
        task_identifier,
        type: task_type,
        task_generator: '',
        position,
        default_inputs: [],
        inputs_complete: false,
        default_error_node: false,
        default_error_attributes: {
          map_all_data: true,
          data_mapping: [],
        },
        optional_input_names: tempTask.optional_input_names,
        output_names: tempTask.output_names,
        required_input_names: tempTask.required_input_names,
        data: {
          label: trimLabel(task_identifier),
          type: 'internal',
          icon,
          moreHandles: false,
          nodeWidth: 100,
        },
      };

      const newGraph = {
        graph: graphRF.graph,
        nodes: [...graphRF.nodes, newNode],
        links: graphRF.links,
      } as GraphRF;

      setGraphRF(newGraph, true);
      setUndoRedo({ action: 'Added a Node', graph: newGraph });
      setRecentGraphs(newGraph);
    } else {
      setOpenSnackbar({
        open: true,
        text: 'Not allowed to add a new node to any sub-graph!',
        severity: 'success',
      });
    }
  };

  const onEdgeUpdate = (oldEdge: Edge, newConnection: Connection) => {
    // TODO: it is link: EwoksRFLink but not compatible with Edge?
    const link = {
      ...oldEdge,
      ...newConnection,
    };

    // DOC: if the new link is:
    // 1. attached to a node-handle where there is already a link or
    // 2. is attached to an input-output already connected to a node then
    // edgeUpdate should not happen and a message informs it is not ewoks-compatible

    const { isValid, reason } = isValidLink(newConnection, graphRF, oldEdge);
    if (!isValid) {
      setOpenSnackbar({
        open: true,
        text: reason,
        severity: 'warning',
      });
    } else {
      const newGraph = {
        graph: { ...graphRF.graph },
        nodes: nodes.filter((el) => el.position), // [...graphRF.nodes],
        links: [
          ...edges
            .filter((el) => el.source)
            .filter((lin) => lin.id !== oldEdge.id),
          link,
        ],
      };

      setGraphRF(newGraph as GraphRF, true);
      setUndoRedo({ action: 'Updated a Link', graph: newGraph });
      setRecentGraphs(newGraph as GraphRF);
    }
  };

  const onConnect = (params: Connection) => {
    if (workingGraph.graph.id === graphRF.graph.id) {
      const sourceTask = graphRF.nodes.find((nod) => nod.id === params.source);
      const targetTask = graphRF.nodes.find((nod) => nod.id === params.target);
      // TODO: take link out
      const link = {
        data: {
          getAroundProps: { x: 0, y: 0 },
          on_error: false,
          comment: '',
          // node optional_input_names are link's optional_output_names
          links_optional_output_names: targetTask.optional_input_names || [],
          // node required_input_names are link's required_output_names
          links_required_output_names: targetTask.required_input_names || [],
          // node output_names are link's input_names
          links_input_names: sourceTask.output_names || [],
          conditions: [],
          data_mapping: [],
          map_all_data:
            ['ppfmethod', 'ppfport'].includes(sourceTask.task_type) ||
            ['ppfmethod', 'ppfport'].includes(targetTask.task_type),
          sub_source:
            sourceTask.task_type === 'graph' ? params.sourceHandle : '',
          sub_target:
            targetTask.task_type === 'graph' ? params.targetHandle : '',
        },
        id: `${params.source}:${params.sourceHandle}->${params.target}:${params.targetHandle}`,
        label: '', // `${params.source.slice(0, 6)}->${params.target.slice(0, 6)}`,
        source: params.source,
        target: params.target,
        sourceHandle: params.sourceHandle,
        targetHandle: params.targetHandle,
        type: 'default',
        animated: false,
        markerEnd: { type: 'arrowclosed' },
        style: { stroke: '#96a5f9', strokeWidth: '2.5' },
        labelBgStyle: {
          fill: 'rgb(223, 226, 247)',
          color: 'rgb(50, 130, 219)',
          fillOpacity: 1,
        },
        labelBgPadding: [8, 4],
        labelBgBorderRadius: 4,
        labelStyle: { fill: 'blue', fontWeight: 500, fontSize: 14 },
        startEnd:
          sourceTask.task_type === 'graphInput' ||
          targetTask.task_type === 'graphOutput',
      };

      const newGraph = {
        graph: graphRF.graph,
        nodes: graphRF.nodes,
        links: [...graphRF.links, link], // addEdge(params, graphRF.links),
      };
      // setElements((els) => addEdge(params, els));
      setGraphRF(newGraph as GraphRF, true);
      // need to also save it in recentGraphs if we leave and come back                // className={classes.openFileButton} to the graph?
      setRecentGraphs(newGraph as GraphRF);

      // add action and new GraphRF to undo-redo array
      setUndoRedo({ action: 'new Link', graph: newGraph as GraphRF });
    } else {
      setOpenSnackbar({
        open: true,
        text: 'Not allowed to create new links to any sub-graph!',
        severity: 'success',
      });
    }
  };

  const onPaneContextMenu = (event) => {
    event.preventDefault();
    setOpenSnackbar({
      open: true,
      text: 'Open a graph and click on nodes and links on this Canvas!',
      severity: 'success',
    });
  };

  const onNodeDoubleClick = (event, node) => {
    event.preventDefault();
    const nodeTmp = graphRF.nodes.find((el) => el.id === node.id);
    if (nodeTmp.task_type === 'graph') {
      // if type==graph get the subgraph from the recentGraphs
      const subgraph = recentGraphs.find(
        (gr) => gr.graph.id === nodeTmp.task_identifier
      );
      if (subgraph && subgraph.graph.id) {
        setGraphRF(subgraph);
        setSubgraphsStack({
          id: subgraph.graph.id,
          label: subgraph.graph.label,
        });
      } else {
        setOpenSnackbar({
          open: true,
          text: 'Seems the specific subgraph cannot be located!',
          severity: 'error',
        });
      }
    } else {
      nodeTmp.data['details'] = true;
      setSelectedElement({
        ...nodeTmp,
        data: { ...nodeTmp.data, details: true },
      } as EwoksRFNode);
    }
  };

  const onSelectionDragStart = (event) => {
    event.preventDefault();
  };

  const onSelectionDrag = (event) => {
    event.preventDefault();
  };

  const onSelectionDragStop = (event, selectedElements) => {
    event.preventDefault();
    if (workingGraph.graph.id === graphRF.graph.id) {
      // DOC: find selectedElements and update its position and save grapRF
      const newElements = [];
      const newElementsIds = [];
      selectedElements.forEach((el) => {
        const rfNode = { ...graphRF.nodes.find((nod) => nod.id === el.id) };
        rfNode.position = el.position;
        newElements.push(rfNode);
        newElementsIds.push(rfNode.id);
      });

      const newGraph = {
        graph: graphRF.graph,
        nodes: [
          ...graphRF.nodes.filter((nod) => !newElementsIds.includes(nod.id)),
          ...newElements,
        ],
        links: graphRF.links,
      };

      setGraphRF(newGraph as GraphRF, true);
      setUndoRedo({
        action: 'Dragged a selection',
        graph: newGraph as GraphRF,
      });
      setRecentGraphs(newGraph);
    } else {
      setOpenSnackbar({
        open: true,
        text: 'Any positional change in any subgraph wont be saved!',
        severity: 'warning',
      });
    }
  };

  const onNodeDragStop = (event, node) => {
    event.preventDefault();
    if (workingGraph.graph.id === graphRF.graph.id) {
      // DOC: find RFEwoksNode and update its position and save grapRF
      const RFEwoksNode: EwoksRFNode = {
        ...graphRF.nodes.find((nod) => nod.id === node.id),
      };
      RFEwoksNode.position = node.position;
      const newGraph: GraphRF = {
        graph: graphRF.graph,
        nodes: [
          ...graphRF.nodes.filter((nod) => nod.id !== node.id),
          RFEwoksNode,
        ],
        links: graphRF.links,
      };

      setGraphRF(newGraph, true);
      setUndoRedo({ action: 'Dragged a Node', graph: newGraph });
      // need to also save it in recentGraphs if we leave and come back to the graph?
      setRecentGraphs(newGraph);
    } else {
      setOpenSnackbar({
        open: true,
        text: 'Any positional change in any subgraph wont be saved!',
        severity: 'warning',
      });
    }
  };

  const onClick = () => {
    setSelectedTask({});
  };

  const handleKeyDown = (event) => {
    const charCode = String.fromCharCode(event.which).toLowerCase();

    const keys = event.ctrlKey || event.metaKey;
    if (keys && charCode === 'v') {
      event.preventDefault();
      event.stopPropagation();
      if ('position' in selectedElement) {
        const newClone = {
          ...selectedElement,
          id: calcNewId(selectedElement.id, graphRF.nodes),
          selected: false,
          position: {
            x: selectedElement.position.x + 100,
            y: selectedElement.position.y + 100,
          },
        };
        setGraphRF(
          {
            ...graphRF,
            nodes: [...graphRF.nodes, newClone],
          },
          true
        );
        setSelectedElement(newClone as EwoksRFNode);
      } else {
        setOpenSnackbar({
          open: true,
          text: 'Clone is for cloning nodes within the working workflow',
          severity: 'warning',
        });
      }
    }
  };

  return (
    <div
      className={classes.root}
      onKeyDown={handleKeyDown}
      role="button"
      tabIndex={0}
    >
      <div
        className="reactflow-wrapper"
        style={{
          height: '100%',
          width: '100%',
          backgroundColor: '#e9ebf7',
        }}
        ref={reactFlowWrapper}
      >
        <ReactFlow
          fitView
          connectOnClick
          nodesDraggable
          attributionPosition="bottom-right"
          // defaultPosition={[-200, -200]}
          minZoom={0.2}
          snapToGrid
          nodes={nodes}
          edges={edges}
          onNodeClick={(evt, node) => {
            onNodeClick(evt, node);
          }}
          onEdgeClick={(evt, node) => {
            onEdgeClick(evt, node);
          }}
          onPaneClick={onPaneClick}
          onClick={onClick}
          onInit={onInit}
          onDrop={onDrop}
          onConnect={onConnect}
          onEdgeUpdate={onEdgeUpdate}
          onDragOver={onDragOver}
          onPaneContextMenu={onPaneContextMenu}
          onNodeDoubleClick={onNodeDoubleClick}
          onSelectionDragStop={onSelectionDragStop}
          onSelectionDragStart={onSelectionDragStart}
          onSelectionDrag={onSelectionDrag}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeDragStop={onNodeDragStop}
          edgeTypes={edgeTypes}
          nodeTypes={nodeTypes}
          deleteKeyCode="Delete"
        >
          <Background />
          <Controls />
          <MiniMap
            nodeStrokeColor={(n): string => {
              if (n.style?.background) {
                return n.style.background as string;
              }
              if (['graphOutput', 'graphInput'].includes(n.type)) {
                return '#0041d0';
              }
              if (n.type === 'graph') {
                return '#ff0072';
              }
              return 'rgb(60, 81, 202)';
            }}
            nodeColor={(n): string => {
              if (n.style?.background) {
                return n.style.background as string;
              }
              if (['graphOutput', 'graphInput'].includes(n.type)) {
                return 'rgb(223, 226, 247)';
              }
              if (n.type === 'graph') {
                return 'rgba(244, 179, 131, 0.87)';
              }

              return 'rgb(60, 81, 202)';
            }}
            nodeBorderRadius={2}
          />
        </ReactFlow>
      </div>
    </div>
  );
}

export default Canvas;
