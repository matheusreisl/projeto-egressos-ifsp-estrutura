<?php

/**
 * Cria, na base central de participantes, os atributos que a importacao usa.
 *
 * Existe porque a API RemoteControl grava valores de atributo da base central
 * (`cpd_importParticipants`), mas so de atributos que ja existem — e nao tem
 * metodo que os crie. Conferido na E17 contra a lista de metodos da instancia.
 * Criar pela tela contraria o criterio K7 da ADR-0002.
 *
 * Usa o mesmo modelo que o painel (ParticipantAttributeName). E idempotente:
 * atributo que ja existe com o mesmo nome e mantido.
 *
 * Cifragem. A plataforma ja cifra nome, sobrenome e e-mail da base central por
 * padrao. Os atributos de contato deste projeto entram cifrados do mesmo modo —
 * deixa-los em claro ao lado de um e-mail cifrado esvaziaria a protecao. Os
 * academicos e o identificador ficam em claro. Marca-se com ":cifrado".
 * Trocar a marca de um atributo que ja tem valores e RECUSADO: os valores
 * gravados nao mudam sozinhos, e a leitura passaria a falhar.
 *
 * Uso, dentro do conteiner, com os nomes separados por virgula:
 *
 *   YII_CONSOLE_COMMANDS=<dir> php application/commands/console.php \
 *       prepararbasecentral identificador,curso,...,telefone:cifrado
 *
 * Quem chama e o instrumento.py (subcomando preparar-participantes).
 * Imprime uma linha por atributo: "<nome> <id> <cifrado|claro> criado|existente".
 */
class PrepararbasecentralCommand extends CConsoleCommand
{
    public function run($args)
    {
        if (count($args) !== 1 || trim($args[0]) === '') {
            fwrite(STDERR, "uso: prepararbasecentral nome1,nome2,...\n");
            return 2;
        }
        $pedidos = [];
        foreach (array_filter(array_map('trim', explode(',', $args[0]))) as $item) {
            if (!preg_match('/^([a-z][a-z0-9_]{0,63})(:cifrado)?$/', $item, $m)) {
                fwrite(STDERR, "nome de atributo invalido: $item\n");
                return 2;
            }
            $pedidos[$m[1]] = isset($m[2]) ? 'Y' : 'N';
        }

        foreach ($pedidos as $nome => $cifra) {
            $rotuloCifra = $cifra === 'Y' ? 'cifrado' : 'claro';
            $existente = ParticipantAttributeName::model()
                ->findByAttributes(array('defaultname' => $nome));
            if ($existente !== null) {
                if ($existente->encrypted !== $cifra) {
                    $valores = ParticipantAttribute::model()
                        ->countByAttributes(['attribute_id' => $existente->attribute_id]);
                    if ($valores > 0) {
                        fwrite(STDERR, "$nome tem $valores valores gravados: a marca de "
                            . "cifragem nao pode mudar com dados na base\n");
                        return 1;
                    }
                    $existente->encrypted = $cifra;
                    $existente->save();
                    echo "$nome {$existente->attribute_id} $rotuloCifra existente (cifragem ajustada)\n";
                    continue;
                }
                echo "$nome {$existente->attribute_id} $rotuloCifra existente\n";
                continue;
            }
            $atributo = new ParticipantAttributeName();
            $atributo->attribute_type = 'TB';   // caixa de texto
            $atributo->defaultname = $nome;
            $atributo->visible = 'TRUE';
            $atributo->encrypted = $cifra;
            $atributo->core_attribute = 'N';
            if (!$atributo->save()) {
                fwrite(STDERR, "falha ao criar $nome: " . json_encode($atributo->getErrors()) . "\n");
                return 1;
            }
            // O painel grava o rotulo no idioma da sessao do administrador, que
            // no console nao existe; aqui o idioma e explicito.
            $rotulo = new ParticipantAttributeNameLang();
            $rotulo->attribute_id = (int) $atributo->attribute_id;
            $rotulo->attribute_name = $nome;
            $rotulo->lang = 'pt-BR';
            if (!$rotulo->save()) {
                fwrite(STDERR, "falha ao rotular $nome: " . json_encode($rotulo->getErrors()) . "\n");
                return 1;
            }
            echo "$nome {$atributo->attribute_id} $rotuloCifra criado\n";
        }
        return 0;
    }
}
