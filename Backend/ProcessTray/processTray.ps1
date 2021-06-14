properties {
    #------------- Paths -----------------
    #- in dev mode -#
    $EnvDir = "C:\dev2\env"
    $BinDir = "$EnvDir\bin"
    $PythonCmd = "$BinDir\python.exe"
  
    $BuildDir = "$EnvDir\cura-build\build"
    
    $TestDir = "$BuildDir\RegressionTests"
    $BackendTestDir  = "$TestDir\Backend"
    $TestDataDir = "$TestDir\Data"
  
    $CuraDir  = "$BuildDir\Cura-prefix\src\cura-nano"
    $CuraCmd  = "$CuraDir\cura_app.py"

    $OutputDir = ".\Output\"
    $RefDir = ".\Reference\"
}

task default -depends VerifyTrays

task VerifyTrays  {
    # Run The Engine processing on trays and verify the results
    
    Write-Host -ForegroundColor White -BackgroundColor DarkGreen "<<<----------------------------------------------------------------------"
    Write-Host -ForegroundColor White -BackgroundColor DarkGreen "### Running Trays Comparison"
    
    foreach ($TestFile in (Get-ChildItem "$TestDataDir" -Filter *.amt)) {
        
        Write-Host -ForegroundColor White -BackgroundColor LightGreen "###"
        Write-Host -ForegroundColor White -BackgroundColor LightGreen "### Validating $($TestFile.BaseName)..."
        Write-Host -ForegroundColor White -BackgroundColor LightGreen "###"

        $OutputFile = "$OutputDir\$($TestFile.BaseName).pcbjc"

        Invoke-Task ProcessTray

        Invoke-Task CheckProcessedTray
    }        
        
    Write-Host -ForegroundColor White -BackgroundColor DarkGreen "Finita la Comedia"
    Write-Host -ForegroundColor White -BackgroundColor DarkGreen "<<<----------------------------------------------------------------------"
}

task ProcessTray {
    # Run Cura to process the tray file and save the pcbjc

    if ($TestFile -eq $null)
    {
        #Why are we even here?
        throw "`$TestFile var unset"
    }

    if ($OutputFile -eq $null)
    {
        #Why are we even here?
        throw "`$OutputFile var unset"
    }

    # Clean the slate
    Remove-Item $OutputDir -Force -Recurse
    New-Item -ItemType directory -Path $OutputDir
    
    & $PythonCmd $CuraCmd --process-tray-after-loading --skip-user-interaction --quit-after-processing --save-tray-to $OutputFile "$($TestFile.FullName)"

    if ((Test-Path -path $OutputFile) -ne $True)
    {
        throw "Processing of Tray $($TestFile.FullName) FAILED"
    }
  
}

task CheckProcessedTray {
    # Run the PCBJC-comparing script to validate the result

    if ($OutputFile -eq $null)
    {
        #Why are we even here?
        throw "`$OutputFile var unset"
    }

    
}