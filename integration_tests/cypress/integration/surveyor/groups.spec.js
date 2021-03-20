/// <reference types="Cypress" />

import { testNavBar } from "./nav.spec.js";

describe("The groups page: ", () => {
  beforeEach(() => {
    cy.LogInAsSurveyor();
    cy.visit("/groups");
  });

  it("Should display a modal when the New Group button is clicked", () => {
    cy.get("#modal-new-group").should("be.hidden");
    cy.get(".btn").contains("New Group").click();
    cy.get("#modal-new-group").should("be.visible");
  });

  it("Should take you to a Manage Group page if you click into a Task in the table", () => {
    cy.get("tbody tr:first").click();
    cy.location("pathname").should("contain", "manage-group/");
  });

  it("Should show a confirmation dialog if you click the Delete button", () => {
    cy.on("window:confirm", (str) => {
      expect(str === "Are you sure you want to delete this group?").to.be.true;
      return false;
    });
    cy.get(".delete-group").eq(0).click();
  });

  testNavBar();
});
