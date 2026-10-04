<?php

/**
 * Garante que a tabela de participantes de um questionario tenha as colunas
 * attribute_1 a attribute_N, acrescentando as que faltarem.
 *
 * Existe porque a API RemoteControl cria a tabela de participantes com os
 * atributos pedidos (`activate_tokens`), mas, se a tabela ja existe, responde
 * "OK" e NAO acrescenta coluna alguma — conferido na E17. E a E20 precisou de
 * um setimo atributo (`variante_lembrete`) num instrumento ja ativo, com 500
 * participantes. Acrescentar pela tela contraria o criterio K7 da ADR-0002.
 *
 * Faz o mesmo que o painel (Tokens::updatetokenattributes): coluna `text`
 * acrescentada a tabela existente, sem tocar as outras nem os participantes.
 * A descricao do atributo e gravada depois, pela API, por quem chama.
 * Idempotente: coluna existente e mantida.
 *
 * Uso, dentro do conteiner:
 *
 *   YII_CONSOLE_COMMANDS=<dir> php application/commands/console.php \
 *       completaratributos <sid> <N>
 *
 * Quem chama e o instrumento.py (subcomando aplicar-mensagens).
 * Imprime uma linha por coluna: "attribute_<i> existente|acrescentada".
 */
class CompletaratributosCommand extends CConsoleCommand
{
    public function run($args)
    {
        if (count($args) !== 2 || !ctype_digit($args[0]) || !ctype_digit($args[1])) {
            fwrite(STDERR, "uso: completaratributos <sid> <N>\n");
            return 2;
        }
        $sid = (int) $args[0];
        $n = (int) $args[1];
        if ($n < 1 || $n > 100) {
            fwrite(STDERR, "N fora de 1..100\n");
            return 2;
        }
        $survey = Survey::model()->findByPk($sid);
        if ($survey === null) {
            fwrite(STDERR, "questionario $sid nao existe\n");
            return 1;
        }
        if (!$survey->hasTokensTable) {
            fwrite(STDERR, "questionario $sid nao tem tabela de participantes\n");
            return 1;
        }
        $db = Yii::app()->db;
        $tabela = $survey->tokensTableName;
        $colunas = $db->schema->getTable($tabela, true)->columnNames;
        for ($i = 1; $i <= $n; $i++) {
            $coluna = "attribute_$i";
            if (in_array($coluna, $colunas, true)) {
                echo "$coluna existente\n";
                continue;
            }
            $db->createCommand($db->getSchema()->addColumn($tabela, $coluna, 'text'))->execute();
            echo "$coluna acrescentada\n";
        }
        // A web guarda o esquema das tabelas em cache de arquivo por uma hora
        // (internal.php, schemaCachingDuration). Sem esvazia-lo, ela segue sem
        // a coluna nova e recusa gravar nela ("Property ... is not defined") —
        // observado na E20. O cache do console NAO serve para isso: no console
        // o componente e CDummyCache (YII_DEBUG ligado), e seu flush() nao faz
        // nada — tambem observado. Esvazia-se o cache de arquivo da web pelo
        // caminho, que e o mesmo diretorio de runtime. E inofensivo: e cache.
        // Sempre, e nao so quando acrescenta, para que uma execucao interrompida
        // depois do ALTER se resolva rodando de novo.
        $cache = new CFileCache();
        $cache->cachePath = Yii::app()->getRuntimePath() . DIRECTORY_SEPARATOR . 'cache';
        $cache->init();
        $cache->flush();
        echo "cache de esquema da web esvaziado ({$cache->cachePath})\n";
        return 0;
    }
}
