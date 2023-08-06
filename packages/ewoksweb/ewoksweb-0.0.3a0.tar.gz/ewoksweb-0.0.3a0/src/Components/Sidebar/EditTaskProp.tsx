import React, { useEffect } from 'react';
import EditIcon from '@material-ui/icons/EditOutlined';
import { IconButton } from '@material-ui/core';
import DashboardStyle from '../../layout/DashboardStyle';
import TextButtonSave from './TextButtonSave';

const useStyles = DashboardStyle;

interface EditTaskProps {
  id: string;
  label: string;
  value: string;
  editProps: boolean;
  propChanged(props: editableNodeProps): void;
}
interface editableNodeProps {
  task_identifier?: string;
  task_type?: string;
  task_generator?: string;
}
// DOC: For editing Node properties related to the Task it is based on
function EditTaskProp(props: EditTaskProps) {
  const { id, label, value, editProps } = props;
  const classes = useStyles();

  const [editProp, setEditProp] = React.useState(false);
  const [taskProp, setTaskProp] = React.useState('');

  useEffect(() => {
    setTaskProp(value);
    if (!editProps) {
      setEditProp(false);
    }
  }, [value, editProps]);

  function onEditProp() {
    setEditProp(!editProp);
  }

  function taskPropChanged(taskP) {
    setTaskProp(taskP);
    props.propChanged({ [id]: taskP });
  }

  // TODO: new textButton should it have a save on enter?
  // function enterPressed(event) {
  //   if (event.key === 'Enter') {
  //     event.preventDefault();
  //     setEditProp(!editProp);
  //   }
  // }

  return (
    <>
      <div className={classes.detailsLabels}>
        {editProps && (
          <IconButton
            style={{ padding: '1px' }}
            aria-label="edit"
            onClick={onEditProp}
          >
            <EditIcon />
          </IconButton>
        )}
        {!editProp && (
          <>
            <b>{label}: </b>
            <span>{value}</span>
          </>
        )}
      </div>
      {editProp && (
        <div>
          <TextButtonSave
            label="Identifier"
            value={taskProp || ''}
            valueSaved={(val) => taskPropChanged(val)}
          />
        </div>
      )}
    </>
  );
}
export default EditTaskProp;
