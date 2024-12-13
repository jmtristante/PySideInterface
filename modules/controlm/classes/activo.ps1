$Ruta="C:\Users\X710675\Simulador_mallas"
enum JobStatus
{
   OK = 0
   KO = 1
   WAITING = 2
   EJECUTANDO = 3
   HOLDED = 4
}
class Conditioncl{
    [string]$Name
    [string]$Exit
    [string]$Sign
    [string]$Operator
    Conditioncl ($JsonObject){
        $this.Name=$JsonObject.name
        $this.Exit=$JsonObject.exit
        $this.Sign=$JsonObject.sign
        if($null -eq $JsonObject.operator){
            $this.Operator="AND"
        }else{
            $this.Operator=$JsonObject.operator
        }
    }
}
class FTPcl{
    [string]$Host1
    [string]$Host2
    [string]$OrigPath
    [string]$DestPath
    [string]$Borrado
    FTPcl([string]$Host1,[string]$Host2,[string]$Orig,[string]$Dest,[string]$Borrado){
        $this.Host1=$Host1
        $this.Host2=$Host2
        $this.OrigPath=$Orig
        $this.DestPath=$Dest
        $this.Borrado=$Borrado
    }
}
class Jobcl{
    [string]$Id
    [string]$Type
    $Prerequisites
    $Actions
    [JobStatus]$Status
    $Log
    #$Holded
    $ExitCode

    Jobcl ($JsonObject){
        $this.Prerequisites=[System.Collections.ArrayList]::new()
        $this.Actions=[System.Collections.ArrayList]::new()
        $this.Id=$JsonObject.id
        $this.Type=$JsonObject.type
        foreach ($action in $JsonObject.prerequisites){
            $this.Prerequisites.Add([Conditioncl]::new($action))
        }
        foreach ($action in $JsonObject.actions){
            $this.Actions.Add([Conditioncl]::new($action))
        }
        $this.Status=[JobStatus]::WAITING
        #$this.Holded=$false
    }

    Hold(){
        #$this.Holded=$true
        $this.Status=[JobStatus]::HOLDED
    }

    UnHold(){
        #$this.Holded=$false
        $this.Status=[JobStatus]::WAITING
    }

    Ejecutar(){}
    EjecutarForce(){}
    Kill(){}

    [string] Print(){
        return "$($this.Id) - $($this.Status) - $($this.ExitCode)`n"
    }

    [bool] JobCanStart(){
        $CanStart=$false

        if ($this.Status -ne [JobStatus]::WAITING){
            return $CanStart
        }

        [Activo]$Activo = [Activo]::Instance

        #No tiene requisitos, puede empezar
        if ($this.Prerequisites.count -eq 0) {
            $CanStart=$true
            return $CanStart
        }

        #Comprobamos los requisitos OR
        foreach ($requisito in $this.Prerequisites){
            $requisito=[Conditioncl]$requisito
            if($Activo.HasCondition($requisito.Name) -AND $requisito.Operator -eq "OR"){
                $CanStart=$true
                return $CanStart
            }
        }

        #Comprobamos los requisitos AND
        foreach ($requisito in $this.Prerequisites){
            $requisito=[Conditioncl]$requisito
            if ($requisito.Operator -eq "AND"){
                if($Activo.HasCondition($requisito.Name)){
                    $CanStart=$true
                }
                if(!$Activo.HasCondition($requisito.Name)){
                    $CanStart=$false
                    return $CanStart
                }
            }

        }

        return $CanStart

        #return $this.Prerequisites.count -eq 0 -OR $Activo.HasCondition($this.Prerequisites[0])
    }
}
class Jobscriptcl : Jobcl{
    [string]$File_name
    [string]$File_path
    [string]$Host_name
    $Parameters
    Jobscriptcl($JsonObject):base($JsonObject){
        $this.Parameters=[System.Collections.ArrayList]::new()
        $this.File_name=$JsonObject.file_name
        $this.File_path=$JsonObject.file_path
        $this.Host_name=$JsonObject.host
        foreach ($param in $JsonObject.parameters){
            $this.Parameters.Add($param.parm)
        }
    }
    Ejecutar(){
        if ($this.JobCanStart()){
            Write-Host "Comienza la ejecución normal del job: " $this.Id
            $this.EjecutarInThread()
        }
        $this.RevisarEjecucion()
    }
    EjecutarForce(){
        Write-Host "Comienza la ejecución forzada del job: " $this.Id
        $this.EjecutarInThread()
    }

