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

    it('redirect to /progress when you click on "Progress"', () => {
      cy.get("#sidebarMenu").contains("Progress").click();
      cy.location("pathname").should("eq", "/progress");
    });
  });
}
