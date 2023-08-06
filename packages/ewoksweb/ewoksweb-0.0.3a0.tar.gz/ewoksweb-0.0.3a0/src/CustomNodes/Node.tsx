/* eslint-disable react/function-component-definition */
/* jshint sub:true*/
/* eslint-disable sonarjs/cognitive-complexity */
import React, { memo, useEffect, useState } from 'react';
import orange1 from '../images/orange1.png';
import orange2 from '../images/orange2.png';
import orange3 from '../images/orange3.png';
import AggregateColumns from '../images/AggregateColumns.svg';
import Continuize from '../images/Continuize.svg';
import graphInput from '../images/graphInput.svg';
import right from '../images/right.svg';
import left from '../images/left.svg';
import up from '../images/up.svg';
import down from '../images/down.svg';
import graphOutput from '../images/graphOutput.svg';
import Correlations from '../images/Correlations.svg';
import CreateClass from '../images/CreateClass.svg';
import { Handle, Position } from 'react-flow-renderer';
import type { EwoksRFNode, NodeProps } from '../types';
import { contentStyle, style } from './NodeStyle';
import Tooltip from '@material-ui/core/Tooltip';
import ExecuteSpinner from '../Components/Execution/ExecuteSpinner';
import isValidLink from '../utils/IsValidLink';
import FileCopyIcon from '@material-ui/icons/FileCopy';
import EditIcon from '@material-ui/icons/EditOutlined';
import SaveIcon from '@material-ui/icons/Save';
import { calcNewId } from '../utils/calcNewId';

import state from '../store/state';
import { IconButton, TextField } from '@material-ui/core';
import tooltipText from '../Components/General/TooltipText';

const iconsObj = {
  'left.svg': left,
  left,
  'right.svg': right,
  right,
  'up.svg': up,
  up,
  'down.svg': down,
  down,
  'graphInput.svg': graphInput,
  graphInput,
  'graphOutput.svg': graphOutput,
  graphOutput,
  'orange1.png': orange1,
  orange1,
  'Continuize.svg': Continuize,
  Continuize,
  'orange2.png': orange2,
  orange2,
  'orange3.png': orange3,
  orange3,
  'AggregateColumns.svg': AggregateColumns,
  AggregateColumns,
  'Correlations.svg': Correlations,
  Correlations,
  'CreateClass.svg': CreateClass,
  CreateClass,
};

const onDragStart = (e) => {
  e.preventDefault();
};

const execution = () => {
  return true;
};

