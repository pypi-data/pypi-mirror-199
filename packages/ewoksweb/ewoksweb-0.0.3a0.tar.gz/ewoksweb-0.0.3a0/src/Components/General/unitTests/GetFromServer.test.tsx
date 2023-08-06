import { render, screen } from '@testing-library/react';
import GetFromServer from '../GetFromServer';

test('renders 4 buttons', () => {
  render(<GetFromServer />);

  const buttonElements = screen.getAllByRole('button');

  expect(buttonElements).toHaveLength(4);
});
