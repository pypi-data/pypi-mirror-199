// NOT USED until signUp/signIn is decided
// import Avatar from '@material-ui/core/Avatar';
// import Button from '@material-ui/core/Button';
// import CssBaseline from '@material-ui/core/CssBaseline';
// import TextField from '@material-ui/core/TextField';
// import FormControlLabel from '@material-ui/core/FormControlLabel';
// import Checkbox from '@material-ui/core/Checkbox';
// import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
// import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import ArrowForwardIosIcon from '@material-ui/icons/ArrowForwardIos';
import { Fab, IconButton } from '@material-ui/core';
import { Link } from 'react-router-dom';
import ewoksUI from 'assets/ewoksUI.png';
import { Theme, createStyles, makeStyles } from '@material-ui/core/styles';
import ImageList from '@material-ui/core/ImageList';
import ImageListItem from '@material-ui/core/ImageListItem';
// import itemData from './itemData';

// const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
//   event.preventDefault();
//   // const data = new FormData(event.currentTarget);
// };

// const linkStyle = {
//   textDecoration: 'none',
//   color: 'rgb(63, 81, 181)',
// };
const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      display: 'flex',
      flexWrap: 'wrap',
      justifyContent: 'space-around',
      overflow: 'hidden',
      backgroundColor: theme.palette.background.paper,
    },
    linkStyle: {
      textDecoration: 'none',
      color: 'rgb(63, 81, 181)',
    },
    arrowForwardStyle: {
      margin: '5px',
    },
    imageList: {
      width: 600,
      height: 350,
    },
  })
);

export default function SignUp(props) {
  const classes = useStyles();

  return (
    <Grid
      container
      spacing={5}
      direction="row"
      // justifyContent="flex-start"
      alignItems="center"
    >
      <Grid item xs={12} sm={12} md={12} lg={6}>
        <Container component="main">
          <Box
            sx={{
              marginTop: 8,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Typography component="h1" variant="h5">
              Welcome to the <b className={classes.linkStyle}>Ewoks-UI</b> for
              managing your Workflows. Select to Edit or Monitor or get started
              with a graph where Ewoks-UI describes itself:
            </Typography>
            {/* TODO: repetitive iconButton abstract when stable */}
            <IconButton
              color="inherit"
              // onClick={props.handleCloseDialog || ''}
            >
              <Typography
                component="h1"
                variant="h5"
                color="primary"
                style={{ padding: '5px' }}
              >
                <Link to="/edit-workflows" className={classes.linkStyle}>
                  Edit Workflows
                  <Fab
                    // className={classes.openFileButton}
                    color="primary"
                    size="small"
                    component="span"
                    aria-label="add"
                    className={classes.arrowForwardStyle}
                  >
                    <ArrowForwardIosIcon />
                  </Fab>
                </Link>
              </Typography>
            </IconButton>
            <IconButton color="inherit">
              <Typography
                component="h1"
                variant="h5"
                color="primary"
                style={{ padding: '5px' }}
              >
                <Link to="/monitor-workflows" className={classes.linkStyle}>
                  Monitor Workflows
                  <Fab
                    // className={classes.openFileButton}
                    color="primary"
                    size="small"
                    component="span"
                    aria-label="add"
                    className={classes.arrowForwardStyle}
                  >
                    <ArrowForwardIosIcon />
                  </Fab>
                </Link>
              </Typography>
            </IconButton>
            <IconButton color="inherit" onClick={props.handleCloseDialog || ''}>
              <Typography
                component="h1"
                variant="h5"
                color="primary"
                style={{ padding: '5px' }}
              >
                <Link to="/edit-workflows" className={classes.linkStyle}>
                  Tutorial Workflow
                  <Fab
                    // className={classes.openFileButton}
                    color="primary"
                    size="small"
                    component="span"
                    aria-label="add"
                    className={classes.arrowForwardStyle}
                  >
                    <ArrowForwardIosIcon />
                  </Fab>
                </Link>
              </Typography>
            </IconButton>
          </Box>
        </Container>
      </Grid>
      <Grid item xs={12} sm={12} md={12} lg={6}>
        <ImageList rowHeight={300} className={classes.imageList} cols={1}>
          <ImageListItem>
            <img src={ewoksUI} alt="" />
          </ImageListItem>
        </ImageList>
        {/* <Box>
          <img src={ewoksUI} alt="ewoks image" />
        </Box> */}
      </Grid>

      {/* <Grid item xs={12} sm={12} md={6} lg={4}>
        <Container component="main" maxWidth="lg">
          <CssBaseline />

          <Box
          // sx={{
          //   marginTop: 8,
          //   display: 'flex',
          //   flexDirection: 'column',
          //   alignItems: 'center',
          // }}
          >
            <Avatar>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Sign up
            </Typography>
            <Box
              component="form"
              // noValidate
              onSubmit={handleSubmit}
              sx={{ mt: 3 }}
            >
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    autoComplete="given-name"
                    name="firstName"
                    required
                    fullWidth
                    id="firstName"
                    label="First Name"
                    // autoFocus
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    required
                    fullWidth
                    id="lastName"
                    label="Last Name"
                    name="lastName"
                    autoComplete="family-name"
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    id="email"
                    label="Email Address"
                    name="email"
                    autoComplete="email"
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    name="password"
                    label="Password"
                    type="password"
                    id="password"
                    autoComplete="new-password"
                  />
                </Grid>
                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Checkbox value="allowExtraEmails" color="primary" />
                    }
                    label="I agree with the terms and conditions."
                  />
                </Grid>
              </Grid>
              <Button
                type="submit"
                // fullWidth
                variant="contained"
                // sx={{ mt: 3, mb: 2 }}
              >
                Sign Up
              </Button>
              <Grid container justifyContent="flex-end">
                <Grid item>
                  Already have an account? Sign in
                </Grid>
              </Grid>
            </Box>
          </Box>
        </Container>
      </Grid> */}
    </Grid>
  );
}
