// / <reference types="cypress" />

describe('example to-do app', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000');
  });

  it('displays a welcome message', () => {
    cy.get('h1').should('include.text', 'Welcome to the Ewoks-UI');
    cy.location('pathname').should('not.include', 'edit-workflows');
    cy.location('pathname').should('not.include', 'monitor-workflows');
  });

  it('offers 3 options to go ahead', () => {
    cy.get('a').should('have.length', 3);
  });

  it('has an img of the canvas', () => {
    cy.get('img').should('have.length', 1);
  });

  it('gets to editing when the appropriete button is pressed', () => {
    cy.get('a').first().should('have.text', 'Edit Workflows');
    cy.get('a').first().click();
    cy.contains('tutorial_Graph').should('not.exist');

    cy.location().should((loc) => {
      expect(loc.hash).to.eq('#/edit-workflows');
      expect(loc.host).to.eq('localhost:3000');
    });

    cy.go('back');
  });

  it('gets to editing when the appropriete button is pressed', () => {
    cy.get('a').last().should('have.text', 'Tutorial Workflow');
    cy.get('a').last().click();
    cy.get('h1').should('include.text', 'tutorial_Graph');

    cy.location().should((loc) => {
      expect(loc.hash).to.eq('#/edit-workflows');
      expect(loc.host).to.eq('localhost:3000');
    });
  });
});
