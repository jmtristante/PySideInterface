$Ruta="C:\Users\X710675\Simulador_mallas"
$Activo = Invoke-Expression "$Ruta\Activo.ps1"
Write-Host "El activo es $Activo"
[void][System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")
[void][System.Reflection.Assembly]::LoadWithPartialName("System.Drawing")

##########################
#PARA ACTUALIZAR EL ACTIVO
$timer = New-Object System.Windows.Forms.Timer -Property @{Interval = 1000} #Forms.Timer doesn't support AutoReset property
$script:num=0 #scope must be at script level to increment in event handler
$timer.start()
$timer.add_Tick({
    #Actualizar Activo
    #[Activo]$Activo = [Activo]::Instance
    $Activo.Update()

    #Actualizar InfoView
    $InfoView.Text=GetJobInfo $TreeView.SelectedNode.Tag

    #Actualizar LogView
    $LogView.Text=GetJobLog $TreeView.SelectedNode.Tag

    #Actualizar CView
    $CView.Text=GetActiveConditions

    #Actualizar Paneles
    foreach ($tab in $MallaTabControl.Controls){
        $Panel=$tab.Controls[0]#.Controls[0]
        UpdatePanel $Panel

    }

    #Actualizar TreeView
    foreach ($m in $TreeView.Nodes){
        foreach ($j in $m.Nodes){
            $Job=$j.Tag
            $Fichero_log="$($Ruta)\log\$($Job.Id)"
            if (Test-Path $Fichero_log){
                $j.ContextMenuStrip.Items[2].Enabled=$true
            }else{
                $j.ContextMenuStrip.Items[2].Enabled=$false
            }
            switch($Job.Status){
                "EJECUTANDO"{
                    $j.ForeColor = [System.Drawing.Color]::Gold
                    $j.Text=$j.Tag.Id
                    $j.ContextMenuStrip.Items[0].Text="Hold"
                    $j.ContextMenuStrip.Items[1].Text="Rerun"
                    $j.ContextMenuStrip.Items[1].Enabled=$false
                }
                "OK"{
                    $j.ForeColor = [System.Drawing.Color]::Green
                    $j.Text=$j.Tag.Id
                    $j.ContextMenuStrip.Items[0].Text="Hold"
                    $j.ContextMenuStrip.Items[1].Text="Rerun"
                    $j.ContextMenuStrip.Items[1].Enabled=$true
                }
                "KO"{
                    $j.ForeColor = [System.Drawing.Color]::DarkRed
                    $j.Text=$j.Tag.Id
                    $j.ContextMenuStrip.Items[0].Text="Hold"
                    $j.ContextMenuStrip.Items[1].Text="Rerun"
                    $j.ContextMenuStrip.Items[1].Enabled=$true
                }
                "WAITING"{
                    $j.ForeColor = [System.Drawing.Color]::Black
                    $j.Text=$j.Tag.Id
                    $j.ContextMenuStrip.Items[0].Text="Hold"
                    $j.ContextMenuStrip.Items[1].Text="Run Now"
                    $j.ContextMenuStrip.Items[1].Enabled=$true
                }
                "HOLDED"{
                    $j.ForeColor = [System.Drawing.Color]::Gray
                    $j.Text="$($j.Tag.Id) (H)"
                    $j.ContextMenuStrip.Items[0].Text="Release"
                    $j.ContextMenuStrip.Items[0].Image=[System.Drawing.Bitmap]::FromFile("$Ruta\images\release.png")
                    $j.ContextMenuStrip.Items[1].Enabled=$false
                    $j.ContextMenuStrip.Refresh()
                }
            }
        }
    }
})

##########################

###################
#Variables Globales
###################
$AlturasJobs=@{}
#$Botones=@{}

###################
#Funciones
###################
Function GetJobsInActive(){
    #[Activo]$Activo = [Activo]::Instance
    #Write-Output
    $Activo.Mallas.GetType()
    $Jobs= $Activo.GetAllJobs()
    $Activo.Print()
    $MallasActivas=$Activo.GetMallas()
}

Function GetJobInfo($Job) {
    if ($null -eq $Job.Id){
        return "Seleccione un job para ver su informacion"
    }
    $Info = $Job.Id
    $Info += "`n------------`n"
    $Info += "Status`n"
    $Info += "  $($Job.Status)"
    $Info += "`n------------`n"
    switch ($Job.Type) {
        "script" {
            $Info += "Operating System Job `n"
            $Info += "  File name      $($Job.File_name)`n"
            $Info += "  File path      $($Job.File_path)`n"
            $Info += "`n"
            $Info += "Variables`n"
            $p=1
            foreach ($param in $Job.Parameters){
                $Info += "  PARM$($p): $param`n"
                $p++
            }
            $Info += "`n"
            $Info += "Run Where`n"
            $Info += "  $($Job.Host_name)`n"

        }
        "ftp" {
            $Info += "File Transfer Job`n"
        }

    }
    return $Info
}

#Devuelve una cadena de texto con el log del job
Function GetJobLog($Job) {
    if ($null -eq $Job.Id){
        return "Seleccione un job para ver su log"
    }
    $Fichero_log="$($Ruta)\log\$($Job.Id)"
    if (Test-Path $Fichero_log){
        $Log = Get-Content $Fichero_log -Raw
       # $Len=(Get-Content $Fichero_log).Length
       # $Len=$Len*16.3
       # $LogView.Size = New-Object System.Drawing.Size($LogView.Size.Width,$Len)
        #Write-Host $Log
        return $Log
    }
    else{
        return "Seleccione un job para ver su informacion"
    }
}

Function GetActiveConditions(){
    if ($Activo.Conditions.Count -eq 0){
        $Condiciones="No hay condiciones"
    }
    else{
        $Condiciones="Condiciones activas: `n"
        foreach ($c in $Activo.Conditions){
            $Condiciones+=$C
            $Condiciones+="`n"
        }
    }

    return $Condiciones
}


#Devuelve una lista de los padres de un job dentro de una malla
Function GetJobPadres($Malla, $Job){
    $CondicionesHijo=$Job.Prerequisites.Name

    $Padres=[System.Collections.ArrayList]::new()
    foreach ($c in $CondicionesHijo){

        $Padres+=$Malla.Jobs | Where {$_.Id -ne $Job.Id} | Where {$_.Actions.Name -ccontains $c}
    }

    #$Padres= $Malla.Jobs | Where {$_.Actions.Name -ccontains $CondicionesHijo}
    ##Write-Host "El padre de $($Job.Id) es $($Padres.Id)"
    $Padres=$Padres | Sort-Object -Unique -Property Id
    Return $Padres
}

#Devuelve una lista de los hijos de un job dentro de una malla
Function GetJobHijos($Malla, $Job){
    $CondicionesPadre=$Job.Actions.Name

    $Hijos=[System.Collections.ArrayList]::new()
    $Hijos2=[System.Collections.ArrayList]::new()
    foreach ($c in $CondicionesPadre){

        $Hijos+=$Malla.Jobs | Where {$_.Id -ne $Job.Id} | Where {$_.Prerequisites.Name -ccontains $c} | Where {(GetJobAltura $Malla $_) -eq (GetJobAltura $Malla $Job)+1}
    }
    #$Hijos=$Hijos | select -Property Id -Unique
    #$Padres= $Malla.Jobs | Where {$_.Actions.Name -ccontains $CondicionesHijo}
    ##Write-Host "El padre de $($Job.Id) es $($Padres.Id)"
    Return $Hijos
}

Function GetJobHermanos($Malla, $Job){
    $Padres=[System.Collections.ArrayList]::new()
    $Padres+=GetJobPadres $Malla $Job
    $Hermanos=[System.Collections.ArrayList]::new()
    $Hermanos2=[System.Collections.ArrayList]::new()

    if ($Padres){
        #$Padres=$Padres | select -Property Id -Unique
        foreach ($p in $Padres){
            $PosiblesHermanos=GetJobHijos $Malla $p
            $Hermanos+=$PosiblesHermanos | Where {(GetJobAltura $Malla $_) -eq (GetJobAltura $Malla $Job)}
        }
    }
    $Hermanos=$Hermanos | Sort-Object -Unique -Property Id
    return $Hermanos

}

Function GetJobAltura($Malla, $Job){
    #Si ya está incluido en el diccionario lo devolvemos
    if( $AlturasJobs[$Job.Id] ){
        return $AlturasJobs[$Job.Id]
    }

    #Obtenemos los padres
    $Padres=GetJobPadres $Malla $Job

    #Si no tiene padres su altura es 1
    if ($null -eq $Padres){
        $AlturasJobs[$Job.Id]=1
        return $AlturasJobs[$Job.Id]
    }


    $AlturaPadre=1
    #Si tiene padres, hay que encontrar el padre con altura máxima y sumarle 1
    foreach ($Padre in $Padres){
        $AlturaAux=GetJobAltura $Malla $Padre
        $AlturaAux+=1
        if ($AlturaAux -gt $AlturaPadre){
            $AlturaPadre=$AlturaAux
        }
    }

    $AlturasJobs[$Job.Id]=$AlturaPadre
    return $AlturasJobs[$Job.Id]

}

Function GetMallaAnchura($Malla){
    $Alturas=@{}
    $Max=0
    foreach ($Job in $Malla.Jobs){
        $Altura=GetJobAltura $Malla $Job
        if ($Alturas[$Altura]){
            $Alturas[$Altura]+=1
        }else{
            $Alturas[$Altura]=1
        }

        if ($Alturas[$Altura] -gt $Max){
            $Max=$Alturas[$Altura]
        }
    }
    Return $Max
}


Function PintarJobs(){
    #[Activo]$Activo = [Activo]::Instance
    foreach ($malla in $Activo.Mallas.Values){
        #Write-Host "Analizando malla $($malla.Name)"
        foreach ($job in $malla.Jobs){
            #Write-Host "----------------------------"
            #Write-Host "Analizando job $($job.Id)"
            $Padres=GetJobPadres $malla $job
            $Altura=GetJobAltura $malla $job
            #Write-Host "Los padres son: $($Padres.Id)"
            #Write-Host "La altura es: $Altura"
        }
        $Anchura = GetMallaAnchura $malla
        #Write-Host "La anchura maxima es: $Anchura"
    }


}

Function CrearContextMenuMalla(){
    #Menu contextual para click derecho
    $contextMenuStrip1 = New-Object System.Windows.Forms.ContextMenuStrip
    #Opcion de hold y unhold
    $contextMenuStrip1.Items.Add("Eliminar").add_Click({
        $Malla=$TreeView.SelectedNode.Tag
        $Activo.DeleteFromActive($Malla.Name)
        $TreeView.Nodes[$Malla.Name].Remove()
        $MallaTabControl.TabPages["Tab_$($Malla.Name)"].Dispose()

    })
    $contextMenuStrip1.Items[0].Image=[System.Drawing.Bitmap]::FromFile("$Ruta\images\borrar.png")
    return $contextMenuStrip1
}


Function CrearContextMenuJob(){
    #Menu contextual para click derecho
    $contextMenuStrip1 = New-Object System.Windows.Forms.ContextMenuStrip
    #Opcion de hold y unhold
    $contextMenuStrip1.Items.Add("Hold").add_Click({
        $Job=$TreeView.SelectedNode.Tag
        $Malla=$TreeView.SelectedNode.Parent.Tag
        if ($Job.Status -eq "HOLDED"){
        #if ($Job.Status -eq [JobStatus]::HOLDED){
            $Activo.UnHoldJob($Malla.Name,$Job.Id)
        }else{
            $Activo.HoldJob($Malla.Name,$Job.Id)
        }
    })
    $contextMenuStrip1.Items[0].Image=[System.Drawing.Bitmap]::FromFile("$Ruta\images\hold.png")

    #Opcion de run now Y rerun
    $contextMenuStrip1.Items.Add("Run Now").add_Click({
        $Job=$TreeView.SelectedNode.Tag
        $Malla=$TreeView.SelectedNode.Parent.Tag
        #$Activo=[Activo]::Instance
        #Write-Host "Corriendo job $($TreeView.SelectedNode.Tag.Id)"
        $Activo.ExecuteJob($Malla.Name,$Job.Id)
    })
    $contextMenuStrip1.Items[1].Image=[System.Drawing.Bitmap]::FromFile("$Ruta\images\start.png")

    #Opcion de Kill
    $contextMenuStrip1.Items.Add("Kill").add_Click({
        $Job=$TreeView.SelectedNode.Tag
        $Malla=$TreeView.SelectedNode.Parent.Tag
        #$Activo=[Activo]::Instance
        #Write-Host "Corriendo job $($TreeView.SelectedNode.Tag.Id)"
        $Activo.KillJob($Malla.Name,$Job.Id)
    })
    $contextMenuStrip1.Items[2].Image=[System.Drawing.Bitmap]::FromFile("$Ruta\images\cancel.png")

    #Opcion de log
    $contextMenuStrip1.Items.Add("Log").add_Click({
        $Job=$TreeView.SelectedNode.Tag
        $Malla=$TreeView.SelectedNode.Parent.Tag
        #$Activo=[Activo]::Instance
        #Write-Host "Corriendo job $($TreeView.SelectedNode.Tag.Id)"
        $Fichero_log="$($Ruta)\log\$($Job.Id)"
        if (Test-Path $Fichero_log){
            Start notepad++ $Fichero_log
        }else{
            Write-Host "El fichero no existe"
        }
    })
    $contextMenuStrip1.Items[3].Image=[System.Drawing.Bitmap]::FromFile("$Ruta\images\log.png")
    return $contextMenuStrip1
}

Function NumeroJobsEnAltura($altura){
    $contador=0
    foreach ($a in $AlturasJobs.Values){
        if ($a -eq $altura){
            $contador++
        }
    }
    return $contador
}

Function DibujarPanel($Panel){
    $NombreMalla=$Panel.Name
    $Botones=$Panel.Tag
    $Margen=20
    $ancho=100
    $alto=$ancho/2
    $DistanciaAnchura=$ancho + 10
    $DistanciaAltura=$alto + 10
    $Niveles=@{}
    $Anchos=@{}



    #[Activo]$Activo = [Activo]::Instance
    foreach ($malla in $Activo.Mallas.Values | Where {$_.Name -eq $NombreMalla}){
        $Anchura = GetMallaAnchura $malla
        foreach ($job in $malla.Jobs){
            $Padres=GetJobPadres $malla $job
            $Altura=GetJobAltura $malla $job
            #Obtenemos cuantos jobs hay ya en esa línea
            if ($null -eq $Niveles[$Altura]){
                $Niveles[$Altura]=0
            }else{
                $Niveles[$Altura]=$Niveles[$Altura]+1
            }

            #Calculamos el eje X
            if ($null -eq $Padres){ #No tiene padres, es el primero
                $min=$Margen
                $max=($DistanciaAnchura*$Anchura)+($Margen/2)
                $X=(($min+$max)/2)-($ancho/2)
                $Y=($Altura-1)*$DistanciaAltura+$Margen
            }

            elseif ($Padres.Count -eq 1){
                $Hermanos=GetJobHermanos $malla $job
                if ($Hermanos.Count -eq 1){ #Solo tiene un padre y ese padre solo tiene un hijo
                    $BotonPadre=$Botones[$Padres[0].Id]
                    $X=$BotonPadre.Bounds.X
                    $Y=($Altura-1)*$DistanciaAltura+$Margen
                }else{#Tiene mas hermanos
                    $LongitudTotal=($Ancho*$Hermanos.Count)+(($DistanciaAnchura-$Ancho)*($Hermanos.Count-1))
                    $Centro=$BotonPadre=$Botones[$Padres[0].Id].Bounds.X+$ancho/2

                    $X=($Centro-($LongitudTotal/2))+($Niveles[$Altura])*$DistanciaAnchura
                    $Y=($Altura-1)*$DistanciaAltura+$Margen
                }
            }elseif ($Padres.Count -gt 1){

                $Hermanos=GetJobHermanos $malla $job
                #Hay que obtener el centro de todos los padres
                $Xmin=100000
                $Xmax=0
                foreach ($p in $Padres){
                    $BotonPadre=$Botones[$p.Id]
                    if($BotonPadre.Bounds.X -gt $Xmax){
                        $Xmax=$BotonPadre.Bounds.X
                    }
                    if($BotonPadre.Bounds.X -lt $Xmin){
                        $Xmin=$BotonPadre.Bounds.X
                    }
                }
                $Centro=($Xmin+$Xmax)/2



                if ($Hermanos.Count -eq 1){ #Solo tiene un padre y ese padre solo tiene un hijo
                    $X=$Centro
                    $Y=($Altura-1)*$DistanciaAltura+$Margen
                }else{#Tiene mas hermanos
                    $X=($Centro-($LongitudTotal/2))+($Niveles[$Altura])*$DistanciaAnchura
                    $Y=($Altura-1)*$DistanciaAltura+$Margen
                }
            }

            else{

                $X=$Niveles[$Altura]*$DistanciaAnchura+$Margen
                $Y=($Altura-1)*$DistanciaAltura+$Margen

            }

            DibujarJob $Panel $job $X $Y $ancho $alto
            DibujarArrow $Panel $job $malla
        }

    }
}



Function UpdatePanel($Panel){
    $Botones=$Panel.Tag
    foreach ($boton in $Botones.Values){
        $Job=$boton.Tag
        $Fichero_log="$($Ruta)\log\$($Job.Id)"
        if (Test-Path $Fichero_log){
            $boton.ContextMenuStrip.Items[2].Enabled=$true
        }else{
            $boton.ContextMenuStrip.Items[2].Enabled=$false
        }
            switch($Job.Status){
                "EJECUTANDO"{
                    $boton.ForeColor = [System.Drawing.Color]::Gold
                    $boton.Text=$boton.Tag.Id
                    $boton.ContextMenuStrip.Items[0].Text="Hold"

                    $boton.ContextMenuStrip.Items[1].Text="Rerun"
                    $boton.ContextMenuStrip.Items[1].Enabled=$false
                    $boton.ContextMenuStrip.Items[2].Enabled=$true

                    $boton.ContextMenuStrip.Refresh()
                }
                "OK"{
                    $boton.ForeColor = [System.Drawing.Color]::Green
                    $boton.Text=$boton.Tag.Id
                    $boton.ContextMenuStrip.Items[0].Text="Hold"

                    $boton.ContextMenuStrip.Items[1].Text="Rerun"
                    $boton.ContextMenuStrip.Items[1].Enabled=$true
                    $boton.ContextMenuStrip.Items[2].Enabled=$false

                    $boton.ContextMenuStrip.Refresh()
                }
                "KO"{
                    $boton.ForeColor = [System.Drawing.Color]::DarkRed
                    $boton.Text=$boton.Tag.Id
                    $boton.ContextMenuStrip.Items[0].Text="Hold"

                    $boton.ContextMenuStrip.Items[1].Text="Rerun"
                    $boton.ContextMenuStrip.Items[1].Enabled=$true

                    $boton.ContextMenuStrip.Items[2].Enabled=$false

                    $boton.ContextMenuStrip.Refresh()
                }
                "WAITING"{
                    $boton.ForeColor = [System.Drawing.Color]::Black
                    $boton.Text=$boton.Tag.Id
                    $boton.ContextMenuStrip.Items[0].Text="Hold"

                    $boton.ContextMenuStrip.Items[1].Text="Run Now"
                    $boton.ContextMenuStrip.Items[1].Enabled=$true

                    $boton.ContextMenuStrip.Items[2].Enabled=$false

                    $boton.ContextMenuStrip.Refresh()
                }
                "HOLDED"{
                    $boton.ForeColor = [System.Drawing.Color]::Gray
                    $boton.Text="$($boton.Tag.Id) (H)"
                    $boton.ContextMenuStrip.Items[0].Text="Release"
                    $boton.ContextMenuStrip.Items[0].Image=[System.Drawing.Bitmap]::FromFile("$Ruta\images\release.png")
                    $boton.ContextMenuStrip.Items[1].Enabled=$false
                    $boton.ContextMenuStrip.Items[2].Enabled=$false
                    $boton.ContextMenuStrip.Refresh()
                }
            }

    }

}

Function DibujarArrow($Panel, $Job, $Malla){
    <#
    $Panel.Add_Paint({
        $graphics = $_.Graphics
        $pen = new-object Drawing.Pen black
        $pen.Width=1

        $hijos = GetJobHijos($Malla,$Job)
        Write-Host "Padre: $($Job)"
        Write-Host "Padre: $($Job.Id)"
        foreach ($h in $hijos){
            Write-Host "    Hijo: $($h.Id)"
        }
        $graphics.DrawLine($pen,10,10,200,200)

    })
    #>
}

Function DibujarJob($Panel, $Job, $x, $y,$ancho,$alto){

    $Button = New-Object System.Windows.Forms.Button
    $Button.Location = New-Object System.Drawing.Size($x,$y)
    $Button.Size = New-Object System.Drawing.Size($ancho,$alto)
    $Button.Text = $Job.Id
    $Button.Tag = $Job
    $Botones[$Job.Id]=$Button
    $Button.ContextMenuStrip=CrearContextMenuJob

    #Write-Host $Botones.Values

    $Button.Add_MouseUP( {
        SelectTreeJob $this.Tag.Id #Seleccionamos el job en el tree view
        if ($_.Button -eq 'Left' -and $_) {
            ##Write-Host "Left Click Node: " $_.Node.Tag
            $InfoView.Text=GetJobInfo $this.Tag
            #$this.SelectedNode = $_.Node #Select the node (Helpful when using a ContextMenuStrip)
        }
        if ($_.Button -eq 'Right' -and $_) {
            ##Write-Host "Left Click Node: " $_.Node.Tag
            $InfoView.Text=GetJobInfo $this.Tag
            #$this.SelectedNode = $_.Node #Select the node (Helpful when using a ContextMenuStrip)
        }
    })


    $Panel.Controls.Add($Button)



}

#Se llama a esta funcion cuando se selecciona a un Job en el Panel
Function SelectTreeJob($Id){
    foreach ($node_malla in $TreeView.Nodes){
        foreach ($node_job in $node_malla.Nodes){
            if ($node_job.Tag.Id -eq $Id){
                $Treeview.SelectedNode=$node_job
                #$MallaTabControl.SelectedTab=$MallaTabControl.Controls["Tab_$($node_malla.Text)"]
                #$MallaTabControl.SelectedTab
            }
        }
    }
}



Function AddToActiveGui($NombreMalla, $Odate){

    #[Activo]$Activo = [Activo]::Instance
    $malla_string=$Activo.GetJsonMallas($Ruta,$NombreMalla)


    $malla_string=$malla_string.Replace("%%odate",$Odate)


    $malla_json = $malla_string | ConvertFrom-Json
    $Activo.AddToActive($NombreMalla,$malla_json)

    DibujarTreeView $NombreMalla
    CrearPanelMalla $NombreMalla
}

Function VentanaAddMallas(){
    #$Activo=[Activo]::Instance
    $MallasDisponibles=$Activo.GetAvailableMallas()
    $MallasDisponibles=$MallasDisponibles.Name
    $FormAddMalla = New-Object System.Windows.Forms.Form
    $FormAddMalla.Text = "Anadir malla"
    $FormAddMalla.Size = New-Object System.Drawing.Size(500, 500)

    #Parametros
    $Label = New-Object System.Windows.Forms.Label
    $Label.Location = New-Object System.Drawing.Size(300,0)
    $Label.Text="ODATE"
    $FormAddMalla.Controls.Add($Label)

    $textBox = New-Object System.Windows.Forms.TextBox
    $textBox.Location = New-Object System.Drawing.Point(300,30)
    $textBox.Size = New-Object System.Drawing.Size(100,30)
    $textBox.Name = "textBox"
    $FormAddMalla.Controls.Add($textBox)

    #Listado de mallas
    $ListaMallas= New-Object System.Windows.Forms.ListBox
    $ListaMallas.Size = New-Object System.Drawing.Size(300, 500)
    $ListaMallas.Name="ListaMallas"
    foreach ($m in $MallasDisponibles){
        $ListaMallas.Items.Add($m)
    }
    $FormAddMalla.Controls.Add($ListaMallas)



    #Boton de añadir
    $AddButton = New-Object System.Windows.Forms.Button
    $AddButton.Location = New-Object System.Drawing.Size(320,300)
    $AddButton.Size = New-Object System.Drawing.Size(100,70)
    $AddButton.Text = "Add Malla"
    $AddButton.Add_Click({
        $MallaSeleccionada=$this.Parent.Controls["ListaMallas"].SelectedItem
        $OdateSeleccionado=$this.Parent.Controls["textBox"].Text
        AddToActiveGui $MallaSeleccionada $OdateSeleccionado
    })
    $FormAddMalla.Controls.Add($AddButton)


    $FormAddMalla.Show()


}

Function MenuSuperior(){
    $MS_Main = new-object System.Windows.Forms.MenuStrip
    $ActivoToolStripMenuItem = new-object System.Windows.Forms.ToolStripMenuItem
    $ActivoAnadirToolStripMenuItem = new-object System.Windows.Forms.ToolStripMenuItem
    $MallasToolStripMenuItem = new-object System.Windows.Forms.ToolStripMenuItem
    #
    # MS_Main
    #
    $MS_Main.Items.AddRange(@(
    $ActivoToolStripMenuItem,
    $MallasToolStripMenuItem))
    $MS_Main.Location = new-object System.Drawing.Point(0, 0)
    $MS_Main.Name = "MS_Main"
    $MS_Main.Size = new-object System.Drawing.Size(354, 24)
    $MS_Main.TabIndex = 0
    $MS_Main.Text = "menuStrip1"
    #
    # ActivoToolStripMenuItem
    #
    $ActivoToolStripMenuItem.DropDownItems.AddRange(@(
    $ActivoAnadirToolStripMenuItem))
    $ActivoToolStripMenuItem.Name = "ActivoToolStripMenuItem"
    $ActivoToolStripMenuItem.Size = new-object System.Drawing.Size(35, 20)
    $ActivoToolStripMenuItem.Text = "&Activo"
    #
    # ActivoAnadirToolStripMenuItem
    #
    $ActivoAnadirToolStripMenuItem.Name = "ActivoAnadirToolStripMenuItem"
    $ActivoAnadirToolStripMenuItem.Size = new-object System.Drawing.Size(152, 22)
    $ActivoAnadirToolStripMenuItem.Text = "&Anadir Malla"


    $ActivoAnadirToolStripMenuItem.Add_Click( {
        VentanaAddMallas
    } )
    #
    # MallasToolStripMenuItem
    #
    $MallasToolStripMenuItem.Name = "MallasToolStripMenuItem"
    $MallasToolStripMenuItem.Size = new-object System.Drawing.Size(51, 20)
    $MallasToolStripMenuItem.Text = "&Mallas"

    return $MS_Main
}

Function CrearPanelMalla($NombreMalla){
    #Creamos el tab
    $Tab = New-object System.Windows.Forms.Tabpage
    $Tab.DataBindings.DefaultDataSourceUpdateMode = 0
    $Tab.UseVisualStyleBackColor = $True
    $Tab.Name = "Tab_$($NombreMalla)"
    $Tab.Text = $NombreMalla

    #Creamos el panel exterior
    $PanelExt = New-Object System.Windows.Forms.Panel
    $PanelExt.Location = New-Object System.Drawing.Point(0, 0)
    $PanelExt.Size = New-Object System.Drawing.Size(400, 400)
    $PanelExt.AutoScroll=$true
    #$PanelExt.BorderStyle = 'FixedDialog';
    $PanelExt.Name = "PanelExt_$($NombreMalla)"


    $PanelExt.Anchor = [System.Windows.Forms.AnchorStyles]::Top `
    -bor [System.Windows.Forms.AnchorStyles]::Bottom `
    -bor [System.Windows.Forms.AnchorStyles]::Left `
    -bor [System.Windows.Forms.AnchorStyles]::Right


    #>

    #Creamos el panel interior
    #$Anchura tenemos que calcular correctamente las dimensiones del panel, para que no sobre
    $Panel = New-Object System.Windows.Forms.Panel
    $Panel.Size = New-Object System.Drawing.Size(1600, 1550)
    $Panel.Name=$NombreMalla
    $Panel.Tag=@{}
    $PanelExt.Name = "Panel_$($NombreMalla)"
    #$Panel.BackColor=[Drawing.Color]::FromArgb(65, 204, 212, 230)

    #$PanelExt.BackColor= [System.Drawing.Color]::Gray

    #$PanelExt.Controls.Add($Panel)
    #$PanelExt.Controls.AddRange($Panel)


    #$Tab.Controls.Add($PanelExt)
    $Tab.Controls.AddRange(@($Panel))
    $Tab.AutoScroll=$true


    $MallaTabControl.Controls.Add($Tab)

    DibujarPanel $Panel





}


####COMIENZA LA INTERFAZ####
$Form = New-Object System.Windows.Forms.Form
$Form.Text = "Control-M"
$Form.Size = New-Object System.Drawing.Size(1200, 600)
#$Form.FormBorderStyle='FixedDialog'
$Form.AutoScale=$true
#$Form.AutoSize=$true
$RutaIcono="$Ruta\images\controlm.ico"
Write-Host $RutaIcono
$Form.Icon=New-Object system.drawing.icon ($RutaIcono)


$MenuSuperior=MenuSuperior

#TabControl para las mallas
$MallaTabControl = New-object System.Windows.Forms.TabControl
$MallaTabControl.Location = New-Object System.Drawing.Point(200, 24)
$MallaTabControl.Size = New-Object System.Drawing.Size(600, 525)
$MallaTabControl.Name = "Tabs_mallas"

$MallaTabControl.Anchor = [System.Windows.Forms.AnchorStyles]::Top `
-bor [System.Windows.Forms.AnchorStyles]::Bottom `
-bor [System.Windows.Forms.AnchorStyles]::Left `
-bor [System.Windows.Forms.AnchorStyles]::Right


#TabControl para la información
$InfoTabControl = New-object System.Windows.Forms.TabControl
$InfoTabControl.Location = New-Object System.Drawing.Point(800, 24)
$InfoTabControl.Size = New-Object System.Drawing.Size(380, 525)
$InfoTabControl.Name = "Tabs_info"
$InfoTabControl.Anchor = [System.Windows.Forms.AnchorStyles]::Top `
-bor [System.Windows.Forms.AnchorStyles]::Bottom `
-bor [System.Windows.Forms.AnchorStyles]::Right

#Creamos el tab para la informacion en texto
$TabInfo = New-object System.Windows.Forms.Tabpage
$TabInfo.DataBindings.DefaultDataSourceUpdateMode = 0
$TabInfo.UseVisualStyleBackColor = $True
$TabInfo.Name = "Tab_Info"
$TabInfo.Text = "Info"

$InfoView = New-Object System.Windows.Forms.RichTextBox
$InfoView.Location = New-Object System.Drawing.Point(0, 0)
$InfoView.Size = New-Object System.Drawing.Size(380, 525)
$InfoView.ReadOnly=$true

$InfoView.Anchor = [System.Windows.Forms.AnchorStyles]::Top `
-bor [System.Windows.Forms.AnchorStyles]::Bottom `
-bor [System.Windows.Forms.AnchorStyles]::Left `
-bor [System.Windows.Forms.AnchorStyles]::Right

$TabInfo.Controls.AddRange(@($InfoView))
$TabInfo.AutoScroll=$true
$InfoTabControl.Controls.Add($TabInfo)

#Creamos el tab para el log
$TabLog = New-object System.Windows.Forms.Tabpage
$TabLog.DataBindings.DefaultDataSourceUpdateMode = 0
$TabLog.UseVisualStyleBackColor = $True
$TabLog.Name = "Tab_Log"
$TabLog.Text = "Log"

$LogView = New-Object System.Windows.Forms.RichTextBox
$LogView.Location = New-Object System.Drawing.Point(0, 0)
$LogView.Size = New-Object System.Drawing.Size(400,2000)
$LogView.ReadOnly=$true
$LogView.AutoSize=$true

<#
$LogView.Anchor = [System.Windows.Forms.AnchorStyles]::Top `
-bor [System.Windows.Forms.AnchorStyles]::Bottom `
-bor [System.Windows.Forms.AnchorStyles]::Left `
-bor [System.Windows.Forms.AnchorStyles]::Right
#>

#$TabLog.Controls.AddRange(@($LogView))
$TabLog.Controls.Add($LogView)
$TabLog.AutoScroll=$true
$InfoTabControl.Controls.Add($TabLog)

#$Form.Controls.Add($InfoView)

#Creamos el tab para la informacion del activo
$CInfo = New-object System.Windows.Forms.Tabpage
$CInfo.DataBindings.DefaultDataSourceUpdateMode = 0
$CInfo.UseVisualStyleBackColor = $True
$CInfo.Name = "Tab_Conditions"
$CInfo.Text = "General Conditions"

$CView = New-Object System.Windows.Forms.RichTextBox
$CView.Location = New-Object System.Drawing.Point(0, 0)
$CView.Size = New-Object System.Drawing.Size(380, 525)
$CView.ReadOnly=$true

$CView.Anchor = [System.Windows.Forms.AnchorStyles]::Top `
-bor [System.Windows.Forms.AnchorStyles]::Bottom `
-bor [System.Windows.Forms.AnchorStyles]::Left `
-bor [System.Windows.Forms.AnchorStyles]::Right

$CInfo.Controls.AddRange(@($CView))
$CInfo.AutoScroll=$true
$InfoTabControl.Controls.Add($CInfo)


$TreeView = New-Object System.Windows.Forms.TreeView
$TreeView.Location = New-Object System.Drawing.Point(0, 24)
$TreeView.Size = New-Object System.Drawing.Size(200, 525)
$TreeView.Anchor = [System.Windows.Forms.AnchorStyles]::Top `
-bor [System.Windows.Forms.AnchorStyles]::Bottom `
-bor [System.Windows.Forms.AnchorStyles]::Left


#$Form.Controls.Add($TreeView)
$form.Controls.AddRange(@($TreeView, $InfoTabControl,$MallaTabControl, $MenuSuperior))

Function DibujarTreeView($NombreMalla){
    #[Activo]$Activo = [Activo]::Instance
    $TreeView.BeginUpdate()

    foreach ($malla in $Activo.Mallas.Values){
        if ($malla.Name -eq $NombreMalla){
            $NodoMalla=$TreeView.Nodes.Add($malla.Name)
            $NodoMalla.Tag=$malla
            $NodoMalla.Name=$malla.Name
            $NodoMalla.ContextMenuStrip=CrearContextMenuMalla
            foreach ($job in $malla.Jobs){
                $NodoHijo=$NodoMalla.Nodes.Add($job.Id)
                $NodoHijo.Tag=$job
                $NodoHijo.ContextMenuStrip=CrearContextMenuJob
            }
        }
    }
    $TreeView.EndUpdate()
}
#DibujarTreeView


$TreeView.add_NodeMouseClick({
        if ($_.Button -eq 'Left' -and $_) {
            ##Write-Host "Left Click Node: " $_.Node.Tag
            $InfoView.Text=GetJobInfo $_.Node.Tag
            $this.SelectedNode = $_.Node #Select the node (Helpful when using a ContextMenuStrip)
        }
        if ($_.Button -eq 'Right') {
            $InfoView.Text=GetJobInfo $_.Node.Tag
            $this.SelectedNode = $_.Node
            $_.Node.ContextMenuStrip.Show()
        }
        #Cuando se clica se activa la pestaña correspondiente
        if($null -eq $_.Node.Parent){ #Es el nodo malla
            $MallaTabControl.SelectedTab=$MallaTabControl.Controls["Tab_$($_.Node.Text)"]
        }else{
            $MallaTabControl.SelectedTab=$MallaTabControl.Controls["Tab_$($_.Node.Parent.Text)"]
        }
    })

$TreeView.EndUpdate()




$Form.ShowDialog()


$Timer.Stop() #This will keep running in the background unless you stop it

