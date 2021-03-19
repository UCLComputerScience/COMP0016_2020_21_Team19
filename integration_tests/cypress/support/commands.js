// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

Cypress.Commands.add("LogInAsSurveyor", () => {
    cy.visit('/')
    cy.get("[name=csrfmiddlewaretoken]")
      .should("exist")
      .should("have.attr", "value")
      .as("csrfToken");

    cy.get("@csrfToken").then((token) => {
      cy.request({
        method: "POST",
        url: "/accounts/login/", 
        form: true,
        body: {
          csrfmiddlewaretoken: token,
          login: "christine@black.com",
          password: "activityleague",
        },
        headers: {
          "X-CSRFTOKEN": token,
        },
      });
    });

    cy.getCookie("sessionid").should("exist");
    cy.getCookie("csrftoken").should("exist");
})

Cypress.Commands.add("LogInAsRespondent", () => {
  cy.visit('/')
  cy.get("[name=csrfmiddlewaretoken]")
    .should("exist")
    .should("have.attr", "value")
    .as("csrfToken");

  cy.get("@csrfToken").then((token) => {
    cy.request({
      method: "POST",
      url: "/accounts/login/", 
      form: true,
      body: {
        csrfmiddlewaretoken: token,
        login: "christine@black.com",
        password: "activityleague",
      },
      headers: {
        "X-CSRFTOKEN": token,
      },
    });
    cy.getCookie("sessionid").should("exist");
    cy.getCookie("csrftoken").should("exist");
    cy.visit('/dashboard')
  });
})