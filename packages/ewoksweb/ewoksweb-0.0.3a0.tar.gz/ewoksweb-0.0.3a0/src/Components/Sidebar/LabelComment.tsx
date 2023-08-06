/* eslint-disable sonarjs/cognitive-complexity */
import { useEffect, useState } from 'react';

import type { EwoksRFLink, EwoksRFNode } from '../../types';
import { FormControl, TextField, IconButton, Fab } from '@material-ui/core';
import DashboardStyle from '../../layout/DashboardStyle';
import state from '../../store/state';
import SidebarTooltip from './SidebarTooltip';
import { Autocomplete } from '@material-ui/lab';
import TextButtonSave from './TextButtonSave';
import SaveIcon from '@material-ui/icons/Save';

const useStyles = DashboardStyle;

interface LabelCommentProps {
  element: EwoksRFNode | EwoksRFLink;
  showComment: boolean;
}

// DOC: the label and comment for nodes-links when selected
export default function LabelComment(props: LabelCommentProps) {
  const classes = useStyles();

  const { element, showComment } = props;

  const [comment, setComment] = useState('');
  const [label, setLabel] = useState('');
  const [labelChoices, setLabelChoices] = useState([
    'use mappings',
    'use conditions',
  ]);
  const [valueIsChanged, setValueIsChanged] = useState(false);

  const setSelectedElement = state((state) => state.setSelectedElement);
  const inExecutionMode = state((state) => state.inExecutionMode);

  useEffect(() => {
    if ('position' in element) {
      setLabel(element.data.label);
      setComment(element.data.comment);
    } else if ('source' in element) {
      const el = element;
      setLabel(el.label);
      setComment(el.data && el.data.comment);

      const mappings =
        el.data.data_mapping.length > 0
          ? el.data.data_mapping
              .map((con) => `${con.source_output}->${con.target_input}`)
              .join(', ')
          : '';
      const conditions =
        el.data.conditions.length > 0
          ? el.data.conditions
              .map(
                (con) => `${con.source_output}: ${JSON.stringify(con.value)}`
              )
              .join(', ')
          : '';

      setLabelChoices([mappings, conditions, 'text...']);
    }
  }, [element]);

  function saveLabel(labelLocal: string) {
    if ('position' in element) {
      const el = element;
      setSelectedElement(
        {
          ...el,
          label: labelLocal,
          data: { ...element.data, label: labelLocal },
        },
        'fromSaveElement'
      );
    } else {
      setSelectedElement(
        {
          ...element,
          label: labelLocal,
        },
        'fromSaveElement'
      );
    }
  }

  function saveComment(commentLocal: string) {
    const el = element as EwoksRFLink;
    setSelectedElement(
      {
        ...el,
        data: { ...element.data, comment: commentLocal },
      },
      'fromSaveElement'
    );
  }

  function valueSavedLocal(val: string) {
    setValueIsChanged(false);
    saveLabel(val);
  }

  function setChanged(event) {
    if (event && label !== event.target.value) {
      setValueIsChanged(true);
    } else {
      setValueIsChanged(false);
    }
  }

  function valueChanged(event) {
    if (event?.target.value !== 0) {
      setChanged(event);
      if (event) {
        setLabel(event.target.value);
      }
    }
  }

  function valueSelectedChanged(event) {
    setChanged(event);
    setLabel(event.target.textContent);
  }

  return (
    <div className={classes.detailsLabels}>
      {Object.keys(element).includes('source') ? (
        <SidebarTooltip text="Use Conditions or Data Mapping as label.">
          <FormControl
            fullWidth
            variant="outlined"
            className={classes.formStyleFlex}
          >
            <Autocomplete
              freeSolo
              options={labelChoices}
              value={label}
              onChange={(event) => valueSelectedChanged(event)}
              onInputChange={(event) => valueChanged(event)}
              style={{ width: valueIsChanged ? '80%' : '98%' }}
              renderInput={(params) => (
                <TextField
                  data-cy="node-edge-label"
                  {...params}
                  label="Label"
                  margin="normal"
                  variant="outlined"
                  multiline
                />
              )}
            />
            {valueIsChanged && (
              <IconButton
                style={{ width: '20%', minWidth: '30px' }}
                color="inherit"
                onClick={() => valueSavedLocal(label)}
                data-cy="saveLabelComment"
              >
                <Fab
                  className={classes.openFileButton}
                  color="primary"
                  size="small"
                  component="span"
                  aria-label="add"
                  disabled={inExecutionMode}
                >
                  <SaveIcon />
                </Fab>
              </IconButton>
            )}
          </FormControl>
        </SidebarTooltip>
      ) : (
        <TextButtonSave label="Label" value={label} valueSaved={saveLabel} />
      )}

      <div style={{ display: showComment ? 'block' : 'none' }}>
        <TextButtonSave
          label="Comment"
          value={comment}
          valueSaved={saveComment}
        />
      </div>
    </div>
  );
}
