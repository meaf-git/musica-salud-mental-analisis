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

#Calculamos la mediana
mediana_hours <- median(datos_musica$hours_per_day, na.rm = TRUE)

#Rellenamos con la mediana en los huecos
datos_musica <- datos_musica |> 
  mutate(hours_per_day = ifelse(is.na(hours_per_day), mediana_hours, hours_per_day))

#Verificando el rango de las escalas, que el mínimo sea 0 y el máximo 10
datos_musica |> 
  select(anxiety, depression, insomnia, ocd) |> summary()

# Vemos la estructura y el tipo de datos antes del cambio
datos_musica |> 
select(starts_with("frequency_")) |> 
glimpse()

#Verificando si las columnas de frequency tienen espacios vacíos
datos_musica |> 
  summarise(across(starts_with("frequency_"), ~sum(is.na(.) | . == "" | . == " ")))

#Identificar las columnas y le asignamos su nuevo valor 
datos_musica <- datos_musica |> 
  mutate(across(starts_with("frequency_"), 
                ~ case_match(.,
                             "Never" ~ 1,
                             "Rarely" ~ 2,
                             "Sometimes" ~ 3,
                             "Very frequently" ~ 4,
                             .default = NA_real_)))
#Verificamos el cambio
datos_musica |> 
  select(starts_with("frequency_")) %>% 
  glimpse()

# Vemos la estructura y el tipo de dato
str(datos_musica[c("while_working", "exploratory", "instrumentalist", "composer")])

#Identificamos las columnas que tienen "Yes"/"No"
columnas_si_no <- c("while_working", "instrumentalist", "composer", 
                    "exploratory", "foreign_languages")

# Convertimos Yes a 1 y No a 0
datos_musica <- datos_musica |> 
  mutate(across(c(while_working, instrumentalist, composer, 
                  exploratory, foreign_languages),
                ~ case_when(
                  . == "Yes" ~ 1,
                  . == "No" ~ 0,
                  TRUE ~ NA_real_
                )))

#Verificamos el cambio
str(datos_musica[c("while_working", "exploratory", "instrumentalist", "composer")])

# Vemos la estructura y el tipo de dato antes del cambio
table(datos_musica$music_effects)

#Identificar las columnas y le asignamos su nuevo valor 
datos_musica <- datos_musica |> 
  mutate(music_effects = case_match(music_effects,
                                    "Worsen" ~ -1,
                                    "No effect" ~ 0,
                                    "Improve" ~ 1,
                                    .default = NA_real_))
#Verificamos el cambio
table(datos_musica$music_effects)

#Guardamos los datos limpios
write_csv(datos_musica, "datos_musica_limpios_FINAL.csv")
dfclean <- read_csv("datos_musica_limpios_FINAL.csv")
view(dfclean)
