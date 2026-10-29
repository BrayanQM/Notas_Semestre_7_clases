describe("Inicio de sesión", () => {
    it("permite entrar con una cuenta válida", function () {
        const correo = "pedrito@gmail.com";
        const contrasena = "bolivia123";

        if (!correo || !contrasena) {
            this.skip();
        }

        cy.visit("/");
        cy.get("#vista-login").should("be.visible");
        cy.get("#correo-login").type(correo);
        cy.get("#contrasena-login").type(contrasena, { log: false });
        cy.get("#form-login").submit();

        cy.get("#vista-app").should("be.visible");
        cy.get("#usuario-nombre").should("be.visible").and("not.be.empty");
        cy.get("#usuario-perfil").should("be.visible").and("not.be.empty");
        cy.get("#seccion-producto").should("be.visible");
    });
});