    Kill(){
        $Activo=[Activo]::Instance
        $Maquina=[Activo]::Instance.GetHost($this.Host_name)
        #$Command="kill `$(ps aux | grep Peticion_Unidad | awk '{ print `$2 }' | head -1)"
        $Command="kill ```$(ps aux | grep ```"$($this.File_path)/$($this.File_name)"
        #Concatenar parametros
        foreach ($p in $this.Parameters){
            $Command = $Command + " " + $p
        }
        $Command = $Command + "```"| awk '{ print ```$2 }' | head -1)"
        #$comm=""
        $LineaEjecucion=""
        #Write-Host "Ejecutando job $($this.Id)"
        switch ($Maquina.tipo_auth){
            "fichero"{
                #$this.Log=echo y | plink -i $Maquina.ruta_auth "$($Maquina.usuario)@$($Maquina.direccion)" $Command
                $LineaEjecucion="echo y | plink -i `"$($Maquina.ruta_auth)`" `"$($Maquina.usuario)@$($Maquina.direccion)`" $Command"
                #Write-Host $LineaEjecucion
            }
            "pass"{
                #$this.Log=echo "$($Command);exit"|plink -pw $($Maquina.passwd) "$($Maquina.usuario)@$($Maquina.direccion)"
                $LineaEjecucion="echo `"$($Command);exit`"|plink -pw $($Maquina.passwd) `"$($Maquina.usuario)@$($Maquina.direccion)`""
            }
        }
        Write-Host "Comando a ejecutar"
        Write-Host $LineaEjecucion
        $Activo.ExecuteCommandDirect($this.Id,$LineaEjecucion)
    }

    RevisarEjecucion(){
        $Activo=[Activo]::Instance
        $Exit=$Activo.Executions[$this.Id]
        #Borramos el exit del activo porque ya lo hemos obtenido
        $Activo.Executions.Remove($this.Id)


        if ($null -ne $Exit -and $this.Status -eq [JobStatus]::EJECUTANDO){
            $this.ExitCode=$Exit
            #Actualizamos condiciones en el activo

            foreach ($action in $this.Actions){
                $action=[Conditioncl]$action
                if ($action.Exit -eq $Exit -or $action.Exit -eq "*"){
                    switch($action.Sign){
                        "+"{
                            $this.Status=[JobStatus]::OK #Ha dado una de las salidas esperadas
                            $Activo.AddCondition($action.Name)
                        }
                        "-"{
                            $Activo.RemoveCondition($action.Name)
                        }
                    }

                }
            }
            #En caso de no haber dado una salida esperada lo ponemos a KO
            if ($this.Status -ne [JobStatus]::OK){
                $this.Status=[JobStatus]::KO
            }

            $Activo.NotificarFinJob()
        }
    }

    EjecutarInThread(){
        #if ($this.Status=[JobStatus]::WAITING)
        Write-Host "Comienza la ejecución"

        $this.Status=[JobStatus]::EJECUTANDO
        #$Maquina=[Maquinas]::Instance.GetAuth($this.Host_name)
        $Maquina=[Activo]::Instance.GetHost($this.Host_name)
        #$Maquina=[Maquinas]$Maquina
        $Command="$($this.File_path)/$($this.File_name)"
        #Concatenar parametros
        foreach ($p in $this.Parameters){
            $Command = $Command + " " + $p
        }
        #$comm=""
        $LineaEjecucion=""
        #Write-Host "Ejecutando job $($this.Id)"
        switch ($Maquina.tipo_auth){
            "fichero"{
                #$this.Log=echo y | plink -i $Maquina.ruta_auth "$($Maquina.usuario)@$($Maquina.direccion)" $Command
                $LineaEjecucion="echo y | plink -i `"$($Maquina.ruta_auth)`" `"$($Maquina.usuario)@$($Maquina.direccion)`" $Command"
                #Write-Host $LineaEjecucion
            }
            "pass"{
                #$this.Log=echo "$($Command);exit"|plink -pw $($Maquina.passwd) "$($Maquina.usuario)@$($Maquina.direccion)"
                $LineaEjecucion="echo `"$($Command);exit`"|plink -pw $($Maquina.passwd) `"$($Maquina.usuario)@$($Maquina.direccion)`""
            }
        }
        $Activo=[Activo]::Instance
        $Activo.ExecuteCommand($this.Id,$LineaEjecucion)

    }
}
class Jobftpcl : Jobcl{
    $FtpList
    Jobftpcl($JsonObject):base($JsonObject){
        #$this.FtpList=[System.Collections.ArrayList]::new()
        $this.FtpList=@{}
        $OrdenAux=1
        foreach ($f in $JsonObject.ftp){
            #$this.FtpList.Add([FTPcl]::new($JsonObject.host1,$JsonObject.host2,$f.orig,$f.dest,$f.borrado))
            #Si no se ha especificado orden va aleatorio
            if ($null -eq $f.orden){
                $this.FtpList[$OrdenAux]=[FTPcl]::new($JsonObject.host1,$JsonObject.host2,$f.orig,$f.dest,$f.borrado)
                $OrdenAux++
            }else{
                $this.FtpList[$f.orden]=[FTPcl]::new($JsonObject.host1,$JsonObject.host2,$f.orig,$f.dest,$f.borrado)
            }

        }
    }

