// Test like Conditions.test
// TO TEST:
// if addDataMapping is pressed on a selected link
// a new line is added in the table or not if last line empty

// a dataMappingValuesChanged changes the selected link conditions

import { fireEvent, render, screen } from '@testing-library/react';
import DataMapping from '../DataMapping';
// import state from 'store/state';
import type { EwoksRFLink } from 'types';

describe('In the DataMapping:', () => {
  test('Initially it renders "Data Mapping" text and one button element', async () => {
    render(
      <DataMapping
        element={
          {
            source: '1',
            target: '2',
            data: { data_mapping: [] },
          } as EwoksRFLink
        }
      />
    );
    // not working
    // const addDataMapping = jest.fn();

    const dataMappingText = screen.getByText(/Data Mapping/u);
    expect(dataMappingText).toBeInTheDocument();

    const button = screen.getByRole('button', { name: /dataMapping/u });
    expect(button).toBeInTheDocument();

    const editableTable = screen.queryByRole('table', {
      name: /editable table/u,
    });
    expect(editableTable).not.toBeInTheDocument();

    // The following wont work for the UI but it creates one link in graphRF with
    // { data_mapping: [ { id: '', name: '', value: '' } ] } ??????
    // fireEvent(
    //   button,
    //   new MouseEvent('click', {
    //     bubbles: true,
    //     cancelable: true,
    //   })
    // );
    // TODO: fireEvent is not working!

    // await waitFor(() => {
    //   const editableTable1 = screen.queryByRole('table');
    //   expect(editableTable1).toBeInTheDocument();
    // });

    // expect(addDataMapping).toHaveBeenCalledTimes(1);

    // const editableTable1 = screen.queryByRole('table', {
    //   name: /editable table/u,
    // });

    // expect(editableTable1).toBeInTheDocument();
  });

  test('renders correctly the table if mappings are present', async () => {
    render(
      <DataMapping
        element={
          {
            source: '1',
            target: '2',
            data: {
              data_mapping: [
                { source_output: 'source', target_input: 'target' },
              ],
              links_input_names: [],
              links_optional_output_names: [],
              links_required_output_names: [],
            },
          } as EwoksRFLink
        }
      />
    );

    const editableTable = screen.getByRole('table', {
      name: /editable table/u,
    });
    expect(editableTable).toBeInTheDocument();

    const sourceOutput = screen.getByText(/Source/u);
    expect(sourceOutput).toBeInTheDocument();

    const value = screen.getByText(/Target/u);
    expect(value).toBeInTheDocument();

    const tr = screen.getAllByRole('row');
    expect(tr).toHaveLength(2);

    const td = screen.getAllByRole('cell');
    expect(td).toHaveLength(3);

    const headerSource = screen.getByRole('columnheader', {
      name: /Source/u,
    });
    expect(headerSource).toBeInTheDocument();

    const headerTarget = screen.getByRole('columnheader', {
      name: /Target/u,
    });
    expect(headerTarget).toBeInTheDocument();
  });

  test('a dataMappingValuesChanged changes the selected link conditions', async () => {
    render(
      <DataMapping
        element={
          {
            source: '1',
            target: '2',
            data: {
              data_mapping: [
                { source_output: 'source1', target_input: 'target1' },
              ],
              links_input_names: [],
              links_optional_output_names: [],
              links_required_output_names: [],
            },
          } as EwoksRFLink
        }
      />
    );

    const button = screen.getByRole('button', { name: /dataMapping/u });
    expect(button).toBeInTheDocument();

    fireEvent(
      button,
      new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
      })
    );

    // const { graphRF } = state.getState();

    // expect(graphRF.links[0].data.data_mapping[0].source_output).toEqual(
    //   'source'
    // );

    const tr = screen.getAllByRole('row');
    expect(tr).toHaveLength(2);

    const td = screen.getAllByRole('cell');
    expect(td).toHaveLength(3);

    expect(td[0]).toHaveTextContent('source1');
    expect(td[1]).toHaveTextContent('target1');
    expect(td[2]).toHaveTextContent('');

    // const headerTarget = screen.getByRole('columnheader', {
    //   name: /Target1/u,
    // });
    // expect(headerTarget).toBeInTheDocument();
  });
});
