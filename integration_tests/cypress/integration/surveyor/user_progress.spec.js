/// <reference types="Cypress" />

import { testNavBar } from "./nav.spec.js";

describe("The user progress page: ", () => {
  beforeEach(() => {
    cy.LogInAsSurveyor();
    cy.visit("/users");
    cy.get("tbody tr:first").click();
  });

  it("Should take you to the User Response page if you click on a user in the table", () => {
    cy.get("tbody tr:first").click();
    cy.location("pathname").should("contain", "response/");
  });

  it("Group button should deactivate when others are pressed.", () => {
    let old_btn = cy.get(".btn-primary");
    cy.get(".btn-light").click;
    old_btn.should("not.have.class", "btn-primary");
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

  it("Should sort the table by the Due Date if you click on the Due Date heading", () => {
    cy.get("tbody tr:first td").eq(2).should("contain.text", "Feb. 15, 2021");
    cy.get(".sortable").eq(2).click().click();
    cy.get("tbody tr:first td").eq(2).should("contain.text", "March 17, 2021");
  });

  it("Should display the task specified in the search box", () => {
    cy.get("tbody tr").should("have.length", 2);
    cy.get("tbody tr:first td").eq(0).should("have.text", "Active COPD Rehab");
    cy.get("input[type=search]").type("Sciatica Medication");
    cy.get("tbody tr").should("have.length", 1);
    cy.get("tbody tr:first td")
      .eq(0)
      .should("have.text", "Sciatica Medication");
  });

  testNavBar();
});
