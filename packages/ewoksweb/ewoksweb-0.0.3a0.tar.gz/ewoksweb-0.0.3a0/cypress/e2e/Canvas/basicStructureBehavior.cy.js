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

  it('displays the canvas', () => {
    cy.get('.react-flow').should('be.visible');
    cy.get('.react-flow__controls').should('be.visible');
    cy.get('.react-flow__minimap').should('be.visible');
    cy.get('.react-flow__background').should('be.visible');
    cy.get('.react-flow__attribution').should('be.visible');
  });

  it('opens the tutorial_Graph on the canvas', () => {
    cy.contains('tutorial_Graph');
    cy.get('h1').should('include.text', 'tutorial_Graph');
  });

  it('displays the number of nodes the tutorial_Graph has', () => {
    cy.get('.react-flow__node').should('have.length', 20);
  });

  it('displays the number of links the tutorial_Graph has', () => {
    cy.get('.react-flow__edge').should('have.length', 12);
  });
});
