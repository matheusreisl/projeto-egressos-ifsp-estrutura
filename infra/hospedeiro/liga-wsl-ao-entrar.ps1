<#
Registra, no Windows, a tarefa que liga a distribuicao do WSL quando o usuario
entra na sessao (E21).

Por que existe. Com instanceIdleTimeout = -1 no .wslconfig (E07), a distribuicao
nao e encerrada por ociosidade. Mas depois de reiniciar o Windows ela so liga
quando algo a invoca - e, parada, o agendador da composicao nao roda: o horario
de disparo passa sem execucao, com a maquina ligada e tudo aparentemente certo.
Foi o estado em que a E21 encontrou a maquina.

O que a tarefa faz, e so isto: invoca a distribuicao (wsl --exec /bin/true). O
systemd sobe o Docker, a politica de reinicio religa os conteineres e o
agendamento continua DENTRO da composicao (ADR-0008). A tarefa nao agenda
disparo nenhum e nao conhece o projeto; e o equivalente, no Windows, ao Docker
subir no boot de um Linux.

O que ela nao resolve: hibernacao e suspensao. Com o Windows suspenso no horario,
o disparo e registrado como perdido quando a rotina volta (egressos_execucoes),
e o que venceu sai no proximo dia util.

So para hospedeiro Windows com WSL2. Em Linux nativo nada disto e necessario.

Uso, no PowerShell do proprio usuario (sem administrador):

    .\liga-wsl-ao-entrar.ps1                      # distribuicao Ubuntu-24.04
    .\liga-wsl-ao-entrar.ps1 -Distro <nome>

Idempotente: rodar de novo substitui a tarefa. Para desfazer:

    Unregister-ScheduledTask -TaskName "Egressos - ligar WSL ao entrar" -Confirm:$false
#>
param([string]$Distro = "Ubuntu-24.04")

$ErrorActionPreference = "Stop"
$nome = "Egressos - ligar WSL ao entrar"
$usuario = "$env:USERDOMAIN\$env:USERNAME"

$acao = New-ScheduledTaskAction -Execute "wsl.exe" -Argument "-d $Distro --exec /bin/true"
$gatilho = New-ScheduledTaskTrigger -AtLogOn -User $usuario
# Em notebook, a tarefa precisa rodar tambem na bateria; e, se o logon ocorrer
# sem que ela possa rodar, roda assim que puder.
$config = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
$principal = New-ScheduledTaskPrincipal -UserId $usuario -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $nome -Action $acao -Trigger $gatilho -Settings $config `
    -Principal $principal -Force `
    -Description "Liga a distribuicao $Distro do WSL ao entrar, para que os conteineres do projeto egressos IFSP voltem e o agendador da rotina rode (E21). Nao agenda disparo." | Out-Null

Get-ScheduledTask -TaskName $nome | Select-Object TaskName, State,
    @{n = "Acao"; e = { "$($_.Actions[0].Execute) $($_.Actions[0].Arguments)" } },
    @{n = "Gatilho"; e = { "ao entrar: $($_.Triggers[0].UserId)" } }
