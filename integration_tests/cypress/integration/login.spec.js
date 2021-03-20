/// <reference types="Cypress" />

describe("Log In", () => {
  before(() => {
    cy.fixture("users.json").as("usersData");
  });

  beforeEach(() => {
    cy.visit("/");
  });

  // https://on.cypress.io/interacting-with-elements

  it("Accepts valid username/passwords", () => {
    // https://on.cypress.io/type
    cy.get("#id_login")
      .type("christine@black.com")
      .should("have.value", "christine@black.com");

    cy.get("#id_password")
      .type("activityleague")
      .should("have.value", "activityleague");

    cy.get("button[type=submit]").click();
    cy.location("pathname").should("eq", "/dashboard");
  });

  it("Rejects invalid credentials", () => {
    cy.get("#id_login")
      .type("invalid@email.com")
      .should("have.value", "invalid@email.com");

    cy.get("#id_password")
      .type("activityleague")
      .should("have.value", "activityleague");

    cy.get("button[type=submit]").click();
    cy.location("pathname").should("eq", "/accounts/login/");
  });

  it("Takes you to Google SSO on Google button click", () => {
    cy.get(".sb-google").click();

    cy.url().should("contain", "google.com");
  });

  it("Takes you to the forgot password page on forgot password click", () => {
    cy.get('a[href="/accounts/password/reset/"]').click();
    cy.location("pathname").should("eq", "/accounts/password/reset/");
  });

  it("Takes you to the create or/ganisation  page on create organisation click", () => {
    cy.get('a[href="/create-organisation"]').click();
    cy.location("pathname").should("eq", "/create-organisation");
  });
});
