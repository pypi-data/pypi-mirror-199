/* eslint-disable sonarjs/no-duplicate-string */
// / <reference types="cypress" />

describe('structure and basics for edit-workflows', () => {
  before(() => {
    cy.visit('http://localhost:3000/#/edit-workflows');

    cy.get('label')
      .should('include.text', 'Open Workflow')
      .parents('.MuiAutocomplete-root')
      .click()
      .get('input[type=text]')
      .type('tutorial_Graph');

    cy.contains('tutorial_Graph').parent().click();
  });

  it('selects a default node', () => {
    cy.get('.react-flow__nodes')
      .children()
      .filter('.react-flow__node-ppfmethod')
      .first()
      .click();
  });

  it('changes label of node', () => {
    cy.get('[data-cy="node-edge-label"]')
      .first()
      .should('be.visible')
      .click()
      .type('Always and forever...');

    cy.get('[data-cy="saveLabelComment"]').click();

    cy.get('.react-flow')
      .contains('Always and forever...')
      .should('be.visible');

    cy.window()
      .its('__state__')
      .then((store) => store.getState().selectedElement.label)
      .as('label')
      .should('include', 'Always and forever...');
  });

  it('changes comment of node', () => {
    cy.contains('Advanced').siblings().click();

    cy.get('[data-cy="node-edge-label"]')
      .last()
      .should('be.visible')
      .click()
      .type('Always and forever comment...');

    cy.get('[data-cy="saveLabelComment"]').click();

    cy.get('.react-flow')
      .contains('Always and forever...')
      .should('be.visible')
      .click();

    cy.get('#root')
      .contains('Always and forever comment...')
      .should('be.visible');

    cy.window()
      .its('__state__')
      .then((store) => store.getState().selectedElement.data.comment)
      .as('label')
      .should('include', 'Always and forever comment...');
  });

  it('changes withImage of node true->false->true', () => {
    cy.contains('Styling Node').click();

    cy.get('.react-flow')
      .contains('Always and forever...')
      .should('be.visible')
      .siblings()
      .should('have.length', 3);

    cy.contains('With Image').siblings().first('span').click();

    cy.get('.react-flow')
      .contains('Always and forever...')
      .should('be.visible')
      .siblings()
      .should('have.length', 2);

    cy.window()
      .its('__state__')
      .then((store) => store.getState().selectedElement.data.withImage)
      .as('label')
      .should('eq', false);

    cy.contains('With Image').siblings().first('span').click();

    cy.get('.react-flow')
      .contains('Always and forever...')
      .should('be.visible')
      .siblings()
      .should('have.length', 3);

    cy.window()
      .its('__state__')
      .then((store) => store.getState().selectedElement.data.withImage)
      .as('label')
      .should('eq', true);
  });

  it('changes withLabel of node true->false->true', () => {
    cy.get('.react-flow').contains('Always and forever...').parent().as('node');

    cy.contains('With Label').siblings().last('span').click();

    cy.get('@node').children().should('have.length', 3);

    cy.window()
      .its('__state__')
      .then((store) => store.getState().selectedElement.data.withLabel)
      .as('label')
      .should('eq', false);

    cy.contains('With Label').siblings().last('span').click();

    cy.get('@node').children().should('have.length', 4);

    cy.get('.react-flow')
      .contains('Always and forever...')
      .should('be.visible')
      .siblings()
      .should('have.length', 3);

    cy.window()
      .its('__state__')
      .then((store) => store.getState().selectedElement.data.withLabel)
      .as('label')
      .should('eq', true);
  });

  it('changes width of node', () => {
    cy.get('.react-flow').contains('Always and forever...').parent().as('node');

    cy.window()
      .its('__state__')
      .then((store) => store.getState().selectedElement.data.nodeWidth)
      .as('width')
      .should('eq', 187);

    cy.contains('Node Size').siblings().last('span').as('slider');

    cy.get('@slider')
      .children('span')
      .last()
      .should('have.attr', 'aria-valuenow')
      .and('eq', '187');

    cy.get('@slider').click();

    cy.get('@slider')
      .children('span')
      .last()
      .should('have.attr', 'aria-valuenow')
      .and('eq', '169');
  });

  it('changes moreHandles of node true->false->true', () => {
    cy.get('.react-flow').contains('Always and forever...').parent().as('node');

    cy.get('@node').children('.react-flow__handle').should('have.length', 2);

    cy.window()
      .its('__state__')
      .then((store) => store.getState().selectedElement.data.moreHandles)
      .as('moreHandlesFalse')
      .should('eq', false);

    cy.contains('More handles').siblings('span').click();

    cy.window()
      .its('__state__')
      .then((store) => store.getState().selectedElement.data.moreHandles)
      .as('moreHandlesTrue')
      .should('eq', true);

    cy.get('@node').children('.react-flow__handle').should('have.length', 4);

    cy.get('@node')
      .children('#choice')
      .should('have.length', 1)
      .children('.react-flow__handle')
      .should('have.length', 2);

    cy.contains('More handles').siblings('span').click();

    cy.get('@node').children('.react-flow__handle').should('have.length', 2);

    cy.window()
      .its('__state__')
      .then((store) => store.getState().selectedElement.data.moreHandles)
      .as('moreHandlesFalse')
      .should('eq', false);
  });

  it('clones a node by button', () => {
    cy.get('.react-flow__node').should('have.length', 20);
    cy.contains('Clone').click();

    cy.get('.react-flow__node').should('have.length', 21);
  });

  it('deletes a node by button and keyboard', () => {
    cy.get('.react-flow__node').should('have.length', 21);
    cy.contains('Delete').click();

    cy.get('.react-flow__node').should('have.length', 20);
    cy.get('.react-flow')
      .contains('Always and forever...')
      .parent()
      .should('have.length', 1);
  });

  // TODO: find a way to set a color from the firefox color picker
  // TODO: changing the state with setState wont show on the canvas border attr???
  // it('changes color of node', () => {
  //   cy.get('.react-flow').contains('Always and forever...').parent().as('node');

  //   cy.contains('Color').siblings().first().click();
  //   cy.contains('custom').should('be.visible');
  //   cy.get('input[type=color]').invoke('val', '#ff0000').trigger('change');

  //   cy.get('@node')
  //     .parent()
  //     .should('have.attr', 'style')
  //     .and('include', 'border: 2px solid rgb(233, 235, 247)');

  //   cy.window()
  //     .its('__state__')
  //     .then((store) => store.getState().selectedElement.data.colorBorder)
  //     .as('colorBorder')
  //     .should('eq', '');

  //   cy.window()
  //     .its('__state__')
  //     .then((store) =>
  //       store.setState({
  //         selectedElement: { data: { colorBorder: 'red' } },
  //       })
  //     );

  //   cy.get('@node')
  //     .parent()
  //     .should('have.attr', 'style')
  //     .and('include', 'border: 2px solid rgb(0, 0, 0)');

  //   cy.window()
  //     .its('__state__')
  //     .then((store) => console.log(store.getState().selectedElement));
  // });
});
