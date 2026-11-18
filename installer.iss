[Setup]
AppName=MTG Match Tracker
AppVersion=1.0.0
AppPublisher=Comancherah
AppPublisherURL=https://github.com
DefaultDirName={autopf}\MTG Match Tracker
DefaultGroupName=MTG Match Tracker
OutputDir=installer_output
OutputBaseFilename=MTG_Tracker_Setup_v1.0.0
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\MTG_Tracker.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\MTG Match Tracker"; Filename: "{app}\MTG_Tracker.exe"
Name: "{group}\Uninstall MTG Match Tracker"; Filename: "{uninstallexe}"
Name: "{autodesktop}\MTG Match Tracker"; Filename: "{app}\MTG_Tracker.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\MTG_Tracker.exe"; Description: "{cm:LaunchProgram,MTG Match Tracker}"; Flags: nowait postinstall skipifsilent
