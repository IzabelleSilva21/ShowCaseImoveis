// console.log("O arquivo mascaras.js foi carregado com sucesso!");
document.addEventListener("DOMContentLoaded", function () {
    const inputTelefone = document.getElementById("telefone");

    if (inputTelefone) {
        inputTelefone.addEventListener("input", function (e) {
            let value = e.target.value.replace(/\D/g, ""); // Remove tudo o que não é dígito

            // Limita a 11 caracteres (DDD + 9 dígitos)
            if (value.length > 11) {
                value = value.slice(0, 11);
            }

            // Aplica a formatação dinamicamente
            if (value.length > 10) {
                // Formato para celular: (XX) XXXXX-XXXX
                value = value.replace(/^(\d{2})(\d{5})(\d{4})$/, "($1) $2-$3");
            } else if (value.length > 6) {
                // Formato intermediário enquanto digita
                value = value.replace(/^(\d{2})(\d{4})(\d{0,4})$/, "($1) $2-$3");
            } else if (value.length > 2) {
                value = value.replace(/^(\d{2})(\d{0,5})$/, "($1) $2");
            } else if (value.length > 0) {
                value = value.replace(/^(\d*)$/, "($1");
            }

            e.target.value = value;
        });
    }
});