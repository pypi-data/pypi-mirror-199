import React, { useEffect } from 'react';
import state from '../../store/state';
import type { EwoksRFLink, EwoksRFNode, GraphDetails } from '../../types';
import TextButtonSave from './TextButtonSave';

// DOC: the label and the comment when the graph is the selectedElement
export default function GraphLabelComment() {
  const [label, setLabel] = React.useState('');
  const [comment, setComment] = React.useState('');
  const [category, setCategory] = React.useState('');
  const setSelectedElement = state((state) => state.setSelectedElement);
  const selectedElement = state((state) => state.selectedElement);

  useEffect(() => {
    const graphElement = selectedElement as GraphDetails;
    setLabel(graphElement.label);
    setCategory(graphElement.category);
    setComment(graphElement.uiProps && graphElement.uiProps.comment);
  }, [selectedElement.id, selectedElement]);

  function saveCategory(category) {
    setSelectedElement(
      {
        ...selectedElement,
        category,
      } as GraphDetails,
      'fromSaveElement'
    );
  }

  function saveLabel(label: string) {
    setSelectedElement(
      {
        ...selectedElement,
        label,
      },
      'fromSaveElement'
    );
  }

  function saveComment(comment: string) {
    setSelectedElement(
      {
        ...selectedElement,
        uiProps: { ...selectedElement.uiProps, comment },
      } as EwoksRFNode | EwoksRFLink,
      'fromSaveElement'
    );
  }

  return (
    <>
      <TextButtonSave label="Label" value={label} valueSaved={saveLabel} />
      <TextButtonSave
        label="Comment"
        value={comment}
        valueSaved={saveComment}
      />
      <TextButtonSave
        label="Category"
        value={category}
        valueSaved={saveCategory}
      />
    </>
  );
}
