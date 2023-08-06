/* eslint-disable sonarjs/no-duplicate-string */
// / <reference types="cypress" />

describe('links in a graph', () => {
  before(() => {
    cy.visit('http://localhost:3000/#/edit-workflows');

    cy.get('label')
      .should('include.text', 'Open Workflow')
      .parents('.MuiAutocomplete-root')
      .click()
      .get('input[type=text]')
      .type('tutorial_Graph');

    cy.contains('tutorial_Graph').parent().click();
    cy.window().should('have.property', '__state__');
  });

  it('link has the default style', () => {
    cy.get('.react-flow')
      .contains('then...')
      .should(
        'have.attr',
        'style',
        'color: rgb(150, 165, 249); fill: rgb(150, 165, 249); font-weight: 500; font-size: 14px;'
      )
      .siblings('rect')
      .should(
        'have.attr',
        'style',
        'fill: rgb(223, 226, 247); fill-opacity: 1; stroke-width: 3px; stroke: rgb(150, 165, 249);'
      );

    cy.window()
      .its('__state__')
      .then((store) => store.getState().graphRF.graph.label)
      .as('label')
      .should('eq', 'tutorial_Graph');
  });

  it('selects a link and adds selected class and sidebar shows details', () => {
    cy.get('.react-flow')
      .contains('then...')
      .parent()
      .click()
      .parent()
      .should('include.class', 'selected');

    cy.contains('Map all Data').should('be.visible');

    cy.window()
      .its('__state__')
      .then((store) => store.getState().selectedElement.label)
      .as('label')
      .should('eq', 'then...');

    cy.get('[data-cy="node-edge-label"]')
      .children()
      .last()
      .children('textarea')
      .first()
      .should('have.value', 'then...');

    // equal to the above without getting into the structure mui is producing
    cy.get('[data-cy="node-edge-label"]')
      .contains('then...')
      .should('have.value', 'then...');
  });
});
