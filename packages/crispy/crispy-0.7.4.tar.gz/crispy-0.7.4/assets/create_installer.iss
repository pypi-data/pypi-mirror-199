[Setup]
AppId={{1B71F614-D6B1-4E28-83C8-E04068C7F91A}
AppName=Crispy
AppVersion=0.7.4
AppVerName=Crispy
AppPublisher=Marius Retegan
AppPublisherURL=https://github.com/mretegan/crispy
AppSupportURL=https://github.com/mretegan/crispy
AppUpdatesURL=https://github.com/mretegan/crispy/releases
DefaultDirName={pf}\Crispy
DefaultGroupName=Crispy
LicenseFile=..\LICENSE.txt
OutputDir=..\..\artifacts
OutputBaseFilename=Crispy-0.7.4-x64
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "..\..\build\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
Source: "crispy.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\Crispy"; Filename: "{app}\crispy.exe"; IconFilename: "{app}\crispy.ico"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"

// Code from https://stackoverflow.com/questions/2000296/inno-setup-how-to-automatically-uninstall-previous-installed-version/2099805#209980
[Code]

/////////////////////////////////////////////////////////////////////
function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{#emit SetupSetting("AppId")}_is1');
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;


/////////////////////////////////////////////////////////////////////
function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;


/////////////////////////////////////////////////////////////////////
function UnInstallOldVersion(): Integer;
var
  sUnInstallString: String;
  iResultCode: Integer;
begin
  // Return Values:
  // 1 - uninstall string is empty
  // 2 - error executing the UnInstallString
  // 3 - successfully executed the UnInstallString

  // default return value
  Result := 0;

  // get the uninstall string of the old app
  sUnInstallString := GetUninstallString();
  if sUnInstallString <> '' then begin
    sUnInstallString := RemoveQuotes(sUnInstallString);
    if Exec(sUnInstallString, '/VERYSILENT /NORESTART /SUPPRESSMSGBOXES','', SW_HIDE, ewWaitUntilTerminated, iResultCode) then
      Result := 3
    else
      Result := 2;
  end else
    Result := 1;
end;

/////////////////////////////////////////////////////////////////////
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep=ssInstall) then
  begin
    if (IsUpgrade()) then
    begin
      UnInstallOldVersion();
    end;
  end;
end;