<?php

/**
 * Ativa o plugin AuditLog, a trilha de auditoria nativa da plataforma (E23).
 *
 * Existe porque a ativacao de plugin so e oferecida pela tela, e a E08 mostrou
 * que marcar `active = 1` no banco nao basta: a tabela de registro e criada pelo
 * evento `beforeActivate`, que essa via nao dispara. Ativar pela tela contraria
 * o criterio K7 da ADR-0002. Este comando faz o que o painel faz
 * (PluginManagerController::activate, conferido no codigo): carrega o plugin,
 * despacha `beforeActivate` e so entao marca o plugin como ativo.
 *
 * Idempotente: plugin ja ativo e tabela existente sao mantidos, e o evento
 * pode ser despachado de novo sem efeito — o plugin so cria a tabela que nao
 * existe.
 *
 * Uso, dentro do conteiner:
 *
 *   YII_CONSOLE_COMMANDS=<dir> php application/commands/console.php ativarauditoria
 *
 * Quem chama e infra/conformidade.py (subcomando aplicar). Imprime o estado do
 * plugin e o nome da tabela.
 */
class AtivarauditoriaCommand extends CConsoleCommand
{
    public function run($args)
    {
        $plugin = Plugin::model()->findByAttributes(['name' => 'AuditLog']);
        if ($plugin === null) {
            fwrite(STDERR, "plugin AuditLog nao encontrado\n");
            return 1;
        }
        $gerente = App()->getPluginManager();
        $gerente->loadPlugin($plugin->name, $plugin->id);
        $resultado = $gerente->dispatchEvent(
            new PluginEvent('beforeActivate', $this), $plugin->name);
        if (!$resultado->get('success', true)) {
            fwrite(STDERR, "beforeActivate recusou: "
                . ($resultado->get('message') ?: 'sem mensagem') . "\n");
            return 1;
        }
        if ((int) $plugin->active !== 1) {
            $plugin->active = 1;
            if (!$plugin->save()) {
                fwrite(STDERR, "nao foi possivel marcar o plugin como ativo\n");
                return 1;
            }
            echo "AuditLog ativado\n";
        } else {
            echo "AuditLog ja estava ativo\n";
        }

        $tabela = Yii::app()->db->tablePrefix . 'auditlog_log';
        if (Yii::app()->db->schema->getTable($tabela, true) === null) {
            fwrite(STDERR, "tabela $tabela nao existe depois da ativacao\n");
            return 1;
        }
        echo "tabela $tabela presente\n";

        // A web guarda o esquema em cache de arquivo; uma tabela nova precisa
        // dele vazio (o mesmo cuidado de completaratributos, E20).
        $cache = new CFileCache();
        $cache->cachePath = Yii::app()->getRuntimePath() . DIRECTORY_SEPARATOR . 'cache';
        $cache->init();
        $cache->flush();
        return 0;
    }
}
