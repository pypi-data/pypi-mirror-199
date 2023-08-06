/* eslint-disable sonarjs/no-duplicate-string */
// / <reference types="cypress" />

describe('links in a graph', () => {
  before(() => {
    cy.visit('http://localhost:3000/#/edit-workflows');
  });

  it('creates new task', () => {
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

    cy.get('@dialogContent')
      .contains('Task Type')
      .should('exist')
      .parent()
      .click();

    cy.contains('ppfmethod').click();

    cy.get('@dialogContent')
      .contains('Category')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('not.has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Optional Inputs')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Required Inputs')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Outputs')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Icon')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('not.has.attr', 'disabled');

    // Test if the choice in Task Type is class
    cy.get('@dialogContent')
      .contains('Task Type')
      .should('exist')
      .parent()
      .click();

    cy.contains('class').click();

    cy.get('@dialogContent')
      .contains('Category')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('not.has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Optional Inputs')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('not.has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Required Inputs')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('not.has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Outputs')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('not.has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Icon')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('not.has.attr', 'disabled');

    // Test if the choice in Task Type is method
    cy.get('@dialogContent')
      .contains('Task Type')
      .should('exist')
      .parent()
      .click();

    cy.contains('method').click();

    cy.get('@dialogContent')
      .contains('Category')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('not.has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Optional Inputs')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Required Inputs')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Outputs')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .should('have.value', 'return_value')
      .and('has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Icon')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('not.has.attr', 'disabled');

    // Test if the choice in Task Type is script
    cy.get('@dialogContent')
      .contains('Task Type')
      .should('exist')
      .parent()
      .click();

    cy.contains('script').click();

    cy.get('@dialogContent')
      .contains('Category')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('not.has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Optional Inputs')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Required Inputs')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Outputs')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .should('have.value', 'return_value')
      .and('has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Icon')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('not.has.attr', 'disabled');

    // Test if the choice in Task Type is ppfport
    cy.get('@dialogContent')
      .contains('Task Type')
      .should('exist')
      .parent()
      .click();

    cy.contains('ppfport').click();

    cy.get('@dialogContent')
      .contains('Category')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .as('categoryInput')
      .first()
      .and('not.has.attr', 'disabled');

    cy.get('@categoryInput').type('till-forever-ends');

    cy.get('@dialogContent')
      .contains('Optional Inputs')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Required Inputs')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Outputs')
      .should('exist')
      .siblings('div')
      .first()
      .children('input')
      .and('has.attr', 'disabled');

    cy.get('@dialogContent')
      .contains('Icon')
      .should('exist')
      .siblings('div')
      .first()
      .as('iconInput')
      .children('input')

      .and('not.has.attr', 'disabled');

    cy.get('@iconInput').click();

    cy.contains('default.png').click();
  });
});
