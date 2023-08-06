/* eslint-disable sonarjs/cognitive-complexity */
// TODO: break apart when stable
import React, { useState } from 'react';
import Box from '@material-ui/core/Box';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';
import TableSortLabel from '@material-ui/core/TableSortLabel';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Checkbox from '@material-ui/core/Checkbox';
import IconButton from '@material-ui/core/IconButton';
import Tooltip from '@material-ui/core/Tooltip';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import DeleteIcon from '@material-ui/icons/Delete';
import FilterListIcon from '@material-ui/icons/FilterList';
import RemoveRedEyeIcon from '@material-ui/icons/RemoveRedEye';
import ExecutionFilters from './ExecutionFilters';
import state from '../../store/state';
import type { Event, ExecutedJobsResponse } from '../../types';
import { Link } from 'react-router-dom';
import { Fab, makeStyles } from '@material-ui/core';
import ArrowForwardIosIcon from '@material-ui/icons/ArrowForwardIos';
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import KeyboardArrowDownIcon from '@material-ui/icons/KeyboardArrowDown';
import Collapse from '@material-ui/core/Collapse';
import { getExecutionEvents } from '../../utils/api';

interface Data {
  host_name: number;
  process_id: number;
  user_name: number;
  name: string;
  job_id: number;
  binding: string;
  workflow_id: string;
  time: string;
  error: string;
  error_message: string;
  error_traceback: string;
  task_uri: string;
  input_uris: string;
  output_uris: string;
  status: string; // "finished"
}

function descendingComparator(a: Event[], b: Event[], orderBy: string) {
  // TODO: compare time start-end
  if (['start time', 'end time'].includes(orderBy)) {
    if (b[0]['time'] < a[0]['time']) {
      return -1;
    }
    if (b[0]['time'] > a[0]['time']) {
      return 1;
    }
  }
  // DOC: if orderBy === 'workflow_id' wont work because it is not included in a context: job
  // use the context: workflow that has both => a[1] which is the workflow context
  if (b[1][orderBy] < a[1][orderBy]) {
    return -1;
  }
  if (b[1][orderBy] > a[1][orderBy]) {
    return 1;
  }
  return 0;
}

type Order = 'asc' | 'desc';

function getComparator(
  order: Order,
  orderBy: string
): (a: Event[], b: Event[]) => number {
  return order === 'desc'
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

function stableSort<T>(
  array: readonly T[],
  comparator: (a: T, b: T) => number
) {
  const stabilizedThis = array.map((el, index) => [el, index] as [T, number]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) {
      return order;
    }
    return a[1] - b[1];
  });
  return stabilizedThis.map((el) => el[0]);
}

interface HeadCell {
  disablePadding: boolean;
  id: string;
  label: string;
  numeric: boolean;
}

const headCells: readonly HeadCell[] = [
  {
    id: 'details',
    numeric: false,
    disablePadding: true,
    label: 'details',
  },
  {
    id: 'workflow_id',
    numeric: false,
    disablePadding: true,
    label: 'workflow_id',
  },
  {
    id: 'job_id',
    numeric: false,
    disablePadding: true,
    label: 'job_id',
  },
  {
    id: 'start time',
    numeric: false,
    disablePadding: true,
    label: 'Started',
  },
  {
    id: 'end time',
    numeric: false,
    disablePadding: true,
    label: 'Ended',
  },
  {
    id: 'process_id',
    numeric: false,
    disablePadding: true,
    label: 'process_id',
  },
  {
    id: 'user_name',
    numeric: true,
    disablePadding: false,
    label: 'user_name',
  },
  {
    id: 'host_name',
    numeric: true,
    disablePadding: false,
    label: 'host_name',
  },
];

interface EnhancedTableProps {
  numSelected: number;
  onRequestSort: (event: React.MouseEvent<unknown>, property: string) => void;
  onSelectAllClick: (event: React.ChangeEvent<HTMLInputElement>) => void;
  order: Order;
  orderBy: string;
  rowCount: number;
}

