/* eslint-disable sonarjs/cognitive-complexity */
import { useState, useEffect } from 'react';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import CircularProgress from '@material-ui/core/CircularProgress';
import { getWorkflows } from 'utils';
import type { WorkflowDescription } from 'types';

import state from 'store/state';

interface AutocompleteDropProps {
  placeholder: string;
  category: string;
  setInputValue(input: WorkflowDescription): void;
}

const openWorkflowPlaceholder = 'Open Workflow';

// DOC: A dropdown that can be an input as well
function AutocompleteDrop(props: AutocompleteDropProps) {
  const [options, setOptions] = useState([]);
  const [value] = useState(options[0]);
  const [open, setOpen] = useState(false);
  const setAllWorkflows = state((state) => state.setAllWorkflows);
  const setAllCategories = state((state) => state.setAllCategories);
  const loading = open && options.length === 0;
  const setOpenSnackbar = state((state) => state.setOpenSnackbar);
  const inExecutionMode = state((state) => state.inExecutionMode);

  useEffect(() => {
    if (!open) {
      setOptions([]);
    }
  }, [open]);

  function setInputValue(newInputValue: WorkflowDescription) {
    props.setInputValue(newInputValue);
  }

  async function openDropdown() {
    setOpen(true);
    let active = true;
    // DOC: getWorkflows will fetch {label, category} not just label
    // depending on props.placeholder will show categories of workflows
    // after selecting a category workflows will be filtered for this category
    // TODO: error handling with try catch
    const workF: WorkflowDescription[] = await getWorkflows();

    if (workF.length === 0) {
      setOpenSnackbar({
        open: true,
        text: 'It seems you have no workflows to work with!',
        severity: 'error',
      });
    } else if (workF[0].label === 'network error') {
      setOpenSnackbar({
        open: true,
        text: `Something went wrong when contacting the server!
          Error status: ${workF[0].category}`,
        severity: 'error',
      });
    } else if (workF && workF.length > 0) {
      const categoriesSet = new Set(
        workF.filter((wof) => wof.category).map((det) => det.category)
      );

      const categories = [...categoriesSet].map((cat) => {
        return { label: cat };
      });

      setAllCategories([...categories, { label: 'All' }]);

      setAllWorkflows(workF);

      if (active) {
        setOptions(
          props.placeholder === openWorkflowPlaceholder
            ? filterworkfToCategories([...workF]).map((workf) => {
                return { ...workf, category: workf.category || 'NoCategory' };
              })
            : [...categories, { label: 'All' }]
        );
      }
    }

    return () => {
      active = false;
    };
  }

  function filterworkfToCategories(
    WorkflowDescriptions: WorkflowDescription[]
  ) {
    let workflowToShow = [];
    if (
      props.category === 'All' ||
      ['', null, undefined].includes(props.category)
    ) {
      workflowToShow = WorkflowDescriptions;
    } else {
      workflowToShow = WorkflowDescriptions.filter(
        (work) => work.category === props.category
      );
    }
    return workflowToShow;
  }

  return (
    <Autocomplete
      disabled={inExecutionMode}
      data-testid="async-autocomplete-drop"
      open={open}
      onOpen={() => {
        openDropdown();
      }}
      onClose={() => {
        setOpen(false);
      }}
      getOptionSelected={(option) => {
        return option.label || '';
      }}
      getOptionLabel={(option) => {
        return props.placeholder === openWorkflowPlaceholder
          ? option.label || option.id || ''
          : option.label || '';
      }}
      groupBy={(option) => {
        return option.category;
      }}
      options={
        props.placeholder === openWorkflowPlaceholder
          ? options.sort((a, b) => -b.category.localeCompare(a.category))
          : options
      }
      loading={loading}
      value={value}
      onChange={(event, newValue: WorkflowDescription | null) => {
        setInputValue(newValue);
      }}
      renderInput={(params) => (
        <TextField
          variant="filled"
          {...params}
          label={props.placeholder}
          InputProps={{
            ...params.InputProps,
            endAdornment: (
              <>
                {loading ? (
                  <CircularProgress color="inherit" size={20} />
                ) : null}
                {params.InputProps.endAdornment}
              </>
            ),
          }}
        />
      )}
    />
  );
}

export default AutocompleteDrop;
