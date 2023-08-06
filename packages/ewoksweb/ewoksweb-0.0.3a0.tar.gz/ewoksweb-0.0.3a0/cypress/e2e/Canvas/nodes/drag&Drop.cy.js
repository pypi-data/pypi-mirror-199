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

  it('should drag and drop 2 nodes from add nodes into canvas', () => {
    const dataTransfer = new DataTransfer();
    cy.contains('Add Nodes').click();

    cy.contains('General').click();

    cy.get('.dndnode').last().trigger('dragstart', {
      dataTransfer,
    });

    cy.get('.react-flow').trigger('drop', {
      dataTransfer,
    });

    cy.get('.react-flow__node').should('have.length', 21);

    cy.contains('General')
      .parents('#add-nodes-accordion')
      .find('.dndnode')
      .first()
      .trigger('dragstart', {
        dataTransfer,
      });

    cy.get('.react-flow').trigger('drop', {
      dataTransfer,
    });

    cy.get('.react-flow__node').should('have.length', 22);
  });

  // TODO: move node - dragstart seems to grasp the inner and creates a ghost
  it('should move a node in the canvas', () => {
    const dataTransfer = new DataTransfer();

    cy.get('.react-flow__node-graph').last().find('img').trigger('dragstart', {
      dataTransfer,
    });

    cy.get('.react-flow').last().trigger('drop', {
      dataTransfer,
    });
    cy.get('.react-flow__node').should('have.length', 22);
  });
});
