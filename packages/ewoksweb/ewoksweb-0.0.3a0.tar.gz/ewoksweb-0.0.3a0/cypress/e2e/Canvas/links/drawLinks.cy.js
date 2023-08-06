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

  // draw link by clicking two handles in simple nodes
  it('draws a link by clicking two handles in simple nodes', () => {
    cy.get('.react-flow__nodes')
      .children()
      .filter('.react-flow__node-ppfmethod')
      .first()
      .find('div[data-handleid="sr"]')
      .click();

    cy.get('.react-flow__nodes')
      .children()
      .filter('.react-flow__node-ppfmethod')
      .last()
      .find('div[data-handleid="tl"]')
      .click();

    cy.get('.react-flow__edge').should('have.length', 13);
  });

  it('wont draw a link between 2 outputs', () => {
    cy.get('.react-flow__nodes')
      .children()
      .filter('.react-flow__node-ppfmethod')
      .first()
      .find('div[data-handleid="sr"]')
      .click();

    cy.get('.react-flow__nodes')
      .children()
      .filter('.react-flow__node-ppfmethod')
      .last()
      .find('div[data-handleid="sr"]')
      .click();

    cy.get('.react-flow__edge').should('have.length', 13);
  });

  it('wont draw a link between 2 inputs', () => {
    cy.get('.react-flow__nodes')
      .children()
      .filter('.react-flow__node-ppfmethod')
      .first()
      .find('div[data-handleid="tl"]')
      .click();

    cy.get('.react-flow__nodes')
      .children()
      .filter('.react-flow__node-ppfmethod')
      .last()
      .find('div[data-handleid="tl"]')
      .click();

    cy.get('.react-flow__edge').should('have.length', 13);
  });

  // try to draw link between 2 already connected simple nodes, graph nodes, input-output nodes
  it('wont draw a link between 2 already connected simple nodes', () => {
    cy.get('.react-flow__nodes')
      .children()
      .filter('.react-flow__node-ppfmethod')
      .first()
      .find('div[data-handleid="sr"]')
      .click();

    cy.get('.react-flow__nodes')
      .children()
      .filter('.react-flow__node-ppfmethod')
      .last()
      .find('div[data-handleid="tl"]')
      .click();

    cy.get('.react-flow__edge').should('have.length', 13);
  });

  // it('wont draw a link between 2 already connected graph nodes', () => {
  //   cy.get('.react-flow__nodes')
  //     .children()
  //     .filter('.react-flow__node-graph')
  //     .first()
  //     .find('div[data-handleid="sr"]')
  //     .click();

  //   cy.get('.react-flow__nodes')
  //     .children()
  //     .filter('.react-flow__node-graph')
  //     .last()
  //     .find('div[data-handleid="tl"]')
  //     .click();

  //   cy.get('.react-flow__edge').should('have.length', 13);
  // });

  it('deletes a link by button and keyboard', () => {
    cy.get('.react-flow__edge')
      .should('have.length', 13)
      .first()
      .click({ force: true })
      .should('include.class', 'selected');

    cy.contains('Delete').click();

    cy.get('.react-flow__edge').should('have.length', 12);
  });
});
