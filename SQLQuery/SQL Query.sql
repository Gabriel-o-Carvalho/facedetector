CREATE DATABASE IF NOT EXISTS controle_acesso_dee;
USE controle_acesso_dee;

-- Tabela de usuários autorizados
CREATE TABLE usuarios (
    id SMALLINT UNSIGNED AUTO_INCREMENT, -- max 65535
    nome VARCHAR(60) NOT NULL,
    CPF VARCHAR(20) UNIQUE NOT NULL,
    tipo ENUM('Aluno', 'Professor', 'Técnico', 'Visitante', 'Terceirizado') NOT NULL,
    cadastro_valido_ate DATE NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Tabela de logs de acesso (autorizados ou não)
CREATE TABLE log_acesso (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, -- max 4294967295
    usuario_id INT, -- NULL se não autorizado
    autorizado BOOLEAN NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    imagem_base64 LONGTEXT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);