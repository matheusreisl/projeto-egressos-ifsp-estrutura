<?php

/**
 * Exporta a estrutura de um questionario no formato .lss, por linha de comando.
 *
 * Existe porque a API RemoteControl do LimeSurvey 7 importa .lss
 * (`import_survey`) mas nao exporta — conferido na E15 contra a lista de metodos
 * da instancia. A exportacao pela tela contraria o criterio K7 da ADR-0002.
 *
 * Usa a mesma funcao que o painel usa no botao "Estrutura do questionario
 * (.lss)": `surveyGetXMLData`. O que sai daqui e, portanto, o que a plataforma
 * exportaria pela tela.
 *
 * O console do LimeSurvey carrega comandos adicionais do diretorio indicado em
 * YII_CONSOLE_COMMANDS. Uso, dentro do conteiner:
 *
 *   YII_CONSOLE_COMMANDS=<dir> php application/commands/console.php \
 *       exportarestrutura <sid>
 *
 * Quem chama e o instrumento.py, que copia este arquivo para o conteiner.
 */
class ExportarestruturaCommand extends CConsoleCommand
{
    public function run($args)
    {
        if (count($args) !== 1 || !ctype_digit((string) $args[0])) {
            fwrite(STDERR, "uso: exportarestrutura <sid>\n");
            return 2;
        }
        $sid = (int) $args[0];
        Yii::import('application.helpers.common_helper', true);
        Yii::import('application.helpers.export_helper', true);
        if (Survey::model()->findByPk($sid) === null) {
            fwrite(STDERR, "questionario $sid inexistente\n");
            return 1;
        }
        echo surveyGetXMLData($sid);
        return 0;
    }
}
