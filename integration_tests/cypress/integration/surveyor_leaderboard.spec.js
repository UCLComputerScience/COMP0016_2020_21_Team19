/// <reference types="Cypress" />

import { testNavBar } from './surveyor_nav.spec.js'

describe('The leaderboard page: ', () => {
    beforeEach(() => {
      cy.LogIn()
      cy.visit('/leaderboard')
    })
    
    it('Button should deactivate when others are pressed.', () => {
        let old_btn = cy.get('.btn-primary')
        cy.get('.btn-light').click
        old_btn = cy.get(old_btn)
        old_btn.should('not.have.class', 'btn-primary')
    })

    describe('Nav Bar Test: ', () => {
        testNavBar();
    })
})