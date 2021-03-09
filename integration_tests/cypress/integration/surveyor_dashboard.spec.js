/// <reference types="cypress" />

before(() => {
    // Sign in to the site
    cy.visit('/')
    cy.get('#id_login')
      .type('christine@black.com')
      .should('have.value', 'christine@black.com')

    cy.get('#id_password')
      .type('activityleague')
      .should('have.value', 'activityleague')

    cy.get('button[type=submit]').click();
})

context('Actions', () => {

    beforeEach(() => {
      cy.visit('/')
    })
    
    it('Takes you to new task page when you click new task', () => {
        cy.get('a[href="/accounts/password/reset/"]').click()
        cy.location('pathname').should('eq', '/accounts/password/reset/')
    })

    it('Takes you to new task page when you click new task', () => {
        cy.get('a[href="/accounts/password/reset/"]').click()
        cy.location('pathname').should('eq', '/accounts/password/reset/')
    })

})