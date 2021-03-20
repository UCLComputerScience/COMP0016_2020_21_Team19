/// <reference types="Cypress" />

import { testNavBar } from "./nav.spec.js";

describe("The Manage users page: ", () => {
  beforeEach(() => {
    cy.LogInAsSurveyor();
    cy.visit("/users");
  });

  it("Should take you to the User Progress page if you click on a user in the table", () => {
    cy.get("tbody tr:first").click();
    cy.location("pathname").should("contain", "user/");
  });

  it("Should sort the table by First Name alphabetically if you click on the First Name heading", () => {
    cy.get("tbody tr:first td").eq(0).should("have.text", "Jack");
    cy.get("tbody tr:first td").eq(1).should("have.text", "White");
    cy.get(".sortable").eq(0).click();
    cy.get("tbody tr:first td").eq(0).should("have.text", "Isabelle");
    cy.get("tbody tr:first td").eq(1).should("have.text", "Chandler");
  });

  it("Should sort the table by Surname alphabetically if you click on the Surname heading", () => {
    cy.get("tbody tr:first td").eq(0).should("have.text", "Jack");
    cy.get("tbody tr:first td").eq(1).should("have.text", "White");
    cy.get(".sortable").eq(1).click();
    cy.get("tbody tr:first td").eq(0).should("have.text", "Jean");
    cy.get("tbody tr:first td").eq(1).should("have.text", "Brunton");
    cy.get(".sortable").eq(1).click();
    cy.get("tbody tr:first td").eq(0).should("have.text", "Jack");
    cy.get("tbody tr:first td").eq(1).should("have.text", "White");
  });

  it("Should display the task specified in the search box", () => {
    cy.get("tbody tr:first td").eq(0).should("have.text", "Jack");
    cy.get("tbody tr:first td").eq(1).should("have.text", "White");
    cy.get("input[type=search]").type("John");
    cy.get("tbody tr").should("have.length", 1);
    cy.get("tbody tr:first td").eq(0).should("have.text", "John");
    cy.get("tbody tr:first td").eq(1).should("have.text", "Doe");
  });

  it("Should take you to a manage group page if you click on one of the pill group tags", () => {
    cy.get(".badge").contains("COPD Therapy").click();
    cy.location("pathname").should("contain", "manage-group/");
  });

  testNavBar();
});
