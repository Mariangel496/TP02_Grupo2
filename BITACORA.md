# Bitácora técnica - TP02

| Nº | Fecha | Acción / comando | Resultado | Problema | Solución intentada | Estado |
|----|-------|------------------|-----------|----------|--------------------|--------|
| 1 | 23/09 | `cd %USERPROFILE%\Desktop` | No encuentra la ruta | El Escritorio está en `C:\Users\Administrator\.vscode\Desktop`, no en la ruta estándar | Probé `OneDrive\Escritorio` (falló). Abrí cmd desde la barra del Explorador | RESUELTO |
| 2 | 23/09 | `git clone https://github.com/Mariangel496/TP02_Grupo2.git` | Repo clonado OK | - | - | RESUELTO |
| 3 | 23/09 | `git push` | Pidió iniciar sesión en GitHub | Primera vez que se sube desde esta PC | Sign in with your browser, autoricé con mi cuenta | RESUELTO |
| 4 | 23/09 | `for /d %d in (evidencias\*) do ...` | No creó los .gitkeep | El comando es de cmd y la terminal era PowerShell | Usé el equivalente en PowerShell (Get-ChildItem ... New-Item) | RESUELTO |
| 5 | 23/09 | `git push` + otro comando en la misma línea | `error: unknown switch 'D'` | Pegué dos comandos juntos sin apretar Enter | Ejecuté un comando por vez | RESUELTO |
| 6 | 23/09 | Comando .gitkeep desde terminal de VS Code | No encontraba la carpeta | La terminal estaba dentro de `evidencias` | `cd ..` para subir a la raíz del repo | RESUELTO |