function EnhancedTableHead(props: EnhancedTableProps) {
  const {
    onSelectAllClick,
    order,
    orderBy,
    numSelected,
    rowCount,
    onRequestSort,
  } = props;
  const createSortHandler = (property: string) => (
    event: React.MouseEvent<unknown>
  ) => {
    onRequestSort(event, property);
  };

  return (
    <TableHead>
      <TableRow>
        <TableCell padding="checkbox">
          <Checkbox
            color="primary"
            indeterminate={numSelected > 0 && numSelected < rowCount}
            checked={rowCount > 0 && numSelected === rowCount}
            onChange={onSelectAllClick}
            inputProps={{
              'aria-label': 'select all desserts',
            }}
          />
        </TableCell>
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            // align={headCell.numeric ? 'right' : 'left'}
            padding={headCell.disablePadding ? 'none' : 'normal'}
            sortDirection={orderBy === headCell.id ? order : false}
          >
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : 'asc'}
              onClick={createSortHandler(headCell.id)}
            >
              {headCell.label}
              {/* TODO: do I need the following text */}
              {orderBy === headCell.id ? (
                <Box component="span">{order === 'desc' ? ' ' : '  '}</Box>
              ) : null}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
}

function EnhancedTableToolbar(props) {
  const { selected } = props;

  const executedWorkflows = state((state) => state.executedWorkflows);
  const setWatchedWorkflows = state((state) => state.setWatchedWorkflows);
  const watchedWorkflows = state((state) => state.watchedWorkflows);

  const addToWatchedJobs = () => {
    const watchedJobs = [] as Event[][];
    const allExJobs = [...executedWorkflows];
    // DOC: from the jobs from server take the selected to watchedJobs
    selected.forEach((selectedjobid) => {
      watchedJobs.push(
        allExJobs.find((job) => job[0].job_id === selectedjobid)
      );
    });

    const newWatchedJobs: Event[][] = [];
    const existingJobs = new Set(watchedWorkflows.map((job) => job[0].job_id));

    // DOC: newWatchedJobs by exluding the ones already there
    watchedJobs.forEach((job) => {
      if (!existingJobs.has(job[0].job_id)) {
        newWatchedJobs.push(job);
      }
    });
    // DOC: set the watched in store with the existing and the new
    setWatchedWorkflows([...watchedWorkflows, ...newWatchedJobs]);
  };

  const removeJobs = () => {
    /* eslint-disable no-console */
    console.log('remove jobs (delete to server) as unwanted', selected); // TODO on server
  };

  return (
    <Toolbar>
      {selected.length > 0 ? (
        <Typography color="inherit" variant="subtitle1" component="div">
          {selected.length} selected
        </Typography>
      ) : (
        <Typography variant="h6" id="tableTitle" component="div">
          <ExecutionFilters />
        </Typography>
      )}
      {selected.length > 0 ? (
        <>
          <Tooltip title="open in editor">
            <IconButton onClick={addToWatchedJobs}>
              <RemoveRedEyeIcon color="primary" />
            </IconButton>
          </Tooltip>
          <Tooltip title="Delete">
            <IconButton onClick={removeJobs}>
              <DeleteIcon color="primary" />
            </IconButton>
          </Tooltip>
        </>
      ) : (
        <Tooltip title="Filter list">
          <IconButton>
            <FilterListIcon />
          </IconButton>
        </Tooltip>
      )}
    </Toolbar>
  );
}

const formatedTime = (time) => {
  const dat = new Date(time);
  return `${dat.toTimeString().slice(0, 8)}
    ${dat.toDateString()}`;
};

