import Accordion from '@material-ui/core/Accordion';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import Typography from '@material-ui/core/Typography';
import OpenInBrowser from '@material-ui/icons/OpenInBrowser';

import type { EwoksRFLink, EwoksRFNode, GraphDetails } from '../../types';
import EditNodeStyle from './EditNodeStyle';
import EditLinkStyle from './EditLinkStyle';
import state from '../../store/state';

// DOC: For eiting the style of nodes and links
export default function EditElementStyle() {
  const selectedElement = state<EwoksRFNode | EwoksRFLink | GraphDetails>(
    (state) => state.selectedElement
  );

  return (
    ('position' in selectedElement || 'source' in selectedElement) && (
      <Accordion className="Accordions-sidebar">
        <AccordionSummary
          expandIcon={<OpenInBrowser />}
          aria-controls="panel1a-content"
        >
          <Typography>
            Styling{' '}
            {'position' in selectedElement
              ? 'Node'
              : 'source' in selectedElement
              ? 'Link'
              : 'Graph'}
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <form noValidate autoComplete="off">
            {'position' in selectedElement && (
              <EditNodeStyle element={selectedElement} />
            )}
            {'source' in selectedElement && (
              <EditLinkStyle element={selectedElement} />
            )}
          </form>
        </AccordionDetails>
      </Accordion>
    )
  );
}
