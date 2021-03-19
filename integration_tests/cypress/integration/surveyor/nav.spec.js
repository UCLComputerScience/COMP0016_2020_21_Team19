/// <reference types="Cypress" />

export function testNavBar() {
  describe("The navbar should: ", () => {
    it('redirect to /dashboard when you click on "Activity League"', () => {
      cy.get("#navbar").contains("Activity League").click();
      cy.location("pathname").should("eq", "/dashboard");
    });

    it('redirect to /accounts/login when you click on "Sign Out"', () => {
      cy.get("#navbar .dropdown-toggle").click();
      cy.get("#navbar").contains("Sign Out").click();
      cy.location("pathname").should("eq", "/accounts/login/");
    });
  });

  describe("The sidebar should: ", () => {
    it('redirect to /dashboard when you click on "Dashboard"', () => {
      cy.get("#sidebarMenu").contains("Dashboard").click();
      cy.location("pathname").should("eq", "/dashboard");
    });

    it('redirect to /leaderboard when you click on "Leaderboard"', () => {
      cy.get("#sidebarMenu").contains("Leaderboard").click();
      cy.location("pathname").should("eq", "/leaderboard");
    });

    it('redirect to /groups when you click on "Groups"', () => {
      cy.get("#sidebarMenu").contains("Groups").click();
      cy.location("pathname").should("eq", "/groups");
    });

    it('redirect to /users when you click on "Manage Users"', () => {
      cy.get("#sidebarMenu").contains("Manage Users").click();
      cy.location("pathname").should("eq", "/users");
    });

    it('redirect to /history when you click on "Task History"', () => {
      cy.get("#sidebarMenu").contains("Task History").click();
      cy.location("pathname").should("eq", "/history");
    });

    it('redirect to /organisation when you click on "Organisation"', () => {
      cy.get("#sidebarMenu").contains("Organisation").click();
      cy.location("pathname").should("eq", "/organisation");
    });
  });
}
