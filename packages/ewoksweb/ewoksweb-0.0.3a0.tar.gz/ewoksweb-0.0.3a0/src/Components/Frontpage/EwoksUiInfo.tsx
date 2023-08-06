import OpenInBrowser from '@material-ui/icons/OpenInBrowser';
import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Typography,
  Grid,
  Fab,
  IconButton,
} from '@material-ui/core';
import SignUp from './SignUp';
import NotListedLocationIcon from '@material-ui/icons/NotListedLocation';
import { getWorkflow } from 'utils/api';
import state from 'store/state';
import type { GraphEwoks } from 'types';

interface EwoksUiInfoProps {
  closeDialog?(event?: React.KeyboardEvent | React.MouseEvent): void;
}

export default function EwoksUiInfo(props: EwoksUiInfoProps) {
  const setWorkingGraph = state((state) => state.setWorkingGraph);
  const setOpenSnackbar = state((state) => state.setOpenSnackbar);

  const closeDialog = async () => {
    if (props.closeDialog) {
      props.closeDialog();
    }
    try {
      const response = await getWorkflow('tutorial_Graph');
      if (response.data) {
        const graph = response.data as GraphEwoks;

        setOpenSnackbar({
          open: true,
          text: `Workflow ${graph.graph.label} was downloaded succesfully`,
          severity: 'success',
        });
        setWorkingGraph(response.data as GraphEwoks, 'fromServer');
      } else {
        setOpenSnackbar({
          open: true,
          text: 'Could not locate the requested workflow! Maybe it is deleted!',
          severity: 'warning',
        });
      }
    } catch (error) {
      setOpenSnackbar({
        open: true,
        text:
          error.response?.data?.message ||
          'Error in retrieving workflow. Please check connectivity with the server!',
        severity: 'error',
      });
    }
  };

  return (
    <div className="infoAccordion">
      <Grid container spacing={5} direction="row" alignItems="center">
        <Grid item xs={12} sm={12} md={12} lg={12}>
          <SignUp handleCloseDialog={closeDialog} />
        </Grid>
        <Grid item xs={12} sm={12} md={12} lg={8}>
          <h2 style={{ color: '#3f51b5' }}>
            <IconButton color="inherit" disabled>
              <Fab
                color="primary"
                size="small"
                component="span"
                aria-label="add"
              >
                <NotListedLocationIcon />
              </Fab>
            </IconButton>
            Using Ewoks-UI
          </h2>
          {infoCategories.map(({ summary, details }) => (
            <Accordion key={summary}>
              <AccordionSummary
                expandIcon={<OpenInBrowser />}
                aria-controls="panel1a-content"
              >
                <Typography>{summary}</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography>
                  {/* The following will be deleted once decided how the documentation will be displayed */}
                  {/* eslint-disable-next-line react/no-danger */}
                  <span dangerouslySetInnerHTML={{ __html: details }} />
                </Typography>
              </AccordionDetails>
            </Accordion>
          ))}
        </Grid>
      </Grid>
    </div>
  );
}
const UD = 'Under Development';

const infoCategories = [
  {
    summary: 'Create a graph',
    details: UD,
  },
  {
    summary: 'Nodes editing details',
    details: `details`,
  },
  { summary: 'Nodes style editing', details: UD },
  { summary: 'Links editing details', details: UD },
  { summary: 'Clone Node, Graph', details: UD },
  { summary: 'Manage Icons', details: UD },
  { summary: 'Manage Tasks', details: UD },
  { summary: 'other', details: UD },
];
