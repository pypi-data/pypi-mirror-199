/* eslint-disable @typescript-eslint/restrict-plus-operands */
// TODO: UNDER DEVELOPMENT AND TESTING BY THE USERS
import { getEdgeCenter } from 'react-flow-renderer';

// const bottomLeftCorner = (x: number, y: number, size: number) => {
//   console.log(x, y, size);
//   return `L ${x},${y - size}Q ${x},${y} ${x + size},${y}`;
// };
const leftBottomCorner = (x: number, y: number, size: number) => {
  // console.log(x, y, size);
  return `L ${x + size},${y}Q ${x},${y} ${x},${y - size}`;
};
const bottomRightCorner = (x: number, y: number, size: number) =>
  `L ${x},${y - size}Q ${x},${y} ${x - size},${y}`;
// const rightBottomCorner = (x: number, y: number, size: number) => {
//   console.log(x, y, size);
//   return `L ${x - size},${y}Q ${x},${y} ${x},${y - size}`;
// };
const leftTopCorner = (x: number, y: number, size: number) =>
  `L ${x + size},${y}Q ${x},${y} ${x},${y + size}`;
// const topLeftCorner = (x: number, y: number, size: number) =>
//   `L ${x},${y + size}Q ${x},${y} ${x + size},${y}`;
const topRightCorner = (x: number, y: number, size: number) =>
  `L ${x},${y + size}Q ${x},${y} ${x - size},${y}`;
// const rightTopCorner = (x: number, y: number, size: number) =>
//   `L ${x - size},${y}Q ${x},${y} ${x},${y + size}`;

function getSmoothStepPathC({
  sourceX = 0,
  sourceY = 0,
  targetX = 0,
  targetY = 0,
  // borderRadius = 4,
  data,
  // centerY = 120,
}) {
  const [, _centerY] = getEdgeCenter({
    // offsetX, offsetY
    sourceX,
    sourceY,
    targetX,
    targetY,
  });

  // const cornerWidth = Math.min(borderRadius, Math.abs(targetX - sourceX));
  // const cornerHeight = Math.min(borderRadius, Math.abs(targetY - sourceY));
  const cornerSize = 0; // Math.min(cornerWidth, cornerHeight, offsetX, offsetY);
  const cY = _centerY;

  let firstCornerPath = '';
  let secondCornerPath = '';
  // console.log(data);
  if (sourceX <= targetX) {
    return `M ${sourceX},${sourceY}L ${targetX},${targetY}`;
    // firstCornerPath =
    //   sourceY <= targetY
    //     ? bottomLeftCorner(sourceX, cY, cornerSize)
    //     : topLeftCorner(sourceX, cY, cornerSize);
    // secondCornerPath =
    //   sourceY <= targetY
    //     ? rightTopCorner(targetX + 10, cY + 120, cornerSize)
    //     : rightBottomCorner(targetX + 120, cY, cornerSize);
  } else if (sourceX > targetX) {
    // console.log('sourceX > targetX');
    firstCornerPath =
      sourceY < targetY
        ? bottomRightCorner(
            sourceX + data.getAroundProps.x,
            cY + data.getAroundProps.y,
            cornerSize
          )
        : topRightCorner(sourceX + data.getAroundProps.x, cY + 120, cornerSize);
    secondCornerPath =
      sourceY < targetY
        ? leftTopCorner(
            targetX - data.getAroundProps.x,
            cY + data.getAroundProps.y,
            cornerSize
          )
        : leftBottomCorner(
            targetX - data.getAroundProps.x,
            cY + data.getAroundProps.y,
            cornerSize
          );
  }

  if (sourceY >= targetY) {
    // console.log('sourceY > targetY');
    const cornerX = Math.min(sourceX, targetX);
    const firstStop = bottomRightCorner(
      sourceX + data.getAroundProps.x,
      sourceY + data.getAroundProps.y,
      cornerSize
    );
    const secondStop = leftBottomCorner(
      cornerX - data.getAroundProps.x,
      sourceY + data.getAroundProps.y,
      cornerSize
    );
    // const thirdStop = topLeftCorner(cornerX, targetY - 5, cornerSize);
    // const fourthStop = rightTopCorner(targetX, targetY - 5, cornerSize);

    return `M ${sourceX},${sourceY}${firstStop}${secondStop}L ${targetX},${targetY}`;
    // return `M ${sourceX},${sourceY}${firstStop}${secondStop}${thirdStop}${fourthStop}L ${targetX},${targetY}`;
  }

  return `M ${sourceX},${sourceY}${firstCornerPath}${secondCornerPath}L ${targetX},${targetY}`;
}

export default function getAround({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  // sourcePosition,
  // targetPosition,
  style = {},
  label,
  // arrowHeadType,
  markerEnd,
  data,
}) {
  const edgePath = getSmoothStepPathC({
    sourceX,
    sourceY,
    // sourcePosition,
    targetX,
    targetY,
    data,
    // targetPosition,
  });

  // const markerEnd = getMarkerEnd(arrowHeadType, markerEndId);
  // console.log(edgePath, markerEnd);
  return (
    <>
      <path
        id={id}
        style={style}
        className="react-flow__edge-path"
        d={edgePath}
        markerEnd={markerEnd}
        fill="none"
        strokeWidth={1}
      />
      <text style={{ color: 'red' }}>
        <textPath
          href={`#${id as string}`}
          style={{ ...style, strokeWidth: '1', fontSize: '16px' }}
          startOffset="50%"
          textAnchor="middle" // TODO? make exact label place editable start, end
        >
          {label}
        </textPath>
      </text>
    </>
  );
}
