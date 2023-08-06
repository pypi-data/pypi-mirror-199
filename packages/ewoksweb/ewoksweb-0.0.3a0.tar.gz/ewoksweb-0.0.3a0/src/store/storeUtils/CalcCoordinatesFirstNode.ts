import type { EwoksRFNode } from 'types';

export function calcCoordinatesFirstNode(nodes: EwoksRFNode[]) {
  let x = 500;
  let y = 500;
  for (const nod of nodes) {
    if (nod.position.x < x) {
      ({ x } = nod.position);
    }
    if (nod.position.y < y) {
      ({ y } = nod.position);
    }
  }
  return { x: x + 20, y: y - 50 };
}
