document.getElementById("addProduto").addEventListener("click", function () {
    const produtosDiv = document.getElementById("produtos");
    const novoProduto = document.createElement("div");
    novoProduto.classList.add("produto");
    novoProduto.innerHTML = `
        <label for="medicamento">Medicamento:</label>
        <select name="medicamento" class="medicamento">
            <option value="Paracetamol">Paracetamol</option>
            <option value="Dipirona">Dipirona</option>
            <option value="Shampoo">Shampoo</option>
        </select>
        <label for="quantidade">Quantidade:</label>
        <input type="number" name="quantidade" class="quantidade" min="1" required>
    `;
    produtosDiv.appendChild(novoProduto);
});

document.getElementById("cubagemForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    const medicamentos = document.querySelectorAll(".medicamento");
    const quantidades = document.querySelectorAll(".quantidade");

    const produtos = [];
    for (let i = 0; i < medicamentos.length; i++) {
        produtos.push({
            medicamento: medicamentos[i].value,
            quantidade: parseInt(quantidades[i].value),
        });
    }

    const response = await fetch("http://127.0.0.1:5000/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ produtos }),
    });

    const data = await response.json();
    if (response.ok) {
        let resultadoHTML = "";

        for (const [tipo, info] of Object.entries(data)) {
            resultadoHTML += `<h3>Tipo: ${tipo}</h3>`;

            info.distribuicao.forEach((dist, index) => {
                resultadoHTML += `
                    <p><strong>Embalagem ${index + 1} (${dist.embalagem}):</strong></p>
                    <ul>
                        ${Object.entries(dist.itens)
                        .map(([med, qtd]) => `<li>${med}: ${qtd}</li>`)
                        .join("")}
                    </ul>
                `;
            });
        }
        console.log(resultadoHTML)
        document.getElementById("resultado").innerHTML = resultadoHTML;
    } else {
        document.getElementById("resultado").innerHTML = `<p style="color: red;">${data.error}</p>`;
    }
});
