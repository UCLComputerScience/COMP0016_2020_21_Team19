/// <reference types="cypress" />

context('Actions', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8000')
  })

  // https://on.cypress.io/interacting-with-elements

  it('accepts valid username/passwords', () => {
    // https://on.cypress.io/type
    cy.get('#id_login')
      .type('christine@black.com').should('have.value', 'christine@black.com')

    cy.get('#id_password')
      .type('activityleague')
      .should('have.value', 'activityleague')

    cy.get('button[type=submit]').click();
    cy.location('pathname').should('eq', '/dashboard')
  })

})
