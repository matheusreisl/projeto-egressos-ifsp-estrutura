<?php

/**
 * Grava, na base central de participantes, os registros ja validados de um
 * arquivo de entrada, aplicando a regra de precedencia da E17.
 *
 * Por que comando de console, e nao a API. A base central da plataforma CIFRA
 * nome, sobrenome e e-mail por padrao, e os atributos de contato deste projeto
 * tambem sao cifrados. A regra de precedencia precisa comparar o contato atual
 * e o ultimo valor visto na origem — e so se compara o que se decifra. Aqui,
 * dentro da plataforma, a decifracao e a dos proprios modelos, e a chave nunca
 * sai do conteiner. Pela API isso nao e possivel: ela nao devolve participante
 * da base central, e `cpd_importParticipants`, ao atualizar, ainda grava
 * blacklisted = 'N' quando o campo nao vem — apagaria a recusa permanente
 * (conferido no codigo da plataforma, E17).
 *
 * Regra de precedencia (docs/especificacao/importacao-base.md, secao 5):
 *   - nome e atributos academicos: prevalece a origem (E13, secao 12.5);
 *   - contato: prevalece o valor atual — talvez corrigido por busca ativa — ATE
 *     a origem mudar; se o arquivo traz valor diferente do ultimo visto, a
 *     origem tem informacao nova e prevalece, e a substituicao e contada;
 *   - recusa (blacklisted): nunca alterada aqui.
 *
 * Entrada, em JSON pela entrada padrao:
 *   {"idioma": "pt-BR", "registros": [{"participant_id", "nome",
 *    "identificador", "curso", "nivel", "campus", "ano_conclusao",
 *    "semestre_conclusao", "email_principal", "email_alternativo",
 *    "telefone"}, ...]}
 *
 * Saida, em JSON: contagens e, por participant_id, o e-mail principal final e
 * a recusa — o que a importacao precisa para criar os participantes do
 * questionario. Tudo numa transacao: ou grava todos, ou nenhum.
 *
 * Quem chama e scripts/importar_base.py, pelo console:
 *   YII_CONSOLE_COMMANDS=<dir> php application/commands/console.php \
 *       importarbasecentral < registros.json
 */
class ImportarbasecentralCommand extends CConsoleCommand
{
    const CONTATOS = ['email_principal', 'email_alternativo', 'telefone'];
    const ACADEMICOS = ['identificador', 'curso', 'nivel', 'campus',
                        'ano_conclusao', 'semestre_conclusao'];
    const DONO = 1;  // o administrador criado pela instalacao

