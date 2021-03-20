/// <reference types="Cypress" />

import { testNavBar } from "./nav.spec.js";

context("The Response page ", () => {
  beforeEach(() => {
    cy.LogInAsRespondent();
    cy.get("tbody tr:first").click();
  });
  
  it("Should prompt user to fill in the empty fields when pressing Submit", () => {
    cy.get(".btn").contains("Submit").click();
    cy.get("input:invalid").should("have.length", 13);
  });

  it("Should have read-write fields for each field", () => {
    cy.get("input").each((elem) => {
      expect(elem).not.to.be.disabled;
    });
  });

  it("Should take you back to the dashboard if Cancel is clicked", () => {
    cy.get(".btn").contains("Cancel").click();
    cy.location("pathname").should("eq", "/dashboard");
  });

  testNavBar();
});