    Ejecutar(){
        if ($this.JobCanStart()){
            Write-Host "Comienza la ejecución normal del job: " $this.Id
            $this.EjecutarInThread()
        }
        $this.RevisarEjecucion()
    }

    EjecutarForce(){
        Write-Host "Comienza la ejecución forzada de $($this.Id)"
        $this.EjecutarInThread()
    }

    RevisarEjecucion(){
        $Activo=[Activo]::Instance
        $Exit=$Activo.Executions[$this.Id]
        #Borramos el exit del activo porque ya lo hemos obtenido
        $Activo.Executions.Remove($this.Id)


        if ($null -ne $Exit -and $this.Status -eq [JobStatus]::EJECUTANDO){
            $this.ExitCode=$Exit
            #Actualizamos condiciones en el activo

            foreach ($action in $this.Actions){
                $action=[Conditioncl]$action
                if ($action.Exit -eq $Exit -or $action.Exit -eq "*"){
                    switch($action.Sign){
                        "+"{
                            $this.Status=[JobStatus]::OK #Ha dado una de las salidas esperadas
                            $Activo.AddCondition($action.Name)
                        }
                        "-"{
                            $Activo.RemoveCondition($action.Name)
                        }
                    }

                }
            }
            #En caso de no haber dado una salida esperada lo ponemos a KO
            if ($this.Status -ne [JobStatus]::OK){
                $this.Status=[JobStatus]::KO
            }

            $Activo.NotificarFinJob()
        }
    }

