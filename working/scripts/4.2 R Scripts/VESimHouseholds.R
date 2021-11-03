source(file.path(ve.runtime, "initTableRD.R"))
source(file.path(ve.runtime, "initDatasetRD.R"))
source(file.path(ve.runtime, "writeToTableRD.R"))

Hhsize_ls <-
  list(
      NAME = "HhSize",
      TABLE = "Household",
      GROUP = "Year",
      TYPE = "people",
      UNITS = "PRSN",
      NAVALUE = -1,
      PROHIBIT = c("NA", "<= 0"),
      ISELEMENTOF = "",
      SIZE = 0,
      DESCRIPTION = "Number of persons",
      MULTIPLIER = "NA",
      YEAR = "NA",
      MODULE = "CreateHouseholds"
    )

age0to14_ls <-
  list(
    NAME ="Age0to14",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "people",
    UNITS = "PRSN",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "CreateHouseholds",
    DESCRIPTION ="Persons in 0 to 14 year old age group"
  )

age15to19_ls <-
  list(
    NAME ="Age15to19",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "people",
    UNITS = "PRSN",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "CreateHouseholds",
    DESCRIPTION ="Persons in 15 to 19 year old age group"
  )

age20to29_ls <-
  list(
    NAME ="Age20to29",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "people",
    UNITS = "PRSN",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "CreateHouseholds",
    DESCRIPTION ="Persons in 20 to 29 year old age group"
  )

age30to54_ls <-
  list(
    NAME ="Age30to54",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "people",
    UNITS = "PRSN",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "CreateHouseholds",
    DESCRIPTION ="Persons in 30 to 54 year old age group"
  )

age55to64_ls <-
  list(
    NAME ="Age55to64",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "people",
    UNITS = "PRSN",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "CreateHouseholds",
    DESCRIPTION ="Persons in 55 to 64 year old age group"
  )

age65Plus_ls <-
  list(
    NAME ="Age65Plus",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "people",
    UNITS = "PRSN",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "CreateHouseholds",
    DESCRIPTION ="Persons in 65 or older age group"
  )

HhId_ls <-
  list(
    NAME = "HhId",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "character",
    UNITS = "ID",
    NAVALUE = "NA",
    SIZE = 11,
    PROHIBIT = "",
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "CreateHouseholds",
    DESCRIPTION = "Unique household ID"
  )

Azone_ls <-
  list(
    NAME = "Azone",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "character",
    UNITS = "ID",
    NAVALUE = "NA",
    SIZE = 11,
    PROHIBIT = "",
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "CreateHouseholds",
    DESCRIPTION = "Azone ID"
  )

HhType_ls <-
  list(
    NAME = "HhType",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "character",
    UNITS = "category",
    NAVALUE = "NA",
    SIZE = 11,
    PROHIBIT = "",
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "CreateHouseholds",
    DESCRIPTION = "Coded household age composition (e.g. 2-1-0-2-0-0) or Grp for group quarters"
  )

NumHh_ls <-
  list(
    NAME = "NumHh",
    TABLE = "Azone",
    GROUP = "Year",
    TYPE = "households",
    UNITS = "HH",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "CreateHouseholds",
    DESCRIPTION = "Number of households (non-group quarters)"
  )

NumGq_ls <-
  list(
    NAME = "NumGq",
    TABLE = "Azone",
    GROUP = "Year",
    TYPE = "people",
    UNITS = "PRSN",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "CreateHouseholds",
    DESCRIPTION = "Number of people in non-institutional group quarters"
  )

wkr15to19_ls <-
  list(
    NAME ="Wkr15to19",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "people",
    UNITS = "PRSN",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "PredictWorkers",
    DESCRIPTION ="Workers in 15 to 19 year old age group"
  )

wkr20to29_ls <-
  list(
    NAME ="Wkr20to29",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "people",
    UNITS = "PRSN",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "PredictWorkers",
    DESCRIPTION ="Workers in 20 to 29 year old age group"
  )

wkr30to54_ls <-
  list(
    NAME ="Wkr30to54",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "people",
    UNITS = "PRSN",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "PredictWorkers",
    DESCRIPTION ="Workers in 30 to 54 year old age group"
  )

wkr55to64_ls <-
  list(
    NAME ="Wkr55to64",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "people",
    UNITS = "PRSN",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "PredictWorkers",
    DESCRIPTION ="Workers in 55 to 64 year old age group"
  )

wkr65Plus_ls <-
  list(
    NAME ="Wkr65Plus",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "people",
    UNITS = "PRSN",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "PredictWorkers",
    DESCRIPTION ="Workers in 65 or older age group"
  )

workers_ls <-
  list(
    NAME ="Workers",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "people",
    UNITS = "PRSN",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "PredictWorkers",
    DESCRIPTION ="Total workers"
  )

NumWkr_ls <-
  list(
    NAME = "NumWkr",
    TABLE = "Azone",
    GROUP = "Year",
    TYPE = "people",
    UNITS = "PRSN",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "PredictWorkers",
    DESCRIPTION = "Number of workers residing in the zone"
  )

