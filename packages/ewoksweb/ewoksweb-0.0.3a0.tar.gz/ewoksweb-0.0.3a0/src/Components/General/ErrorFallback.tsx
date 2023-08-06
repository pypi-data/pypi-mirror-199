import type { ReactNode } from 'react';
import { Button } from '@material-ui/core';
import type { FallbackProps } from 'react-error-boundary';

function prepareReport(message: string): string {
  return `Hi,

  I encountered the following error in Ewoks-UI:

  - ${message}

  Here is some additional context:

  - User agent: ${navigator.userAgent}
  - << Please provide as much information as possible (beamline, file or dataset accessed, etc.) >>

  Thanks,
  << Name >>`;
}

interface Props extends FallbackProps {
  // path?: string;
  children?: ReactNode;
}

function ErrorFallback(props: Props) {
  const { error, resetErrorBoundary, children } = props;

  return (
    <div role="alert" style={{ padding: '1.5rem' }}>
      <p>Something went wrong:</p>
      <pre style={{ color: 'var(--bs-danger)' }}>{error.message}</pre>
      <p>
        <Button
          style={{ margin: '4px' }}
          variant="outlined"
          color="primary"
          onClick={() => resetErrorBoundary()}
        >
          Try again
        </Button>{' '}
        <Button
          // startIcon={<BookmarksIcon />}
          style={{ margin: '4px' }}
          variant="outlined"
          color="primary"
          target="_blank"
          href={`mailto:data-analysis@esrf.fr?subject=Error%20report&body=${encodeURIComponent(
            prepareReport(error.message)
          )}`}
          // onClick={sendReport}
          size="small"
        >
          Report issue
        </Button>
        {/* <Button
          variant="dark"
          target="_blank"
          href={`mailto:braggy@esrf.fr?subject=Error%20report&body=${encodeURIComponent(
            prepareReport(error.message, path)
          )}`}
        >
          Report issue
        </Button> */}
      </p>
      {children}
    </div>
  );
}

export default ErrorFallback;
