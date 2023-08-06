/* eslint-disable react/function-component-definition */
/* jshint sub:true*/
import React, { useEffect, useState } from 'react';
import { style } from './NodeStyle';
import SaveIcon from '@material-ui/icons/Save';

import state from '../store/state';
import { IconButton, TextField } from '@material-ui/core';

const NoteNode = (args) => {
  const [comment, setComment] = useState('');
  const graphRF = state((state) => state.graphRF);
  const setGraphRF = state((state) => state.setGraphRF);
  const [nodeSize, setNodeSize] = useState(args.data.nodeWidth);

  useEffect(() => {
    setComment(args.data.comment);
    setNodeSize(args.data.nodeWidth);
  }, [args.data]);

  const customTitle = {
    ...style.title,
    wordWrap: 'break-word',
    borderRadius: '10px',
    backgroundColor: '#ced3ee',
    textAlign: 'center',
    padding: '1px',
  };

  const commentChanged = (event) => {
    setComment(event.target.value);
  };

  const save = () => {
    // TODO: If permenant put it in undo-redo
    setGraphRF({
      graph: graphRF.graph,
      links: graphRF.links,
      nodes: [
        ...graphRF.nodes.filter((nod) => nod.id !== args.id),
        {
          data: {
            label: args.data.label,
            comment,
          },
          id: args.id,
          task_type: 'note',
          task_identifier: args.id,
          type: 'note',
          position: { x: args.xPos, y: args.yPos },
        },
      ],
    });
  };

  return (
    <div
      style={
        {
          ...style.body,
          ...(args.selected ? style.selected : []),
          padding: '10px',
        } as React.CSSProperties
      }
      role="button"
      tabIndex={0}
    >
      <span style={{ maxWidth: `${nodeSize as string}px` }} className="icons">
        {args.data.label.length > 0 && (
          <div style={customTitle as React.CSSProperties}>
            {args.data.label}
          </div>
        )}
        {args.data.details ? (
          <TextField
            id="standard-multiline-flexible"
            label="edit comment"
            multiline
            maxRows={4}
            value={comment}
            onChange={commentChanged}
            variant="standard"
          />
        ) : (
          <div style={{ wordWrap: 'break-word' }}>{comment}</div>
        )}
        {args.data.details && (
          <IconButton
            style={{ margin: '0px 2px', padding: '0px' }}
            aria-label="edit"
            onClick={save}
          >
            <SaveIcon color="primary" />
          </IconButton>
        )}
        {/* {!edit ? (
          <IconButton
            style={{ padding: '0px' }}
            aria-label="edit"
            onClick={() => {
              setEdit(true);
            }}
          >
            <EditIcon />
          </IconButton>
        ) : (
          <>
            <SaveIcon onClick={save} />

            <UndoIcon onClick={cancel} />
          </>
        )} */}
      </span>
    </div>
  );
};

export default NoteNode;
