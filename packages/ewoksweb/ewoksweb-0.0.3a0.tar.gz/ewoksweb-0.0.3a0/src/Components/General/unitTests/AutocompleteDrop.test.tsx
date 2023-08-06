import { act, fireEvent, render, screen, within } from '@testing-library/react';
import state from 'store/state';
import AutocompleteDrop from '../AutocompleteDrop';
// click and see the menu of workflows
// select a workflow and check the input
// e2e open and check call for tasks
describe('AutocompleteDrop should:', () => {
  test('initially render a label ¨Workflows¨', async (): Promise<void> => {
    render(
      <AutocompleteDrop
        setInputValue={() => {}}
        placeholder="Categories"
        category="demo"
      />
    );
    const textbox = screen.getByRole('textbox', { name: /Workflows/u });
    expect(textbox).toBeInTheDocument();
    act(() => {
      state.setState({
        allWorkflows: [],
      });
    });

    const { allWorkflows } = state.getState();
    expect(allWorkflows).toHaveLength(0);

    const autocomplete = screen.getByTestId('async-autocomplete-drop');
    const dropButton = within(autocomplete).getByRole('button', {
      name: /Open/u,
    });

    const input = within(autocomplete).getByRole('textbox');
    expect((input as HTMLInputElement).value).toHaveValue('some_value');

    fireEvent(
      dropButton,
      new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
      })
    );

    act(() => {
      state.setState({
        allWorkflows: [
          {
            id: 'EnergyInterleavedMAD',
            label: 'EnergyInterleavedMAD',
            category: 'Energy',
          },
          { id: 'MXPressA_dozor', label: 'MXPressA_dozor', category: 'MX' },
        ],
      });
    });

    // autocomplete.focus();
    // // assign value to input field
    // fireEvent.change(input, { target: { value: 'Ene' } });
    // await waitFor(() => {});
    // // navigate to the first item in the autocomplete box
    fireEvent.keyDown(autocomplete, { key: 'ArrowDown' });
    // select the first item
    fireEvent.keyDown(autocomplete, { key: 'Enter' });
    // check the new value of the input field
    expect(input).toHaveValue('EnergyInterleavedMAD.json');

    fireEvent(
      autocomplete,
      new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
      })
    );

    // const { openSnackbar } = state.getState();

    // console.log(openSnackbar, autocomplete);

    const allWorkflows2 = state.getState().allWorkflows;

    expect(allWorkflows2).toHaveLength(2);
  });
});
