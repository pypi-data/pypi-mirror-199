import type { GraphRF, Note } from '../types';

// EwoksRFNode --> EwoksNode for saving
export function calcNoteNodes(graph: GraphRF): Note[] {
  return graph.nodes
    .filter((nod) => nod.type === 'note')
    .map((noteNod) => {
      return {
        id: noteNod.id,
        label: noteNod.data.label,
        comment: noteNod.data.comment,
        position: noteNod.position,
        nodeWidth: noteNod.data.nodeWidth,
      } as Note;
    });
}
