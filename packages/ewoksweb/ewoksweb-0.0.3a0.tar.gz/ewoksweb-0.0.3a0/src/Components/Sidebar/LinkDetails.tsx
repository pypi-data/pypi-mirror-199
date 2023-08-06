import React, { useEffect } from 'react';

import type { EwoksRFLink } from '../../types';
import { Checkbox, Paper } from '@material-ui/core';
import DashboardStyle from '../../layout/DashboardStyle';
import state from '../../store/state';
import DataMappingComponent from './EditableTableProperties/DataMapping';
import Conditions from './EditableTableProperties/Conditions';
import SidebarTooltip from './SidebarTooltip';
import LabelComment from './LabelComment';

const useStyles = DashboardStyle;

export default function LinkDetails(props: { element: EwoksRFLink }) {
  const classes = useStyles();

  const { element } = props;
  const on_error: boolean = element?.data?.on_error || false;
  const map_all_data: boolean = element?.data?.map_all_data || false;

  const setSelectedElement = state((state) => state.setSelectedElement);

  const [mapAllData, setMapAllData] = React.useState<boolean>(false);
  const [elementL, setElementL] = React.useState<EwoksRFLink>(
    {} as EwoksRFLink
  );
  const [onError, setOnError] = React.useState<boolean>(false);
  const [advanced, setAdvanced] = React.useState<boolean>(false);
  const [required, setRequired] = React.useState<boolean>(false);

  useEffect(() => {
    setElementL(element);
    setMapAllData(!!element.data.map_all_data || false);
    setOnError(!!element.data.on_error || false);
    setRequired(element.data.required);
  }, [element.id, element, on_error, map_all_data]);

  const mapAllDataChanged = (event) => {
    setSelectedElement(
      {
        ...element,
        data: { ...element.data, map_all_data: event.target.checked },
      },
      'fromSaveElement'
    );
  };

  function onErrorChanged(event) {
    setSelectedElement(
      {
        ...element,
        data: { ...element.data, on_error: event.target.checked },
      },
      'fromSaveElement'
    );
  }

  const advancedChanged = (event) => {
    setAdvanced(event.target.checked);
  };

  const requiredChanged = (event) => {
    setSelectedElement(
      {
        ...element,
        data: { ...element.data, required: event.target.checked },
      },
      'fromSaveElement'
    );
  };

  return (
    <Paper
      style={{
        backgroundColor: '#e9ebf7',
        borderRadius: '10px 0px 0px 10px',
        border: '#96a5f9',
        borderStyle: 'solid none solid solid',
        padding: '4px',
        marginBottom: '10px',
      }}
    >
      <LabelComment element={element} showComment={advanced} />
      <hr style={{ color: '#96a5f9' }} />
      <SidebarTooltip
        text={`Setting this to True is equivalent to Data Mapping
        being the identity mapping for all input names.
        Cannot be used in combination with data_mapping.`}
      >
        <div>
          <b>Map all Data</b>
          <Checkbox
            checked={mapAllData}
            onChange={mapAllDataChanged}
            inputProps={{ 'aria-label': 'controlled' }}
          />
        </div>
      </SidebarTooltip>
      {!mapAllData && elementL.source && (
        <div>
          <DataMappingComponent element={element} />
        </div>
      )}
      <hr style={{ color: '#96a5f9' }} />
      <SidebarTooltip
        text={`A special condition where the task raises an exception.
        Cannot be used in combination with conditions.`}
      >
        <div>
          <b>on_error</b>
          <Checkbox
            checked={onError}
            onChange={onErrorChanged}
            inputProps={{ 'aria-label': 'controlled' }}
          />
        </div>
      </SidebarTooltip>
      {!onError && elementL.source && (
        <div>
          <Conditions element={element} />
        </div>
      )}
      <hr style={{ color: '#96a5f9' }} />
      <div>
        <b>Advanced</b>
        <Checkbox
          checked={advanced}
          onChange={advancedChanged}
          inputProps={{ 'aria-label': 'controlled' }}
        />
      </div>
      <div style={{ display: advanced ? 'block' : 'none' }}>
        <div>
          <b>Required</b>
          <Checkbox
            checked={required}
            onChange={requiredChanged}
            // inputProps={{ 'aria-label': 'controlled' }}
          />
        </div>
        <div className={classes.detailsLabels}>
          <b>Source:</b> {element.source}
        </div>
        <div className={classes.detailsLabels}>
          <b>Target:</b> {element.target}
        </div>
        {element.data.sub_target && (
          <div className={classes.detailsLabels}>
            <b>Sub_target:</b> {element.data.sub_target}
          </div>
        )}
        {element.data.sub_target_attributes && (
          <div className={classes.detailsLabels}>
            <b>Sub_target_attributes:</b>
            {element.data.sub_target_attributes}
          </div>
        )}
      </div>
    </Paper>
  );
}