    EjecutarInThread(){


        #$Exit=0
        $LineaEjecucion=""

            $this.Status=[JobStatus]::EJECUTANDO
            $n=$this.FtpList.count
            #foreach ($tareaFTP in $this.FtpList){
            for ($i=1;$i -lt $this.FtpList.count+1;$i++){

                $tareaFTP=[FTPcl]$this.FtpList["$($i)"]
                $Origen=[Activo]::Instance.GetHost($tareaFTP.Host1)
                $Destino=[Activo]::Instance.GetHost($tareaFTP.Host2)

                $Directorio="tmp_$($this.Id)"

                #Paso 1: de origen a local
                $LineaEjecucion+="New-Item -ItemType Directory -Path .\$($Directorio);" #Directorio temporal para los archivos ftp
                switch($Origen.tipo_auth){
                    "fichero"{
                        $LineaEjecucion+="pscp -C -i $($Origen.ruta_auth) `"$($Origen.usuario)@$($Origen.direccion):$($tareaFTP.OrigPath)`" `".\$($Directorio)\`";"
                        Write-Host $LineaEjecucion
                    }
                    "pass"{
                        $LineaEjecucion+="pscp -C -pw $($Origen.passwd) `"$($Origen.usuario)@$($Origen.direccion):$($tareaFTP.OrigPath)`" `".\$($Directorio)\`";"
                    }
                }
                #$Exit=$Exit + $LASTEXITCODE




                if ($tareaFTP.Borrado -eq "true"){
                    $Command="rm $($tareaFTP.OrigPath)"
                    $LineaEjecucion+="`"$($Command);exit`"|plink -pw $($Origen.passwd) `"$($Origen.usuario)@$($Origen.direccion)`";"
                }
                #$Exit=$Exit + $LASTEXITCODE


                #Paso 2: de local a destino
                switch($Destino.tipo_auth){
                    "fichero"{
                        $LineaEjecucion+="pscp -C -i $($Destino.ruta_auth) `".\$($Directorio)\*`" `"$($Destino.usuario)@$($Destino.direccion):$($tareaFTP.DestPath)`";"
                    }
                    "pass"{
                        $LineaEjecucion+="pscp -C -pw $($Destino.passwd) `".\$($Directorio)\*`" `"$($Destino.usuario)@$($Destino.direccion):$($tareaFTP.DestPath)`";"
                    }
                }
                #$Exit=$Exit + $LASTEXITCODE


                #Borramos la carpeta temporal
                $LineaEjecucion+="Remove-Item .\$($Directorio)\ -Recurse;"


            }
            $Activo=[Activo]::Instance
            $Activo.ExecuteCommand($this.Id,$LineaEjecucion)
         <#
        $Exit="$($Exit)"
        $this.ExitCode=$Exit
        #Write-Host "Job ejecutado: $($this.Id)"
        #Actualizamos condiciones en el activo
        $Activo=[Activo]::Instance
        foreach ($action in $this.Actions){
            $action=[Conditioncl]$action
            if ($action.Exit -eq $Exit -or $Exit -eq '*'){
                switch($action.Sign){
                    "+"{
                        $this.Status=[JobStatus]::OK #Ha dado una de las salidas esperadas
                        $Activo.AddCondition($action.Name)
                    }
                    "-"{
                        $Activo.RemoveCondition($action.Name)
                    }
                }

            }

        }
        #En caso de no haber dado una salida esperada lo ponemos a KO
        if ($this.Status -ne [JobStatus]::OK){
            $this.Status=[JobStatus]::KO
        }

        $Activo.NotificarFinJob()
        #>

    }
}
class Malla{
    $Name
    $Jobs
    Malla($Name,$JsonObject){
        $this.Name=$Name
        $this.Jobs=[System.Collections.ArrayList]::new()

        foreach ($j in $JsonObject.jobs){
            switch ($j.type){
                "script"{
                    [Jobscriptcl]$job=[Jobscriptcl]::new($j)
                }
                "ftp"{
                    [Jobftpcl]$job=[Jobftpcl]::new($j)

                }
            }
            if(0 -eq $job.Prerequisites.Count){
                $job.Hold()

            }
            $this.Jobs.Add($job)
        }
    }
    [string] Print(){
        $JobsString= "$($this.Name) `n"
        foreach ($j in $this.Jobs){
            [Jobcl]$j=$j
            $JobsString=$JobsString+$j.Print()
        }
        return $JobsString
    }
    HoldJob($JobName){
        foreach ($j in $this.Jobs){
            [Jobcl]$j=$j
            if($j.Id -eq $JobName){
                $j.Hold()
            }
        }
    }
    UnHoldJob($JobName){
        foreach ($j in $this.Jobs){
            [Jobcl]$j=$j
            if($j.Id -eq $JobName){
                $j.UnHold()
            }
        }
    }

    EjecutarJob($JobName){
        foreach ($j in $this.Jobs){
            [Jobcl]$j=$j
            if($j.Id -eq $JobName){
                $j.EjecutarForce()
            }
        }
    }

    KillJob($JobName){
        foreach ($j in $this.Jobs){
            [Jobcl]$j=$j
            if($j.Id -eq $JobName){
                $j.Kill()
            }
        }
    }


    Ejecutar(){
        foreach ($j in $this.Jobs){
            $j.Ejecutar()
        }
    }

}
class Maquinas {
    $JsonObject

    Maquinas($JsonObject) {
        $this.JsonObject=$JsonObject
    }
    [System.Object] GetHost($Host_name){
        $Maquina = $this.JsonObject.maquinas | Where-Object { $_.nombre -eq $Host_name }
        return $Maquina
    }
}

class Activo {
    [Maquinas]$Maquinas
    [Object]$JsonMallas
    $Mallas
    $Conditions
    $Executions
    hidden static [Activo] $_instance = [Activo]::new()
    static [Activo] $Instance = [Activo]::GetInstance()
    $Ruta

    [Guid] $ActivoTarget = [Guid]::NewGuid()

