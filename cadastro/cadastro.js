// Script para cadastro.html

// Prevenir o comportamento padrão do formulário
document.querySelector('form').addEventListener('submit', async (e) => {
    e.preventDefault(); // Impede o formulário de recarregar a página
    
    // Capturar os valores dos inputs
    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    const confirmarSenha = document.getElementById('confirmar-senha').value;
    
    // Validações no front-end
    if (!nome || !email || !senha || !confirmarSenha) {
        alert('Por favor, preencha todos os campos!');
        return;
    }
    
    if (senha !== confirmarSenha) {
        alert('As senhas não coincidem!');
        return;
    }
    
    if (senha.length < 6) {
        alert('A senha deve ter no mínimo 6 caracteres!');
        return;
    }
    
    try {
        // Enviar dados para o servidor Flask
        const resposta = await fetch('http://localhost:5000/cadastro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nome: nome,
                email: email,
                senha: senha
            })
        });
        
        // Receber resposta do servidor
        const dados = await resposta.json();
        
        if (dados.sucesso) {
            // Cadastro bem-sucedido
            alert(dados.mensagem);
            
            // Redirecionar para página de login
            window.location.href = 'index.html';
        } else {
            // Cadastro falhou
            alert(dados.mensagem);
        }
        
    } catch (erro) {
        console.error('Erro ao fazer cadastro:', erro);
        alert('Erro ao conectar com o servidor. Verifique se o servidor Flask está rodando!');
    }
});