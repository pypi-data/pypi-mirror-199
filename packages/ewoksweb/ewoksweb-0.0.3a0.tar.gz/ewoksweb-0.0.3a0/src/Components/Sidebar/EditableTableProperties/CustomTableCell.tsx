import { makeStyles } from '@material-ui/core/styles';
import TableCell from '@material-ui/core/TableCell';

import TableCellInEditMode from './TableCellInEditMode';
import type { CustomTableCellProps } from 'types';

// DOC: Used as an app-wide dialog when confirmation is needed. Open is a prop
function CustomTableCell(props: CustomTableCellProps) {
  const { row, name } = props;

  const useStyles = makeStyles(() => ({
    tableCell: {
      width: name === 'value' ? '50%' : '30%',
      height: 20,
      padding: '1px',
    },
  }));
  const classes = useStyles();
  const { isEditMode } = row;

  return (
    <TableCell align="left" className={classes.tableCell}>
      {/* In edit mode the type comes from sidebar in data-mapping and
      from the selected type here for conditions and default-values */}
      {isEditMode ? (
        <TableCellInEditMode props={props} />
      ) : row[name] && typeof row[name] === 'object' ? (
        JSON.stringify(row[name])
      ) : (
        (row[name] === null ? 'null' : row[name].toString()) || ''
      )}
    </TableCell>
  );
}

export default CustomTableCell;