    hidden Activo() {
        #$this.Mallas=[System.Collections.ArrayList]::new()
        $this.Mallas=@{}
        $this.Conditions=[System.Collections.ArrayList]::new()
        $this.Executions=@{}
        $this.Ruta="C:\Users\X710675\Simulador_mallas"
    }

    Update(){
        #Avisamos a las mallas de que hay una nueva condicion
        foreach ($m in $this.Mallas.values){
            $m.Ejecutar() #A ver que pasa aqui que no sigue ejecutando
        }
    }

    ExecuteCommand($JobName, $Command){
        Write-Host "Activo: ejecutando job " $JobName
        Write-Host "Activo: ejecutando comando " $Command
        $job = [PowerShell]::Create().AddScript({
            param($JobName,$Command,$Result,$Ruta)

            Invoke-Expression $Command > $Ruta\log\$JobName
            $Result[$JobName] = $LASTEXITCODE

          }).AddArgument($JobName).AddArgument($Command).AddArgument($this.Executions).AddArgument($this.Ruta)

          # start thee job
        $async = $job.BeginInvoke()
    }

    ExecuteCommandDirect($JobName, $Command){
        Write-Host "Activo: ejecutando job " $JobName
        Write-Host "Activo: ejecutando comando " $Command
        Invoke-Expression $Command
    }


    AddMaquinas($JsonObject){
        $this.Maquinas=[Maquinas]::new($JsonObject)
    }

    AddJsonMallas($JsonObject){
        $this.JsonMallas=$JsonObject
    }

    [Jobcl]GetJob($JobName){

        foreach ($m in $this.Mallas.Values){
            foreach ($j in $m.Jobs){
                $Job=[Jobcl]$j
                if ($Job.Id -eq $JobName){
                    return $Job
                }
            }
        }
        return $null
    }

    [Malla]GetMalla($MallaName){

        foreach ($m in $this.Mallas.Values){
           if ($m.Name -eq $MallaName){
                return $m
           }
        }

        return $null
    }

    [string]GetJsonMallas($Ruta,$MallaName){
        $DirMalla = $this.JsonMallas.mallas | Where-Object { $_.name -eq $MallaName }
        $RutaMalla=$Ruta+"\"+$DirMalla.path
        #Write-Host $RutaMalla
        #$malla_json = Get-Content -Path $DirMalla.path -Raw | ConvertFrom-Json
        $malla_json = Get-Content -Path $RutaMalla -Raw | ConvertFrom-Json
        $malla_string=ConvertTo-Json -Depth 4 $malla_json
        return $malla_string
    }

    [System.Collections.ArrayList] GetAvailableMallas(){
        return $this.JsonMallas.mallas | Sort-Object -Unique -Property Name
    }

    [System.Collections.ArrayList]GetAllJobs(){
        $Jobs=[System.Collections.ArrayList]::new()
        foreach ($m in $this.Mallas.Values){
            foreach ($j in $m.Jobs){
                $Jobs.Add([Jobcl]$j)
            }
        }
        return $Jobs
    }

