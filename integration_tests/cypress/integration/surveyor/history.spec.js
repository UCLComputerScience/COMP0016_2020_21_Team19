/// <reference types="Cypress" />

import { testNavBar } from "./nav.spec.js";

describe("The history page: ", () => {
  beforeEach(() => {
    cy.LogInAsSurveyor();
    cy.visit("/history");
  });

  it("Should take you to a Task Overview page if you click into a Task in the table", () => {
    cy.get("tbody tr:first").click();
    cy.location("pathname").should("contain", "task/");
  });

  it("Should sort the table by Task Name alphabetically if you click on the Task Name heading", () => {
    cy.get("tbody tr:first td").eq(0).should("have.text", "Active COPD Rehab");
    cy.get(".sortable").eq(0).click().click();
    cy.get("tbody tr:first td")
      .eq(0)
      .should("have.text", "Sciatica Medication");
  });

  it("Should sort the table by Group alphabetically if you click on the Group heading", () => {
    cy.get("tbody tr:first td").eq(1).should("have.text", "COPD Therapy");
    cy.get(".sortable").eq(1).click().click();
    cy.get("tbody tr:first td").eq(1).should("have.text", "Hip Therapy");
  });

  it("Should sort the table by the number of Users assigned if you click on the Users Assigned heading", () => {
    cy.get("tbody tr:first td").eq(2).should("have.text", "5");
    cy.get(".sortable").eq(2).click().click();
    cy.get("tbody tr:first td").eq(2).should("have.text", "5");
  });

  it("Should sort the table by the number of Users completed if you click on the Users Completed heading", () => {
    cy.get("tbody tr:first td").eq(3).should("have.text", "4");
    cy.get(".sortable").eq(3).click().click();
    cy.get("tbody tr:first td").eq(3).should("have.text", "4");
  });

  it("Should sort the table by the Due Date if you click on the Due Date heading", () => {
    cy.get("tbody tr:first td").eq(4).should("contain.text", "Feb. 15, 2021");
    cy.get(".sortable").eq(4).click().click();
    cy.get("tbody tr:first td").eq(4).should("contain.text", "March 17, 2021");
  });

  it("Should sort the table by the Status if you click on the Status heading", () => {
    cy.get("tbody tr:first td").eq(5).should("contain.text", "Incomplete");
    cy.get(".sortable").eq(5).click().click();
    cy.get("tbody tr:first td").eq(5).should("contain.text", "Incomplete");
  });

  it("Should display the task specified in the search box", () => {
    cy.get("tbody tr:first td").eq(0).should("have.text", "Active COPD Rehab");
    cy.get("input[type=search]").type("Sciatica Medication");
    cy.get("tbody tr").should("have.length", 1);
    cy.get("tbody tr:first td")
      .eq(0)
      .should("have.text", "Sciatica Medication");
  });

  testNavBar();
});
