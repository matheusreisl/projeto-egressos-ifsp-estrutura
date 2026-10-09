<?php

/**
 * Repara o contato de uma pessoa na base central: o e-mail alternativo passa a
 * ser o principal (E26).
 *
 * E a metade da base central da operacao de reparo do P8 (secao 6.1 de
 * parametros-contato.md); a outra metade, o participante do questionario, e
 * pela API, em infra/reparo-contato.py, que chama este comando. Por que console:
 * o e-mail e o alternativo estao cifrados na base central, e so se le o
 * alternativo decifrando-o com os modelos da plataforma — a chave nao sai do
 * conteiner (o mesmo motivo da importacao, E17).
 *
 * O que grava:
 *   - o e-mail principal passa a ser o alternativo;
 *   - o alternativo fica vazio: o endereco que devolveu e conhecido como
 *     invalido, e nao volta a ser via de reparo. A devolucao fica registrada
 *     em egressos_devolucoes;
 *   - os valores *_origem NAO mudam. E o que faz a correcao sobreviver a
 *     reimportacao do mesmo arquivo, pela regra de precedencia da E17: o
 *     contato corrigido prevalece ate a origem mudar.
 *
 * Recusa, sem gravar nada: pessoa inexistente, pessoa com recusa de contato,
 * pessoa sem alternativo, e alternativo igual ao principal.
 *
 * Entrada, em JSON pela entrada padrao: {"participant_id": "..."}
 * Saida, em JSON: {"reparado": true, "email": "<novo principal>"} — o endereco
 * vai para quem chama, que o grava no participante do questionario, e nao e
 * impresso por ele; ou {"reparado": false, "motivo": "..."}.
 *
 * Quem chama e infra/reparo-contato.py, pelo console:
 *   YII_CONSOLE_COMMANDS=<dir> php application/commands/console.php \
 *       repararcontato < entrada.json
 */
class RepararcontatoCommand extends CConsoleCommand
{
    public function run($args)
    {
        $entrada = json_decode(stream_get_contents(STDIN), true);
        $pid = is_array($entrada) ? ($entrada['participant_id'] ?? '') : '';
        if ($pid === '') {
            fwrite(STDERR, "entrada invalida: esperado JSON com 'participant_id'\n");
            return 2;
        }

        // A decifracao do participante consulta o Expression Manager, que o
        // console nao carrega sozinho (armadilha 3 da E17).
        Yii::import('application.helpers.common_helper', true);
        Yii::import('application.helpers.expressions.em_manager_helper', true);

        $nome = ParticipantAttributeName::model()
            ->findByAttributes(['defaultname' => 'email_alternativo']);
        if ($nome === null) {
            fwrite(STDERR, "atributo email_alternativo ausente na base central\n");
            return 2;
        }

        $p = Participant::model()->findByPk($pid);
        if ($p === null) {
            return self::recusa('pessoa inexistente na base central');
        }
        if ($p->blacklisted === 'Y') {
            return self::recusa('pessoa com recusa de contato: nao se repara contato de quem recusou');
        }
        $p->decrypt();
        $principal = (string) $p->email;

        $atributo = ParticipantAttribute::model()->findByAttributes(
            ['participant_id' => $pid, 'attribute_id' => $nome->attribute_id]);
        $alternativo = '';
        if ($atributo !== null) {
            $atributo->decrypt();
            $alternativo = trim((string) $atributo->value);
        }
        if ($alternativo === '') {
            return self::recusa('sem e-mail alternativo');
        }
        if (mb_strtolower($alternativo) === mb_strtolower($principal)) {
            return self::recusa('alternativo igual ao principal');
        }

        $transacao = Yii::app()->db->beginTransaction();
        try {
            $p->email = $alternativo;
            $p->modified = date('Y-m-d H:i:s');
            if (!$p->encryptSave(true)) {
                throw new Exception('participante recusado: ' . json_encode($p->getErrors()));
            }
            $a = new ParticipantAttribute();
            $a->attribute_id = $nome->attribute_id;
            $a->participant_id = $pid;
            $a->value = '';
            $a->encrypt();
            $a->updateParticipantAttributeValue($a->attributes);
            $transacao->commit();
        } catch (Exception $e) {
            $transacao->rollback();
            fwrite(STDERR, 'reparo desfeito: ' . $e->getMessage() . "\n");
            return 1;
        }
        echo json_encode(['reparado' => true, 'email' => $alternativo], JSON_UNESCAPED_UNICODE);
        return 0;
    }

    private static function recusa($motivo)
    {
        echo json_encode(['reparado' => false, 'motivo' => $motivo], JSON_UNESCAPED_UNICODE);
        return 3;
    }
}
