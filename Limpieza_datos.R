#install.packages("tidyverse")
#nstall.packages("janitor")
library(janitor)
library(tidyverse)
#BASE DE DATOS 
datos_musica <- read_csv("1. Musica.csv")
#RENOMBRAR COLUMNAS 
datos_musica <- datos_musica |> clean_names()
#LIMPIEZA DE BASE DE DATOS
View(datos_musica)
#ELIMINACIÓN DE COLUMNAS INNECESARIA PARA EL ANÁLISIS
datos_musica <- datos_musica |> select(-timestamp, -permissions)
#VERIFICACIÓN DE DATOS FALTANTES
summary(datos_musica)
#ESTURUCTURA DE LOS DATOS
glimpse(datos_musica)
#ELIMINACIÓN DE NA Y SU SUSTITUCIÓN CON LA MEDIANA
datos_musica <- datos_musica |>
  mutate(age = if_else(is.na(age), median(age, na.rm = TRUE), age))
datos_musica <- datos_musica |>
  mutate(bpm = if_else(is.na(bpm), median(bpm, na.rm = TRUE), bpm))
colSums(is.na(datos_musica))
#VERIFICACIÓN DE ESPACIOS VACIOS 
datos_musica |>
  summarise(across(where(is.character), ~sum(. == "" | . == " ", na.rm = TRUE)))
#VER CUALES VARIABLES SE REPITEN EN LAS VARIABLES CUALITATIVAS Y SUSTITUIR POR LA MODA
#1 music_effects
datos_musica |> tabyl(music_effects) |> arrange(desc(n))
datos_musica <- datos_musica |> 
  mutate(music_effects = if_else(music_effects == "" | music_effects == " " | is.na(music_effects), 
  "Improve", music_effects))
datos_musica |> tabyl(music_effects)
#2 foreign_languages
datos_musica |> tabyl(foreign_languages) |> arrange(desc(n))
datos_musica <- datos_musica |> 
  mutate(foreign_languages = if_else(foreign_languages == "" | foreign_languages == " " | is.na(foreign_languages), 
  "Yes", foreign_languages))
datos_musica |> tabyl(foreign_languages)
#3 instrumentalist            
datos_musica |> tabyl(instrumentalist) |> arrange(desc(n))
datos_musica <- datos_musica |> 
  mutate(instrumentalist = if_else(is.na(instrumentalist) | instrumentalist == "" | instrumentalist == " ", 
  "No", instrumentalist))
datos_musica |> tabyl(instrumentalist)
#4 while_working
datos_musica |> tabyl(while_working) |> arrange(desc(n))
datos_musica <- datos_musica |> 
  mutate(while_working = if_else(is.na(while_working) | while_working == "" | while_working == " ", 
  "Yes", while_working))
datos_musica |> tabyl(while_working)
#5 primary_streaming_service 
datos_musica |> tabyl(primary_streaming_service) |> arrange(desc(n))
datos_musica <- datos_musica |> 
  mutate(primary_streaming_service = if_else(is.na(primary_streaming_service) | primary_streaming_service == "" | primary_streaming_service == " ", 
  "Spotify", primary_streaming_service))
datos_musica |> tabyl(primary_streaming_service)
#6 composer                   
datos_musica |> tabyl(composer) |> arrange(desc(n))
datos_musica <- datos_musica |> 
  mutate(composer = if_else(is.na(composer) | composer == "" | composer == " ", "No", composer))
datos_musica |> tabyl(composer)
#REVISIÓN DE LAS EDADES
summary(datos_musica$age)
#DEFINIMOS QUE CUALQUIER BPM MAYOR A 500 ES UN ERROR Y LO PASAMOS A LA MEDIANA 
summary(datos_musica$bpm)
#Usamos 500 porque es el límite aproximado de géneros súper rápidos como el Speedcore
datos_musica <- datos_musica |> 
  mutate(bpm = if_else(bpm > 500 | bpm < 40, median(bpm, na.rm = TRUE), bpm))
summary(datos_musica$bpm)
#VERIFICANDO EL RESUMEN DE ESCUCHA POR DIA
summary(datos_musica$hours_per_day)
#VERIFICANDO EL RANGO DE LAS ESCALAS, QUE EL MINIMO SEA 0 Y EL MAXIMO 10
datos_musica |> 
  select(anxiety, depression, insomnia, ocd) |> summary()
#VERIFICANDO SI LAS COLUMNAS DE FREQUENCY TIENEN ESPACIOS VACIOS 
datos_musica |> 
  summarise(across(starts_with("frequency_"), ~sum(is.na(.) | . == "" | . == " ")))
orden_logico <- c("Never", "Rarely", "Sometimes", "Very frequently")
datos_musica <- datos_musica |> mutate(across(starts_with("frequency_"), 
~factor(., levels = orden_logico, ordered = TRUE)))
glimpse(datos_musica |> select(frequency_rock))

## Instalamos librerias necesarias 
install.packages("usethis")
install.packages("gitcreds")
## Cargamos libreria y configuramos
library(usethis)
use_git_config(
  user.name = "ddaza-alt", # Cambia esto por tu nombre
  user.email = "danieladaza400@gmail.com" # Usa el email asociado a tu cuenta de GitHub
)
## Creamos token para credenciales de github
create_github_token()
## Configuramos token
library(gitcreds)
gitcreds_set()

write_csv(datos_musica, "datos_musica_limpios_FINAL.csv")
