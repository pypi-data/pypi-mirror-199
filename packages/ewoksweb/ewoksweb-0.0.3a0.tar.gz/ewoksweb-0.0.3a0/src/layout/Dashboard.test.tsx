import { render, screen } from '@testing-library/react';
import Dashboard from './Dashboard';

test('renders hello world', () => {
  render(<Dashboard />);
  const linkElement = screen.getByText('Hello World');
  expect(linkElement).toBeInTheDocument();
});
