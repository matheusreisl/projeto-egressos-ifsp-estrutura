<?php

/**
 * Revoga a recusa de contato de uma pessoa (E23): tira o bloqueio da base
 * central e devolve `emailstatus = 'OK'` aos participantes dela que estiverem
 * com `OptOut`, em qualquer questionario.
 *
 * Por que comando de console, e nao a via da plataforma. A revogacao pelo
 * proprio egresso (OptinController, global) exige `allowunblacklist = Y`, que
 * fica DESLIGADO por decisao do orientando: com ele ligado, qualquer pessoa com
 * o endereco individual do egresso poderia desfazer a recusa dele. A revogacao
 * e feita pelo operador, a pedido do egresso — que responde a uma mensagem,
 * como o termo diz. E a API nao tem operacao sobre a lista de bloqueio.
 *
 * Grava pelos modelos da plataforma (Participant, Token), e nao por SQL, para
 * que a trilha de auditoria (AuditLog) registre a mudanca, como registra a
 * recusa. O registro proprio da revogacao — quando, a pedido de quem, por que
 * via — e de infra/conformidade.py, que chama este comando.
 *
 * Uso, dentro do conteiner:
 *
 *   YII_CONSOLE_COMMANDS=<dir> php application/commands/console.php \
 *       revogarrecusa <participant_id>
 *
 * Imprime uma linha por alteracao. Idempotente.
 */
class RevogarrecusaCommand extends CConsoleCommand
{
    public function run($args)
    {
        if (count($args) !== 1 || !preg_match('/^[0-9a-f-]{36}$/', $args[0])) {
            fwrite(STDERR, "uso: revogarrecusa <participant_id>\n");
            return 2;
        }
        $pid = $args[0];
        $pessoa = Participant::model()->findByPk($pid);
        if ($pessoa === null) {
            fwrite(STDERR, "pessoa $pid nao esta na base central\n");
            return 1;
        }
        if ($pessoa->blacklisted === 'Y') {
            $pessoa->blacklisted = 'N';
            if (!$pessoa->save()) {
                fwrite(STDERR, "nao foi possivel tirar o bloqueio da base central\n");
                return 1;
            }
            echo "base central: bloqueio retirado\n";
        } else {
            echo "base central: sem bloqueio\n";
        }

        foreach (Survey::model()->findAll() as $questionario) {
            if (!$questionario->hasTokensTable) {
                continue;
            }
            $sid = $questionario->sid;
            foreach (Token::model($sid)->findAllByAttributes(['participant_id' => $pid]) as $token) {
                if (strpos((string) $token->emailstatus, 'OptOut') !== 0) {
                    continue;
                }
                $token->emailstatus = 'OK';
                if (!$token->save()) {
                    fwrite(STDERR, "questionario $sid, tid {$token->tid}: nao foi possivel gravar\n");
                    return 1;
                }
                echo "questionario $sid, tid {$token->tid}: OptOut -> OK\n";
            }
        }
        return 0;
    }
}
