/// <reference types="Cypress" />

import { testNavBar } from "./nav.spec.js";

describe("The leaderboard page: ", () => {
  beforeEach(() => {
    cy.LogInAsSurveyor();
    cy.visit("/leaderboard");
  });

  it("Group button should deactivate when others are pressed.", () => {
    let old_btn = cy.get(".btn-primary");
    cy.get(".btn-light").click;
    old_btn.should("not.have.class", "btn-primary");
  });

  testNavBar();
});
