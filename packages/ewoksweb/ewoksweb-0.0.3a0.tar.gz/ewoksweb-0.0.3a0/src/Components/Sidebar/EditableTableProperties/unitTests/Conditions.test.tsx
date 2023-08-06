import { fireEvent, render, screen } from '@testing-library/react';
import type { EwoksRFLink } from 'types';
import Conditions from '../Conditions';
// import state from '../store/state';

describe('In the Conditions:', () => {
  test('Initially it renders "Conditions" text and one button element', async () => {
    render(
      <Conditions
        element={
          { source: '1', target: '2', data: { conditions: [] } } as EwoksRFLink
        }
      />
    );
    // not working
    // const addConditions = jest.fn();

    const conditionText = screen.getByText(/Conditions/u);
    expect(conditionText).toBeInTheDocument();

    const button = screen.getByRole('button', { name: /Add Condition/u });
    expect(button).toBeInTheDocument();

    const editableTable = screen.queryByRole('table', {
      name: /editable table/u,
    });
    expect(editableTable).not.toBeInTheDocument();

    fireEvent(
      button,
      new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
      })
    );
    // TODO: fireEvent is not working!

    // await waitFor(() => {
    //   const editableTable1 = screen.queryByRole('table');
    //   expect(editableTable1).toBeInTheDocument();
    // });

    // expect(addConditions).toHaveBeenCalledTimes(1);

    // expect(editableTable).toBeInTheDocument();
  });

  test('renders correctly the table if conditions are present', async () => {
    render(
      <Conditions
        element={
          {
            source: '1',
            target: '2',
            data: { conditions: [{ id: '1', name: 'name1', value: '1' }] },
          } as EwoksRFLink
        }
      />
    );

    const editableTable = screen.getByRole('table', {
      name: /editable table/u,
    });
    expect(editableTable).toBeInTheDocument();

    const sourceOutput = screen.getByText(/Source_output/u);
    expect(sourceOutput).toBeInTheDocument();

    const value = screen.getByText(/Value/u);
    expect(value).toBeInTheDocument();

    const cellType = screen.getByRole('cell', { name: /Type/u });
    expect(cellType).toBeInTheDocument();

    const tr = screen.getAllByRole('row');
    expect(tr).toHaveLength(3);

    const typeSelectionButton = screen.getByRole('button', { name: /string/u });
    expect(typeSelectionButton).toBeInTheDocument();
  });

  test('renders correctly the type of the value to number', async () => {
    render(
      <Conditions
        element={
          {
            source: '1',
            target: '2',
            data: { conditions: [{ id: '1', name: 'name1', value: '1' }] },
          } as EwoksRFLink
        }
      />
    );

    const typeSelectionButton = screen.getByRole('button', { name: /number/u });
    expect(typeSelectionButton).toBeInTheDocument();
  });

  test('renders correctly the type of the value to list', async () => {
    render(
      <Conditions
        element={
          {
            source: '1',
            target: '2',
            data: { conditions: [{ id: '1', name: 'name1', value: '[1]' }] },
          } as EwoksRFLink
        }
      />
    );

    const typeSelectionButton = screen.getByRole('button', { name: /list/u });
    expect(typeSelectionButton).toBeInTheDocument();
  });

  test('renders correctly the type of the value to dict', async () => {
    render(
      <Conditions
        element={
          {
            source: '1',
            target: '2',
            data: {
              conditions: [
                { id: '1', name: 'name1', value: "{ name: 'name1' }" },
              ],
            },
          } as EwoksRFLink
        }
      />
    );

    const typeSelectionButton = screen.getByRole('button', { name: /dict/u });
    expect(typeSelectionButton).toBeInTheDocument();
  });

  test('renders correctly the type of the value to bool', async () => {
    render(
      <Conditions
        element={
          {
            source: '1',
            target: '2',
            data: {
              conditions: [{ id: '1', name: 'name1', value: true }],
            },
          } as EwoksRFLink
        }
      />
    );

    const typeSelectionButton = screen.getByRole('button', { name: /bool/u });
    expect(typeSelectionButton).toBeInTheDocument();
  });

  test('renders correctly the type of the value to null', async () => {
    render(
      <Conditions
        element={
          {
            source: '1',
            target: '2',
            data: {
              conditions: [{ id: '1', name: 'name1', value: null }],
            },
          } as EwoksRFLink
        }
      />
    );

    const typeSelectionButton = screen.getByRole('button', { name: /null/u });
    expect(typeSelectionButton).toBeInTheDocument();
  });
});

// TO TEST:
// if addConditions is pressed on a selected link
// a new line is added in conditions or not if last line empty

// a conditionsValuesChanged changes the selected link conditions