    #Recibe el nombre de la malla y su json asociado, es decir, todo el archivo json, con las correcciones de parámetros
    AddToActive($MallaName,$malla_json){
        [Malla]$malla=[Malla]::new($MallaName,$malla_json)
        $this.Mallas[$MallaName<#+$this.Mallas.count#>]=$malla
        Write-Host
    }

    #Recibe el nombre de la malla a eliminar
    DeleteFromActive($MallaName){
        $auxConditions=[System.Collections.ArrayList]::new()
        #Eliminamos todas las condiciones

        foreach ($m in $this.Mallas.Values){
            if($m.Name -eq $MallaName){
                Write-Host "Pendiente eliminar condiciones de jobs eliminados, aunque deberían estar eliminadas. Por ahora falla el del FTP. Pero se podrían eliminar las mallas en cualquer momento"
                Write-Host $this.Conditions

                foreach ($cond in $this.Conditions){
                    Write-Host "Comprobando $($cond.Name)"
                    if ($cond.Name -eq $m.Jobs.Actions.Values.Name){
                        $auxConditions.Add($cond)
                        Write-Host "Lista para borrar $($cond.Name)"
                    }
                }
            }
        }
        foreach ($c in $auxConditions){
            $this.Conditions.Remove($c)
            Write-Host "Borrado" $c.Name
        }

        $this.Mallas.Remove($MallaName)
    }

    [boolean]HasCondition($ConditionName){
        return $this.Conditions -contains $ConditionName
    }

    AddCondition($ConditionName){
        if (!$this.HasCondition($ConditionName)){
            $this.Conditions.Add($ConditionName)
        }
    }
    RemoveCondition($ConditionName){
        if ($this.HasCondition($ConditionName)){
            $this.Conditions.Remove($ConditionName)
        }
    }

    NotificarFinJob(){
        #Avisamos a las mallas de que hay una nueva condicion
        foreach ($m in $this.Mallas.values){
            $m.Ejecutar() #A ver que pasa aqui que no sigue ejecutando
        }
    }

    ExecuteMalla($MallaName){
        [Malla]$m=$this.Mallas[$MallaName]
        $m.Ejecutar()
    }
    ExecuteJob($MallaName, $JobName){
        [Malla]$m=$this.Mallas[$MallaName]
        $m.EjecutarJob($JobName)
    }

    KillJob($MallaName, $JobName){
        [Malla]$m=$this.Mallas[$MallaName]
        $m.KillJob($JobName)
    }

    HoldJob($MallaName,$JobName){
        [Malla]$m=$this.Mallas[$MallaName]
        $m.HoldJob($JobName)
    }
    UnHoldJob($MallaName,$JobName){
        [Malla]$m=$this.Mallas[$MallaName]
        $m.UnHoldJob($JobName)
    }

    Print(){
        $ActiveString=""
        foreach ($m in $this.Mallas.values){
            $ActiveString=$ActiveString+$m.Print()
        }
        #return $ActiveString
        #Write-Host $ActiveString
    }

    [System.Collections.Hashtable]GetMallas(){
        return $this.Mallas
    }

    [System.Object] GetHost($Host_name){
        return $this.Maquinas.GetHost($Host_name)
    }

    hidden static [Activo] GetInstance() {
        return [Activo]::_instance
    }
}

Function Init(){
    #$json_maquinas = Get-Content -Path .\maquinas.json -Raw | ConvertFrom-Json
    #$json_mallas = Get-Content -Path .\mallas.json -Raw | ConvertFrom-Json
    $json_maquinas = Get-Content -Path $Ruta\maquinas.json -Raw | ConvertFrom-Json
    $json_mallas = Get-Content -Path $Ruta\mallas.json -Raw | ConvertFrom-Json
    $Activo = [Activo]::Instance
    $Activo.AddMaquinas($json_maquinas)
    $Activo.AddJsonMallas($json_mallas)

    $Env:Activo=$Activo
}

Function AddToActive(){
    param(
        $NombreMalla
    )
    [Activo]$Activo = [Activo]::Instance
    $malla_string=$Activo.GetJsonMallas($Ruta,$NombreMalla)

    #Obtenemos los parámetros que tiene que introducir el usuario
    $list = Select-String "(%%\w+)" -InputObject $malla_string -AllMatches |
    Foreach {$_.matches.Value}

    $table = new-object System.Collections.Hashtable
    foreach ($coincidence in $list){
        if(!$table.Contains($coincidence)){
        $p=Read-Host "Introduce el valor para el parametro $($coincidence): "
        $table.Add($coincidence,$p)
        }
        $malla_string=$malla_string.Replace($coincidence,$p)
    }
    ##Write-Host $malla_string
    $malla_json = $malla_string | ConvertFrom-Json
    $Activo.AddToActive($NombreMalla,$malla_json)
    #Write-Host "Malla $($NombreMalla) añadida al activo"
}



Function GetJobsInActive(){
    [Activo]$Activo = [Activo]::Instance
    #Write-Output
    $Activo.Mallas.GetType()
    $Jobs= $Activo.GetAllJobs()
    $Activo.Print()
    $MallasActivas=$Activo.GetMallas()
}

Function EjecutarMalla(){
    param(
        $NombreMalla
    )
    [Activo]$Activo = [Activo]::Instance
    $Activo.ExecuteMalla($NombreMalla)
}
Function EjecutarJob(){
    param(
        $NombreMalla,
        $NombreJob
    )
    [Activo]$Activo = [Activo]::Instance
    $Activo.ExecuteJob($NombreMalla, $NombreJob)
}

Init
[Activo]$Activo = [Activo]::Instance
return $Activo
