/// <reference types="Cypress" />

import { testNavBar } from "./nav.spec.js";

context("The Progress page ", () => {
  beforeEach(() => {
    cy.LogInAsRespondent();
    cy.visit("/progress");
  });

  it("Displays the same number of canvases and graphs as the number of groups that the respondent is in", () => {
    cy.get("canvas").should("have.length", 1);
  });

  testNavBar();
});
