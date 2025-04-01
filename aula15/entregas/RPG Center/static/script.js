function adicionarAtaque() {
    let listaAtaques = document.getElementById("lista-ataques");
    let index = listaAtaques.querySelectorAll("li").length; // Conta os ataques existentes

    let ataqueContainer = document.createElement("li");

    ataqueContainer.innerHTML = `
        
        <label><strong>Arma:</strong></label>
        <input type="text" name="ataques[\${index}][arma]" required><br>

        <label><strong>Bônus:</strong></label>
        <input type="number" name="ataques[\${index}][bonos]" required><br>

        <label><strong>Dado:</strong></label>
        <input type="number" name="ataques[\${index}][dado]" required><br>

        <button class="botao botao_mesa" type="button" onclick="removerAtaque(this)">Remover</button>
    `;

    listaAtaques.appendChild(ataqueContainer);
}

function removerAtaque(botao) {
    botao.parentElement.remove();
}

function calcularAtaque() {
    // Pega os valores do dado e bônus
    let ladosDado = document.getElementById("ladosDado").value;
    let bonus = document.getElementById("bonosDado").value;

    // Gera um número aleatório de 1 até o valor de ladosDado
    let valorDado = Math.floor(Math.random() * ladosDado) + 1;

    // Calcula o resultado
    let resultado = parseInt(valorDado) + parseInt(bonus);

    // Exibe o resultado no elemento <span>
    let resultadoSpan = document.getElementById("resultado");
    resultadoSpan.innerHTML = `${valorDado} + ${bonus} = ${resultado}`;
}