// Script para login.html

// Prevenir o comportamento padrão do formulário
document.querySelector('form').addEventListener('submit', async (e) => {
    e.preventDefault(); // Impede o formulário de recarregar a página
    
    // Capturar os valores dos inputs
    const email = document.getElementById('user').value;
    const senha = document.getElementById('pass').value;
    
    // Validação básica no front-end
    if (!email || !senha) {
        alert('Por favor, preencha todos os campos!');
        return;
    }
    
    try {
        // Enviar dados para o servidor Flask
        const resposta = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                senha: senha
            })
        });
        
        // Receber resposta do servidor
        const dados = await resposta.json();
        
        if (dados.sucesso) {
            // Login bem-sucedido
            alert(dados.mensagem);
            
            // Salvar informações do usuário no localStorage
            localStorage.setItem('usuario_logado', JSON.stringify(dados.usuario));
            
            // Redirecionar para página de conteúdo
            window.location.href = 'home/index.html';
        } else {
            // Login falhou
            alert(dados.mensagem);
        }
        
    } catch (erro) {
        console.error('Erro ao fazer login:', erro);
        alert('Erro ao conectar com o servidor. Verifique se o servidor Flask está rodando!');
    }
});