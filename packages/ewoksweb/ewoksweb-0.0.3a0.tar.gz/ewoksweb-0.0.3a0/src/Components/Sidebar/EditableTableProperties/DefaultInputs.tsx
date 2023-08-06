import React, { useEffect } from 'react';

import type { EwoksRFNode, Inputs } from 'types';
import AddCircleOutlineIcon from '@material-ui/icons/AddCircleOutline';
import EditableTable from './EditableTable';
import { IconButton } from '@material-ui/core';

import state from 'store/state';
import SidebarTooltip from '../SidebarTooltip';

export default function DefaultInputs(props) {
  const { element } = props;

  const [defaultInputs, setDefaultInputs] = React.useState<Inputs[]>([]);
  const setSelectedElement = state((state) => state.setSelectedElement);
  const setOpenSnackbar = state((state) => state.setOpenSnackbar);

  useEffect(() => {
    setDefaultInputs(element.default_inputs ? element.default_inputs : []);
  }, [element.id, element]);

  const addDefaultInputs = () => {
    const el = element as EwoksRFNode;
    const elIn = el.default_inputs;

    if (elIn && elIn[elIn.length - 1] && elIn[elIn.length - 1].id === '') {
      setOpenSnackbar({
        open: true,
        text: 'Please fill in the empty line before addining another!',
        severity: 'warning',
      });
    } else {
      setSelectedElement(
        {
          ...element,
          default_inputs: [...elIn, { id: '', name: '', value: '' }],
        },
        'fromSaveElement'
      );
    }
  };

  const defaultInputsChanged = (table) => {
    setSelectedElement(
      {
        ...element,
        default_inputs: table.map((dval) => {
          return {
            id: dval.name,
            name: dval.name,
            value: dval.value,
          };
        }),
      },
      'fromSaveElement'
    );
  };

  return (
    <div>
      <SidebarTooltip
        text={`Used to create an input when not provided
              by the output of other connected nodes(tasks).`}
      >
        <div>
          <b>Default Inputs </b>
          <IconButton
            style={{ padding: '1px' }}
            aria-label="delete"
            onClick={() => addDefaultInputs()}
          >
            <AddCircleOutlineIcon />
          </IconButton>
        </div>
      </SidebarTooltip>

      {defaultInputs.length > 0 && (
        <EditableTable
          headers={['Name', 'Value']}
          defaultValues={defaultInputs}
          valuesChanged={defaultInputsChanged}
          typeOfValues={[
            {
              type: 'select',
              values: [
                ...(element.optional_input_names || []),
                ...(element.required_input_names || []),
              ],
            },
            { type: 'input' },
          ]}
        />
      )}
    </div>
  );
}
