/* eslint-disable sonarjs/no-duplicate-string */
// / <reference types="cypress" />

describe('links in a graph', () => {
  before(() => {
    cy.visit('http://localhost:3000/#/edit-workflows');

    // cy.get('label')
    //   .should('include.text', 'Open Workflow')
    //   .parents('.MuiAutocomplete-root')
    //   .click()
    //   .get('input[type=text]')
    //   .type('tutorial_Graph');

    // cy.contains('tutorial_Graph').parent().click();
    cy.window().should('have.property', '__state__');
  });

  it('opens the newTask form', () => {
    cy.get('[data-cy="iconMenu"]').click();

    cy.get('.MuiListItem-button')
      .should('have.length', 3)
      .first()
      .children('.MuiListItemText-root')
      .should('have.length', 1)
      .and('have.text', 'New Task')
      .click();

    cy.contains('Give the new Task details')
      .parent()
      .should('have.class', 'MuiDialogTitle-root')
      .siblings()
      .first()
      .as('dialogContent')
      .should('have.class', 'MuiDialogContent-root');

    cy.get('@dialogContent')
      .contains('New Name - Identifier')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .type('Always-and-forever');

    cy.contains('Cancel').click();
  });

  it('wont open the clone Task form when node is not selected', () => {
    cy.get('.MuiListItem-button').contains('Clone as Task').parent().click();

    cy.contains('First select in the canvas a Node to clone and Save as Task');

    // TODO: cannot close the menu with clicks outside?
    // cy.get('.react-flow').click({ force: true }).click({ force: true });
    // cy.contains('Add Nodes').click({ force: true });
  });

  it('opens the clone Task form when node is selected', () => {
    cy.visit('http://localhost:3000/#/edit-workflows');

    cy.get('label')
      .should('include.text', 'Open Workflow')
      .parents('.MuiAutocomplete-root')
      .click()
      .get('input[type=text]')
      .type('tutorial_Graph');

    cy.contains('tutorial_Graph').parent().click();

    cy.get('.react-flow__nodes')
      .children()
      .filter('.react-flow__node-ppfmethod')
      .first()
      .click();

    cy.get('[data-cy="iconMenu"]').click();

    cy.get('.MuiListItem-button').contains('Clone as Task').parent().click();

    cy.contains('Give the new Task details')
      .parent()
      .should('have.class', 'MuiDialogTitle-root')
      .siblings()
      .first()
      .as('dialogContent')
      .should('have.class', 'MuiDialogContent-root');
  });

  it('opens the clone Graph form with new workflow name', () => {
    cy.visit('http://localhost:3000/#/edit-workflows');

    cy.get('[data-cy="iconMenu"]').click();

    cy.get('.MuiListItem-button').contains('Clone Graph').parent().click();

    cy.contains('Give the new Workflow name')
      .parent()
      .should('have.class', 'MuiDialogTitle-root')
      .siblings()
      .first()
      .as('dialogContent')
      .should('have.class', 'MuiDialogContent-root');
  });
});
