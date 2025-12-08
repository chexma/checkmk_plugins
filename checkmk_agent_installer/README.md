# CheckMK Agent Remote Installer

PowerShell-Skript zur Remote-Installation und Registrierung des CheckMK Agents auf Windows-Systemen via PowerShell Remoting.

## Übersicht

Dieses Skript ermöglicht die automatisierte Installation und Konfiguration des CheckMK Monitoring Agents auf mehreren Windows-Servern. Es unterstützt sowohl Domänen- als auch Workgroup-Umgebungen.

## Funktionen

| Funktion | Beschreibung |
|----------|-------------|
| Agent-Installation | Kopiert und installiert das CheckMK Agent MSI-Paket |
| TLS-Registrierung | Registriert den Agent für verschlüsselte Kommunikation |
| Agent Updater | Registriert den Agent Updater für automatische Updates |
| Hostname-Anpassung | Passt den Hostnamen an die CheckMK-Konfiguration an |

## Voraussetzungen

### Quellsystem (von dem aus das Skript ausgeführt wird)
- PowerShell 5.1 oder höher
- Netzwerkzugriff zu den Zielservern (WinRM, Port 5985/5986)
- CheckMK Agent MSI-Paket lokal verfügbar

### Zielsysteme
- PowerShell Remoting aktiviert
- WinRM-Dienst gestartet

## Parameter

### Aktionen

| Parameter | Beschreibung |
|-----------|-------------|
| `-Install` | Kopiert das MSI-Paket und installiert den CheckMK Agent |
| `-RegisterTls` | Registriert den Agent für TLS-verschlüsselte Kommunikation |
| `-RegisterAgentUpdater` | Registriert den Agent Updater für automatische Updates |
| `-RemoveAgentInstallationFile` | Löscht das MSI-Paket nach der Installation |
| `-CleanInstall` | Führt eine saubere Neuinstallation durch |

### Authentifizierung

| Parameter | Beschreibung |
|-----------|-------------|
| `-UseCredentialPopup` | Zeigt einen Dialog zur Eingabe der Anmeldedaten |
| `-Credential <PSCredential>` | Verwendet ein PSCredential-Objekt für die Authentifizierung |
| `-WorkgroupMode` | Aktiviert NTLM-Authentifizierung für Nicht-Domänen-Systeme |

### CheckMK-Konfiguration

| Parameter | Beschreibung |
|-----------|-------------|
| `-CheckMkServer <string>` | Hostname oder IP-Adresse des CheckMK-Servers |
| `-CheckMkSite <string>` | Name der CheckMK-Site |
| `-RegistrationUser <string>` | Benutzername für die TLS-Registrierung |
| `-RegistrationPassword <string>` | Passwort für die TLS-Registrierung |
| `-UpdaterUser <string>` | Benutzername für den Agent Updater |
| `-UpdaterPassword <string>` | Passwort für den Agent Updater |
| `-protocol <http\|https>` | Protokoll für die Kommunikation (Standard: https) |

### Hostname-Anpassung

| Parameter | Beschreibung |
|-----------|-------------|
| `-ConvertCase <lowercase\|uppercase\|titlecase>` | Konvertiert die Groß-/Kleinschreibung des Hostnamens |
| `-DomainSuffix <string>` | Fügt ein Domain-Suffix zum Hostnamen hinzu |

### Pfad-Konfiguration

| Parameter | Beschreibung |
|-----------|-------------|
| `-CheckMkAgentPackageName <string>` | Name des MSI-Pakets |
| `-CheckMkAgentSourceFolder <string>` | Quellpfad des MSI-Pakets |
| `-CheckmkAgentDestinationFolder <string>` | Zielpfad auf dem Remote-System |

### Sonstige

| Parameter | Beschreibung |
|-----------|-------------|
| `-EnableDebug` | Aktiviert ausführliche Debug-Ausgaben |
| `-Help` | Zeigt die Hilfe an |

## Konfiguration im Skript

Vor der Verwendung müssen folgende Variablen im Skript angepasst werden:

```powershell
# Zielsysteme (Liste oder aus Datei)
$Servers = "server01", "server02", "server03"
# oder:
# $Servers = Get-Content "C:\temp\hosts.txt"

# MSI-Paket Konfiguration
$CheckMkAgentPackageName = "check-mk-agent.msi"
$CheckMkAgentSourceFolder = "C:\Pfad\zur\MSI\"
$CheckmkAgentDestinationFolder = "C:\Windows\TEMP\"
```

