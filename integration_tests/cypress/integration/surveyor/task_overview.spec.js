/// <reference types="Cypress" />

import { testNavBar } from "./nav.spec.js";
import "cypress-wait-until";

describe("The Task Overview page: ", () => {
  beforeEach(() => {
    cy.LogInAsSurveyor();
    cy.visit("/dashboard");
    cy.get("tbody tr:first").click();
  });

  it("Should mark a task as complete/incomplete after clicking Mark as complete/incomplete", () => {
    cy.get(".badge").should("contain.text", "Incomplete");
    cy.get(".btn").contains("Mark as complete").click();
    cy.get(".badge", { timeout: 5000 }).should("contain.text", "Complete");
    cy.get(".btn").contains("Mark as incomplete").click();
    cy.get(".badge", { timeout: 5000 }).should("contain.text", "Incomplete");
  });

  it("Should expand/collapse all cards when the Expand/Collapse all button is clicked", () => {
    cy.get("div[data-toggle=collapse]").each((elem) => {
      expect(elem).to.have.class("collapsed");
    });
    cy.get("#toggleAccordions-show").click();
    cy.get("div[data-toggle=collapse]").each((elem) => {
      expect(elem).not.to.have.class("collapsed");
    });
    cy.waitUntil(function () {
      return cy.get("#collapse1").should("not.have.class", "collapsing");
    });
    cy.get("#toggleAccordions-hide").click();
    cy.get("div[data-toggle=collapse]").each((elem) => {
      expect(elem).to.have.class("collapsed");
    });
  });

  it("Should hide the pie chart and showo the bar chart when the bar chart button is clicked", () => {
    cy.get("#toggleAccordions-show").click();
    cy.waitUntil(function () {
      return cy.get("#collapse1").should("not.have.class", "collapsing");
    });
    cy.get("[id$=canvas_pie]").each((elem) => {
      expect(elem).to.be.visible;
    });
    cy.get("[id$=canvas_bar]").each((elem) => {
      expect(elem).to.be.hidden;
    });
    cy.get("[id^=bar-chart-button]").each((elem) => {
      cy.wrap(elem).click({ force: true });
    });
    cy.wait(100);
    cy.get("[id$=canvas_pie]").each((elem) => {
      expect(elem).to.be.hidden;
    });
    cy.get("[id$=canvas_bar]").each((elem) => {
      expect(elem).to.be.visible;
    });
  });

  it("Should show a confirmation dialog if you click the Delete Task button", () => {
    cy.on("window:confirm", (str) => {
      expect(
        str ===
          "Deleting this task will also delete all responses associated with it. Are you sure you want to delete this task?"
      ).to.be.true;
      return false;
    });
    cy.get("#delete").eq(0).click();
  });

  testNavBar();
});
