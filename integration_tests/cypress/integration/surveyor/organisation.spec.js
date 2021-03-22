/// <reference types="Cypress" />

import { testNavBar } from "./nav.spec.js";

describe("The Organisation page: ", () => {
  beforeEach(() => {
    cy.LogInAsSurveyor();
    cy.visit("/organisation");
  });

  it("Should sort the table by First Name alphabetically if you click on the First Name heading", () => {
    cy.get("tbody tr:first td").eq(0).should("have.text", "Christine");
    cy.get("tbody tr:first td").eq(1).should("have.text", "Black");
    cy.get(".sortable").eq(0).click();
    cy.get("tbody tr:first td").eq(0).should("have.text", "Ben");
    cy.get("tbody tr:first td").eq(1).should("have.text", "Connolly");
  });

  it("Should sort the table by Surname alphabetically if you click on the Surname heading", () => {
    cy.get("tbody tr:first td").eq(0).should("have.text", "Christine");
    cy.get("tbody tr:first td").eq(1).should("have.text", "Black");
    cy.get(".sortable").eq(1).click().click();
    cy.get("tbody tr:first td").eq(0).should("have.text", "Reece");
    cy.get("tbody tr:first td").eq(1).should("have.text", "Gilbert");
  });

  it("Should display the user specified in the search box", () => {
    cy.get("tbody tr").should("have.length", 3);
    cy.get("tbody tr:first td").eq(0).should("have.text", "Christine");
    cy.get("tbody tr:first td").eq(1).should("have.text", "Black");
    cy.get("input[type=search]").type("Reece");
    cy.get("tbody tr").should("have.length", 1);
    cy.get("tbody tr:first td").eq(0).should("have.text", "Reece");
    cy.get("tbody tr:first td").eq(1).should("have.text", "Gilbert");
  });

  
  it("Should display a modal when the Add Member button is clicked", () => {
    cy.get("#modal-add-surveyor").should("be.hidden");
    cy.get(".btn").contains("Add Member").click();
    cy.get("#modal-add-surveyor").should("be.visible");
  });
  
  it("Should display a modal when the Add Multiple Members button is clicked", () => {
    cy.get("#modal-add-multiple-surveyors").should("be.hidden");
    cy.get(".btn").contains("Add Multiple Members").click();
    cy.get("#modal-add-multiple-surveyors").should("be.visible");
  });

  testNavBar();
});