## Beispiele

### Einfache Installation (Domänen-Umgebung)

```powershell
# Installation mit aktuellem Benutzer
.\checkmk_agent_installer.ps1 -Install

# Installation mit Credential-Dialog
.\checkmk_agent_installer.ps1 -Install -UseCredentialPopup
```

### Vollständige Installation mit Registrierung

```powershell
.\checkmk_agent_installer.ps1 `
    -Install `
    -RegisterTls `
    -RegisterAgentUpdater `
    -CheckMkServer "checkmk.example.com" `
    -CheckMkSite "mysite" `
    -RegistrationUser "automation" `
    -RegistrationPassword "secret123" `
    -UpdaterUser "automation" `
    -UpdaterPassword "secret123" `
    -ConvertCase lowercase
```

### Mit gespeicherten Credentials

```powershell
# Credentials einmal abfragen und speichern
$cred = Get-Credential

# Für mehrere Durchläufe verwenden
.\checkmk_agent_installer.ps1 -Install -Credential $cred
.\checkmk_agent_installer.ps1 -RegisterTls -Credential $cred
```

### Workgroup/Nicht-Domänen-Systeme

```powershell
# Mit Credential-Dialog
.\checkmk_agent_installer.ps1 -Install -UseCredentialPopup -WorkgroupMode

# Mit gespeicherten Credentials
$cred = Get-Credential
.\checkmk_agent_installer.ps1 -Install -Credential $cred -WorkgroupMode

# Vollständige Installation mit Debug-Ausgabe
.\checkmk_agent_installer.ps1 `
    -Install `
    -RegisterTls `
    -RegisterAgentUpdater `
    -UseCredentialPopup `
    -WorkgroupMode `
    -EnableDebug
```

### Hostname-Anpassung

```powershell
# Hostname in Kleinbuchstaben konvertieren
.\checkmk_agent_installer.ps1 -Install -ConvertCase lowercase

# Domain-Suffix hinzufügen
.\checkmk_agent_installer.ps1 -Install -DomainSuffix "example.com"

# Beides kombinieren
.\checkmk_agent_installer.ps1 -Install -ConvertCase lowercase -DomainSuffix "example.com"
```

## Workgroup-Voraussetzungen

Für Nicht-Domänen-Systeme sind zusätzliche Konfigurationsschritte erforderlich:

### Auf dem Zielsystem (einmalig, als Administrator)

```powershell
# PowerShell Remoting aktivieren
Enable-PSRemoting -Force

# Lokale Adminkonten für Remote-Zugriff erlauben
New-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" `
    -Name "LocalAccountTokenFilterPolicy" -Value 1 -PropertyType DWORD -Force
```

### Auf dem Quellsystem (einmalig, als Administrator)

```powershell
# Zielsystem zu TrustedHosts hinzufügen
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "ZIELSERVER" -Concatenate -Force

# Mehrere Server hinzufügen
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "SERVER1,SERVER2,SERVER3" -Force

# Alle Server erlauben (nicht empfohlen für Produktion)
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "*" -Force
```

## Fehlerbehebung

### Fehler 0x80090311 (SEC_E_NO_AUTHENTICATING_AUTHORITY)

**Ursache:** Kerberos-Authentifizierung fehlgeschlagen (typisch bei Nicht-Domänen-Systemen)

**Lösung:** Parameter `-WorkgroupMode` verwenden

### Fehler 0x8009030e (SEC_E_NO_CREDENTIALS)

**Ursache:** Falsches Benutzernamenformat für Workgroup-Authentifizierung

**Lösung:** Das Skript konvertiert automatisch den Benutzernamen in das Format `COMPUTERNAME\Username`. Alternativ den Benutzernamen direkt im Format `SERVERNAME\Administrator` eingeben.

### Verbindung wird abgelehnt

**Mögliche Ursachen:**
1. WinRM-Dienst nicht gestartet
2. Firewall blockiert Port 5985/5986
3. Server nicht in TrustedHosts (bei Workgroup)

**Lösungen:**
```powershell
# WinRM-Status prüfen
Get-Service WinRM

# WinRM starten und aktivieren
Enable-PSRemoting -Force

# Firewall-Regel prüfen
Get-NetFirewallRule -Name "WINRM*"
```

## Autor

Andre Eckstein
Andre.Eckstein@Bechtle.com

## Lizenz

Dieses Skript wird ohne Gewährleistung bereitgestellt. Die Nutzung erfolgt auf eigene Gefahr.
