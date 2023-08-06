import Typography from '@material-ui/core/Typography';
import DashboardStyle from '../../layout/DashboardStyle';
import Breadcrumbs from '@material-ui/core/Breadcrumbs';
import HomeIcon from '@material-ui/icons/Home';

import Link from '@material-ui/core/Link';
import state from '../../store/state';

const useStyles = DashboardStyle;

export default function SubgraphsStack() {
  const classes = useStyles();

  const recentGraphs = state((state) => state.recentGraphs);
  const setGraphRF = state((state) => state.setGraphRF);
  const setSubgraphsStack = state((state) => state.setSubgraphsStack);
  const subgraphsStack = state((state) => {
    return state.subgraphsStack;
  });

  const goToGraph = (e) => {
    e.preventDefault();
    setSubgraphsStack({ id: e.target.id, label: e.target.text });

    const subgraph = recentGraphs.find((gr) => gr.graph.id === e.target.id);

    setGraphRF(subgraph);
  };

  return (
    <Typography
      component="h1"
      variant="h6"
      color="inherit"
      noWrap
      className={classes.title}
    >
      <Breadcrumbs aria-label="breadcrumb" color="secondary">
        {subgraphsStack.length > 1 &&
          subgraphsStack.map((gr, index) => (
            <span key={gr.id}>
              {index === 0 && <HomeIcon className={classes.icon} />}
              <Link
                underline="hover"
                color="textPrimary"
                href="/"
                id={gr.id}
                key={gr.id}
                className={
                  index === subgraphsStack.length - 1 && classes.isDisabled
                }
                onClick={goToGraph}
              >
                {gr.label}
              </Link>
            </span>
          ))}
      </Breadcrumbs>
      {subgraphsStack[0] && subgraphsStack[subgraphsStack.length - 1].label}
    </Typography>
  );
}
