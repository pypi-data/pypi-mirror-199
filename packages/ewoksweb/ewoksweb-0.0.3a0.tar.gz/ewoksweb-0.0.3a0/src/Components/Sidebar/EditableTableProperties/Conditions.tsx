import React, { useEffect } from 'react';

import type { EditableTableRow, EwoksRFLink, Inputs } from 'types';
import { IconButton } from '@material-ui/core';
import AddCircleOutlineIcon from '@material-ui/icons/AddCircleOutline';
import EditableTable from './EditableTable';
import state from 'store/state';
import SidebarTooltip from '../SidebarTooltip';

interface ConditionsProps {
  element: EwoksRFLink;
}
// DOC: The conditions for a link are being set in this component
export default function Conditions(props: ConditionsProps) {
  const { element } = props;

  const [conditions, setConditions] = React.useState<Inputs[]>([]);
  const setOpenSnackbar = state((state) => state.setOpenSnackbar);
  const setSelectedElement = state((state) => state.setSelectedElement);

  useEffect(() => {
    if (element?.data?.conditions) {
      setConditions(element.data.conditions);
    }
  }, [element]);

  const addConditions = () => {
    const el = element;
    const elCon = el.data.conditions;
    // check if an empty line already exists
    if (elCon && elCon[elCon.length - 1] && elCon[elCon.length - 1].id === '') {
      setOpenSnackbar({
        open: true,
        text: 'Cannot add another line!',
        severity: 'warning',
      });
    } else {
      setSelectedElement(
        {
          ...el,
          data: {
            ...element.data,
            on_error: false,
            conditions: [...elCon, { id: '', name: '', value: false }],
          },
        },
        'fromSaveElement'
      );
    }
  };

  const conditionsValuesChanged = (table: EditableTableRow[]) => {
    setSelectedElement(
      {
        ...element,
        data: {
          ...element.data,
          conditions: table.map((con1) => {
            return {
              source_output: con1.name,
              value: con1.value,
            };
          }),
        },
      },
      'fromSaveElement'
    );
  };

  return (
    <div>
      <SidebarTooltip
        text={`Provides a list of expected values for source outputs.
          [{"source_output": "result", "value": 10}]`}
      >
        <b>Conditions </b>
      </SidebarTooltip>

      <IconButton
        style={{ padding: '1px' }}
        aria-label="Add Condition"
        onClick={addConditions}
      >
        <AddCircleOutlineIcon />
      </IconButton>
      {conditions && conditions.length > 0 && (
        <EditableTable
          headers={['Output', 'Value']}
          defaultValues={conditions}
          valuesChanged={conditionsValuesChanged}
          typeOfValues={[
            {
              type: 'select',
              values: element.data.links_input_names || [],
            },
            {
              type: 'input',
            },
          ]}
        />
      )}
    </div>
  );
}
