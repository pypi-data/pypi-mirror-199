import { getBezierPath, getEdgeCenter } from 'react-flow-renderer';

function multilineText({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  label = '',
  markerEnd,
  style = {},
}) {
  const edgePath = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  const [edgeCenterX, edgeCenterY] = getEdgeCenter({
    sourceX,
    sourceY,
    targetX,
    targetY,
  });

  const titleWidth = Math.max(...label.split(',').map((mp) => mp.length)) * 7;

  const titleHeight = label.split(',').length * 30;

  return (
    <>
      <path
        id={id}
        style={style}
        className="react-flow__edge-path"
        d={edgePath}
        markerEnd={markerEnd}
      />
      <foreignObject
        width={titleWidth}
        height={titleHeight}
        x={edgeCenterX - titleWidth / 2}
        y={edgeCenterY - titleWidth / 8}
        style={{ ...style, backgroundColor: 'blue' }}
      >
        <div
          style={{
            ...style,
            backgroundColor: 'rgb(223, 226, 247)',
            color: 'rgb(150, 165, 249)',
            borderRadius: '10px',
            borderStyle: 'solid',
            borderColor: 'rgb(150, 165, 249)',
            wordWrap: 'break-word',
            overflow: 'hidden',
          }}
        >
          {label && label.split(',').map((mp) => <div key={mp}>{mp}</div>)}
        </div>
      </foreignObject>
    </>
  );
}

export default multilineText;