export default function EnhancedTable() {
  const [order, setOrder] = useState<Order>('asc');
  const [orderBy, setOrderBy] = useState<keyof Data>('workflow_id');
  const [selected, setSelected] = useState<readonly string[]>([]);
  const [expandRow, setExpandRow] = useState<string>('');
  const [page, setPage] = useState(0);
  const [dense, setDense] = useState(true);
  const [rowsPerPage, setRowsPerPage] = useState(25);
  const executedWorkflows = state((state) => state.executedWorkflows);
  const [open, setOpen] = useState(false);
  const [eventsForWorflow, setEventsForWorflow] = useState([]);

  const useRowStyles = makeStyles({
    root: {
      '& > *': {
        borderBottom: 'unset',
      },
    },
  });
  const classes = useRowStyles();

  const handleRequestSort = (
    event: React.MouseEvent<unknown>,
    property: keyof Data
  ) => {
    console.log(event, property);
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const handleSelectAllClick = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.checked) {
      const newSelecteds = executedWorkflows.map((n) => n[0].job_id);
      setSelected(newSelecteds);
      return;
    }
    setSelected([]);
  };

  const handleClick = (event: React.MouseEvent<unknown>, name: string) => {
    const selectedIndex = selected.indexOf(name);
    let newSelected: readonly string[] = [];

    // if (event.target)

    if (selectedIndex === -1) {
      newSelected = [...selected, name];
    } else if (selectedIndex === 0) {
      newSelected = [...selected.slice(1)];
    } else if (selectedIndex === selected.length - 1) {
      newSelected = [...selected.slice(0, -1)];
    } else if (selectedIndex > 0) {
      newSelected = [
        ...selected.slice(0, selectedIndex),
        ...selected.slice(selectedIndex + 1),
      ];
    }

    setSelected(newSelected);
  };

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setRowsPerPage(Number.parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleChangeDense = (event: React.ChangeEvent<HTMLInputElement>) => {
    setDense(event.target.checked);
  };

  const isSelected = (job_id: string) => selected.includes(job_id);

  // Avoid a layout jump when reaching the last page with empty rows.
  const emptyRows =
    page > 0
      ? Math.max(0, (1 + page) * rowsPerPage - executedWorkflows.length)
      : 0;

  async function setOpenRow(job_id) {
    if (expandRow === job_id) {
      setOpen(!open);
    } else if (expandRow === '' || expandRow !== job_id) {
      try {
        const response = await getExecutionEvents({ job_id });
        if (response.data) {
          const execJobs = response.data as ExecutedJobsResponse;
          setEventsForWorflow(execJobs.jobs[0]);
        } else {
          /* eslint-disable no-console */
          console.log('no response data');
        }
      } catch (error) {
        /* eslint-disable no-console */
        console.log(error);
      }
      setOpen(true);
    }

    setExpandRow(job_id);
  }

  return (
    <Box sx={{ width: '100%' }}>
      <Paper>
        <EnhancedTableToolbar selected={selected} />
        <hr style={{ color: '#dee3ff' }} />
        <TableContainer
          style={{
            backgroundColor: 'rgb(227, 229, 245)',
            borderRadius: '10px',
          }}
        >
          <Table
            aria-labelledby="tableTitle"
            size={dense ? 'small' : 'medium'}
            stickyHeader
            style={{ borderCollapse: 'collapse' }}
          >
            <EnhancedTableHead
              numSelected={selected.length}
              order={order}
              orderBy={orderBy}
              onSelectAllClick={handleSelectAllClick}
              onRequestSort={handleRequestSort}
              rowCount={executedWorkflows.length}
            />
            <TableBody>
              {/* TODO: if we don't need to support IE11, you can replace the `stableSort` call with:
              rows.slice().sort(getComparator(order, orderBy)) */}
              {stableSort(executedWorkflows, getComparator(order, orderBy))
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((row, index) => {
                  console.log(row, index, row.slice(-1)[0].error);
                  const isItemSelected = isSelected(row[0].job_id);
                  const labelId = `enhanced-table-checkbox-${index}`;

                  return (
                    <React.Fragment key={row[0].job_id}>
                      <TableRow
                        hover
                        role="checkbox"
                        aria-checked={isItemSelected}
                        tabIndex={-1}
                        key={row[0].job_id}
                        selected={isItemSelected}
                        className={classes.root}
                        style={{
                          whiteSpace: 'nowrap',
                          borderRadius: '15px',
                          // TODO border not working
                          border: row.slice(-1)[0].error
                            ? '2px solid #fa7faa'
                            : '',
                          backgroundColor: row.slice(-1)[0].error
                            ? 'rgb(189, 193, 221)'
                            : '',
                        }}
                      >
                        <TableCell padding="checkbox">
                          <Checkbox
                            color="primary"
                            checked={isItemSelected}
                            inputProps={{
                              'aria-labelledby': labelId,
                            }}
                            onClick={(event) =>
                              handleClick(event, row[0].job_id)
                            }
                          />
                        </TableCell>
                        <TableCell>
                          <IconButton
                            aria-label="expand row"
                            size="small"
                            onClick={() => setOpenRow(row[0].job_id)}
                          >
                            {open && expandRow === row[0].job_id ? (
                              <KeyboardArrowUpIcon />
                            ) : (
                              <KeyboardArrowDownIcon />
                            )}
                          </IconButton>
                        </TableCell>
                        <TableCell
                          // component="th"
                          id={labelId}
                          align="left"
                        >
                          {row[1]?.workflow_id}
                        </TableCell>
                        <TableCell align="right">{row[0].job_id}</TableCell>
                        <TableCell align="right">
                          {formatedTime(row[0] && row[0].time)}
                        </TableCell>
                        <TableCell align="right">
                          {formatedTime(
                            row[row.length - 1] && row[row.length - 1].time
                          )}
                        </TableCell>
                        <TableCell align="right">{row[0].process_id}</TableCell>
                        <TableCell align="right">{row[0].user_name}</TableCell>
                        <TableCell align="right">{row[0].host_name}</TableCell>
                      </TableRow>
                      <TableRow className={classes.root}>
                        <TableCell
                          style={{
                            paddingBottom: 2,
                            paddingTop: 2,
                            paddingLeft: 2,
                            margin: '5px',
                          }}
                          colSpan={8}
                        >
                          <Collapse
                            in={open && expandRow === row[0].job_id}
                            timeout="auto"
                            unmountOnExit
                            style={{
                              backgroundColor: 'white',
                              borderRadius: '15px',
                              border: '2px solid white',
                              margin: '2px',
                            }}
                          >
                            <Box margin={1}>
                              <Typography
                                variant="h6"
                                gutterBottom
                                component="div"
                              >
                                Execution Events
                              </Typography>
                              <Table size="small" aria-label="purchases">
                                <TableHead>
                                  <TableRow>
                                    <TableCell>Time</TableCell>
                                    <TableCell>progress</TableCell>
                                    <TableCell>outputs</TableCell>
                                    <TableCell>inputs</TableCell>
                                    <TableCell>type</TableCell>
                                    <TableCell>error</TableCell>
                                    <TableCell>error_traceback</TableCell>
                                    <TableCell>error_message</TableCell>
                                    <TableCell>node_id</TableCell>
                                    <TableCell>task_id</TableCell>
                                    <TableCell>task_uri</TableCell>
                                    {/* <TableCell>id</TableCell> */}
                                  </TableRow>
                                </TableHead>
                                <TableBody>
                                  {eventsForWorflow.map((ev) => (
                                    <TableRow
                                      key={ev.time}
                                      style={{
                                        borderRadius: '15px',
                                        border: ev.error ? '2px solid red' : '',
                                        backgroundColor: ev.error
                                          ? 'rgb(227, 229, 244)'
                                          : '',
                                      }}
                                    >
                                      <TableCell component="th" scope="row">
                                        {ev.time}
                                      </TableCell>
                                      <TableCell>{ev.progress}</TableCell>
                                      <TableCell align="right">
                                        {ev.output_uris}
                                      </TableCell>
                                      <TableCell align="right">
                                        {ev.input_uris}
                                      </TableCell>
                                      <TableCell align="right">
                                        {ev.type}
                                      </TableCell>
                                      <TableCell align="right">
                                        {ev.error && ev.error.toString()}
                                      </TableCell>
                                      <TableCell align="right">
                                        <Tooltip title={ev.error_traceback}>
                                          <p>
                                            {ev.error &&
                                              `${
                                                ev.error_traceback?.slice(
                                                  0,
                                                  30
                                                ) as string
                                              }...`}
                                          </p>
                                        </Tooltip>
                                      </TableCell>
                                      <TableCell align="right">
                                        {ev.error_message}
                                      </TableCell>
                                      <TableCell align="right">
                                        <Tooltip title={ev.node_id}>
                                          <p>
                                            {ev.node_id?.slice(
                                              (ev.node_id?.lastIndexOf(
                                                '.'
                                              ) as number) + 1
                                            )}
                                          </p>
                                        </Tooltip>
                                      </TableCell>
                                      <TableCell align="right">
                                        <Tooltip title={ev.task_id}>
                                          <p>
                                            {ev.task_id?.slice(
                                              (ev.task_id?.lastIndexOf(
                                                '.'
                                              ) as number) + 1
                                            )}
                                          </p>
                                        </Tooltip>
                                      </TableCell>
                                      <TableCell align="right">
                                        {ev.task_uri}
                                      </TableCell>
                                    </TableRow>
                                  ))}
                                </TableBody>
                              </Table>
                            </Box>
                          </Collapse>
                        </TableCell>
                      </TableRow>
                    </React.Fragment>
                  );
                })}
              {emptyRows > 0 && (
                <TableRow
                  style={{
                    height: (dense ? 33 : 53) * emptyRows,
                  }}
                >
                  <TableCell colSpan={6} />
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={executedWorkflows.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>
      <FormControlLabel
        control={<Switch checked={dense} onChange={handleChangeDense} />}
        label="Dense padding"
      />
      <IconButton color="inherit">
        <Typography
          component="h1"
          variant="h5"
          color="primary"
          style={{ padding: '5px' }}
        >
          <Link
            to="/edit-workflows"
            style={{
              textDecoration: 'none',
              color: 'rgb(63, 81, 181)',
            }}
          >
            Edit Workflows
            <Fab color="primary" size="small" component="span" aria-label="add">
              <ArrowForwardIosIcon />
            </Fab>
          </Link>
        </Typography>
      </IconButton>
    </Box>
  );
}