income_ls <-
  list(
    NAME ="Income",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "currency",
    UNITS = "USD",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "1999",
    MODULE = "PredictIncome",
    DESCRIPTION ="Total annual household (non-qroup & group quarters) income"
  )

vehicles_ls <-
  list(
    NAME ="Vehicles",
    TABLE = "Household",
    GROUP = "Year",
    TYPE = "vehicles",
    UNITS = "VEH",
    NAVALUE = -1,
    SIZE = 0,
    PROHIBIT = c("NA", "< 0"),
    ISELEMENTOF = "",
    MULTIPLIER = "NA",
    YEAR = "NA",
    MODULE = "AssignVehicleOwnership",
    DESCRIPTION ="Number of automobiles and light trucks"
  )

setwd(file.path(sd$modelPath))

# initialize Household table for year 2016 and 2035
setwd(sd$modelPath)
initTableRD("Household", "2016", 18)
initTableRD("Household", "2035", 18)

# read data which is converted from ABM input files
require(data.table)
df_hh <- fread("ABM/CreateHousehold_household.csv")
df_azone <- fread("ABM/CreateHousehold_azone.csv")
df_wkr <- fread("ABM/PredictWorkers_household.csv")
df_wkrazone <- fread("ABM/PredictWorkers_azone.csv")
df_inc <- fread("ABM/PredictIncome_household.csv")
#df_veh <- fread("ABM/PredictIncome_household.csv")

#for group 2016

year <- list("2016", "2035")

for (x in year) {
  HhSize <- subset(df_hh, Year == x)$HhSize
  age0to14 <- subset(df_hh, Year == x)[,c("Age0to14")]
  age15to19 <- subset(df_hh, Year == x)[,c("Age15to19")]
  age20to29 <- subset(df_hh, Year == x)[,c("Age20to29")]
  age30to54 <- subset(df_hh, Year == x)[,c("Age30to54")]
  age55to64 <- subset(df_hh, Year == x)[,c("Age55to64")]
  age65Plus <- subset(df_hh, Year == x)[,c("Age65Plus")]
  HhId <- subset(df_hh, Year == x)$HhId
  Azone <- subset(df_hh, Year == x)$Azone
  HhType <- subset(df_hh, Year == x)$HhType
  Vehicles <- subset(df_hh, Year == x)$Vehicles  
  NumHh <- subset(df_azone, Year == x)$NumHh
  NumGq <- subset(df_azone, Year == x)$NumGq
  wkr15to19 <- subset(df_wkr, Year == x)[,c("Wkr15to19")]
  wkr20to29 <- subset(df_wkr, Year == x)[,c("Wkr20to29")]
  wkr30to54 <- subset(df_wkr, Year == x)[,c("Wkr30to54")]
  wkr55to64 <- subset(df_wkr, Year == x)[,c("Wkr55to64")]
  wkr65Plus <- subset(df_wkr, Year == x)[,c("Wkr65Plus")]
  workers <- subset(df_wkr, Year == x)$Workers
  NumWkr <- subset(df_wkrazone, Year == x)$NumWkr
  Income <- subset(df_inc, Year == x)$Income
  
  writeToTableRD(HhSize, Hhsize_ls, x, Index = NULL)
  writeToTableRD(age0to14, age0to14_ls, x, Index = NULL)
  writeToTableRD(age15to19, age15to19_ls, x, Index = NULL)
  writeToTableRD(age20to29, age20to29_ls, x, Index = NULL)
  writeToTableRD(age30to54, age30to54_ls, x, Index = NULL)
  writeToTableRD(age55to64, age55to64_ls, x, Index = NULL)
  writeToTableRD(age65Plus, age65Plus_ls, x, Index = NULL)
  writeToTableRD(HhId, HhId_ls, x, Index = NULL)
  writeToTableRD(Azone, Azone_ls, x, Index = NULL)
  writeToTableRD(HhType, HhType_ls, x, Index = NULL)
  writeToTableRD(Vehicles, vehicles_ls, x, Index = NULL)
  writeToTableRD(NumHh, NumHh_ls, x, Index = NULL)
  writeToTableRD(NumGq, NumGq_ls, x, Index = NULL)
  writeToTableRD(wkr15to19, wkr15to19_ls, x, Index = NULL)
  writeToTableRD(wkr20to29, wkr20to29_ls, x, Index = NULL)
  writeToTableRD(wkr30to54, wkr30to54_ls, x, Index = NULL)
  writeToTableRD(wkr55to64, wkr55to64_ls, x, Index = NULL)
  writeToTableRD(wkr65Plus, wkr65Plus_ls, x, Index = NULL)
  writeToTableRD(workers, workers_ls, x, Index = NULL)
  writeToTableRD(NumWkr, NumWkr_ls, x, Index = NULL)
  writeToTableRD(Income, income_ls, x, Index = NULL)
}

