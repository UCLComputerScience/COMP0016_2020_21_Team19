/// <reference types="Cypress" />

import { testNavBar } from "./nav.spec.js";

context("The dashboard page ", () => {
  beforeEach(() => {
    cy.LogInAsRespondent();
    cy.visit("/dashboard");
  });

  it("Takes you to the response page if the task is clicked", () => {
    cy.get("tbody tr:first").click();
    cy.location("pathname").should("contain", "response/");
  });

  testNavBar();
});
