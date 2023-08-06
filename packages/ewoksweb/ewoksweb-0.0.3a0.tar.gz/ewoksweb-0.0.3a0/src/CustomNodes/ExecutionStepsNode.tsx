/*
A kind of node to appear on the canvas carrying the number of the
step that has been executed.
*/
import { style } from './NodeStyle';

import state from '../store/state';

function ExecutionStepsNode(args) {
  const customTitle = {
    ...style.title,
    wordWrap: 'break-word',
    borderRadius: '25px',
    backgroundColor: '#ced3ee',
    textAlign: 'center',
    padding: '1px',
    color: args.data.event.error ? 'red' : '#4493dd',
    fontSize: '1.2em',
  };

  const setCurrentExecutionEvent = state(
    (state) => state.setCurrentExecutionEvent
  );

  const goToEvent = (val) => {
    setCurrentExecutionEvent(val);
  };

  return (
    <div
      style={
        {
          ...style.body,
          ...(args.selected ? style.selected : []),
          padding: '2px',
        } as React.CSSProperties
      }
    >
      {args.data.label.split(',').map((val) => {
        return (
          <span style={{ maxWidth: '25px' }} className="icons" key={val}>
            {args.data.label.length > 0 && (
              <div
                onClick={() => goToEvent(val)}
                onKeyUp={() => goToEvent(val)}
                role="button"
                tabIndex={0}
                style={customTitle as React.CSSProperties}
                key={val}
              >
                {val}
              </div>
            )}
          </span>
        );
      })}
    </div>
  );
}

export default ExecutionStepsNode;
