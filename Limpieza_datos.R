#install.packages("tidyverse")
#nstall.packages("janitor")
library(janitor)
library(tidyverse)
library(readr)

#Base de datos
datos_musica <- read_csv("1. Musica.csv")

#Renombrar columnas 
datos_musica <- datos_musica |> clean_names()

#Limpieza de base de datos
View(datos_musica)

#Eliminación de columnas innecesarias para el análisis
datos_musica <- datos_musica |> select(-timestamp, -permissions)

#Verificación de datos faltantes
summary(datos_musica)

#Estructura de los datos 
glimpse(datos_musica)

#Eliminación de NA y su sustitución con la mediana
datos_musica <- datos_musica |>
  mutate(age = if_else(is.na(age), median(age, na.rm = TRUE), age),
         bpm = if_else(is.na(bpm), median(bpm, na.rm = TRUE), bpm))
colSums(is.na(datos_musica))

##Verificación de espacios vacíos
datos_musica |>
  summarise(across(where(is.character), ~sum(. == "" | is.na(.), na.rm = TRUE)))

#Ver cuales variables se repiten en las variables cualitativas y sustituir por la moda
# Ver la moda de cada columna
datos_musica |> tabyl(music_effects) |> arrange(desc(n))
datos_musica |> tabyl(foreign_languages) |> arrange(desc(n))
datos_musica |> tabyl(instrumentalist) |> arrange(desc(n))
datos_musica |> tabyl(while_working) |> arrange(desc(n))
datos_musica |> tabyl(primary_streaming_service) |> arrange(desc(n))
datos_musica |> tabyl(composer) |> arrange(desc(n))

datos_musica <- datos_musica |>
  mutate(music_effects = if_else(music_effects == "" | is.na(music_effects), "Improve",
        music_effects)) |>
  mutate(foreign_languages = if_else(foreign_languages == "" | is.na(foreign_languages), "Yes",
        foreign_languages)) |>
  mutate(instrumentalist = if_else(instrumentalist == "" | is.na(instrumentalist), "No", 
        instrumentalist)) |>
  mutate(while_working = if_else(while_working == "" | is.na(while_working), "Yes", 
        while_working)) |>
  mutate(primary_streaming_service = if_else(primary_streaming_service == "" | 
        is.na(primary_streaming_service), "Spotify", primary_streaming_service)) |>
  mutate(composer = if_else(composer == "" | is.na(composer), "No", composer))

#Revisión de las edades
summary(datos_musica$age)

#Definimos que cualquier bpm mayor a 500 es un error y lo pasamos a la mediana 
summary(datos_musica$bpm)

#Usamos 500 porque es el límite aproximado de géneros súper rápidos como el Speedcore
datos_musica <- datos_musica |> 
  mutate(bpm = if_else(bpm > 500 | bpm < 40, median(bpm, na.rm = TRUE), bpm))
summary(datos_musica$bpm)

#Verificando el resumen de escucha por día
summary(datos_musica$hours_per_day)

#Reemplazar valores fuera de rango (0-24) con NA
datos_musica <- datos_musica |> 
  mutate(hours_per_day = ifelse(hours_per_day > 24 | hours_per_day < 0, NA, 
  hours_per_day))

#Calcular la mediana
mediana_hours <- median(datos_musica$hours_per_day, na.rm = TRUE)

#Imputar la mediana en los huecos
datos_musica <- datos_musica |> 
  mutate(hours_per_day = ifelse(is.na(hours_per_day), mediana_hours, hours_per_day))

#Verificando el rango de las escalas, que el mínimo sea 0 y el máximo 10
datos_musica |> 
  select(anxiety, depression, insomnia, ocd) |> summary()

#Verificando si las columnas de frequency tienen espacios vacíos
datos_musica |> 
  summarise(across(starts_with("frequency_"), ~sum(is.na(.) | . == "" | . == " ")))

#Definimos el orden lógico
orden_logico <- c("Never", "Rarely", "Sometimes", "Frequently", "Very frequently")

#Convertimos a factor ordenado
datos_musica <- datos_musica |>
  mutate(across(starts_with("frequency_"), ~factor(., levels = orden_logico, 
                                                   ordered = TRUE)))
#Verificamos correción
datos_musica |> 
  select(starts_with("frequency_")) |> 
  glimpse()

#Guardamos los datos limpios
write_csv(datos_musica, "datos_musica_limpios_FINAL.csv")
dfclean <- read_csv("datos_musica_limpios_FINAL.csv")
view(dfclean)
