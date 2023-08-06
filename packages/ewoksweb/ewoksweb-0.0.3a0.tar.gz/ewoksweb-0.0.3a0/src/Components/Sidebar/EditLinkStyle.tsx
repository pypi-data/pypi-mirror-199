import React, { useEffect, useState } from 'react';
import {
  Button,
  Checkbox,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Slider,
} from '@material-ui/core';

import DashboardStyle from '../../layout/DashboardStyle';
import state from '../../store/state';
import type { EwoksRFLink, GraphRF } from '../../types';

const useStyles = DashboardStyle;

interface EditLinkStyleProps {
  element: EwoksRFLink;
}
// DOC: Edit the link style
export default function EditLinkStyle(props: EditLinkStyleProps) {
  const classes = useStyles();

  const { element } = props;

  const setSelectedElement = state((state) => state.setSelectedElement);
  const selectedElement = state((state) => state.selectedElement);
  const graphRF = state((state) => state.graphRF);
  const setGraphRF = state((state) => state.setGraphRF);

  const [linkType, setLinkType] = useState('');
  const [arrowType, setArrowType] = useState({
    type: 'arrow',
  });
  const [animated, setAnimated] = useState<boolean>(false);
  const [colorLine, setColorLine] = useState<string>('');
  const [x, setX] = useState(80);
  const [y, setY] = useState(80);

  useEffect(() => {
    if ('source' in element) {
      setLinkType(element.type);

      if (element.markerEnd === '') {
        setArrowType({ type: 'none' });
      } else {
        setArrowType(element.markerEnd);
      }

      // setArrowType(element.markerStart);
      setAnimated(element.animated);
      setColorLine(element.style.stroke);
    }
  }, [element.id, element]);

  const linkTypeChanged = (event) => {
    setLinkType(event.target.value);
    setSelectedElement(
      {
        ...element,
        type: event.target.value,
      },
      'fromSaveElement'
    );
  };

  const arrowTypeChanged = (event) => {
    setArrowType({ type: event.target.value });

    // 'none' is not available anymore in reactFlow so we
    // need to remove markerEnd if 'none' is selected in dropdown
    if (event.target.value === 'none') {
      setSelectedElement({ ...element, markerEnd: '' }, 'fromSaveElement');
    } else {
      setSelectedElement(
        { ...element, markerEnd: { type: event.target.value } },
        'fromSaveElement'
      );
    }
  };

  const colorLineChanged = (event) => {
    setColorLine(event.target.value);
    setSelectedElement(
      {
        ...element,
        style: { ...element.style, stroke: event.target.value },
        labelStyle: { ...element.labelStyle, fill: event.target.value },
        labelBgStyle: { ...element.labelBgStyle, stroke: event.target.value },
      },
      'fromSaveElement'
    );
  };

  const animatedChanged = (event) => {
    setAnimated(event.target.checked);
    setSelectedElement(
      {
        ...element,
        animated: event.target.checked,
      },
      'fromSaveElement'
    );
  };

  const changeX = (event, number) => {
    const elem = selectedElement as EwoksRFLink;
    setSelectedElement(
      {
        ...elem,
        data: {
          ...elem.data,
          getAroundProps: { ...elem.data.getAroundProps, x: number },
        },
      },
      'fromSaveElement'
    );
    setX(number);
  };

  const changeY = (event, number) => {
    const elem = selectedElement as EwoksRFLink;
    setSelectedElement(
      {
        ...elem,
        data: {
          ...elem.data,
          getAroundProps: { ...elem.data.getAroundProps, y: number },
        },
      },
      'fromSaveElement'
    );
    setY(number);
  };

  function applyLinkTypeToAll() {
    const newGraph: GraphRF = {
      ...graphRF,
      links: graphRF.links.map((link) => ({ ...link, type: linkType })),
    };
    setGraphRF(newGraph, true);
  }

  function applyArrowTypeToAll() {
    const newGraph: GraphRF = {
      ...graphRF,
      links: graphRF.links.map((link) => {
        let linkFinal = {} as EwoksRFLink;
        if (arrowType?.type && arrowType.type === 'none') {
          linkFinal = { ...link, markerEnd: '' };
        } else {
          linkFinal = { ...link, markerEnd: { type: arrowType.type } };
        }
        return linkFinal;
      }),
    };
    setGraphRF(newGraph, true);
  }

  return (
    <>
      <FormControl variant="filled" fullWidth className={classes.formStyleFlex}>
        <InputLabel id="linkTypeLabel">Link type</InputLabel>
        <Select
          className={classes.styleLinkDropdowns}
          labelId="linkTypeLabel"
          value={linkType ? linkType : 'default'}
          label="Link type"
          onChange={linkTypeChanged}
        >
          {[
            'straight',
            'smoothstep',
            'step',
            'default',
            'bendingText',
            'multilineText',
            'getAround',
          ].map((text) => (
            <MenuItem key={text} value={text}>
              {text}
            </MenuItem>
          ))}
        </Select>
        <Button
          style={{ margin: '8px' }}
          variant="outlined"
          color="primary"
          onClick={applyLinkTypeToAll}
          size="small"
        >
          Apply to all
        </Button>
      </FormControl>
      <FormControl variant="filled" fullWidth className={classes.formStyleFlex}>
        <InputLabel id="markerEnd">Arrow Head</InputLabel>
        <Select
          className={classes.styleLinkDropdowns}
          value={arrowType?.type || 'none'}
          label="Arrow head"
          onChange={arrowTypeChanged}
        >
          {['arrow', 'arrowclosed', 'none'].map((tex) => (
            <MenuItem value={tex} key={tex}>
              {tex}
            </MenuItem>
          ))}
        </Select>
        <Button
          style={{ margin: '8px' }}
          variant="outlined"
          color="primary"
          onClick={applyArrowTypeToAll}
          size="small"
        >
          Apply to all
        </Button>
      </FormControl>
      <div>
        <label htmlFor="animated">Animated</label>
        <Checkbox
          name="animated"
          checked={animated ? animated : false}
          onChange={animatedChanged}
          inputProps={{ 'aria-label': 'controlled' }}
        />
      </div>
      <div>
        <label htmlFor="head">Color</label>
        <input
          aria-label="Color"
          type="color"
          id="head"
          name="head"
          value={colorLine}
          onChange={colorLineChanged}
          style={{ margin: '10px' }}
        />
      </div>
      {linkType === 'getAround' && (
        <div>
          Size of Link
          <div>X</div>
          <Slider
            id="slideX"
            color="primary"
            defaultValue={x}
            value={x}
            onChange={changeX}
            min={-200}
            max={200}
            style={{ width: '90%' }}
          />
          <div>Y</div>
          <Slider
            id="slideY"
            color="primary"
            defaultValue={y}
            value={y}
            onChange={changeY}
            min={-200}
            max={200}
            style={{ width: '90%' }}
          />
        </div>
      )}
    </>
  );
}
