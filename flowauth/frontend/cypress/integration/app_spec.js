/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

describe("App", function () {
    it("Render correct component according to login status", function () {
        // Check that login screen renders initially
        cy.visit("/");
        cy.contains("Sign in");
        // Log in, reload, and check that dashboard renders
        cy.login();
        cy.visit("/");
        cy.contains("My Servers");
        // Log out, reload, and check that login screen renders again
        cy.request("/signout");
        cy.visit("/");
        cy.contains("Sign in");
    });

    it("Log out on receiving a 401 error", function () {
        // Log in as a non-admin user
        cy.login();
        cy.visit("/");
        // Send request to an admin route, to get a 401 response
        cy.request({ url: "/admin/servers", failOnStatusCode: false });
        // Check that frontend displays login screen
        cy.contains("Sign in");
        // Check that we are still logged out after reloading the page
        cy.visit("/");
        cy.contains("Sign in");
    });
});
