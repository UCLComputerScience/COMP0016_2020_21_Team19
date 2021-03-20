/// <reference types="Cypress" />

import { testNavBar } from "./nav.spec.js";

describe("The New Task page: ", () => {
  beforeEach(() => {
    cy.LogInAsSurveyor();
    cy.visit("/new-task");
  });

  it("Should prompt user to fill in the empty fields when pressing Submit", () => {
    cy.get(".btn").contains("Submit").click();
    cy.get("input:invalid").should("have.length", 5);
    cy.get("select:invalid").should("have.length", 3);
  });

  it("The number of empty field prompts should decrease after a required field is filled in", () => {
    cy.get(".btn").contains("Submit").click();
    cy.get("input:invalid").should("have.length", 5);
    cy.get("select:invalid").should("have.length", 3);
    cy.get("#id_title").type("This is a title");
    cy.get(".btn").contains("Submit").click();
    cy.get("input:invalid").should("have.length", 4);
    cy.get("select:invalid").should("have.length", 3);
  });

  it("Should add another row for a question after clicking Add More", () => {
    cy.get("#form_set").children().should("have.length", 1);
    cy.get("#add_more").click();
    cy.get("#form_set").children().should("have.length", 2);
  });

  it("Should delete the added row after the Add More button followed by the Delete button is pressed", () => {
    cy.get("#form_set").children().should("have.length", 1);
    cy.get("#add_more").click();
    cy.get("#form_set").children().should("have.length", 2);
    cy.get("button").contains("Delete");
    cy.get("#form_set").children().should("have.length", 2);
  });

  it("Should take you back to the dashboard if Cancel is clicked", () => {
    cy.get(".btn").contains("Cancel").click();
    cy.location("pathname").should("eq", "/dashboard");
  });

  testNavBar();
});