    public function run($args)
    {
        $entrada = json_decode(stream_get_contents(STDIN), true);
        if (!is_array($entrada) || !isset($entrada['registros'])) {
            fwrite(STDERR, "entrada invalida: esperado JSON com 'registros'\n");
            return 2;
        }
        $idioma = $entrada['idioma'] ?? 'pt-BR';

        // A decifracao do participante consulta o Expression Manager, que a
        // aplicacao web carrega e o console nao — o mesmo que o comando
        // importsurvey da plataforma faz.
        Yii::import('application.helpers.common_helper', true);
        Yii::import('application.helpers.expressions.em_manager_helper', true);

        $ids = [];
        foreach (ParticipantAttributeName::model()->findAll() as $n) {
            $ids[$n->defaultname] = (int) $n->attribute_id;
        }
        $necessarios = array_merge(self::ACADEMICOS, ['email_alternativo', 'telefone'],
            array_map(function ($c) { return $c . '_origem'; }, self::CONTATOS));
        $faltando = array_diff($necessarios, array_keys($ids));
        if ($faltando) {
            fwrite(STDERR, 'atributos ausentes na base central: ' . implode(', ', $faltando)
                . " — rode instrumento.py preparar-participantes\n");
            return 2;
        }
        $nomePorId = array_flip($ids);

        $saida = ['criados' => 0, 'atualizados' => 0,
                  'origem_substituiu_correcao' => 0, 'participantes' => []];
        $transacao = Yii::app()->db->beginTransaction();
        try {
            foreach ($entrada['registros'] as $r) {
                $pid = $r['participant_id'];
                $p = Participant::model()->findByPk($pid);
                $novo = ($p === null);
                $atual = [];
                if ($novo) {
                    $p = new Participant();
                    $p->participant_id = $pid;
                    $p->blacklisted = 'N';
                    $p->owner_uid = self::DONO;
                    $p->created_by = self::DONO;
                    $p->created = date('Y-m-d H:i:s');
                } else {
                    $p->decrypt();
                    $atual['email_principal'] = (string) $p->email;
                    $valores = ParticipantAttribute::model()
                        ->findAllByAttributes(['participant_id' => $pid]);
                    foreach ($valores as $a) {
                        $a->decrypt();
                        if (isset($nomePorId[$a->attribute_id])) {
                            $atual[$nomePorId[$a->attribute_id]] = (string) $a->value;
                        }
                    }
                    $p->modified = date('Y-m-d H:i:s');
                }

                $final = [];
                $origem = [];
                foreach (self::CONTATOS as $c) {
                    $chegou = (string) ($r[$c] ?? '');
                    if ($novo) {
                        $final[$c] = $chegou;
                        $origem[$c] = $chegou;
                        continue;
                    }
                    $origemAnterior = $atual[$c . '_origem'] ?? '';
                    $valorAtual = $atual[$c] ?? '';
                    if (self::igual($c, $chegou, $origemAnterior)) {
                        // A origem nao mudou: fica o valor atual, corrigido ou nao.
                        $final[$c] = $valorAtual;
                        $origem[$c] = $origemAnterior;
                    } else {
                        // A origem traz informacao nova: prevalece.
                        $final[$c] = $chegou;
                        $origem[$c] = $chegou;
                        if (!self::igual($c, $valorAtual, $origemAnterior)) {
                            $saida['origem_substituiu_correcao']++;
                        }
                    }
                }

                // Nome: prevalece a origem. Recusa: nao se toca.
                $p->firstname = $r['nome'];
                $p->lastname = '';
                $p->email = $final['email_principal'];
                $p->language = $idioma;
                if (!$p->encryptSave(true)) {
                    throw new Exception("participante $pid recusado: " . json_encode($p->getErrors()));
                }

                $atributos = [];
                foreach (self::ACADEMICOS as $a) {
                    $atributos[$a] = (string) $r[$a];
                }
                $atributos['email_alternativo'] = $final['email_alternativo'];
                $atributos['telefone'] = $final['telefone'];
                foreach (self::CONTATOS as $c) {
                    $atributos[$c . '_origem'] = $origem[$c];
                }
                foreach ($atributos as $nome => $valor) {
                    $a = new ParticipantAttribute();
                    $a->attribute_id = $ids[$nome];
                    $a->participant_id = $pid;
                    $a->value = $valor;
                    $a->encrypt();  // so cifra o que estiver marcado como cifrado
                    $a->updateParticipantAttributeValue($a->attributes);
                }

                $saida[$novo ? 'criados' : 'atualizados']++;
                $saida['participantes'][$pid] = [
                    'email' => $final['email_principal'],
                    'blacklisted' => $novo ? 'N' : (string) $p->blacklisted,
                ];
            }
            $transacao->commit();
        } catch (Exception $e) {
            $transacao->rollback();
            fwrite(STDERR, 'importacao desfeita: ' . $e->getMessage() . "\n");
            return 1;
        }
        echo json_encode($saida, JSON_UNESCAPED_UNICODE);
        return 0;
    }

    private static function igual($campo, $a, $b)
    {
        if (strpos($campo, 'email') === 0) {
            return mb_strtolower((string) $a) === mb_strtolower((string) $b);
        }
        return (string) $a === (string) $b;
    }
}
