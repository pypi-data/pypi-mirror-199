/* eslint-disable sonarjs/no-duplicate-string */
// / <reference types="cypress" />

describe('clicks on canvas and elements', () => {
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

  // TODO: rightClick? Must click on backround and not on a node
  // it('displays the rightClick message', () => {
  //   cy.get('.reactflow-wrapper').rightclick();
  //   cy.contains('Open a graph and click on nodes and links on this Canvas!');
  // });

  // select a node with click
  it('selects a node with click', () => {
    cy.contains('Advanced').should('not.exist');
    cy.contains('Default Inputs').should('not.exist');

    cy.get('.react-flow__node')
      .first()
      .click()
      .should('include.class', 'selected');

    cy.contains('Advanced').should('exist');
    cy.contains('Default Inputs').should('exist');
    cy.contains('Default Inputs').should('be.visible');
    cy.contains('Inputs-complete').should('exist');
    cy.contains('Inputs-complete').should('not.be.visible');
  });

  it('selects a link with click', () => {
    cy.contains('Map all Data').should('not.exist');
    cy.contains('on_error').should('not.exist');
    cy.contains('Conditions').should('not.exist');

    cy.get('.react-flow__edge')
      .first()
      .click({ force: true })
      .should('include.class', 'selected');

    cy.contains('Advanced').should('exist');
    cy.contains('Map all Data').should('exist');
    cy.contains('Map all Data').should('be.visible');
    cy.contains('on_error').should('exist');
    cy.contains('on_error').should('be.visible');
    cy.contains('Conditions').should('exist');
    cy.contains('Conditions').should('be.visible');
    cy.contains('Required').should('exist');
    cy.contains('Required').should('not.be.visible');
    cy.contains('Comment').should('exist');
    cy.contains('Comment').should('not.be.visible');
  });

  it('doubleclick on default node', () => {
    cy.get('.react-flow__nodes')
      .children()
      .filter('.react-flow__node-ppfmethod')
      .first()
      .dblclick()
      .get('.icons')
      .children('button[type=button]')
      .should('have.length', 2);
  });

  it('doubleclick on note node', () => {
    cy.get('.react-flow__node-note')
      .last('include.class', 'node-note')
      .dblclick()
      .should('include.class', 'selected')
      .get('.icons')
      .children('button[type=button]')
      .should('have.length', 1);
  });

  it('doubleclick on graph node', () => {
    cy.get('.react-flow__node-graph')
      .should('have.length', 3)
      .last()
      .dblclick();

    cy.get('.react-flow__node').should('not.have.length', 20);

    cy.get('h1')
      .get('.MuiBreadcrumbs-li')
      .should('have.length', 2)
      .first()
      .contains('tutorial_Graph')
      .click();

    cy.get('.react-flow__node').should('have.length', 20);
  });
});
