/// <reference types="Cypress" />

import { testNavBar } from "./nav.spec.js";

describe("The leaderboard page: ", () => {
  beforeEach(() => {
    cy.LogInAsRespondent();
    cy.visit("/leaderboard");
  });

  it("Group button should deactivate when others are pressed.", () => {
    let old_btn = cy.get(".btn-primary");
    cy.get(".btn-light").eq(0).click;
    old_btn.should("not.have.class", "btn-primary");
  });

  it("Should change the rankings on the leaderboard to the group whose button has been pressed", () => {
    // We are expecting to click on the COPD Therapy button
    cy.get(".btn-light").eq(0).click;
    cy.get("tbody tr:first td").eq(0).should("have.text", "1");
  })

  testNavBar();
});
