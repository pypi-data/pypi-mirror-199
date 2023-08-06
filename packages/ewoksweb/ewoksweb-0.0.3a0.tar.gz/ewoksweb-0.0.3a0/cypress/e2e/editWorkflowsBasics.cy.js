/* eslint-disable sonarjs/no-duplicate-string */
// / <reference types="cypress" />

describe('structure and basics for edit-workflows', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/#/edit-workflows');
  });

  it('should be in the right page', () => {
    cy.location().should((loc) => {
      expect(loc.hash).to.eq('#/edit-workflows');
      expect(loc.hash).not.to.eq('#/monitor-workflows');
      expect(loc.host).to.eq('localhost:3000');
    });
  });

  it('displays 18 buttons', () => {
    cy.get('button').should('have.length', 18);
  });

  it('displays the canvas', () => {
    cy.get('.react-flow').should('be.visible');
    cy.get('.react-flow__controls').should('be.visible');
    cy.get('.react-flow__minimap').should('be.visible');
    cy.get('.react-flow__background').should('be.visible');
    cy.get('.react-flow__attribution').should('be.visible');
  });

  it('displays the autocomplete dropdown', () => {
    cy.get('label').should('include.text', 'Open Workflow');
  });

  it('displays the Add Nodes Accordion', () => {
    cy.get('p').should('include.text', 'Add Nodes');
  });

  it('displays the Edit Graph', () => {
    cy.get('p').should('include.text', 'Edit Graph');
  });

  it('displays the Execution History', () => {
    cy.get('p').should('include.text', 'Execution History');
  });

  it('should be able to open and close Add Nodes and see General category', () => {
    cy.contains('ewokscore').should('be.visible');
    cy.contains('Add Nodes').parents('.MuiButtonBase-root').click();
    cy.contains('ewokscore').should('not.be.visible');
  });

  it('should be able to open and close Edit Graph and see graph editing elements', () => {
    cy.contains('Label').should('not.be.visible');
    cy.contains('Comment').should('not.be.visible');
    cy.contains('Category').should('not.be.visible');
    cy.contains('Edit Graph').parents('.MuiButtonBase-root').click();
    cy.contains('Label').should('be.visible');
    cy.contains('Comment').should('be.visible');
    cy.contains('Category').should('be.visible');
  });

  it('should be able to open and close Execution History and see the buttons', () => {
    cy.contains('Execution History').parents('.MuiButtonBase-root').click();

    cy.contains('Execution History')
      .parents('.MuiAccordion-root')
      .children()
      .find('button')
      .should('have.length', 2)
      .last()
      .should('have.text', 'Clean all');

    cy.get('.MuiSwitch-root').should('have.length', 0);

    cy.contains('Execution History')
      .parents('.MuiAccordion-root')
      .children()
      .find('button')
      .should('have.length', 2)
      .first()
      .should('have.text', 'All Executions')
      .click();

    cy.get('.MuiSwitch-root').should('have.length', 2);
  });
});
