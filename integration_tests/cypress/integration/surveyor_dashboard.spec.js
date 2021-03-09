/// <reference types="Cypress" />

import { testNavBar } from './surveyor_nav.spec.js'

context('Actions', () => {
    beforeEach(() => {
      cy.LogIn()
    })

    it('Takes you to the task overview page', () => {
        cy.get('#task1').click()
        cy.location('pathname').should('contain', 'task/')
    })

    it('Takes you to the New Task page', () => {
      cy.contains('New Task').click()
      cy.location('pathname').should('contain', 'new-task')
    })

    it('Test Sidebar', () => {
      testNavBar()
    })
})