// The basic Node component
const Node: React.FC<NodeProps> = ({
  moreHandles,
  withImage,
  withLabel,
  isGraph,
  type,
  label,
  selected,
  color,
  colorBorder,
  content,
  image,
  comment,
  executing,
  nodeWidth,
  details,
}: NodeProps) => {
  const theCom = comment ? (
    <span
      style={{
        padding: '1px',
        color: 'white',
        fontSize: '0.875rem',
        fontWeight: 300,
        lineHeight: '1.13',
      }}
    >
      {comment}
    </span>
  ) : (
    ''
  );

  const border = colorBorder
    ? `4px solid ${colorBorder}`
    : '2px solid rgb(233, 235, 247)';

  const customTitle = {
    ...style.title,
    wordWrap: 'break-word',
    borderRadius: '0px',
    margin: '2px',
    padding: '2px',
  };

  if (color) {
    customTitle.backgroundColor = color;
    customTitle.borderRadius = '10px 10px 3px 3px';
  }

  const [nodeSize, setNodeSize] = useState(nodeWidth);
  const inExecutionMode = state((state) => state.inExecutionMode);
  const graphRF = state((state) => state.graphRF);
  const setOpenSnackbar = state((state) => state.setOpenSnackbar);
  const setSelectedElement = state((state) => state.setSelectedElement);
  const selectedElement = state((state) => state.selectedElement);
  const [edit, setEdit] = React.useState(false);
  const [labelLocal, setLabelLocal] = React.useState(label);
  const setGraphRF = state((state) => state.setGraphRF);
  const [detailsL, setDetailsL] = React.useState(false);
  const allIcons = state((state) => state.allIcons);
  const setUndoRedo = state((state) => state.setUndoRedo);

  useEffect(() => {
    setNodeSize(nodeWidth);
    setLabelLocal(label);
    setDetailsL(details || false);
  }, [nodeWidth, label, details, detailsL]);

  const displayNode = {
    textAlign: 'center' as const,
    width: `${nodeSize}px`,
    minWidth: '60px', // for standard width
    maxWidth: '300px',
    display: ['graphInput', 'graphOutput'].includes(type) ? 'flex' : 'inline',
    margin: '2px',
    padding: '2px',
  };

  const isValidConnection = (connection) => {
    const { isValid, reason } = isValidLink(connection, graphRF);
    if (!isValid) {
      setOpenSnackbar({
        open: true,
        text: reason,
        severity: 'warning',
      });
    }
    return isValid;
  };

  const labelChanged = (event) => {
    setLabelLocal(event.target.value);
  };

  // TODO: exists in sidebar abstract in a hook?
  const cloneNode = () => {
    const element = selectedElement as EwoksRFNode;
    const newClone = {
      ...element,
      id: calcNewId(selectedElement.id, graphRF.nodes),
      selected: false,
      position: {
        x: element.position.x + 100,
        y: element.position.y + 100,
      },
    };

    const newGraph = {
      ...graphRF,
      nodes: [...graphRF.nodes, newClone],
    };

    setGraphRF(newGraph, true);

    setUndoRedo({ action: 'Cloned a Node', graph: newGraph });
    setSelectedElement(newClone as EwoksRFNode);
  };

  const findImage = (img) => {
    const imgIndex = allIcons.map((ico) => ico.name).indexOf(img);

    return imgIndex !== -1
      ? allIcons[imgIndex].image.data_url
      : iconsObj[img] || orange2;
  };

  function setSelEl() {
    const el = selectedElement as EwoksRFNode;
    setSelectedElement({
      ...el,
      data: {
        ...el.data,
        label: labelLocal,
      },
    });
  }

  return (
    <div
      style={
        {
          ...style.body,
          ...(selected ? style.selected : []),
          border,
        } as React.CSSProperties
      }
      id="choice"
      role="button"
      tabIndex={0}
    >
      <Tooltip title={theCom} enterDelay={800} arrow>
        <span style={displayNode} className="icons">
          {!isGraph && type !== 'graphOutput' && (
            <Handle
              type="source"
              position={Position.Right}
              id="sr"
              style={{ ...contentStyle.handle, ...contentStyle.handleSource }}
              isValidConnection={isValidConnection}
              isConnectable
            />
          )}
          {!isGraph &&
            type !== 'graphOutput' &&
            type !== 'graphInput' &&
            moreHandles && (
              <div id="choice" role="button" tabIndex={0}>
                {/* TODO: break the handles */}
                <Handle
                  type="source"
                  position={Position.Top}
                  id="st"
                  style={{
                    right: 10,
                    left: 'auto',
                    ...contentStyle.handleSource,
                    ...contentStyle.handleUpDown,
                  }}
                  isConnectable
                  isValidConnection={isValidConnection}
                />
                <Handle
                  type="source"
                  position={Position.Bottom}
                  id="sb"
                  style={{
                    right: 10,
                    left: 'auto',
                    ...contentStyle.handleSource,
                    ...contentStyle.handleUpDown,
                  }}
                  isConnectable
                  isValidConnection={isValidConnection}
                />
              </div>
            )}
          {withLabel &&
            (edit ? (
              <TextField
                id="standard-multiline-flexible"
                label="edit node Label"
                multiline
                maxRows={4}
                value={labelLocal}
                onChange={labelChanged}
                variant="standard"
              />
            ) : (
              <div style={customTitle as React.CSSProperties}>{labelLocal}</div>
            ))}
          {!withLabel && !withImage && (
            <div style={customTitle as React.CSSProperties}>
              {label.slice(0, 1)}
            </div>
          )}
          {inExecutionMode &&
            !withImage &&
            type !== 'graphOutput' &&
            type !== 'graphInput' && (
              <ExecuteSpinner
                getting={executing}
                tooltip="Execution"
                action={execution}
              >
                <img
                  style={{ padding: '2px' }}
                  role="presentation"
                  draggable="false"
                  onDragStart={(event) => onDragStart(event)}
                  src={orange1}
                  alt="icon"
                />
              </ExecuteSpinner>
            )}
          {/* If comment also needed sometimes */}
          {/* <div style={{ wordWrap: 'break-word' }}>{comment}</div> */}
          {withImage &&
            type !== 'graphOutput' &&
            type !== 'graphInput' &&
            (inExecutionMode ? (
              <ExecuteSpinner
                getting={executing}
                tooltip="Execution"
                action={execution}
              >
                <img
                  style={{ padding: '2px' }}
                  role="presentation"
                  draggable="false"
                  onDragStart={(event) => onDragStart(event)}
                  src={iconsObj[image] || orange1}
                  alt="icon"
                />
              </ExecuteSpinner>
            ) : (
              <img
                style={{ padding: '2px' }}
                role="presentation"
                draggable="false"
                onDragStart={(event) => onDragStart(event)}
                src={findImage(image)}
                alt="taskIcon"
              />
            ))}
          {withImage && (type === 'graphOutput' || type === 'graphInput') && (
            <img
              style={{ padding: '2px' }}
              role="presentation"
              draggable="false"
              onDragStart={(event) => onDragStart(event)}
              src={iconsObj[image] || orange1}
              alt="icon"
            />
          )}
          {!isGraph && type !== 'graphInput' && (
            <Handle
              type="target"
              position={Position.Left}
              id="tl"
              style={{
                ...contentStyle.handle,
                ...contentStyle.handleTarget,
              }}
              isConnectable
              isValidConnection={isValidConnection}
            />
          )}
          {!isGraph &&
            type !== 'graphOutput' &&
            type !== 'graphInput' &&
            moreHandles && (
              <>
                <Handle
                  type="target"
                  position={Position.Bottom}
                  id="tb"
                  style={{
                    left: 20,
                    ...contentStyle.handleTarget,
                    ...contentStyle.handleUpDown,
                  }}
                  isConnectable
                  isValidConnection={isValidConnection}
                >
                  {/* <img src={iconsObj['up']} alt="" /> */}
                </Handle>
                <Handle
                  type="target"
                  position={Position.Top}
                  id="tt"
                  style={{
                    left: 20,
                    ...contentStyle.handleTarget,
                    ...contentStyle.handleUpDown,
                  }}
                  isConnectable
                  isValidConnection={isValidConnection}
                />
              </>
            )}
          {isGraph && <span style={style.contentWrapper}>{content}</span>}
          {detailsL && type !== 'graphOutput' && type !== 'graphInput' && (
            <>
              <Tooltip
                title={tooltipText('Clone Node')}
                enterDelay={800}
                arrow
                placement="top"
              >
                <IconButton
                  style={{ margin: '0px 2px', padding: '0px' }}
                  aria-label="edit"
                  onClick={() => {
                    cloneNode();
                  }}
                >
                  <FileCopyIcon fontSize="small" color="primary" />
                </IconButton>
              </Tooltip>
              {withLabel && !edit && (
                <Tooltip
                  title={tooltipText('Edit label')}
                  enterDelay={800}
                  arrow
                  placement="top"
                >
                  <IconButton
                    style={{ margin: '0px 2px', padding: '0px' }}
                    aria-label="edit"
                    onClick={() => {
                      setEdit(true);
                    }}
                  >
                    <EditIcon color="primary" />
                  </IconButton>
                </Tooltip>
              )}
              {withLabel && edit && (
                <Tooltip
                  title={tooltipText('Save new label')}
                  enterDelay={800}
                  arrow
                  placement="top"
                >
                  <IconButton
                    style={{ margin: '0px px' }}
                    aria-label="edit"
                    onClick={() => {
                      setEdit(false);
                      setSelEl();
                    }}
                  >
                    <SaveIcon color="primary" />
                  </IconButton>
                </Tooltip>
              )}
            </>
          )}
        </span>
      </Tooltip>
    </div>
  );
};

export default memo(Node);
