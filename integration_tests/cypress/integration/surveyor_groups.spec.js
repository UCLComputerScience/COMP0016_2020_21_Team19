/// <reference types="Cypress" />

import { testNavBar } from './surveyor_nav.spec.js'

describe('The groups page: ', () => {
    beforeEach(() => {
      cy.LogIn()
      cy.visit('/groups')
    })
    
    it('Should display create group partial when the New Group button is clicked', () => {
        let old_btn = cy.get('.btn-primary')

        let btn = cy.get('.btn-light')
        btn.click()

        btn.should('have.class', 'btn-primary')
        old_btn.should('not.have.class', 'btn-primary')
    })

    describe('Nav Bar Test: ', () => {
        testNavBar();
    })
})