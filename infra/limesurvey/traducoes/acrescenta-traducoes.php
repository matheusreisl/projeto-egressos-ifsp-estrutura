<?php
/*
 * Acrescenta traducoes a um arquivo .mo do LimeSurvey (E23).
 *
 * Por que existe. A traducao pt-BR do LimeSurvey 7.2 nao tem as mensagens das
 * paginas de recusa e de revogacao GLOBAIS — as que o egresso ve ao confirmar
 * que nao quer mais ser contatado. A pagina saia com a frase principal em
 * ingles (achado da E22), no momento mais sensivel do contato.
 *
 * Como. Le o .mo, acrescenta as mensagens de um arquivo JSON {original:
 * traducao} que ainda nao tiverem traducao, e reescreve o .mo. NUNCA substitui
 * traducao existente: o que a plataforma ja traduz fica como esta. Ao fim, rele
 * o arquivo escrito e confere cada mensagem acrescentada; se alguma nao
 * conferir, sai com erro, e a construcao da imagem para.
 *
 * O formato .mo e o do GNU gettext: cabecalho de sete inteiros, duas tabelas
 * (comprimento e posicao) de originais e traducoes, e as cadeias. A tabela de
 * dispersao e opcional e e omitida (tamanho zero); o LimeSurvey le o arquivo
 * inteiro para a memoria, e nao a usa.
 *
 * Uso, na construcao da imagem:
 *     php acrescenta-traducoes.php <arquivo.mo> <traducoes.json>
 */

function le_mo($caminho)
{
    $dados = file_get_contents($caminho);
    if ($dados === false || strlen($dados) < 28) {
        fwrite(STDERR, "arquivo .mo ilegivel: $caminho\n");
        exit(1);
    }
    $magico = unpack('V', substr($dados, 0, 4))[1];
    if ($magico == 0x950412de) {
        $f = 'V';
    } elseif ($magico == 0xde120495) {
        $f = 'N';
    } else {
        fwrite(STDERR, "nao e arquivo .mo: $caminho\n");
        exit(1);
    }
    $cab = unpack("{$f}revisao/{$f}n/{$f}orig/{$f}trad", substr($dados, 4, 16));
    $mensagens = [];
    for ($i = 0; $i < $cab['n']; $i++) {
        $o = unpack("{$f}len/{$f}pos", substr($dados, $cab['orig'] + 8 * $i, 8));
        $t = unpack("{$f}len/{$f}pos", substr($dados, $cab['trad'] + 8 * $i, 8));
        $mensagens[substr($dados, $o['pos'], $o['len'])] =
            substr($dados, $t['pos'], $t['len']);
    }
    return $mensagens;
}

function escreve_mo($caminho, $mensagens)
{
    // Originais em ordem binaria: e o que o formato pede para busca.
    ksort($mensagens, SORT_STRING);
    $n = count($mensagens);
    $inicioOrig = 28;
    $inicioTrad = $inicioOrig + 8 * $n;
    $inicioCadeias = $inicioTrad + 8 * $n;

    $tabelaOrig = $tabelaTrad = $cadeias = '';
    $pos = $inicioCadeias;
    foreach (array_keys($mensagens) as $original) {
        $tabelaOrig .= pack('VV', strlen($original), $pos);
        $cadeias .= $original . "\0";
        $pos += strlen($original) + 1;
    }
    foreach ($mensagens as $traducao) {
        $tabelaTrad .= pack('VV', strlen($traducao), $pos);
        $cadeias .= $traducao . "\0";
        $pos += strlen($traducao) + 1;
    }
    $cabecalho = pack('V7', 0x950412de, 0, $n, $inicioOrig, $inicioTrad, 0,
                      $inicioCadeias);
    if (file_put_contents($caminho, $cabecalho . $tabelaOrig . $tabelaTrad . $cadeias) === false) {
        fwrite(STDERR, "nao foi possivel escrever $caminho\n");
        exit(1);
    }
}

if ($argc != 3) {
    fwrite(STDERR, "uso: php acrescenta-traducoes.php <arquivo.mo> <traducoes.json>\n");
    exit(2);
}
[$_, $arquivoMo, $arquivoJson] = $argv;

$novas = json_decode(file_get_contents($arquivoJson), true);
if (!is_array($novas)) {
    fwrite(STDERR, "traducoes ilegiveis: $arquivoJson\n");
    exit(1);
}
$mensagens = le_mo($arquivoMo);
$acrescentadas = [];
foreach ($novas as $original => $traducao) {
    if (isset($mensagens[$original]) && $mensagens[$original] !== '') {
        echo "ja traduzida, mantida: $original\n";
        continue;
    }
    $mensagens[$original] = $traducao;
    $acrescentadas[$original] = $traducao;
}
escreve_mo($arquivoMo, $mensagens);

$relidas = le_mo($arquivoMo);
foreach ($acrescentadas as $original => $traducao) {
    if (($relidas[$original] ?? null) !== $traducao) {
        fwrite(STDERR, "nao conferiu depois de escrita: $original\n");
        exit(1);
    }
}
echo count($acrescentadas) . " traducoes acrescentadas a $arquivoMo ("
    . count($relidas) . " mensagens)\n";
