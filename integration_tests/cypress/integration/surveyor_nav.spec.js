/// <reference types="Cypress" />

export function testNavBar() {
    describe('The sidebar should: ', () => {
        it('redirect to /leaderboard when you click on "Leaderboard"', () => {
            cy.get('#sidebarMenu').contains('Leaderboard').click()
            cy.location('pathname').should('eq', '/leaderboard')
        })
    
        it('redirect to /groups when you click on "Groups"', () => {
            cy.get('#sidebarMenu').contains('Groups').click()
            cy.location('pathname').should('eq', '/groups')
        })
    
        it('redirect to /users when you click on "Manage Users"', () => {
            cy.get('#sidebarMenu').contains('Manage Users').click()
            cy.location('pathname').should('eq', '/users')
        })
    
        it('redirect to /history when you click on "Task History"', () => {
            cy.get('#sidebarMenu').contains('Task History').click()
            cy.location('pathname').should('eq', '/history')
        })
        
        it('redirect to /organisation when you click on "Organisation"', () => {
            cy.get('#sidebarMenu').contains('Organisation').click()
            cy.location('pathname').should('eq', '/organisation')
        })
    })
}