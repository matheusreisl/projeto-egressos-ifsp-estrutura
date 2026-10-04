<?php

/**
 * Registra uma importacao na trilha propria `egressos_importacoes` (E17).
 *
 * A trilha e o que a E11 exige de cada importacao — data, resumo SHA-256 do
 * arquivo e contagens por regra — e alimenta a auditoria da E23. Nao guarda
 * dado pessoal: o arquivo e identificado pelo resumo, e os registros afetados,
 * no relatorio da execucao, pela linha e pelo identificador.
 *
 * Fica na mesma base da plataforma, como a `egressos_devolucoes` da E09, com
 * prefixo proprio para nao se confundir com as tabelas do LimeSurvey.
 *
 * Entrada, em JSON pela entrada padrao: um objeto com as colunas da tabela.
 * Saida: o id do registro criado.
 */
class RegistrarimportacaoCommand extends CConsoleCommand
{
    const COLUNAS = [
        'importado_em', 'arquivo_sha256', 'questionario', 'modo', 'situacao',
        'motivo', 'registros', 'aceitos', 'aceitos_com_alerta', 'rejeitados',
        'contagens_por_regra', 'base_central_criados', 'base_central_atualizados',
        'participantes_criados', 'participantes_atualizados',
        'bloqueados_por_recusa', 'origem_substituiu_correcao', 'arquivo_eliminado',
    ];

    public function run($args)
    {
        $linha = json_decode(stream_get_contents(STDIN), true);
        if (!is_array($linha) || empty($linha['arquivo_sha256'])) {
            fwrite(STDERR, "entrada invalida: esperado JSON com 'arquivo_sha256'\n");
            return 2;
        }
        $db = Yii::app()->db;
        $db->createCommand("
            CREATE TABLE IF NOT EXISTS egressos_importacoes (
              id                         INT AUTO_INCREMENT PRIMARY KEY,
              importado_em               DATETIME     NOT NULL,
              arquivo_sha256             CHAR(64)     NOT NULL,
              questionario               INT          NOT NULL,
              modo                       VARCHAR(10)  NOT NULL,
              situacao                   VARCHAR(20)  NOT NULL,
              motivo                     TEXT         NULL,
              registros                  INT          NOT NULL DEFAULT 0,
              aceitos                    INT          NOT NULL DEFAULT 0,
              aceitos_com_alerta         INT          NOT NULL DEFAULT 0,
              rejeitados                 INT          NOT NULL DEFAULT 0,
              contagens_por_regra        TEXT         NULL,
              base_central_criados       INT          NOT NULL DEFAULT 0,
              base_central_atualizados   INT          NOT NULL DEFAULT 0,
              participantes_criados      INT          NOT NULL DEFAULT 0,
              participantes_atualizados  INT          NOT NULL DEFAULT 0,
              bloqueados_por_recusa      INT          NOT NULL DEFAULT 0,
              origem_substituiu_correcao INT          NOT NULL DEFAULT 0,
              arquivo_eliminado          TINYINT(1)   NOT NULL DEFAULT 0,
              KEY por_arquivo (arquivo_sha256),
              KEY por_questionario (questionario, importado_em)
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")->execute();
        $dados = array_intersect_key($linha, array_flip(self::COLUNAS));
        $db->createCommand()->insert('egressos_importacoes', $dados);
        echo $db->getLastInsertID();
        return 0;
    }
}
