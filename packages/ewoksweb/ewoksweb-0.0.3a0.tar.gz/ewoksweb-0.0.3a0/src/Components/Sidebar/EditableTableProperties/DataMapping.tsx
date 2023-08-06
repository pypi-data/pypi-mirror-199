import React, { useEffect } from 'react';

import type { DataMapping, EwoksRFLink } from 'types';
import { IconButton } from '@material-ui/core';
import AddCircleOutlineIcon from '@material-ui/icons/AddCircleOutline';
import EditableTable from './EditableTable';
import state from 'store/state';
import SidebarTooltip from '../SidebarTooltip';

interface DataMappingProps {
  element: EwoksRFLink;
}

export default function DataMappingComponent(props: DataMappingProps) {
  const { element } = props;

  const setOpenSnackbar = state((state) => state.setOpenSnackbar);
  const setSelectedElement = state((state) => state.setSelectedElement);
  const [dataMapping, setDataMapping] = React.useState<DataMapping[]>([]);
  const [elementL, setElementL] = React.useState<EwoksRFLink>(
    {} as EwoksRFLink
  );
  const graphRF = state((state) => state.graphRF);

  useEffect(() => {
    setElementL(element);

    if (element.data && element.data.data_mapping) {
      setDataMapping(element.data.data_mapping);
    }
  }, [element.id, element]);

  const addDataMapping = () => {
    const el = element;

    const elMap = el.data.data_mapping;

    if (elMap.some((x) => x.id === '')) {
      setOpenSnackbar({
        open: true,
        text: 'Please fill in the empty line before addining another!',
        severity: 'warning',
      });
    } else {
      setSelectedElement(
        {
          ...el,
          data: {
            ...el.data,
            data_mapping: [...elMap, { id: '', name: '', value: '' }],
          },
        },
        'fromSaveElement'
      );
    }
  };

  const dataMappingValuesChanged = (table) => {
    const dmap: DataMapping[] = table.map((row) => {
      return {
        source_output: row.name,
        target_input: row.value,
      };
    });
    setSelectedElement(
      {
        ...element,
        data: {
          ...element.data,
          data_mapping: dmap,
          label: dmap
            .map((el) => `${el.source_output}->${el.target_input}`)
            .join(', '),
        },
      },
      'fromSaveElement'
    );
  };

  return (
    <div>
      <SidebarTooltip
        text={`Describes the data transfer from source output to
          target input arguments.`}
      >
        <b>Data Mapping </b>
      </SidebarTooltip>

      <IconButton
        style={{ padding: '1px' }}
        aria-label="dataMapping"
        onClick={() => addDataMapping()}
      >
        <AddCircleOutlineIcon />
      </IconButton>
      {dataMapping.length > 0 && (
        <EditableTable
          headers={['Source', 'Target']}
          defaultValues={dataMapping}
          valuesChanged={dataMappingValuesChanged}
          typeOfValues={[
            {
              type: elementL.source
                ? ['class'].includes(
                    graphRF &&
                      graphRF.nodes[0] &&
                      graphRF.nodes.find((nod) => {
                        return nod.id === elementL.source;
                      }).task_type
                  )
                  ? 'select'
                  : 'input'
                : 'input',
              values: props.element.data.links_input_names || [],
            },
            {
              type: elementL.target
                ? ['class'].includes(
                    graphRF &&
                      graphRF.nodes[0] &&
                      graphRF.nodes.find((nod) => {
                        return nod.id === elementL.target;
                      }).task_type
                  )
                  ? 'select'
                  : 'input'
                : 'input',
              values:
                [
                  ...props.element.data.links_required_output_names,
                  ...props.element.data.links_optional_output_names,
                ] || [],
            },
          ]}
        />
      )}
    </div>
  );
}
