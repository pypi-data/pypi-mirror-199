import React, { useEffect } from 'react';
import Accordion from '@material-ui/core/Accordion';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import OpenInBrowser from '@material-ui/icons/OpenInBrowser';
import Typography from '@material-ui/core/Typography';
import LinkDetails from './LinkDetails';
import NodeDetails from './NodeDetails';
import GraphLabelComment from './GraphLabelComment';
import type { EwoksRFLink, EwoksRFNode, GraphDetails } from '../../types';

interface EditElementProps {
  element: EwoksRFNode | EwoksRFLink | GraphDetails;
}
// DOC: Container for link-node-graph editing details
function EditElement(props: EditElementProps) {
  const { element } = props;

  const [expanded, setExpanded] = React.useState<boolean>(false);

  useEffect(() => {
    setExpanded(!!element.id);
  }, [element.id]);

  const handleChange = (event: React.SyntheticEvent, newExpanded: boolean) => {
    setExpanded(newExpanded);
  };

  return (
    <Accordion
      expanded={!!expanded}
      onChange={handleChange}
      className="Accordions-sidebar"
    >
      <AccordionSummary
        expandIcon={<OpenInBrowser />}
        aria-controls="panel1a-content"
      >
        <Typography>
          Edit{' '}
          {'position' in element
            ? 'Node'
            : 'source' in element
            ? 'Link'
            : 'Graph'}
        </Typography>
      </AccordionSummary>
      <AccordionDetails style={{ padding: '0px 0px 0px 10px' }}>
        <form noValidate autoComplete="off" style={{ width: '100%' }}>
          {'source' in element ? (
            <LinkDetails element={element} />
          ) : 'position' in element ? (
            <NodeDetails element={element} />
          ) : (
            <GraphLabelComment />
          )}
        </form>
      </AccordionDetails>
    </Accordion>
  );
}

export default EditElement;
