param(
    [string]$Pptx = (Join-Path $PSScriptRoot '..\presentacion\Minicurso_Analisis_de_Datos.pptx'),
    [string]$Pdf = (Join-Path $PSScriptRoot '..\presentacion\Minicurso_Analisis_de_Datos.pdf')
)

$ErrorActionPreference = 'Stop'
$Pptx = [System.IO.Path]::GetFullPath($Pptx)
$Pdf = [System.IO.Path]::GetFullPath($Pdf)

if (-not (Test-Path $Pptx)) {
    throw "No existe la presentación: $Pptx"
}

$temporal = Join-Path ([System.IO.Path]::GetTempPath()) ('exportar_' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $temporal | Out-Null
$copiaPptx = Join-Path $temporal 'presentacion.pptx'
$copiaPdf = Join-Path $temporal 'presentacion.pdf'
Copy-Item -LiteralPath $Pptx -Destination $copiaPptx

$pp = New-Object -ComObject PowerPoint.Application
try {
    $p = $pp.Presentations.Open($copiaPptx, $true, $false, $false)
    try {
        $p.SaveAs($copiaPdf, 32)
        $total = $p.Slides.Count
    }
    finally {
        $p.Close()
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($p)
    }
}
finally {
    $pp.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($pp)
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}

Copy-Item -LiteralPath $copiaPdf -Destination $Pdf -Force
Remove-Item -LiteralPath $temporal -Recurse -Force
Write-Output ("{0} diapositivas exportadas a {1}" -f $total, $Pdf)
