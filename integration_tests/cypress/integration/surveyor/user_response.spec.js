/// <reference types="Cypress" />

import { testNavBar } from "./nav.spec.js";

describe("The user progress page: ", () => {
  beforeEach(() => {
    cy.LogInAsSurveyor();
    cy.visit("/users");
    cy.get("tbody tr:first").click();
    cy.get("tbody tr:first").click();
  });

  it("Should show a form which cannot be edited", () => {
    cy.get("fieldset").should("be.disabled");
  });

  it("Should have data in each text field", () => {
    cy.get("input[type=text]").each((elem) => {
      expect(elem).to.not.have.prop("placeholder", "");
    });
  });

  testNavBar();
});
